

custom_validation_schema = {
    "type" : "object",
    "properties" : {
        "custom_validations" : {
            "type" : "object",
            "properties" : {
                "implementation_key" : {"type" : "string"},
                "query_validation" : {"type" : "string"}
                },
            "required": ["implementation_key", "query_validation"]
            },
        },
    "required": ["custom_validations"]
    }


tags_validation_schema = {
    "type": "object",
    "properties": {
        "rule_tags": {
            "type": "array"
        }
    }
}
