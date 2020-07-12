# Sales Tax Problem

Basic sales tax is applicable at a rate of 10% on all goods, except books, food, and medical products that are exempt. Import duty is an additional sales tax applicable on all imported goods at a rate of 5%, with no exemptions.

 

When I purchase items I receive a receipt which lists the name of all the items and their price (including tax), finishing with the total cost of the items, and the total amounts of sales taxes paid.  The rounding rules for sales tax are that for a tax rate of n%, a shelf price of p contains (np/100 rounded up to the nearest 0.05) amount of sales tax.

 

Write an application that prints out the receipt details for these shopping baskets...

INPUT:

 

Input 1:

1 book at 12.49

1 music CD at 14.99

1 chocolate bar at 0.85

 

Input 2:

1 imported box of chocolates at 10.00

1 imported bottle of perfume at 47.50

 

Input 3:

1 imported bottle of perfume at 27.99

1 bottle of perfume at 18.99

1 packet of headache pills at 9.75

1 box of imported chocolates at 11.25

 

OUTPUT

 

Output 1:

1 book : 12.49

1 music CD: 16.49

1 chocolate bar: 0.85

Sales Taxes: 1.50

Total: 29.83

 

Output 2:

1 imported box of chocolates: 10.50

1 imported bottle of perfume: 54.65

Sales Taxes: 7.65

Total: 65.15

 

Output 3:

1 imported bottle of perfume: 32.19

1 bottle of perfume: 20.89

1 packet of headache pills: 9.75

1 imported box of chocolates: 11.85

Sales Taxes: 6.70

Total: 74.68

==========

## Usage (with Docker):

Run the commands from the root folder. Make sure any additional
input files are in the input_files folder.

```
docker build -t sales_tax .
```

```
docker run sales_tax
```

## Usage (without Docker):

Requirements: Python 3.5

```
python sales_tax.py input1.txt
```

```
python sales_tax.py input2.txt
```

```
python sales_tax.py input3.txt
```

### Run unit tests:
```
python test_sales_tax.py -b
```

## Design:
1. Implemented OOPs concepts to create classes for a purchase item, bill and tax policy
2. Program gets the input file as a command-line argument and contains adequate exception handling
3. Used a Regex pattern to match the input string. Although regex is slightly slower, it
does handle a variety of input string formats which is required for this use case
4. Designed with the assumption that the tax policies (rates) can change in the future

## Assumptions:
1. The category of a product is obtained from the name of the product in the input text.
New products need to be added to the categories.json file if they belong to the tax exempt
categories.
Note: the products from the 3 given input files have already been added to categories.json
file
2. Input string follows a standard format - (quantity)(name)at(price)
3. Price given in the input string is the total price of the item. For example, 10 books at 50.
Here, 50 is the total price and not the price per book
