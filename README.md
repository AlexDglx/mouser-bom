# Mouser BOM creator

## Purpose
This code uses a csv file with a list of Mouser or Manufacturer Part Numbers created with kicad or any other EDA software and outputs details from api response (if the part exists).

The csv file must include either Mouser Part Number or Manufacturer Part number.

> Note: For better results I recommend using Mouser Part Numbers. Mouser part number is [XXX]-[Manufacturer Part Number]

## Getting Started

### API key

Get your Search API key at [mouser.com]('https://www.mouser.com'), log in to your account and go to **Account**, you'll see at the bottom of the left panel an **API** section, and follow Mouser's guide.

### Setup

You never put your API key within your code. Create a .env and place your api key in the environment file.

`.env`
```python
MOUSER_SEARCH_API_KEY="YOUR_API_KEY"
MOUSER_SEARCH_BASE_URL="https://api.mouser.com/api/v1/search/partnumber?apiKey="
```

> This uses version 1 of Mouser's API search.

### Usage

Check out `mouser-response.json` to see which json keys are available to extract which need to be placed in the HEADERS list.

`createBOM()`takes 2 arguments, a list of headers and a path to your csv file with Mouser or Manufacturer Part numbers.

```python
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
    path = "PATH_TO_BOM.csv"
```



### API restrictions

Mouser's search api limits:
- up to 50 results per returned calls
- up to 30 calls per minute
- up to 1,000 calls per day

_source: [api search limits](https://eu.mouser.com/api-search/)_ 

### Search API Developer Guide

I recommend looking into the search API guide available [Search API Developer Guide](https://eu.mouser.com/api-search/) 

Available calls:

- `POST` /api/v1/search/keyword
- `POST` /api/v1/search/partnumber

