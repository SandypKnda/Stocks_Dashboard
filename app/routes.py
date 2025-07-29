from flask import Blueprint, jsonify, render_template, request
from app.services.fetch_data import get_top_stocks_by_all_sectors
from app.services.predict_eod import predict_eod_price
from app.services.fetch_data import get_all_index_stocks

bp = Blueprint('main', __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/api/stocks")
def get_sector_stocks():
    sector_filter = request.args.get('sector')
    print("🔍 Loading stock data...")
    data = get_top_stocks_by_all_sectors(limit_per_sector=5)
    if data is None or len(data) == 0:
        print("⚠️ No data returned from fetch logic.")
        return jsonify([])
    filtered = []
    for row in data:
        try:
            price = row['price']
            if not price or price <= 0:
                continue  # ⛔ skip $0 or None prices
            print(f"✅ Loaded {row['symbol']} @ ${row['price']}")
            if sector_filter and row['sector'] != sector_filter:
                continue
            row['eod_prediction'] = predict_eod_price(price)
            filtered.append(row)
        except Exception as e:
            print(f"⚠️ Skipping row due to error: {e}")
            continue
            
#    for row in data:
#        print(f"✅ Loaded {row['symbol']} @ ${row['price']}")
#        row['eod_prediction'] = predict_eod_price(row['price'])

    return jsonify(filtered)
    
    for stock in data:
        price = stock.get("price", 0)
        stock["eod_prediction"] = predict_eod_price(price)
    return jsonify(data)

@bp.route("/api/index-stocks")
def get_index_stocks():
    print("🔍 Loading stock data...")
    data = get_all_index_stocks(limit=100)
    if data is None or len(data) == 0:
        print("⚠️ No data returned from fetch logic.")
        return jsonify([])

    for row in data:
        print(f"✅ Loaded {row['symbol']} @ ${row['price']}")
        row['eod_prediction'] = predict_eod_price(row['price'])
    return jsonify(data)
    
    for stock in data:
        price = stock.get("price", 0)
        stock["eod_prediction"] = predict_eod_price(price)
    return jsonify(data)
