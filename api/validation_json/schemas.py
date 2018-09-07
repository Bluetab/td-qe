


custom_validation_schema = {
    "type" : "object",
    "properties" : {
        "custom_validations" : {
            "type" : "object",
            "properties" : {
                "rule_id" : {"type" : "number"},
                "query_validation" : {"type" : "string"}
                },
            "required": ["rule_id", "query_validation"]
            },
        },
    "required": ["custom_validations"]
    }
