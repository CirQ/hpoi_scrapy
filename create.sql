DROP TABLE image;
DROP TABLE album;

CREATE TABLE album
(
    url VARCHAR PRIMARY KEY NOT NULL,
    title VARCHAR,
    author VARCHAR,
    date VARCHAR,
    pics INT,
    clicks INT,
    source VARCHAR,
    intro VARCHAR
);
CREATE UNIQUE INDEX album_id_uindex ON album (url);
CREATE TABLE image
(
    url VARCHAR PRIMARY KEY NOT NULL,
    name VARCHAR,
    album_url VARCHAR,
    CONSTRAINT album_id FOREIGN KEY (album_url) REFERENCES album (url) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE UNIQUE INDEX image_id_uindex ON image (url);
