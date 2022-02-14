CREATE TABLE `weatherapp_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(256) DEFAULT NULL,
  `username` varchar(45) DEFAULT NULL,
  `createdon` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
);
 CREATE TABLE `weatherapp_weather` (
  `id` int NOT NULL AUTO_INCREMENT,
  `city` varchar(45) DEFAULT NULL,
  `weather` varchar(45) DEFAULT NULL,
  `user_id` int NOT NULL,
  `createdon` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
);