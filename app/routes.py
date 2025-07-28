from flask import Blueprint, jsonify, render_template
from app.services.fetch_data import get_top_stocks
from app.services.predict_eod import predict_eod_price

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/api/stocks')
def get_stocks():
    df = get_top_stocks()
    df['eod_prediction'] = df['price'].apply(predict_eod_price)
    return jsonify(df.to_dict(orient="records"))
