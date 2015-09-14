CREATE TABLE user(
id integer primary key autoincrement,
user text,
password text,
fullname text,
mail text);

CREATE TABLE rss_source(
id integer primary key autoincrement,
user_id int,
name text,
url text,
tag int);

CREATE TABLE rss_content(
id integer primary key autoincrement,
guid text,
rss_id int,
pub_date datetime,
url text,
title text,
content text,
category text);

CREATE TABLE rss_config(
rss_id int,
tag int);
