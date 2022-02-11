CREATE DATABASE `simmons_testbed`;
USE `simmons_testbed`;

CREATE USER `user`@`%` IDENTIFIED BY `1234`;
GRANT ALL PRIVILEGES ON *.* TO `user`@`%` WITH GRANT OPTION;
FLUSH PRIVILEGES;


DROP TABLE IF EXISTS `user`
CREATE TABLE `user`(
`id_num` int not null AUTO_INCREMENT first,
`howmany` int,
`nowcheck` boolean not null default 0,
`xboundary` int,
`yboundaty` int,
PRIMARY KEY (`id_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

