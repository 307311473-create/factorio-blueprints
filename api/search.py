import json
import os

# 读取蓝图数据
def load_blueprints():
    # Vercel 部署时，当前工作目录是项目根目录
    with open('blueprints.json', 'r', encoding='utf-8') as f:
        return json.load(f)['blueprints']

def handler(request):
    # 获取查询参数
    keyword = request.args.get('keyword', '').strip().lower()
    
    if not keyword:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing keyword parameter'})
        }
    
    # 加载蓝图
    try:
        blueprints = load_blueprints()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to load blueprints', 'details': str(e)})
        }
    
    # 搜索（匹配名称或标签）
    results = []
    for bp in blueprints:
        name_match = keyword in bp['name'].lower()
        tag_match = any(keyword in tag.lower() for tag in bp['tags'])
        if name_match or tag_match:
            results.append(bp)
    
    # 返回结果
    response = {
        'query': keyword,
        'count': len(results),
        'results': results
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # 允许跨域
        },
        'body': json.dumps(response, ensure_ascii=False)
    }

# Vercel 入口点
def main(request):
    return handler(request)
