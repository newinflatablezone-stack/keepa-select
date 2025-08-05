from flask import Flask, render_template, request, jsonify, send_file
import keepa
import pandas as pd
import io

app = Flask(__name__)

# 你的Keepa API Key
KEEPA_API_KEY = "46tuh1bmemurju87b5b83b9kjkn3ih1ejnhj6tuencbjolc4be1bdutm8t85jj9f"

api = keepa.Keepa(KEEPA_API_KEY)

# 筛选逻辑示例
def is_valid(product):
    try:
        price = product['buyBoxPrice'] / 100 if product['buyBoxPrice'] else None
        reviews = product['reviewCount']
        if not price or not (10 <= price <= 70):
            return False
        if reviews < 100:
            return False
        return True
    except:
        return False

@app.route('/')
def index():
    return '''
    <h1>Keepa 选品工具</h1>
    <button onclick="fetchProducts()">抓取选品</button>
    <div id="result"></div>
    <script>
    async function fetchProducts() {
        document.getElementById('result').innerHTML = '正在抓取...';
        const res = await fetch('/fetch');
        const data = await res.json();
        let html = '<table border="1"><tr><th>图片</th><th>ASIN</th><th>标题</th><th>价格</th><th>评论数</th></tr>';
        data.forEach(p => {
            html += `<tr>
                <td><img src="${p.image}" width="50"></td>
                <td>${p.asin}</td>
                <td>${p.title}</td>
                <td>$${p.price}</td>
                <td>${p.reviews}</td>
            </tr>`;
        });
        html += '</table>';
        document.getElementById('result').innerHTML = html;
    }
    </script>
    '''

@app.route('/fetch')
def fetch():
    # 搜索示例关键词
    keywords = ["wireless charger", "kitchen organizer"]
    products = []
    for keyword in keywords:
        search = api.search(keyword, domain='US', category=None, page=0, sort='sales')
        for p in search['products'][:300]:
            if is_valid(p):
                products.append({
                    "asin": p['asin'],
                    "title": p.get('title', 'N/A'),
                    "price": p['buyBoxPrice']/100 if p['buyBoxPrice'] else 0,
                    "reviews": p.get('reviewCount', 0),
                    "image": "https://images-na.ssl-images-amazon.com/images/I/" + p['images'][0] if p.get('images') else ""
                })
    return jsonify(products[:20])

if __name__ == '__main__':
    app.run(debug=True)
