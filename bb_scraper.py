
"""
    Filename: bb_scraper.py
    Author: Jeff Gladstone
    Description:
    This program parses HTML from the Best Buy "Deals of The Day" web page
    to create a list of products with name and price.
    It then writes XML to an output document called 'bb_dotd.xml'
    and interacts with the user to determine what the user can afford
"""


# Initial imports
from lxml import html
import requests
import datetime

# The headers line prevents the 403 error on the request --- some websites have security that require this headers line
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
page = requests.get('http://www.bestbuy.com/site/misc/deal-of-the-day/pcmcat248000050016.c?id=pcmcat248000050016', headers=headers)
tree = html.fromstring(page.content)

# Parse HTML
prices = tree.xpath('//div[@class="pb-current-price  pb-sale-price"]/span/text()')
items = tree.xpath('//h3[@class="offer-link"]/a/text()')
items += tree.xpath('//h3[@class="feature-ellipsis"]/a/text()')

# Clean lists
prices = filter(lambda k: '$' not in k, prices)
items = filter(lambda k: '% Off' not in k, items)
items = filter(lambda k: 'Merchandise' not in k, items)
items = filter(lambda k: 'Save' not in k, items)

# Combine the two lists into one list of tuples. product[0] = item, product[1] = price. Both are str values
products = list(zip(items, prices))

# Write to output
with open("bb_dotd.xml", "w") as f:
	for product in products:
		f.write("<product>\n")
		f.write("\t<item>" + product[0] + "</item>\n")
		f.write("\t<price>" + product[1] + "</price>\n")
		f.write("</product>\n")

# Initializes variable for today's date and time
now = datetime.datetime.now()
now = now.strftime("%A, %B %d, %Y")
# User interaction
print("Welcome to Best Buy's 'Deals of the Day' for " + now + '.')
wallet = float(input('Enter the amount of money you can spend at Best Buy today:'))
wallet = '{0:.2f}'.format(wallet)   #str value
print('Your wallet holds $' + wallet + '. You can afford:')
for product in products:
	if (float(product[1]) <= float(wallet)):
		print('- ' + product[0] + ' [' + product[1] + ']')
