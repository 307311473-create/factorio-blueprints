import json
import os

def load_blueprints():
    # 安全地定位 blueprints.json
    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    json_path = os.path.join(project_root, 'blueprints.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)['blueprints']

def handler(request):
    keyword = request.args.get('keyword', '').strip().lower()
    
    if not keyword:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Missing keyword parameter'})
        }
    
    try:
        blueprints = load_blueprints()
    except FileNotFoundError:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'blueprints.json not found'})
        }
    except json.JSONDecodeError as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Invalid JSON in blueprints.json', 'details': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Unexpected error', 'details': str(e)})
        }
    
    results = []
    for bp in blueprints:
        name_match = keyword in bp['name'].lower()
        tag_match = any(keyword in tag.lower() for tag in bp['tags'])
        if name_match or tag_match:
            results.append(bp)
    
    response = {
        'query': keyword,
        'count': len(results),
        'results': results
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(response, ensure_ascii=False)
    }
