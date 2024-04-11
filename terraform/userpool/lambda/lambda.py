import json


def lambda_handler(event, context):
    assert event["triggerSource"] == "CustomMessage_ForgotPassword"

    template = None
    with open('template.html', 'r') as file_template:
        template = file_template.read()

    template = template.replace('{codeParameter}', event['request']['codeParameter'])
    template = template.replace('{email}', event['request']['userAttributes']['email'])

    event["response"] = {} if "response" not in event else event["response"]
    event["response"]["emailSubject"] = "SCOPE Password Reset"
    event["response"]["emailMessage"] = template

    return event
