import os
import xml.etree.ElementTree as ET
import sec_parser as sp



class Parse10K:

    def __init__(self, path: str):
        self.path = path
        pass

    # def get_all_years(self, ticker: str):
    #     """
    #     Returns all the years in the 10-K filings
    #     """
    #     files = self.__get_path(ticker)
    #     years = [file.split('-')[1] for file in files]
        
    #     return years
    #     # pass

    # def read_all_filings(self, ticker: str):
    #     """
    #     Reads all the 10-K filings for the specified ticker.
    #     """
    #     files = self.__get_path(ticker)
    #     filings = [self.__extract_xml_from_pem(os.path.join(self.path, ticker, '10-K', file, 'full-submission.txt')) for file in files]
    #     parsed_filings = [self._parse_filing(filing) for filing in filings]

    #     return parsed_filings
    
    # def __extract_xml_from_pem(self, pem_file_path):
    #     with open(pem_file_path, 'r') as file:
    #         lines = file.readlines()

    #     try:
    #         # Find the line numbers for the PEM header and footer
    #         start_line = next(i for i, line in enumerate(lines) if line.strip().startswith('<SEC-DOCUMENT>'))
    #         end_line = next(i for i, line in enumerate(lines) if line.strip().startswith('</SEC-DOCUMENT>')) + 1

    #         # Extract the lines between the PEM header and footer
    #         xml_lines = lines[start_line:end_line]
    #     except:
    #         xml_lines = lines

    #     # Join the lines together into a single string
    #     xml_string = ''.join(xml_lines)

    #     return xml_string
    

    # def _parse_filing(self, filing_data: str) -> str:
    #     """
    #     Parses the specified 10-K filing.

    #     Args:
    #         filing_data (str): The 10-K filing to parse.

    #     Returns:
    #         str: The parsed 10-K filing.
    #     """
    #     # Write the filing data to a temporary file
    #     # Create file first
    #     if not os.path.exists('temp'):
    #         os.makedirs('temp')
    #     with open('temp/t.txt', 'w') as file:
    #         file.write(filing_data)
    #     # Parse the XML data
    #     tree = ET.ElementTree(ET.fromstring(filing_data))

    #     # Initialize an empty dictionary to hold the parsed data
    #     parsed_data = {}

    #     # Iterate over all elements in the tree
    #     for elem in tree.iter():
    #         # Use the tag as the key and the text as the value
    #         parsed_data[elem.tag] = elem.text

    #     return parsed_data

    # def __read_file(self, path: str) -> str:
    #     """
    #     Reads the file at the specified path.

    #     Args:
    #         path (str): The path to the file.

    #     Returns:
    #         str: The contents of the file.
    #     """
    #     with open(path, 'r') as file:
    #         return file.read()

    # def __get_path(self, ticker: str):
    #     return os.listdir(os.path.join(self.path, ticker, '10-K'))