#!/usr/bin/env python

from api import app
from database.database import Database
from inference.inference import infer
from processing.fetch10K import Fetch10K
from processing.parse10K import Parse10K
import os

from processing.utils import ProcessingRequest

COMPANY_NAME = os.getenv('COMPANY_NAME') or 'GT'
COMPANY_EMAIL = os.getenv('COMPANY_EMAIL') or 'noreply@gatech.edu'
SEC_DOWNLOAD_PATH = os.getenv('SEC_DOWNLOAD_PATH') or None

def main():
    print('Starting application...')
    _ = Database('fsil.db', 'filingsCache')
    fetcher = Fetch10K(COMPANY_NAME, COMPANY_EMAIL, SEC_DOWNLOAD_PATH)
    sheets = fetcher.get_consolidated_balance_sheets('AAPL')
    inference = infer('AAPL', sheets)
    app.run(debug=True)

if __name__ == '__main__':
    main()