# -----------------------------------------------------------------------------
# AUTHOR: Sam Whang | whitegreyblack
# FILE  : STRINGS.PY
# FORUSE: STARTUP DURING FILE/YAML CHECKING
# MORE  : (INFO|DEBUG|WARNING) [TRY|ERROR|SUCCESS] STRINGS FOR LOGGER
# -----------------------------------------------------------------------------
sql_populate = "-- LOGGER :- Populate() --"
sql_frontend = "-- LOGGER :- FrontEnd() --"

sql_conn_try = "SQL: Creating Connection"
sql_conn_scs = "SQL: Connection Established"
sql_conn_err = "SQL: Connection Error"
sql_conn_cls = "SQL: Connection Close"

sql_push_try = "SQL: Table Write Head and Body for [{}]"
sql_push_err = "SQL: Table Write Error"
sql_push_scs = "SQL: Table Write Success"

yml_load_try = "YML: Load Data [{}]"
yml_load_err = "YML: Load Data Error"
yml_load_scs = "YML: Load Data Success"

sys_exit_nrm = "SYS: Exiting Application Normally"
sys_exit_err = "SYS: Exiting Application Early"

sys_read_try = "SYS: Read File [{}]"
sys_read_err = "SYS: Read File Error"
sys_read_scs = "SYS: Read File Success"

sys_open_try = "SYS: Open File [{}]"
sys_open_err = "SYS: Open File Error"
sys_open_scs = "SYS: Open File Success"

sql_slct_all = "SQL: Select"
sql_slct_try = "SQL: Select {}={}"
sql_slct_err = "SQL: Select Error"
sql_slct_scs = "SQL: Select Success"

# -----------------------------------------------------------------------------
# FORUSE: USED IN CHECKER FOR PRINT OUTPUT TO LOGGER AND STDOUT
# MORE  : USES TERMINAL COLOR CODES FOR COLORED OUTPUT (PASS=GREEN|FAIL=RED)
# -----------------------------------------------------------------------------
ORG = '\x1b[0;34;40m'
YEL = '\x1b[0;33;40m'
GRN = '\x1b[1;32;40m'
RED = '\x1b[1;31;40m'
END = '\x1b[0m'
passfail = {
    'file_safe': {
        True: GRN+("File Pass")+END,
        False: RED+("File Fail")+END,
    },
    'file_regex': {
        True: GRN+("Regx Pass")+END,
        False: RED+("Regx Fail")+END,
    },
    'file_read': {
        True: GRN+("Read Pass")+END,
        False: RED+("Read Fail")+END
    },
    'file_load': {
        True: GRN+("Load Pass")+END,
        False: RED+("Load Fail")+END,
    },
    'store_test': {
        True: GRN+("Store Pass")+END,
        False: RED+("Store Fail")+END,
    },
    'yaml_safe': {
        True: GRN+("Yaml Pass")+END,
        False: RED+("Yaml Fail")+END,
    },
    'yaml_read': {
        True: GRN+("Read Pass")+END,
        False: RED+("Read Fail")+END,
    },
    'yaml_store': {
        True: GRN+("Name Pass")+END,
        False: RED+("Name Fail")+END,
    },
    'yaml_date': {
        True: GRN+("Date Pass")+END,
        False: RED+("Date Fail")+END,
    },
    'yaml_prod': {
        True: GRN+("Prod Pass")+END,
        False: RED+("Prod Fail")+END,
    },
    'yaml_card': {
        True: GRN+("Card Pass")+END,
        False: RED+("Card Fail")+END,
        }
    }
# -----------------------------------------------------------------------------
# FORUSE: USED IN DATABASE CONNECTION DURING STARTUP AND RUNTIME
# MORE  : SQL COMMANDS FOR DATA BASE INSERTION|SELECTION|MODIFICATION|DELETION
# -----------------------------------------------------------------------------
headcreate = """create table if not exists reciepthead (store varchar(25),
    date varchar(10), type varchar(10), code varchar(30) PRIMARY KEY,
    subtotal real, tax real, total real, UNIQUE(store, date, total))"""
headinsert = """insert or ignore into reciepthead values (?,?,?,?,?,?,?);"""

bodycreate = """create table if not exists recieptbody (item varchar(25),
    price real, code varchar(30), UNIQUE(item, price, code))"""
bodyinsert = """insert or ignore into recieptbody values (?,?,?)"""

algrocery = """select * from reciepthead"""
hdgrocery = """select * from reciepthead where {}='{}'"""
bdgrocery = """select * from reciepthead where code={}"""

mindate = """select min(date) from reciepthead"""
maxdate = """select max(date) from reciepthead"""
