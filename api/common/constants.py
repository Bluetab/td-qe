PORT_DES = 4009
PORT_PRO = 4009


SPEC_RESULTSET_JSON_S3 = {'results': ('ResultSet.Rows', ['Data'])}
SPEC_VALUE_JSON_S3 = ('results', [["VarCharValue"]])


GET_RULE_IMPLEMENTATIONS_BY_BUSINESS_CONCEPT = "/api/rule_implementations?rule_business_concept_id={id}&rule_status={status}"
GET_RULE_IMPLEMENTATIONS = "/api/rule_implementations?rule_status={status}"
SEND_CSV_RESULTS = "/api/rule_results"
NAME_KEY_FILES_DQ = "rule_results"
PARAM_RULE_TAGS = "&rule_tags={rule_tags}"

SAVE_RESULTS = "results/"
CSV_EXTENSION = ".csv"
NAME_FILE_TO_UPLOAD = "results_to_send"
SESSIONS = "/api/sessions"

HEADERS_CONTENT = {'content-type': 'application/json'}
HEADERS_ACCEPT = { 'Accept': 'application/json' }

PATH_VAULT_SOURCES = "meta-connect/sources/data/"
API_DATABASE_PATH = "api.v1.databases."


CSV_COLUMNS = ['implementation_key', 'date', 'result']


TYPE_MANDATORY_FIELD = "mandatory_field"
TYPE_MIN_TEXT = "min_text"
TYPE_MAX_TEXT = "max_text"
TYPE_DATE_FORMAT = "date_format"
TYPE_NUMERIC_FORMAT = "numeric_format"
TYPE_DECIMAL_FORMAT = "decimal_format"
TYPE_IN_LIST = "in_list"
TYPE_UNIQUE_VALUES = "unique_values"
TYPE_MIN_VALUE = "min_value"
TYPE_MAX_VALUE = "max_value"
TYPE_INTEGER_VALUES_RANGE = "integer_values_range"
TYPE_INTEGRITY = "integrity"
TYPE_MAX_DATE = "max_date"
TYPE_MIN_DATE = "min_date"
TYPE_DATES_RANGE = "dates_range"
TYPE_CUSTOM = "custom_validation"
VALID_EXEC_STATUS = "selectedToExecute"
