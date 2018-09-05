


custom_validation_schema = {
    "type" : "object",
    "properties" : {
        "custom_validations" : {
            "type" : "object",
            "properties" : {
                "quality_control_id" : {"type" : "number"},
                "query_validation" : {"type" : "string"}
                },
            "required": ["quality_control_id", "query_validation"]
            },
        },
    "required": ["custom_validations"]
    }