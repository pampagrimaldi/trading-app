import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "https://www.interactivebrokers.com/"  # The root URL of the website
current_page_url = base_url + "/en/index.php?f=2222&exch=asx&showcategories=STK&p=&ptab=&cc=&limit=100&page=1"

while True:
    response = requests.get(current_page_url)
    if response.status_code != 200:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        break

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table within the div with class 'table-responsive no-margin'
    table = soup.find('div', class_='table-responsive no-margin').find('table')

    # Process each table row and extract data
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if columns:
            ib_symbol = columns[0].text.strip()
            product_description = columns[1].text.strip()
            symbol = columns[2].text.strip()
            currency = columns[3].text.strip()

            # Print extracted data for debugging
            print(f"IB Symbol: {ib_symbol}, Product Description: {product_description}, Symbol: {symbol}, Currency: {currency}")

    # Find the pagination ul
    pagination = soup.find('ul', class_='pagination')

    if pagination:
        # Find all the page links
        page_links = pagination.find_all('a')

        # Assuming the 'Next' link is always the last one
        next_page_link = page_links[-1] if page_links else None

        # Check if the 'Next' page link is valid and not the current page
        if next_page_link and 'disabled' not in next_page_link.parent.get('class', []) and next_page_link.get(
                'href') != '#':
            # Update the current page URL
            current_page_url = urljoin(base_url, next_page_link['href'])
        else:
            break


    # Optional: Add delay to respect server load
    # time.sleep(1)
