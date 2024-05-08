import json

project_manthan_api_docs = {
    "base_url": "http://127.0.0.1:5000/",
    "endpoints": {
        "/manthan/v1/implementation.initiate": {
            "method": "GET",
            "description": "initiate implementation for onboarding",
            "parameters": None,
            "header": "Authorization, ADP-ConversationID, ADP-MessageID, Originator-ApplicationID",
            "request":{
                        "implementationName": "WFN Onboarding",
                        "saleforceId" : "12387897987"
                    },
            "response": {
                "description": "A JSON object containing complete response from API.",
                "content_type": "application/json"
            }
        },

        "/manthan/v1/implementation.bind": {
            "method": "POST",
            "description": "Bind the implementation object to the ADP domain (payroll, benefits time etc) for onboarding",
            "parameters": None,
            "header": "Authorization, ADP-ConversationID, ADP-MessageID, Originator-ApplicationID",
            "request" : {
                        "implementationRefID": "ecd4cca5-bcce-4c29-8512-7d368ed5f10f",
                          "sourceHCMRef": {
                            "name": "Paylocity",
                            "version": "7.1.8",
                            "databaseExportIndicator": "false"
                            },
                        "domains": [
                            {
                                "name": "payroll",
                                "bindProperties": [{
                               "key": "regionCode",
                               "value": "NA"
                               }
                                ]
                            }
                            ]
                        },
            "response": {
                "description": "A JSON object containing complete response from API.",
                "content_type": "application/json"
            }
        },

        "/manthan/v1/validations/{validation-ref-id}/status": {
            "method": "GET",
            "description": "Get the validation request status from the earlier performed validation",
            "parameters": "validation-ref-id",
            "header": "Authorization, ADP-ConversationID, ADP-MessageID, Originator-ApplicationID",
            "response": {
                "description": "A JSON object containing complete response from API.",
                "content_type": "application/json"
            }
        }
    }
}


project_manthan_api_docs = json.dumps(project_manthan_api_docs, indent=2)
