# Google Search API

> ⚠️ As of January 2025, [Google requires JavaScript](https://techcrunch.com/2025/01/17/google-begins-requiring-javascript-for-google-search/) to render search results. This update aims to block traditional bots, scrapers, and SEO tools that rely on non-JavaScript-based methods. As a result, businesses using Google Search for market research or ranking analysis must adopt tools that support JavaScript rendering.


This repository provides two approaches for collecting Google SERP data:

1. A free, small-scale scraper suitable for basic data collection
2. An enterprise-grade API solution built for high-volume and robust data needs


## Table of Contents
- [Free Scraper](#free-scraper)
  - [Input Parameters](#input-parameters)
  - [Implementation](#implementation)
  - [Sample Output](#sample-output)
  - [Limitations](#limitations)
- [Bright Data Google Search API](#bright-data-google-search-api)
  - [Key Features](#key-features)
  - [Getting Started](#getting-started)
  - [Direct API Access](#direct-api-access)
  - [Native Proxy-Based Access](#native-proxy-based-access)
- [Advanced Features](#advanced-features)
  - [Localization](#localization)
  - [Search Type](#search-type)
  - [Pagination](#pagination)
  - [Geo-Location](#geo-location)
  - [Device Type](#device-type)
  - [Browser Type](#browser-type)
  - [Parsing Results](#parsing-results)
  - [Hotel Search](#hotel-search)
  - [Parallel Searches](#parallel-searches)
  - [AI Overview](#ai-overview)
- [Support & Resources](#support--resources)


## Free Scraper
A lightweight Google scraper for basic data collection needs.

<img width="700" alt="google-search-result" src="https://github.com/luminati-io/google-search-api/blob/main/images/416310595-58573147-5ac2-4cb3-bb5e-295d76f6972c.png" />

### Input Parameters

- **File:** List of search terms to query in Google (required)
- **Pages:** Number of Google pages to scrape data from

### Implementation
Modify these parameters in the [Python file](https://github.com/luminati-io/Google-Search-API/blob/main/free_google_scraper/google_serp.py):

```python
HEADLESS = False        
MAX_RETRIES = 2         
REQUEST_DELAY = (1, 4) 

SEARCH_TERMS = [
    "nike shoes",
    "macbook pro"
]
PAGES_PER_TERM = 3      
```

💡 **Tip:** Set `HEADLESS = False` to help avoid Google's detection mechanisms.

### Sample Output
<img width="700" alt="google-serp-data" src="https://github.com/luminati-io/google-search-api/blob/main/images/416109839-c7048fc9-44c3-4553-8117-2b238d354f70.png" />


### Limitations

Google implements several anti-scraping measures:

1. **CAPTCHAs:** Used to differentiate between humans and bots
2. **IP Blocks:** Temporary or permanent bans for suspicious activity
3. **Rate Limiting:** Rapid requests may trigger blocks
4. **Geotargeting:** Results vary by location, language, and device
5. **Honeypot Traps:** Hidden elements to detect automated access

After multiple requests, you'll likely encounter Google's CAPTCHA challenge:

<img width="700" alt="google-captcha" src="https://github.com/luminati-io/google-search-api/blob/main/images/414117571-21ab3e9f-1162-4aef-9e22-fb08491dd928.png" />

## Bright Data Google Search API
[Bright Data's Google Search API](https://brightdata.com/products/serp-api/google-search) provides real-user search results from Google using customizable search parameters. Built on the same advanced technology as the [SERP API](https://brightdata.com/products/serp-api), it delivers high success rates and robust performance for scraping publicly available data at scale.


### Key Features

- High Success Rates, even with large volumes
- Pay only for successful requests
- Fast response time - under 5 seconds
- Geolocation targeting – Extract data from any country, city, or device
- Output formats – Retrieve data in JSON or raw HTML
- Multiple search types – News, images, shopping, jobs, etc
- Asynchronous requests – Fetch results in batches
- Built for scale – Handles high traffic and peak loads

📌 Test it for free in our [SERP Playground](https://brightdata.com/products/serp-api/google-search):

<img width="700" alt="bright-data-serp-api-playground" src="https://github.com/luminati-io/google-search-api/blob/main/images/416966701-8d516e08-37a1-4723-bf12-9a9da6a13b1a.png" />


### Getting Started

1. **Prerequisites:**
    - Create a [Bright Data account](https://brightdata.com/) (new users receive a $5 credit)
    - Obtain your [API key](https://docs.brightdata.com/general/account/api-token)
2. **Setup:** Follow the [step-by-step guide](https://github.com/luminati-io/Google-Search-API/blob/main/setup_serp_api.md) to integrate the SERP API into your Bright Data account
3. **Implementation Methods:**
    - Direct API Access
    - Native Proxy-Based Access


### Direct API Access
The simplest method is to make a direct request to the API.

**cURL Example**
```bash
curl https://api.brightdata.com/request \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer API_TOKEN" \
  -d '{
        "zone": "ZONE_NAME",
        "url": "https://www.google.com/search?q=ollama&brd_json=1",
        "format": "raw"
      }'
```

**Python Example**
```python
import requests
import json

url = "https://api.brightdata.com/request"

headers = {"Content-Type": "application/json", "Authorization": "Bearer API_TOKEN"}

payload = {
    "zone": "ZONE_NAME",
    "url": "https://www.google.com/search?q=ollama&brd_json=1",
    "format": "raw",
}

response = requests.post(url, headers=headers, json=payload)

with open("serp_direct_api.json", "w") as file:
    json.dump(response.json(), file, indent=4)

print("Response saved to 'serp_direct_api.json'.")
```

👉 View [full JSON output](https://github.com/luminati-io/Google-Search-API/blob/main/google_search_api_outputs/serp_direct_api.json)

> **Note**: Use `brd_json=1` for parsed JSON or `brd_json=html` for parsed JSON + full nested HTML.

Learn more about parsing search results in our [SERP API Parsing Guide](https://docs.brightdata.com/scraping-automation/serp-api/parsing-search-results).

### Native Proxy-Based Access
Alternatively, you can use our proxy routing method.

**cURL Example**
```bash
curl -i \
  --proxy brd.superproxy.io:33335 \
  --proxy-user "brd-customer-<CUSTOMER_ID>-zone-<ZONE_NAME>:<ZONE_PASSWORD>" \
  -k \
  "https://www.google.com/search?q=ollama"
```

**Python Example**
```python
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host = "brd.superproxy.io"
port = 33335
username = "brd-customer-<customer_id>-zone-<zone_name>"
password = "<zone_password>"
proxy_url = f"http://{username}:{password}@{host}:{port}"

proxies = {"http": proxy_url, "https": proxy_url}

url = "https://www.google.com/search?q=ollama"
response = requests.get(url, proxies=proxies, verify=False)

with open("serp_native_proxy.html", "w", encoding="utf-8") as file:
    file.write(response.text)

print("Response saved to 'serp_native_proxy.html'.")
```

👉 View [full HTML output](https://github.com/luminati-io/Google-Search-API/blob/main/google_search_api_outputs/serp_native_proxy.html)

For production, load Bright Data’s SSL certificate (see our [SSL Certificate Guide](https://docs.brightdata.com/general/account/ssl-certificate)).

## Advanced Features

### Localization
<img width="700" alt="bright-data-google-search-api-screenshot-localization" src="https://github.com/luminati-io/google-search-api/blob/main/images/416281053-eb050c00-3c35-451b-a2d2-e98e16f91aee.png" />


1. `gl` (Country Code)
    - Two-letter country code that determines the country for search results
    - Simulates a search as if made from a specific country
    
    Example: Search for restaurants in France
    
    ```bash
    curl --proxy brd.superproxy.io:33335 \
     --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
     "https://www.google.com/search?q=best+restaurants+in+paris&gl=fr"
    ```
    
2. `hl` (Language Code)
    - Two-letter language code that sets the language of page content
    - Affects the interface and search results language
    
    Example: Search for sushi restaurants in Japan (results in Japanese)
    
    ```bash
    curl --proxy brd.superproxy.io:33335 \
     --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
     "https://www.google.com/search?q=best+sushi+restaurants+in+tokyo&hl=ja"
    ```
    
    You can use both parameters together for better localization:
    
    ```bash
    curl --proxy brd.superproxy.io:33335 \
     --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
     "https://www.google.com/search?q=best+hotels+in+berlin&gl=de&hl=de"
    ```

### Search Type
<img width="700" alt="bright-data-google-search-api-screenshot-search-type" src="https://github.com/luminati-io/google-search-api/blob/main/images/416280410-49853108-5e3d-4062-831b-8d55711d5f54.png" />

1. `tbm` (Search Category)
    - Specifies a particular search type (images, news, etc.)
    - **Options**:
        - `tbm=isch` → **Images**
        - `tbm=shop` → **Shopping**
        - `tbm=nws` → **News**
        - `tbm=vid` → **Videos**
    
    **Example** (Shopping search):
    
    ```bash
    curl --proxy brd.superproxy.io:33335 \
         --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
         "https://www.google.com/search?q=macbook+pro&tbm=shop"
    ```
    
2. `ibp` (Jobs Search Parameter)
    - Use specifically for jobs-related searches
    - Example: `ibp=htl;jobs` returns job listings
    
    **Example**:
    
    ```bash
    curl --proxy brd.superproxy.io:33335 \
         --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
         "https://www.google.com/search?q=technical+copywriter&ibp=htl;jobs"
    ```

### Pagination

Navigate through pages of results or adjust the number of displayed results:

1. `start`
    - Defines the starting point for search results
    - Examples:
        - `start=0` (default) - First page
        - `start=10` - Second page (results 11-20)
        - `start=20` - Third page (results 21-30)
    
    **Example** (Start from the 11th result):
    
    ```bash
    curl --proxy brd.superproxy.io:33335 \
         --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
         "https://www.google.com/search?q=best+coding+laptops+2025&start=10"
    ```
    
2. `num`
    - Defines how many results to return per page
    - Examples:
        - `num=10` (default) - Returns 10 results
        - `num=50` - Returns 50 results
    
    **Example** (Return 40 results):
    
    ```bash
    curl --proxy brd.superproxy.io:33335 \
         --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
         "https://www.google.com/search?q=best+coding+laptops+2025&num=40"
    ```


### Geo-Location
<img width="700" alt="bright-data-google-search-api-screenshot-geolocation" src="https://github.com/luminati-io/google-search-api/blob/main/images/416279186-af64c770-0c8a-4007-9415-304d2e0c0fe8.png" />

The `uule` parameter customizes search results based on a specific location:

- It requires an encoded string, not plain text.
- Locate the raw location string in the Canonical Name column of [Google's geotargeting CSV](https://developers.google.com/adwords/api/docs/appendix/geotargeting).
- Convert the raw string into the encoded format using a third-party converter or a built-in library.
- Include the encoded string in your API request as the value for `uule`.

```bash
curl --proxy brd.superproxy.io:33335 \
     --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
     "https://www.google.com/search?q=best+hotels+in+paris&uule=w+CAIQICIGUGFyaXM"
```

### Device Type

<img width="700" alt="bright-data-google-search-api-screenshot-device-type" src="https://github.com/luminati-io/google-search-api/blob/main/images/416278511-cf0f203f-5d62-4eb9-9d28-7a50d75c7a00.png" />


Use the `brd_mobile` parameter to simulate requests from specific devices:

| Value | Device | User-Agent Type |
| --- | --- | --- |
| `0` or omit | Desktop | Desktop |
| `1` | Mobile | Mobile |
| `ios` or `iphone` | iPhone | iOS |
| `ipad` or `ios_tablet` | iPad | iOS Tablet |
| `android` | Android | Android |
| `android_tablet` | Android Tablet | Android Tablet |

**Example: Mobile Search**

```bash
curl --proxy brd.superproxy.io:33335 \
     --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
     "https://www.google.com/search?q=best+laptops&brd_mobile=1"
```

### Browser Type
<img width="700" alt="bright-data-google-search-api-screenshot-browser-type" src="https://github.com/luminati-io/google-search-api/blob/main/images/416277969-df382cb0-0eb2-4fb1-982c-2fa3401cc83a.png" />

Use the `brd_browser` parameter to simulate requests from specific browsers:

- `brd_browser=chrome` — Google Chrome
- `brd_browser=safari` — Safari
- `brd_browser=firefox` — Mozilla Firefox (not compatible with `brd_mobile=1`)

If not specified, the API uses a random browser.

**Example**:

```bash
curl --proxy brd.superproxy.io:33335 \
     --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
     "https://www.google.com/search?q=best+gaming+laptops&brd_browser=chrome"
```

**Example** (Combining browser and device type):

```bash
curl --proxy brd.superproxy.io:33335 \
     --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
     "https://www.google.com/search?q=best+smartphones&brd_browser=safari&brd_mobile=ios"
```

### Parsing Results

Receive search results in a structured format using the `brd_json` parameter:

- **Options**:
    - `brd_json=1` - Returns results in parsed JSON format
    - `brd_json=html` - Returns JSON with an additional `"html"` field containing raw HTML

Example (JSON output):

```bash
curl --proxy brd.superproxy.io:33335 \
     --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
     "https://www.google.com/search?q=best+hotels+in+new+york&brd_json=1"
```

Example (JSON with raw HTML):

```bash
curl --proxy brd.superproxy.io:33335 \
     --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
     "https://www.google.com/search?q=top+restaurants+in+paris&brd_json=html"
```

Learn more in our [SERP API Parsing Guide](https://docs.brightdata.com/scraping-automation/serp-api/parsing-search-results).


### Hotel Search

<img width="700" alt="bright-data-google-search-api-screenshot-google-hotels-search" src="https://github.com/luminati-io/google-search-api/blob/main/images/416277071-0859191a-47c0-4373-b3af-a1bc04ea54b1.png" />


Refine hotel searches with these parameters:

1. `hotel_occupancy` (Number of Guests)
    - Sets the number of guests (up to 4)
    - Examples:
        - `hotel_occupancy=1` → For 1 guest
        - `hotel_occupancy=2` → For 2 guests (default)
        - `hotel_occupancy=4` → For 4 guests
    
    **Example** (Search for hotels in New York for 4 guests):
    
    ```bash
    curl --proxy brd.superproxy.io:33335 \
         --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
         "https://www.google.com/search?q=hotels+in+new+york&hotel_occupancy=4"
    ```
    
2. `hotel_dates` (Check-in & Check-out Dates)
    - Filters results for specific date ranges
    - Format: YYYY-MM-DD, YYYY-MM-DD
    
    **Example** (Search for hotels in Paris from May 1 to May 3, 2025):
    
    ```bash
    curl --proxy brd.superproxy.io:33335 \
         --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
         "https://www.google.com/search?q=hotels+in+paris&hotel_dates=2025-05-01%2C2025-05-03"
    ```
    
    **Combined Example**:
    
    ```bash
    curl --proxy brd.superproxy.io:33335 \
         --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
         "https://www.google.com/search?q=hotels+in+tokyo&hotel_occupancy=2&hotel_dates=2025-05-01%2C2025-05-03"
    ```

### Parallel Searches

Send multiple search requests simultaneously within the same peer and session—ideal for comparing results.

1. Send a POST request with a `multi` array containing search variations
2. Get a `response_id` for later result retrieval
3. Retrieve results using the `response_id` once processing completes

**Step 1: Send Parallel Requests**

```bash
RESPONSE_ID=$(curl -i --silent --compressed \
  "https://api.brightdata.com/serp/req?customer=<customer-id>&zone=<zone-name>" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer API_TOKEN" \
  -d $'{
    "country": "us",
    "multi": [
      {"query": {"q": "top+macbook+for+developers", "num": 20}},
      {"query": {"q": "top+macbook+for+developers", "num": 100}}
    ]
  }' | sed -En 's/^x-response-id: (.*)/\1/p' | tr -d '\r')

echo "Response ID: $RESPONSE_ID"
```

**Step 2: Fetch Results**

```bash
curl -v --compressed \
     "https://api.brightdata.com/serp/get_result?customer=<customer-id>&zone=<zone-name>&response_id=${RESPONSE_ID}" \
     -H "Authorization: Bearer API_TOKEN"
```

You can also search for multiple keywords in one request:

```bash
{
  "multi":[
    {"query":{"q":"best+smartphones+2025"}},
    {"query":{"q":"best+laptops+2025"}}
  ]
}
```

Learn more about asynchronous requests [here](https://docs.brightdata.com/scraping-automation/serp-api/asynchronous-requests).

### AI Overview

<img width="700" alt="bright-data-google-search-api-screenshot-google-ai-overview" src="https://github.com/luminati-io/google-search-api/blob/main/images/416276209-3c7be724-e8d9-45ed-b781-017b1cbec9d4.png" />

Google sometimes includes AI-generated summaries (AI Overviews) at the top of search results. Use `brd_ai_mode=1` to increase the chances of seeing these AI-generated overviews:

```bash
curl --proxy brd.superproxy.io:33335 \
     --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
     "https://www.google.com/search?q=how+does+caffeine+affect+sleep&brd_ai_mode=1"
```


## Support & Resources

- **Documentation:** [SERP API Docs](https://docs.brightdata.com/scraping-automation/serp-api/)
- **SEO Use Cases:** [SEO Tracking and Insights](https://brightdata.com/use-cases/serp-tracking)
- **Other Guides:**
    - [SERP API](https://github.com/luminati-io/serp-api)
    - [Web Unlocker API](https://github.com/luminati-io/web-unlocker-api)
    - [Google Maps Scraper](https://github.com/luminati-io/Google-Maps-Scraper)
    - [Google News Scraper](https://github.com/luminati-io/Google-News-Scraper)
- **Interesting Reads:**
    - [Best SERP APIs](https://brightdata.com/blog/web-data/best-serp-apis)
    - [Build a RAG Chatbot with SERP API](https://brightdata.com/blog/web-data/build-a-rag-chatbot)
    - [Scrape Google Search with Python](https://brightdata.com/blog/web-data/scraping-google-with-python)
- **Technical Support:** [Contact Us](mailto:support@brightdata.com)
