CREATE DATABASE IF NOT EXISTS flag;

USE flag;

DROP TABLE IF EXISTS `flag_table`;
CREATE TABLE `flag_table` (
  `flag_column` VARCHAR(50) NOT NULL
);

INSERT INTO `flag_table` values("CBJS{Lat3r4l_Mov3MEnt_Extr4ct_d4ta_fR0m_DB}");
