DROP DATABASE IF EXISTS giftgiver;
CREATE DATABASE giftgiver;

USE giftgiver;

CREATE TABLE users
  (
      user_id VARCHAR(255) NOT NULL,
      CONSTRAINT users_pk PRIMARY KEY (user_id)
  );

CREATE TABLE item
    (
      item_id INT NOT NULL auto_increment,
      title VARCHAR(510) NOT NULL,
      price FLOAT NOT NULL,
      currency VARCHAR(20) NOT NULL,
      link VARCHAR(510) NOT NULL,
      recipient VARCHAR(255) NOT NULL,
      uid VARCHAR(255) NOT NULL,
      PRIMARY KEY (item_id),
      FOREIGN KEY (uid) REFERENCES users(user_id) ON DELETE CASCADE
    );