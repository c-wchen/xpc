CREATE DATABASE IF NOT EXISTS `xpc`;
USE `xpc`;

CREATE TABLE IF NOT EXISTS `posts` (
	`vid` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '作品表主键',
	`title` VARCHAR(256) NOT NULL COMMENT '作品标题',
	`cover` VARCHAR(512) COMMENT '视频预览图',
	`tags` VARCHAR(512) COMMENT '视频标签',
	`video` VARCHAR(512) COMMENT '视频链接',
	`category` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '作品分类',
	`duration` INT(11) NOT NULL DEFAULT 0 COMMENT '播放时长',
	`update_time` VARCHAR(128) NOT NULL DEFAULT '' COMMENT '发表时间',
	`description` text COMMENT '作品描述',
	`play_counts` INT(8) NOT NULL DEFAULT 0 COMMENT '播放次数',
	`like_counts` INT(8) NOT NULL DEFAULT 0 COMMENT '被点赞次数',
	PRIMARY KEY (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '作品表';


CREATE TABLE IF NOT EXISTS `comments` (
	`cid` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '评论人ID',
	`avatar` VARCHAR(512) COMMENT '评论人头像',
	`uname` VARCHAR(512) COMMENT '评论人名称',
	`add_time` VARCHAR(128) NOT NULL DEFAULT '' COMMENT '发表时间',
	`content` TEXT COMMENT '评论内容',
	PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '评论表';

