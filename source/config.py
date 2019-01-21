"""Configuration settings to standardize all apps under PyCurses"""

ARGS_PATH_IS_NOT_DIR = "ERROR: File specified is not a directory"

DATE_FORMAT = "YYYY-MM-DD"
DATE_FORMAT_REGEX = "\d{4}-\d{1,2}-\d{1,2}"
DATE_FORMAT_INVALID = "Date was not given in the correct format."
DATE_FORMAT_EXPECTED = f"Expected date format is '{DATE_FORMAT}'."

YAML_FILE_EXTENSION = ".yaml"
YAML_FILE_NAME_REGEX = "[0-9]{6}-[a-z_]{,25}"

YAML_CHECKER_RESULTS_TOTAL = "Total number of files checked: {}"
YAML_CHECKER_BATCH_MSG = "files {}: {}"
YAML_CHECKER_NO_BATCH = "No files were {}"
YAML_CHECKER_FILE_MSG = "{} ({}/{}) {}"
YAML_CHECKER_BATCH_SYMBOL = {
    "VERIFIED": '+',
    "UNVERIFIED": 'x',
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

DATABASE_POINTER_CONTACTS = "data/contacts.db"

DATABASE_POINTER_NOTES = "data/notes.db"
DATA_FILE_PATH_NOTES = "data/notes.json"
CONNECTION_CLEAN_SCRIPT_NOTES = "source/db_scripts/create_notes.sql"
CONNECTION_REBUILD_SCRIPT_NOTES = "source/db_scripts/create_notes_examples.sql"

DATA_FILE_PATH_QUIZ = "data/quiz.json"
DATABASE_POINTER_QUIZ = "data/quiz.db"

DATABASE_POINTER_RECEIPTS = "data/receipts.db"
CONNECTION_CLEAN_SCRIPT_QUIZ = "source/db_scripts/create_quiz.sql"
CONNECTION_REBUILD_SCRIPT_QUIZ = "source/db_scripts/create_quiz_examples.sql"
CONNECTION_CLEAN_SCRIPT_RECEIPTS = "source/db_scripts/create_receipts.sql"
CONNECTION_REBUILD_SCRIPT_RECEIPTS = "source/db_scripts/create_receipts_examples.sql"