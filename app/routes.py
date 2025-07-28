from flask import Blueprint, jsonify, render_template
from app.services.fetch_data import get_top_stocks_by_all_sectors
from app.services.predict_eod import predict_eod_price
from app.services.fetch_data import get_all_index_stocks

bp = Blueprint('main', __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/api/stocks")
def get_sector_stocks():
    data = get_top_stocks_by_all_sectors(limit_per_sector=5)
    for stock in data:
        price = stock.get("price", 0)
        stock["eod_prediction"] = predict_eod_price(price)
    return jsonify(data)

@bp.route("/api/index-stocks")
def get_index_stocks():
    data = get_all_index_stocks(limit=100)
    for stock in data:
        price = stock.get("price", 0)
        stock["eod_prediction"] = predict_eod_price(price)
    return jsonify(data)
