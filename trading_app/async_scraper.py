import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time

base_url = "https://www.interactivebrokers.com/"
first_page_url = "/en/index.php?f=2222&exch=asx&showcategories=STK&p=&ptab=&cc=&limit=100&page=1"


async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()


async def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', class_='table-responsive no-margin').find('table')
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if columns:
            ib_symbol = columns[0].text.strip()
            product_description = columns[1].text.strip()
            symbol = columns[2].text.strip()
            currency = columns[3].text.strip()
            print(f"IB Symbol: {ib_symbol}, Product Description: {product_description}, Symbol: {symbol}, Currency: {currency}")
    return soup


async def get_page_urls(session, first_page_url):
    urls = [first_page_url]
    first_page_html = await fetch_page(session, first_page_url)
    soup = await parse_page(first_page_html)

    # Logic to determine the total number of pages
    pagination = soup.find('ul', class_='pagination')
    if pagination:
        # Assuming that the last page number is in the last 'li' before the 'Next' button
        last_page_number = int(pagination.find_all('li')[-2].text)
        for i in range(2, last_page_number + 1):
            page_url = base_url + f"/en/index.php?f=2222&exch=asx&showcategories=STK&p=&ptab=&cc=&limit=100&page={i}"
            urls.append(page_url)

    return urls


async def main():
    async with aiohttp.ClientSession() as session:
        page_urls = await get_page_urls(session, base_url + first_page_url)

        tasks = [asyncio.create_task(fetch_page(session, url)) for url in page_urls]
        pages = await asyncio.gather(*tasks)

        for page_html in pages:
            await parse_page(page_html)

if __name__ == '__main__':

    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f'Total time taken {end_time - start_time} seconds')
