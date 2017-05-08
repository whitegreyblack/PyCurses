folder='\x1b[0;34;40m'
GRN ="\x1b[1;32;40m"
yellow='\x1b[0;33;40m'
RED ='\x1b[1;31;40m'
END ='\x1b[0m'

passfail = {
    'f_safe' : {
        True: GRN+("File Pass")+END,
        False: RED+("File Fail")+END,
    },
    'f_regex': {
        True: GRN+("Regx Pass")+END,
        False: RED+("Regx Fail")+END,
    },
    'f_read': {
        True: GRN+("Read Pass")+END,
        False: RED+("Read Fail")+END
    },
    'f_load': {
        True: GRN+("Load Pass")+END,
        False: RED+("Load Fail")+END,
    },
    'store_test': {
        True: GRN+("Store Pass")+END,
        False: RED+("Store Fail")+END,
    },
    'y_safe': {
        True: GRN+("Yaml Pass")+END,
        False: RED+("Yaml Fail")+END,
    },
    'y_read': {
        True: GRN+("Read Pass")+END,
        False: RED+("Read Fail")+END,
    },
    'y_store': {
        True: GRN+("Name Pass")+END,
        False: RED+("Name Fail")+END,
    },
    'y_date': {
        True: GRN+("Date Pass")+END,
        False: RED+("Date Fail")+END,
    },
    'y_prod': {
        True: GRN+("Prod Pass")+END,
        False: RED+("Prod Fail")+END,
    },
    'y_card': {
        True: GRN+("Card Pass")+END,
        False: RED+("Card Fail")+END,
    },
}