

QUERY_INTEGER_VALUES_RANGE = """
SELECT TRUNC((SELECT COUNT(*)*100
	FROM {TABLE}
	WHERE {COLUMN} >= {MIN_VALUE}
	AND {COLUMN} <= {MAX_VALUE}) / (
		SELECT COUNT(*)
    	FROM {TABLE}),0)
FROM DUAL"""
