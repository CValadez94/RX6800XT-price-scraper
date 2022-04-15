import datetime

import requests
from bs4 import BeautifulSoup
from flask import Flask

mc_data = dict()


class GPU:
    def __init__(self, brand, price, name, stock, link):
        self.brand = brand
        self.prices = [price]
        self.timestamp = [datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")]
        self.name = name
        self.stock = [stock]
        self.link = link

    def update(self, price, stock):
        self.prices.append(price)
        self.stock.append(stock)
        self.timestamp.append(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

    def get_current_price(self):
        return self.prices[-1]

    def get_current_stock(self):
        return self.stock[-1]

    def get_log_html(self):
        p = "<p>"
        for i in range(len(self.prices)):
            p += self.timestamp[-i-1] + " :: $" + self.prices[-i-1] + " Stock: " + self.stock[-i-1] + "</br>"
        p += "</p>"
        return p

    def get_link(self):
        return self.link


def get_microcenter_data():
    """
        Get's data related to a searched item from microcenter.com in Westmont, IL
    """
    # Hardcode link for now
    url = 'https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&rpp=96&N=4294966937+4294820651+4294808485&myStore=true&storeid=025'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    product_grid = soup.find(id="productGrid")
    items = product_grid.find_all("div", class_="details")
    # list = results.find_all('li')
    # file = open("MC_Extract.html", 'r')
    # contents = file.read()
    # soup = BeautifulSoup(contents, "html.parser")
    # items = soup.find_all("div", class_="details")

    print("Found {:d} at Microcenter".format(len(items)))
    for item in items:
        stock = item.find("span", class_="inventoryCnt").text
        details = item.find("a")
        price_wrapper = item.find("div", class_="price_wrapper")
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
        end_index = price_info.find(' ') if len(price_info) > 10 else len(price_info)
        price = price_info[price_info.find('$') + 1:end_index]

        brand = details["data-brand"]
        sku = str(details["data-id"])
        name = details["data-name"]
        link = "https://www.microcenter.com" + details["href"]

        # print("==============================================")
        # print("Brand: {:s}\nID: {:s}\nName: {:s}\nPrice Info: {:s}\n"
        #       "Stock: {:s}\nPrice: {:s}".format(brand, sku, name, price_info, stock, price))

        # Put data in dictionary
        if mc_data.get(sku) is None:  # Item does not exist in dictionary yet. Add it
            mc_data[sku] = GPU(brand, price, name, stock, link)
        else:
            # Update price and stock qty
            gpu = mc_data[sku]
            gpu.update(price, stock)
            mc_data[sku] = gpu


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
    app = Flask(__name__)

    @app.route("/")
    def display():
        get_microcenter_data()
        p = "<p>" + datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S") + "</p>"
        for key in mc_data:
            gpu = mc_data[key]
            p += "<p>" + "Price: <a href=\"" + gpu.get_link() + "\">$" + gpu.get_current_price() + "</a></br>"
            p += "Stock: " + gpu.get_current_stock() + "</br>"
            p += "Brand: " + gpu.brand + "</br>"
            p += "Name: " + gpu.name + "</br>"
            p += "<p>=====================================</p>"
        return p

    @app.route("/cheapest")
    def display_cheapest():
        get_microcenter_data()
        cheapest_price = None
        cheapest_sku = 0
        for key in mc_data:
            gpu = mc_data[key]
            gpu_price = float(gpu.get_current_price().replace(',', ''))
            if cheapest_price is None or (gpu_price < cheapest_price):
                cheapest_price = gpu_price
                cheapest_sku = key

        cheapest_gpu = mc_data[cheapest_sku]
        p = "<p><a href=\"" + cheapest_gpu.get_link() + "\">Cheapest GPU</a>" + " log:</p>"
        p += cheapest_gpu.get_log_html()
        return p


    app.run(host='0.0.0.0', port=5000, debug=True)
    # print_bestbuy()
