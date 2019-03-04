drop table if exists storecategory;
drop table if exists stores;
drop table if exists receipts;
drop table if exists products;
drop table if exists receiptproducts;

create table storecategory (
    id_category     integer PRIMARY KEY AUTOINCREMENT,
    category        varchar(25)
);

create table stores (
    id_store        integer PRIMARY KEY AUTOINCREMENT,
    store           varchar(25) NOT NULL,
    id_category     integer NOT NULL,
    FOREIGN KEY (id_category) REFERENCES storecategory(id_category)
);

create table receipts (
    id_receipt      integer PRIMARY KEY AUTOINCREMENT,
    id_store        integer NOT NULL,
    created         timestamp,
    purchased_on    timestamp,
    subtotal        float,
    tax             float,
    total           float,
    payment         float,
    receipt_file    float,
    FOREIGN KEY (id_store) REFERENCES stores(id_store)
);

create table products (
    id_product      integer PRIMARY KEY AUTOINCREMENT,
    id_store        integer NOT NULL,
    product         varchar(25),
    price           float,
    FOREIGN KEY (id_store) REFERENCES stores(id_store)
);

create table receiptproducts (
    id_receiptproduct integer PRIMARY KEY AUTOINCREMENT,
    id_receipt        integer NOT NULL,
    id_product        integer NOT NULL,
    FOREIGN KEY (id_receipt) REFERENCES receipts(id_receipt),
    FOREIGN KEY (id_product) REFERENCES products(id_product)
);

-- example category
insert into storecategory (category) values ("general store"), ("grocery");
-- example stores
insert into stores (store, id_category) values ("store 1", 2), ("Store 2", 1);
-- example receipts
insert into receipts (id_store, created, purchased_on, subtotal, tax, total, payment) values 
    (1, datetime('now'), datetime('now'), 10.0, 0.0, 10.0, 10.0),
    (2, datetime('now'), datetime('now'), 20.0, 5.0, 25.0, 25.0);
-- example products
insert into products (id_store, product, price) values (1, "product 1", 10.0), (2, "product 2", 20.0);
-- example receieptproducts
insert into receiptproducts (id_receipt, id_product) values (1, 2), (2, 1);