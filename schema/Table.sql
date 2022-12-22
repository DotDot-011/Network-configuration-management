CREATE DATABASE IF NOT EXISTS `ConfigService`;

use `ConfigService`;

create Table if not exists `User`
(
    username varchar(64) primary key,
    userPassword char(255) NOT null,
    token char(255),
    lastLogin datetime
);

create Table if not exists `Repository`
(
	repositoryId int primary key AUTO_INCREMENT,
	repositoryName varchar(64),
    repositoryOwnerName varchar(64),
    repositoryHost varchar(16),
    repositoryDeviceType varchar(16),
    repositoryTimestamp datetime

);

create Table if not exists `File`
(
	fileId bigint primary key AUTO_INCREMENT,
    fileOwnerName ,
    fileName varchar(64),
    fileType varchar(16),
    fileRepositoryId int,
    fileData TEXT,
	fileTimestamp datetime
    
);

create Table if not exists `APILog`
(
	username varchar(64) not null,
    repositoryId int, 
    method varchar(32),
    response TEXT,
    logTimestamp datetime
)
