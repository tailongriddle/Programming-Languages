import requests

url = 'http://quotes.toscrape.com/'
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    html_content = response.text
else:
    print("Failed to retrieve the website")
    
from bs4 import BeautifulSoup

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Example of finding a specific element
# (this will not directly apply to your task but gives you an idea)
# example_element = soup.find('div', class_='quote')
#print(example_element)

# Example of finding all of the elements matching some tag and class
all_quotes = soup.find_all('span', class_='text')
all_authors = soup.find_all('small', class_= 'author')


# Note that the elements of all_funky_divs will contain the full HTML tag
# To extract the inner text of an element, use the .get_text() function:
#all_funky_divs[0]               # --> "<div class="funky">Woah here's some funky stuff</div>"
#toPrint = all_funky_divs.get_text()    # --> "Woah here's some funky stuff"

for each in range(len(all_quotes)):
    print ("Quote: ", all_quotes[each].get_text())
    print ("Author:", all_authors[each].get_text())
    print("")
    
    
    