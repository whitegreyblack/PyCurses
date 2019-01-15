drop table if exists notes;

create table notes (
    id_note integer PRIMARY KEY AUTOINCREMENT,
    title varchar(20),
    created timestamp,
    modified timestamp,
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
);

insert into notes (
    title,
    created,
    modified,
    note
) values (
    'example 2',
    datetime('now'),
    datetime('now'),
    'ali baba had a great meal for those with small bellies.\nAfter a while they went to bed.'
);

insert into notes (
    title,
    created,
    modified,
    note
) values (
    'example 3',
    datetime('now'),
    datetime('now'),
    "ali baba had a great meal for those with small bellies. After a while they went to bed.\nPillows look like clouds during your rest."
);
