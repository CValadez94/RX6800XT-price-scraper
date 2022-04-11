import bs4
import requests
from bs4 import BeautifulSoup


def get_microcenter_data():
    """
        Get's data related to a searched item from microcenter.com in Westmont, IL
    :return: status = [isRebate, isOnSale]
    """
    # Hardcode link for now
    # url = 'https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&rpp=96&N=4294966937+4294820651+4294808485&myStore=true&storeid=025'
    # page = requests.get(url)
    # soup = BeautifulSoup(page.content, "html.parser")
    # productGrid = soup.find(id="productGrid")
    # items = productGrid.find_all("div", class_="details")
    # list = results.find_all('li')
    is_rebate = False
    is_on_sale = False
    file = open("MC_Extract.html", 'r')
    contents = file.read()
    soup = BeautifulSoup(contents, "html.parser")
    items = soup.find_all("div", class_="details")

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
            is_rebate = True
            price_info += buffer.text + " : "

        # Print price (minus rebates)
        price_info += price_wrapper.find("span", {'itemprop': 'price'}).text

        # Deal with sales info
        buffer = price_wrapper.find("span", class_="strike")
        if buffer is not None:
            is_on_sale = True
            price_info += " Was " + buffer.text
            buffer = price_wrapper.find("span", class_="savings")
            if buffer is not None:
                price_info += " " + buffer.text

        # Extract the lowest price from price info, should be the first number in string
        end_index = price_info.find(' ') if len(price_info) > 10 else len(price_info)
        price = price_info[price_info.find('$') + 1:end_index]

        print("==============================================")
        print("Brand: {:s}\nID: {:s}\nName: {:s}\nPrice Info: {:s}\n"
              "Stock: {:s}\nPrice: {:s}".format(
            details["data-brand"], details["data-id"], details["data-name"],
            price_info, stock, price))


def print_bestbuy():
    url = 'https://www.bestbuy.com/'
    user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/' \
                                '20100101 Firefox/83.0'}
    page = requests.get(url, user_agent)
    print(page.status_code)
    # file = open("BB_Extract.html", 'w')
    # file.write(page.text)
    # file.close()


if __name__ == '__main__':
    # get_microcenter_data()
    print_bestbuy()
