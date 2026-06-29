import pandas as pd
import requests
from price_parser import parse_price
from tqdm import tqdm
import random
from time import sleep
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('MOUSER_SEARCH_API_KEY')
BASE_URL= os.getenv('MOUSER_SEARCH_BASE_URL')

def get_parts(part_data: str) -> dict:
    """
    Output Mouser product from Part Number.
    
    :params str part_data: mouser part number format - [Mouser Mfg nb.]-[Mfg. Part Number] 
    :return: json with mouser part number details
    :rtype: dict
    :raises ValueError: if the part number doesn't exist
    """
    
    config = {
        "API_KEY":API_KEY,
        "BASE_URL":f'{BASE_URL}{API_KEY}',
    }
    
    try:
        sleep(random.randint(1,5))
        response = requests.post(config["BASE_URL"], json=part_data)
        data = response.json()
        return data

    except Exception as e:
        print(f'Error: {e}')
        
def main(header: list, pathCSV: str) -> pd.DataFrame:
    '''
    Output dataframe
    
    
    :params list header: header list, header must match predefined mouser keys
    :params str pathCSV: path to csv file
    :return: Return a pandas CSV-ready dataframe
    :rtype: pd.Dataframe
    '''
    try:
        
        product_df = pd.read_csv(pathCSV)
        product_df = product_df.reset_index()
        bom_df = []
        
        sum_price=0
        sum_parts=0
        

        for index, row in tqdm(product_df.iterrows(), desc="Creating BOM Mouser List..."):
            
            qty = row["Qty"]
            partnumber= row["Mouser Part Number"]
            
            part = {
            "SearchByPartRequest": {"mouserPartNumber": partnumber, "partSearchOptions": "None"}
            }
            
            item = get_parts(part_data=part)["SearchResults"]["Parts"][0]

            part_search_data = []
            bulk_price = []

            for key in header:
                try:
                    
                    match key:
                        case "#":
                            part_search_data.append(index)
                        
                        case "PriceBreaks":
                            for price in item.get('PriceBreaks'):
                                bulk_price.append([price.get('Quantity'), price.get('Price')])
                            part_search_data.append(bulk_price) 
                            
                        case "Pricing":
                            part_search_data.append(f'{parse_price(bulk_price[0][1], decimal_separator=",").amount_float*qty} €')
                            sum_price+=parse_price(bulk_price[0][1], decimal_separator=",").amount_float*qty
                
                        case "Quantity":
                            part_search_data.append(qty)
                            sum_parts+=qty
                        
                        case "AvailabilityOnOrder":
                            try:
                                date = item.get(key)[0].get('Date')
                                date = datetime.fromisoformat(date)
                                part_search_data.append(date.strftime("%Y-%m-%d"))
                            except:
                                part_search_data.append(None)
                                
                        
                        case _:
                            part_search_data.append(item.get(key))

                except Exception as e:
                    print(f'Error: {e}')
            bom_df.append(part_search_data)

        bom_df = pd.DataFrame(bom_df)
        
        new_file_name = input('Enter new file name:')

        bom_df.to_csv(f'{new_file_name}.csv',index=False, header=header,float_format='{:.3f}'.format)
        
        return {"bom":bom_df, "amount":sum_price, "totalParts":sum_parts}
    except FileNotFoundError:
        print("File not found, check path")

def bom_summary(df: dict) -> dict:
    
    try:
        summary = {
        "item count":len(df.get("bom").index),
        "price": f'{df.get("amount")} €',
        "VAT price": f'{df.get("amount")*1.2} €',
        "total parts": f'{df.get("totalParts")}',
        }
        
        return summary
    
    except AttributeError:
        print("Error parsing csv file.")

if __name__ == "__main__":
    
    HEARDERS = [
    "#",
    "MouserPartNumber",
    "Category",   
    "Description",
    "Manufacturer",
    "ManufacturerPartNumber",
    "PriceBreaks",
    "Pricing",
    "Quantity",
    "AvailabilityInStock",
    "AvailabilityOnOrder",
    "LeadTime",
    "DataSheetUrl",
    "ProductDetailUrl",
    "ImagePath"
    ]
    path = "bom_list.csv"
    
    print(50*'-')
    print("Creating Mouser BOM List")
    bom_dataframe= main(HEARDERS, path)
    
    print('Summary:\n')
    print(bom_summary(bom_dataframe))
    print(50*'-')