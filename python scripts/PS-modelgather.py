import requests
from bs4 import BeautifulSoup

# URL you want to scrape
url = "https://www.partselect.com/PS8730270-Bosch-00645038-FILTER-MICRO.htm?SourceCode=3&SearchTerm=00645038"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all <a> tags where the href attribute starts with '/Models/'
    links = soup.find_all('a', href=lambda value: value and value.startswith('/Models/'))
    
    # Check if any links were found
    if links:
        for link in links:
            # Print the full URL of each link
            # Assuming the URL is relative to the base URL
            print(url + link['href'])
    else:
        print("No links starting with '/Models/' were found.")
else:
    print(f"Failed to retrieve the web page. Status code: {response.status_code}")
