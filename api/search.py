import json
import os

# 加载蓝图数据
def load_blueprints():
    with open('blueprints.json', 'r', encoding='utf-8') as f:
        return json.load(f)['blueprints']

# Vercel 要求的 handler 函数
def handler(request):
    # 获取查询参数
    keyword = request.args.get('keyword', '').strip().lower()
    
    if not keyword:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Missing or empty keyword parameter'})
        }
    
    try:
        blueprints = load_blueprints()
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Failed to load blueprints', 'details': str(e)})
        }
    
    # 搜索逻辑
    results = []
    for bp in blueprints:
        if (keyword in bp['name'].lower()) or any(keyword in tag.lower() for tag in bp['tags']):
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
        'body': json.dumps(response, ensure_ascii=False, indent=2)
    }
