CREATE DATABASE IF NOT EXISTS `ConfigService`;

use `ConfigService`;

create Table if not exists `User`
(
	userId int primary key AUTO_INCREMENT,
    username varchar(64),
    userPassword char(255),
    token char(255),
    lastLogin datetime
);

create Table if not exists `Repository`
(
	repositoryId int primary key AUTO_INCREMENT,
	repositoryName varchar(64),
    repositoryOwnerId int,
    repositoryHost varchar(16),
    repositoryDeviceType varchar(16),
    repositoryTimestamp datetime

);

create Table if not exists `File`
(
	fileId bigint primary key AUTO_INCREMENT,
    fileOwnerId int,
    fileName varchar(64),
    fileType varchar(16),
    fileRepositoryId int,
    fileData TEXT,
	fileTimestamp datetime
    
);

create Table if not exists `APILog`
(
	userId int not null,
    repositoryId int, 
    method varchar(32),
    response varchar(10000),
    logTimestamp datetime
)
