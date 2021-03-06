QUERY_INTEGER_VALUES_RANGE = """
SELECT COUNT(*)*100/(SELECT COUNT(*)
    FROM {TABLE})
FROM {TABLE}
WHERE {COLUMN} >= {MIN_VALUE}
AND {COLUMN} <= {MAX_VALUE};"""

QUERY_MIN_VALUE = """
SELECT COUNT(*)*100/(SELECT COUNT(*)
    FROM {TABLE})
FROM {TABLE}
WHERE {COLUMN} >= {MIN_VALUE};"""

QUERY_MAX_VALUE = """
SELECT COUNT(*)*100/(SELECT COUNT(*)
    FROM {TABLE})
FROM {TABLE}
WHERE {COLUMN} <= {MAX_VALUE};"""

QUERY_MANDATORY_FIELD = """
SELECT COUNT(*)*100/(SELECT COUNT(*)
    FROM {TABLE})
FROM {TABLE}
WHERE {COLUMN} IS NOT NULL;"""

QUERY_DATES_RANGE = """
SELECT COUNT(*)*100/(SELECT COUNT(*)
    FROM {TABLE})
FROM {TABLE}
WHERE {COLUMN}
BETWEEN {COLUMN} '{MIN_DATE}'
AND {COLUMN} '{MAX_DATE}';"""

QUERY_MIN_DATE = """
SELECT COUNT(*)*100/(SELECT COUNT(*)
    FROM {TABLE})
FROM {TABLE}
WHERE {COLUMN} >= '{MIN_DATE}';"""

QUERY_MAX_DATE = """
SELECT COUNT(*)*100/(SELECT COUNT(*)
    FROM {TABLE})
FROM {TABLE}
WHERE {COLUMN} >= '{MAX_DATE}';"""

QUERY_MIN_TEXT = """
SELECT COUNT(*)*100.0/(SELECT COUNT(*)
    FROM {TABLE})
FROM {TABLE}
WHERE LENGTH({COLUMN}) >= {MIN_TEXT};"""

QUERY_MAX_TEXT = """
SELECT COUNT(*)*100.0/(SELECT COUNT(*)
    FROM {TABLE})
FROM {TABLE}
WHERE LENGTH({COLUMN}) <= {MAX_TEXT};"""
