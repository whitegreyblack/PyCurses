drop table if exists notes;

create table notes (
    id_note integer PRIMARY KEY,
    title varchar(20) NOT NULL UNIQUE,
    created timestamp,
    modified timestamp,
    note varchar(250)
);