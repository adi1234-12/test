--liquibase formatted sql 
--changeset Adi2:1 
create table testLiquibase (  
ID  int ,
Address varchar(255),
name varchar(255)
);