from flask import Blueprint, jsonify, render_template, request
from app.services.fetch_data import get_top_stocks_by_all_sectors
from app.services.predict_eod import predict_eod_price
from app.services.fetch_data import get_all_index_stocks

bp = Blueprint('main', __name__)

@bp.route("/")
def index():
    return render_template("index.html")
    
@bp.route("/api/filters")
def get_filters():
    t = request.args.get("type")
    if t == "stock":
        return jsonify([
            "Information Technology", "Health Care", "Financials",
            "Consumer Discretionary", "Energy", "Industrials", "Real Estate",
            "Materials", "Utilities", "Communication Services", "Consumer Staples"
        ])
    elif t == "index":
        return jsonify(["S&P 500", "NASDAQ 100", "Dow Jones"])
    return jsonify([])

@bp.route("/api/trend")
def get_trend():
    symbol = request.args.get("symbol")
    import yfinance as yf
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1d", interval="5m")
    return jsonify({
        "timestamps": hist.index.strftime("%H:%M").tolist(),
        "prices": hist["Close"].fillna(method="ffill").tolist()
    })


@bp.route("/api/stocks")
def get_stocks():
    type_filter = request.args.get('type', 'stock')
    sector_filter = request.args.get('sector')
    index_filter = request.args.get('index')

    print("🔍 Loading stock data...")

    if type_filter == "index":
        data = get_all_index_stocks(limit=100)
    else:  # default to 'stock'
        data = get_top_stocks_by_all_sectors(limit_per_sector=5)

    if not data:
        print("⚠️ No data returned from fetch logic.")
        return jsonify([])

    filtered = []
    for row in data:
        try:
            price = row.get("price", 0)
            if not price or price <= 0:
                continue
            if type_filter == "stock" and sector_filter and row["sector"] != sector_filter:
                continue
            if type_filter == "index" and index_filter and row["index"] != index_filter:
                continue
            row["eod_prediction"] = predict_eod_price(price)
            filtered.append(row)
            print(f"✅ Loaded {row['symbol']} @ ${row['price']}")
        except Exception as e:
            print(f"⚠️ Skipping {row.get('symbol')} due to: {e}")
            continue

    return jsonify(filtered)

@bp.route("/api/blog")
def get_blog():
    symbol = request.args.get("symbol")
    query = f"{symbol} stock forecast blog site:seekingalpha.com OR site:marketwatch.com OR site:fool.com"
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    return jsonify({ "url": search_url })

