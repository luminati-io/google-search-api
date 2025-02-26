import asyncio
import csv
import time
import random
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from typing import Optional
from playwright.async_api import async_playwright, ElementHandle
from playwright_stealth import stealth_async

# --- Configuration ---
HEADLESS = False        # Visible browser window for debugging 
MAX_RETRIES = 2         # Retry attempts per page request
REQUEST_DELAY = (1, 4)  # Random delay range between requests (seconds)

SEARCH_TERMS = [
    "automated web unlocker",
    "web scraping tutorial"
]
PAGES_PER_TERM = 3      # Results pages per search query

async def scrape_search_element(
    search_element: ElementHandle, 
    rank: int, 
    search_term: str,
    page_number: int
) -> Optional[dict]:
    """Parse individual search result component."""
    try:
        # Title extraction
        title_element = await search_element.query_selector("h3")
        title = await title_element.inner_text() if title_element else None

        # URL cleaning (unwrap Google's redirects)
        url_element = await search_element.query_selector("a[href]")
        raw_url = await url_element.get_attribute("href") if url_element else None
        parsed_url = urlparse(raw_url) if raw_url else None
        
        url = raw_url  # Fallback value
        if parsed_url and parsed_url.path == "/url" and 'q' in parse_qs(parsed_url.query):
            url = parse_qs(parsed_url.query)['q'][0]

        return {
            'search_term': search_term,
            'rank': rank,
            'title': title,
            'url': url,
            'page_number': page_number
        }
    except Exception as e:
        print(f"Error scraping result {rank}: {e}")
        return None

async def perform_search(
    page: ElementHandle,
    search_term: str,
    current_term: int,
    total_terms: int,
    page_number: int
) -> list:
    """Execute search request with retry logic."""
    start_index = (page_number - 1) * 10
    
    for attempt in range(MAX_RETRIES):
        try:
            print(f"[Term {current_term}/{total_terms}] Page {page_number} - Attempt {attempt+1} for '{search_term}'...")
            
            # Construct paginated search URL
            search_url = f"https://www.google.com/search?q={search_term}&hl=en-US&start={start_index}"
            await page.goto(search_url, timeout=60000)
            
            # Dismiss GDPR cookie consent if present
            try:
                await page.wait_for_selector("button:has-text('Accept all')", timeout=5000)
                await page.click("button:has-text('Accept all')")
                await page.wait_for_selector("button:has-text('Accept all')", state="hidden", timeout=10000)
            except Exception:
                pass
            
            # Wait for core results container
            await page.wait_for_selector("div.g", timeout=15000)
            
            # Randomized human interaction pattern
            await asyncio.sleep(random.uniform(*REQUEST_DELAY))
            
            # Process results with actual SERP ranking
            search_elements = await page.query_selector_all("div.g")
            results = []
            base_rank = start_index + 1  # Maintain absolute ranking
            
            for element_rank, element in enumerate(search_elements, base_rank):
                if result := await scrape_search_element(element, element_rank, search_term, page_number):
                    results.append(result)

            print(f"✓ Found {len(results)} results on page {page_number}")
            return results

        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt == MAX_RETRIES - 1:
                return []
            await asyncio.sleep(2 ** (attempt + 1))  # Exponential backoff
    return []

async def main() -> None:
    """Core orchestrator with resource management."""
    start_time = time.time()
    total_results = 0
    
    print(f"Scraper initialized: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Processing {len(SEARCH_TERMS)} terms × {PAGES_PER_TERM} pages")

    # Unique output file per execution
    csv_filename = f"serp_data.csv"
    
    with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            "search_term", "rank", "title", "url", "page_number"
        ])
        writer.writeheader()

        async with async_playwright() as p:
            # Anti-detection browser context
            async with await p.chromium.launch(headless=HEADLESS) as browser:
                async with await browser.new_context() as context:
                    
                    for term_idx, term in enumerate(SEARCH_TERMS, 1):
                        page = await context.new_page()
                        await stealth_async(page)  # Evade basic bot detection
                        
                        for page_num in range(1, PAGES_PER_TERM + 1):
                            results = await perform_search(
                                page, term, term_idx, len(SEARCH_TERMS), page_num
                            )
                            
                            if results:
                                writer.writerows(results)
                                total_results += len(results)
                                csvfile.flush()  # Prevent data loss on crash
                            
                            # Inter-page delay (except last page)
                            if page_num < PAGES_PER_TERM:
                                await asyncio.sleep(random.uniform(*REQUEST_DELAY))
                        
                        await page.close()

    # Performance summary
    duration = time.time() - start_time
    print(f"\nScrape completed in {duration:.1f}s")
    print(f"Total results collected: {total_results}")
    print(f"Output file: {csv_filename}")

if __name__ == "__main__":
    asyncio.run(main())