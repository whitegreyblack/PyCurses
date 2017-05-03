headcreate = """create table if not exists reciepthead (store varchar(25),
    date varchar(10), type varchar(10), code varchar(30) PRIMARY KEY,
    subtotal real, tax real, total real, UNIQUE(store, date, total))"""
headinsert = """insert or ignore into reciepthead values (?,?,?,?,?,?,?);"""

bodycreate = """create table if not exists recieptbody (item varchar(25), 
    price real, code varchar(30))"""
bodyinsert = """insert or ignore into recieptbody values (?,?,?)"""

algrocery = """select * from reciepthead"""
hdgrocery = """select * from reciepthead where {}='{}'"""
bdgrocery = """select * from reciepthead where code={}"""