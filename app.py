from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/api/search')
def search():
    query = request.args.get('q', '').lower().strip()
    
    # 读取蓝图数据
    with open(os.path.join(os.getcwd(), 'blueprints.json'), 'r', encoding='utf-8') as f:
        blueprints = json.load(f)
    
    if query:
        results = [
            bp for bp in blueprints
            if query in bp.get("name", "").lower() or
               query in bp.get("description", "").lower() or
               query in bp.get("author", "").lower()
        ]
    else:
        results = blueprints
    
    return jsonify({
        "count": len(results),
        "results": results[:50]
    })

if __name__ == '__main__':
    app.run(debug=True)
