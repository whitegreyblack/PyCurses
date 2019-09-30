-- drop existing table then recreate notes table
-- drop table if exists notes;
create table notes (
    id_note integer PRIMARY KEY AUTOINCREMENT,
    title varchar(20),
    created timestamp,
    modified timestamp
    note varchar(250)
);
