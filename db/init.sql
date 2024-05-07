DROP TABLE IF EXISTS `candidate`;
CREATE TABLE `candidate` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 collate utf8_bin;

LOCK TABLES `candidate` WRITE;
INSERT INTO `candidate` VALUES
(1, '吴一'),
(2, '红二'),
(3, '张三'),
(4, '李四'),
(5, '王五');
UNLOCK TABLES;


DROP TABLE IF EXISTS `vote`;
CREATE TABLE `vote` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `ip` VARCHAR(100) DEFAULT NULL,
  `candidateId` INT DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ip_index` (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 collate utf8_bin;

LOCK TABLES `vote` WRITE;
INSERT INTO `vote` VALUES
(1, '1111', 1);
UNLOCK TABLES;

SELECT C.id, C.name, IF(V.Num IS NULL, 0, V.Num) AS Num FROM candidate AS C
LEFT JOIN (SELECT candidateId, COUNT(candidateId) AS Num FROM vote GROUP BY candidateId) AS V ON C.id = V.candidateId;

DROP procedure IF EXISTS `vote`;
DELIMITER ;
DELIMITER ;;
CREATE  PROCEDURE `vote`(
    p_ip VARCHAR(100),
    p_candidateId INT
)
/**
    投票判断是否有该IP， 没有投票才会有效
    code: 0 投票失败
    code: 1 投票成功

 */
label:BEGIN
    IF (SELECT COUNT(1) FROM vote WHERE ip = p_ip) = 1 THEN
        SELECT 0 AS code;
        LEAVE label;
    END IF;
    INSERT vote (ip, candidateId) VALUE (p_ip, p_candidateId);
    SELECT 1 AS code;
END ;;
DELIMITER ;

CALL vote('2', 1);