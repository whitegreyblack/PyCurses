folder='\x1b[0;34;40m'
GRN ="\x1b[1;32;40m"
yellow='\x1b[0;33;40m'
RED ='\x1b[1;31;40m'
END ='\x1b[0m'

strings = {
    'file_safe' : {
        True: GRN+("Yaml File")+END,
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
    'yaml_store': {
        True: GRN+("Name Pass")+END,
        False: RED+("Name Fail")+END,
    },
    'yaml_date': {
        True: GRN+("Date Pass")+END,
        False: RED+("Date Fail")+END,
    }
}