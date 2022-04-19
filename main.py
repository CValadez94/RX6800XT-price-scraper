import datetime

import requests
from bs4 import BeautifulSoup
from flask import Flask

data_6800XT = dict()
data_6900XT = dict()
url_6800XT = 'https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&rpp=96&N=4294966937+4294820651+4294808485&myStore=true&storeid=025'
url_6900XT = 'https://www.microcenter.com/search/search_results.aspx?N=4294966937+4294808442&NTK=all&sortby=pricelow&storeid=025'

class GPU:
    def __init__(self, brand, price, price_info, name, stock, link):
        self.brand = brand
        self.prices = [price]
        self.prices_info = [price_info]
        self.timestamp = [datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")]
        self.name = name
        self.stock = [stock]
        self.link = link

    def update(self, price, price_info, stock):
        self.prices.append(price)
        self.prices_info.append(price_info)
        self.stock.append(stock)
        self.timestamp.append(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

    def get_current_price(self):
        return self.prices[-1]

    def get_current_stock(self):
        return self.stock[-1]

    def get_current_price_info(self):
        return self.prices_info[-1]

    def get_log_html(self):
        p = "<p>"
        for i in range(len(self.prices)):
            p += self.timestamp[-i-1] + " :: $" + self.prices[-i-1] + " Stock: " + self.stock[-i-1] + "</br>"
        p += "</p>"
        return p

    def get_link(self):
        return self.link


def get_microcenter_data(url, data):
    """
        Get's data related to a searched item from microcenter.com in Westmont, IL
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    product_grid = soup.find(id="productGrid")
    items = product_grid.find_all("div", class_="details")

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
        if data.get(sku) is None:  # Item does not exist in dictionary yet. Add it
            data[sku] = GPU(brand, price, price_info, name, stock, link)
        else:
            # Update price and stock qty
            gpu = data[sku]
            gpu.update(price, price_info, stock)
            data[sku] = gpu


def sort_skus_by_price(data):
    sku_ordered = []
    for d in data.keys():
        price = data[d].get_current_price()
        sku_ordered.append([d, float(price.replace(',', ""))])

    # Order the sku list by price
    sku_ordered.sort(key=lambda sku_ordered: sku_ordered[1])

    # Flatten sku ordered list and then return list of skus ordered by price
    flat_sku_ordered = sum(sku_ordered, [])
    return flat_sku_ordered[0:len(flat_sku_ordered):2]


def display_gpu_data(data):
    p = "<p>" + datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S") + "</p>"
    skus = sort_skus_by_price(data)
    for key in skus:
        gpu = data[key]
        p += "<p>" + "Price: <a href=\"" + gpu.get_link() + "\">$" + gpu.get_current_price() + "</a></br>"
        p += "Price Info: " + gpu.get_current_price_info() + "</br>"
        p += "Stock: " + gpu.get_current_stock() + "</br>"
        p += "Brand: " + gpu.brand + "</br>"
        p += "Name: " + gpu.name + "</br>"
        p += "<p>=====================================</p>"
    return p


if __name__ == '__main__':
    app = Flask(__name__)

    @app.route("/6800XT")
    def display6800XT():
        get_microcenter_data(url_6800XT, data_6800XT)
        return display_gpu_data(data_6800XT)

    @app.route("/6900XT")
    def display6900XT():
        get_microcenter_data(url_6900XT, data_6900XT)
        return display_gpu_data(data_6900XT)

    # @app.route("/cheapest")
    # def display_cheapest():
    #     get_microcenter_data()
    #     cheapest_price = None
    #     cheapest_sku = 0
    #     for key in mc_data:
    #         gpu = mc_data[key]
    #         gpu_price = float(gpu.get_current_price().replace(',', ''))
    #         if cheapest_price is None or (gpu_price < cheapest_price):
    #             cheapest_price = gpu_price
    #             cheapest_sku = key

        cheapest_gpu = mc_data[cheapest_sku]
        p = "<p><a href=\"" + cheapest_gpu.get_link() + "\">Cheapest GPU</a>" + " log:</p>"
        p += cheapest_gpu.get_log_html()
        return p


    app.run(host='0.0.0.0', port=5000, debug=True)
