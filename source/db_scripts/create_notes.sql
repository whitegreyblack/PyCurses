<<<<<<< HEAD
create table notes (
    id_note integer PRIMARY KEY AUTOINCREMENT,
    title varchar(20),
    created timestamp,
    modified timestamp
    note varchar(250)
);

insert into notes (
    title,
    created,
    modified,
    note
) values (
    'example 1',
    datetime('now'),
    datetime('now'),
    'These are example notes for note 1'
)
=======
drop table if exists notes;

create table notes (
    id_note integer PRIMARY KEY,
    title varchar(20) NOT NULL UNIQUE,
    created timestamp,
    modified timestamp,
    note varchar(250)
);
>>>>>>> 0839317a574efa9caf443dbb5a042d2eed3cac6f
