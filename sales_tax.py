import sys
import constants
from decimal import *
from utilities import round_nearest_005, read_input_file, parse_input

class Taxes():
    def __init__(self, sales_tax, import_duty):
        self.sales_tax = sales_tax
        self.import_duty = import_duty

class PurchaseItem():
    def __init__(self, name, category, qty, price, isImported):
        self.name = name
        self.category = category
        self.qty = qty
        self.price = price
        self.isImported = isImported
        self.tax_on_item = 0
        self.total_price_per_item = 0

    def calculate_tax(self, sales_tax_percentage, import_duty_percentage):
        '''
        calculates the sales tax and total price of the item after adding tax
        '''
        try:
            if self.category in constants.TAX_EXEMPT_CATEGORIES:
                tax = 0
            else:
                tax = sales_tax_percentage
            if self.isImported:
                tax += import_duty_percentage
            self.tax_on_item = round_nearest_005((Decimal(tax) * self.price)/100)
            self.total_price_per_item = self.price + self.tax_on_item
        except Exception as e:
            print('Unexpected Error: ', e)

class Bill():
    def __init__(self, items):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def get_total_sales_tax(self):
        sales_taxes = [item.tax_on_item for item in self.items]
        return sum(sales_taxes)

    def get_total_cost(self):
        total_cost = [item.total_price_per_item for item in self.items]
        return sum(total_cost)

    def generate_bill(self):
        '''
        prints out the final bill
        '''
        try:
            sales_tax = self.get_total_sales_tax()
            total = self.get_total_cost()
            string_output = ''

            if sales_tax is not None and total is not None:
                for item in self.items:
                    string_output += str(item.qty) + ' ' +item.name + ': ' + \
                                     str(item.total_price_per_item) + '\n'
                string_output += "Sales Taxes: " + str(sales_tax) + '\n'
                string_output += "Total: " + str(total)

            return string_output
        except Exception as e:
            print('Unexpected Error: ', e)

if __name__ == '__main__':

    args = sys.argv

    if len(args) == 2: # command line args must be 2
        # read the input file
        inputText = read_input_file(args[1])

        # parse input text and store in an array
        serialized_input = parse_input(inputText)

        # initialize tax policy (10% sales tax, 5% import duty)
        tax = Taxes(sales_tax=constants.SALES_TAX, import_duty=constants.IMPORT_DUTY)
        bill = Bill(items=None)
        for item in serialized_input:
            p = PurchaseItem(item['name'], item['category'], item['qty'],
                             item['price'], item['isImported'])
            p.calculate_tax(tax.sales_tax, tax.import_duty)
            # add every purchase item to a bill
            bill.add(p)
        final_bill = bill.generate_bill()
        print(final_bill)
    else:
        print('Provide the input file as a command line argument: '
              'Eg: python sales_tax.py input1.txt')



