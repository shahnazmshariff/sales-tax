import json
import re
from decimal import *

def read_input_file(filename):
    '''
    :param filename: input file containing the purchase items
    :return: an array of lines in the given input text
    '''
    inputText = []
    try:
        with open('input_files/'+filename, 'r') as input_file:
            for line in input_file:
                if len(line.strip()) > 1:
                    inputText.append(line.strip())
        return inputText
    except IOError:
        print("Error: Can't find the file or read data")

def parse_input(inputText):
    '''
    :param inputText: array of lines in the given input file
    :return: an array of objects containing name, qty, price, isImported (boolean)
    and category
    '''
    parsed_input = []
    try:
        for item in inputText:
            data = {}
            regex_eval = re.search(r"(^\d+)\s((\w+\s)+)at\s(\d*[.,]?\d*)$", item)
            qty = int(regex_eval.group(1))
            if qty > 0:
                data['qty'] = qty
                data['name'] = regex_eval.group(2)
                data['price'] = Decimal(regex_eval.group(4))
                data['isImported'] = 'imported' in data['name']
                data['category'] = get_category(data['name'])
                parsed_input.append(data)
            else:
                print('Invalid input: Qty must be greater than 0')
                raise Exception
        return parsed_input
    except Exception as e:
        print('Unexpected Error: ', e)

def get_category(name):
    '''
    :param name: name of the product
    :return: tax exempt category (food/medical/books)
    '''
    try:
        with open('categories.json', 'r') as categories_json:
            categories = json.load(categories_json)
            for category, products in categories.items():
                for product in products:
                    if product in name:
                        return category
    except Exception as e:
        print('Unexpected Error: ', e)

def round_nearest_005(value):
    return ((value*2).quantize(Decimal('.1'), rounding=ROUND_UP))/2
