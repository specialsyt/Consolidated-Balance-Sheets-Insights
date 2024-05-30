from dataclasses import dataclass
import os
import warnings
from sec_downloader import Downloader
from sec_downloader.types import RequestedFilings
import sec_parser as sp

from database.database import Database
from processing.utils import ProcessingRequest

START_DATE = "1995-01-01"

class Fetch10K:
    """
    A class that handles the processing of financial data.

    Attributes:
        dl (Downloader): The downloader object used for retrieving financial data.

    Methods:
        lookup(ticker): Looks up the specified ticker and retrieves the '10-K' filing data after a specific start date.
        download(req): Downloads the 10-K filings for the specified ticker.
        read(req): Reads the 10-K filings for the specified ticker.
    """
    _instance = None

    def __init__(self, company_name: str, company_email: str, download_path: str = 'data'):
        try:
            Fetch10K._instance = self
            self.dl = Downloader(company_name, company_email)
        except:
            print('Could not connect to SEC EDGAR servers...')
            pass

    def get_all_html(self, ticker: str) -> list[str]:
        req = RequestedFilings(ticker, "10-K", limit=2024-1995)

        result = []
        for metadata in self.dl.get_filing_metadatas(req):
            try:
                html = self.dl.download_filing(url=metadata.primary_doc_url)
                result.append(html)
            except Exception as e:
                warnings.warn(f"Failed to download filing: {e}")
                pass
        
        return result
    
    def download(self, ticker: str) -> list[sp.AbstractSemanticElement]:
        
        result = self.get_all_html(ticker)
        parser = sp.Edgar10QParser()

        elements = []

        for html in result:

            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="Invalid section type for")
                elem = parser.parse(html)
                elements.append(elem)

        return elements
    
    def get_consolidated_balance_sheets(self, ticker: str) -> list[str]:
        db = Database.get_instance()
        if db.filing_is_cached(ticker):
            sheets = db.get_filing(ticker)
            return sheets
        
        elements = self.download(ticker)

        temp_elements: dict[int, list[sp.AbstractSemanticElement]] = {}
        for elem in enumerate(elements):
            temp_elements[2023 - int(elem[0])] = elem[1]

        elements = temp_elements

        sheets: list[str] = []
        for year in elements:
            elem = elements[year]
            for element in elem:
                if element.get_summary().find('CONSOLIDATED BALANCE SHEETS') != -1:
                    index = elem.index(element)
                    table_index = None
                    for i in range(index, index + 10):
                        if isinstance(elem[i], sp.TableElement) or elem[i].text.find('Current assets') != -1:
                            table_index = i
                            break
                    if table_index is not None:
                        sheets.append(f'YEAR {year}:\n\n' + elem[table_index].text)

                    break

        db.cache_filing(ticker, sheets)
        return sheets
    # def __lookup(self, ticker):
    #     """
    #     Looks up the specified ticker and retrieves the '10-K' filing data after a specific start date.

    #     Parameters:
    #         ticker (str): The ticker symbol of the company.

    #     Returns:
    #         dict: The '10-K' filing data for the specified ticker after the start date.
    #     """
    #     return self.dl.get("10-K", ticker, after=START_DATE)
    
    # def download(self, req: ProcessingRequest) -> int:
    #     """
    #     Downloads the 10-K filings for the specified ticker.

    #     Args:
    #         req (ProcessingRequest): The processing request object containing the ticker.

    #     Returns:
    #         str: The downloaded 10-K filings.
    #     """
    #     req.running = True
    #     count = self.dl.get("10-K", req.ticker, after=START_DATE, download_details=True)
    #     req.running = False
    #     req.cached = True

    #     return count
    
    # def get_10K_path(self) -> str:
    #     """
    #     Returns the path to the 10-K filings for the specified ticker.

    #     Args:
    #         ticker (str): The ticker symbol of the company.

    #     Returns:
    #         str: The path to the 10-K filings for the specified ticker.
    #     """
        
    #     return os.path.join(self.download_path, 'sec-edgar-filings')

    # def __new__(cls, *args, **kwargs):
    #     if cls._instance is None:
    #         cls._instance = super(Fetch10K, cls).__new__(cls)
    #     return cls._instance
