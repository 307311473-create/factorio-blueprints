import json
import os

# 获取蓝图文件路径（Vercel 部署时工作目录是项目根）
BLUEPRINTS_PATH = os.path.join(os.path.dirname(__file__), "..", "blueprints.json")

# 全局缓存蓝图数据（避免每次请求都读文件）
_BLUEPRINTS_DATA = None

def get_blueprints():
    global _BLUEPRINTS_DATA
    if _BLUEPRINTS_DATA is None:
        with open(BLUEPRINTS_PATH, "r", encoding="utf-8") as f:
            _BLUEPRINTS_DATA = json.load(f)
    return _BLUEPRINTS_DATA

def handler(request):
    """
    Vercel Serverless 函数入口
    request: 包含 query, method, headers 等
    返回 dict 或 Response 对象
    """
    # 只处理 GET 请求
    if request.method != "GET":
        return {"error": "Method not allowed"}, 405

    # 获取 keyword 参数
    keyword = request.query.get("keyword", "").strip()
    if not keyword:
        return {"error": "Missing 'keyword' query parameter"}, 400

    keyword_lower = keyword.lower()
    results = []

    try:
        blueprints = get_blueprints()["blueprints"]
        for bp in blueprints:
            name_match = keyword_lower in bp["name"].lower()
            tag_match = any(keyword_lower in tag.lower() for tag in bp.get("tags", []))
            if name_match or tag_match:
                results.append({
                    "id": bp["id"],
                    "name": bp["name"],
                    "tags": bp["tags"],
                    "code": bp["code"]
                })
    except Exception as e:
        return {"error": f"Internal error: {str(e)}"}, 500

    return {
        "query": keyword,
        "count": len(results),
        "results": results
    }