from flask import render_template
from api import app
from database.database import Database
from inference.inference import infer
from processing.fetch10K import Fetch10K

fetcher = Fetch10K._instance

@app.before_request
def register_database():
    global db
    global fetcher

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filing/<string:ticker>/isCached')
def filing_is_cached(ticker: str):
    db = Database.get_instance()
    return str(db.filing_is_cached(ticker))

@app.route('/filing/<string:ticker>/infer')
def infer_on_ticker(ticker: str):
    fetcher = Fetch10K._instance
    sheets = fetcher.get_consolidated_balance_sheets(ticker)
    inference = infer(ticker, sheets)
    return inference

@app.route('/filing/<string:ticker>/infer/refresh')
def refresh_infer_on_ticker(ticker: str):
    fetcher = Fetch10K._instance
    sheets = fetcher.get_consolidated_balance_sheets(ticker)
    inference = infer(ticker, sheets, force=True)
    return inference
