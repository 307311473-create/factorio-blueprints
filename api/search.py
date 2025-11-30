import json

def handler(request):
    response = {
        "message": "API is working!"
    }
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response, ensure_ascii=False)
    }
