CREATE DATABASE IF NOT EXISTS student_score_db;
USE student_score_db;
CREATE TABLE IF NOT EXISTS teacherLogin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE IF NOT EXISTS student (
    id INT PRIMARY KEY AUTO_INCREMENT,
    stu_no VARCHAR(20) NOT NULL COMMENT '学号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    chinese DECIMAL(5,2) DEFAULT 0 COMMENT '语文成绩',
    math DECIMAL(5,2) DEFAULT 0 COMMENT '数学成绩',
    english DECIMAL(5,2) DEFAULT 0 COMMENT '英语成绩',
    UNIQUE KEY (stu_no)  -- 学号唯一
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO teacherLogin (username, password) VALUES ('admin', '123456');
