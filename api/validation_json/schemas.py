


custom_validation_schema = {
    "type" : "object",
    "properties" : {
        "custom_validations" : {
            "type" : "object",
            "properties" : {
                "rule_implementation_id" : {"type" : "number"},
                "query_validation" : {"type" : "string"}
                },
            "required": ["rule_implementation_id", "query_validation"]
            },
        },
    "required": ["custom_validations"]
    }
