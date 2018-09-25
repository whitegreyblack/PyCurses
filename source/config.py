"""Configuration settings to standardize all apps under PyCurses"""

DATE_FORMAT = "YYYY-MM-DD"
DATE_FORMAT_REGEX = "\d{4}-\d{1,2}-\d{1,2}"
YAML_FILE_EXTENSION = ".yaml"
YAML_FILE_NAME_REGEX = "[0-9]{6}-[a-z_]{,25}"

YAML_CHECKER_BATCH_MSG = "files {}: {}"
YAML_CHECKER_NO_BATCH = "No files were {}"
YAML_CHECKER_FILE_MSG = "{} ({}/{}) {}"
YAML_CHECKER_BATCH_SYMBOL = {
    "COMMITTED": '+',
    "UNCOMMITTED": 'x',
    "SKIPPED": '?'
    }

DATE_FORMATS = {
    'ISO': {
        'L': "%Y-%m-%d",
        'S': "%y-%m-%d",
    },
    'USA': {
        'L': "%m/%d/%Y",
        'S': "%m/%d/%y",
    },
}

DATE_FORMAT = DATE_FORMATS['USA']