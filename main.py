import bs4
import requests
from bs4 import BeautifulSoup, Tag


def print_microcenter():
    # Hardcode link for now
    # url = 'https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&rpp=96&N=4294966937+4294820651+4294808485&myStore=true&storeid=025'
    # page = requests.get(url)
    # soup = BeautifulSoup(page.content, "html.parser")
    # productGrid = soup.find(id="productGrid")
    # items = productGrid.find_all("div", class_="details")
    # list = results.find_all('li')

    file = open("Test.html", 'r')
    contents = file.read()
    soup = BeautifulSoup(contents, "html.parser")
    items = soup.find_all("div", class_="details")
    # file = open("Test.html", "w")
    # file.write(page.text)
    # file.close()

    print("Found {:d} at Microcenter".format(len(items)))
    for item in items:
        stock = item.find("span", class_="inventoryCnt").text[0]
        details = item.find("a")
        price_wrapper = item.find("div", class_="price_wrapper")
        price = None
        price_info = ""

        # Deal with rebates
        buffer = price_wrapper.find("div", class_="rebate-price")
        if len(buffer.text) > 0:
            price_info += buffer.text + " : "

        # Print price (minus rebates)
        price_info += price_wrapper.find("span", {'itemprop': 'price'}).text

        # Deal with sales info
        buffer = price_wrapper.find("span", class_="strike")
        if buffer is not None:
            price_info += " Was " + buffer.text
            buffer = price_wrapper.find("span", class_="savings")
            if buffer is not None:
                price_info += " " + buffer.text

        # Extract the lowest price from price info, should be the first number in string
        price = price_info[price_info.find('$'):price_info.find(' ')]

        print("==============================================")
        print("Brand: {:s}\nID: {:s}\nName: {:s}\nPrice Info: {:s}\n"
              "Stock: {:s}\nPrice: {:s}".format(
            details["data-brand"], details["data-id"], details["data-name"],
            price_info, stock, price))


def print_bestbuy(url):
    pass


if __name__ == '__main__':
    print_microcenter()
    print_bestbuy('Test.html')
