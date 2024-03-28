DIFF_NAME_ERROR: str = "ERROR: Local file name [%s] with diff name of the database [%s]"
OUT_OF_DATE_ERROR: str = "ERROR: Out of date - Local file missing [%s]"
DIFF_CHECKSUM_ERROR: str = "ERROR: Local file [%s] with diff script (%s) of the database (%s)"
DIFF_CHECKSUM_ERROR_DOS: str = "ERROR: Local file [%s] with diff script (%s) of the database (%s)" \
                               " - one or more files have DOS line breaks which may cause checksum differences"
VALID_NAME_ERROR: str = "ERROR: Local file [%s] has invalid format name - expected: %s"
DIRECTORY_NOT_FOUND: str = "ERROR: directory not found ('%s')"
MIGRATIONS_NOT_FOUND: str = "ERROR: no local migration files found in (%s) folder"
MIGRATIONS_NOT_STARTED: str = "ERROR: no migrations applied yet, no validation necessary."
