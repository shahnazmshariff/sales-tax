import unittest
from sales_tax import *

EXPECTED_INPUT = ['1 imported bottle of perfume at 27.99',
                           '1 bottle of perfume at 18.99',
                           '1 packet of headache pills at 9.75',
                           '1 box of imported chocolates at 11.25']

EXPECTED_PARSED_INPUT = [{'category': None,
                            'price': Decimal('27.99'),
                            'name': 'imported bottle of perfume ',
                            'isImported': True,
                            'qty': 1},
                           {'category': None,
                            'price': Decimal('18.99'),
                            'name': 'bottle of perfume ',
                            'isImported': False,
                            'qty': 1},
                           {'category': u'medical_products',
                            'price': Decimal('9.75'),
                            'name': 'packet of headache pills ',
                            'isImported': False,
                            'qty': 1},
                           {'category': u'food',
                            'price': Decimal('11.25'),
                            'name': 'box of imported chocolates ',
                            'isImported': True,
                            'qty': 1}]


class TestSalesTax(unittest.TestCase):

    def test_read_input(self):
        '''
        tests if the input file can be read or not
        '''
        #file 1 - exists
        actual_input_1 = read_input_file('input3.txt')
        self.assertEqual(actual_input_1, EXPECTED_INPUT)

        # file 2 - does not exist
        actual_input_2 = read_input_file('file.txt')
        self.assertRaises(IOError)
        self.assertNotEqual(actual_input_2, EXPECTED_INPUT)

    def test_parse_input(self):
        '''
        tests if the input text follows the correct format or not
        '''
        # file 1 (correct input)
        actual_parsed_obj = parse_input(EXPECTED_INPUT)
        self.assertEqual(actual_parsed_obj, EXPECTED_PARSED_INPUT)

        # file 2 (incorrect input)
        # 1 imported box of chocolates at $10
        wrong_input_1 = read_input_file('wrongInput1.txt')
        wrong_parsed_obj_1 = parse_input(wrong_input_1)
        self.assertRaises(Exception)

        # file 3 (incorrect input)
        # 1 box of chocolates for 10
        wrong_input_2 = read_input_file('wrongInput2.txt')
        wrong_parsed_obj_2 = parse_input(wrong_input_2)
        self.assertRaises(Exception)

        # file 4 (incorrect input)
        # empty file
        empty = read_input_file('empty.txt')
        wrong_parsed_obj_2 = parse_input(empty)
        self.assertRaises(Exception)

        # When qty is 0
        input = [{'category': None,
          'price': Decimal('0'),
          'name': 'bottle of perfume ',
          'isImported': True,
          'qty': 0}]
        parse_input(input)
        self.assertRaises(Exception)

        # When qty is a decimal
        input[0]['qty'] = 1.5
        parse_input(input)
        self.assertRaises(Exception)

        # When qty is negative
        input[0]['qty'] = -1
        parse_input(input)
        self.assertRaises(Exception)

    def test_round_nearest_005(self):
        '''
        tests if a given number rounds off to the nearest 0.05
        '''
        self.assertEqual(round_nearest_005(Decimal('7.125')), Decimal('7.15'))
        self.assertEqual(round_nearest_005(Decimal('7.14')), Decimal('7.15'))
        self.assertEqual(round_nearest_005(Decimal('7.16')), Decimal('7.20'))


    def test_tax_regular_item(self):
        '''
        tests if 10% tax is added on a regular item
        Eg: perfume
        '''

        item = EXPECTED_PARSED_INPUT[1]
        p = PurchaseItem(item['name'], item['category'], item['qty'], item['price'],
                         item['isImported'])
        p.calculate_tax(constants.SALES_TAX, constants.IMPORT_DUTY)

        self.assertEqual(p.tax_on_item, Decimal('1.9'))
        self.assertEqual(p.total_price_per_item, Decimal('20.89'))

    def test_tax_imported_item(self):
        '''
       tests if 15% tax is added on an imported item
       Eg: imported perfume
        '''

        item = EXPECTED_PARSED_INPUT[0]

        p = PurchaseItem(item['name'], item['category'], item['qty'], item['price'],
                         item['isImported'])

        p.calculate_tax(constants.SALES_TAX, constants.IMPORT_DUTY)
        self.assertEqual(p.tax_on_item, Decimal('4.2'))
        self.assertEqual(p.total_price_per_item, Decimal('32.19'))


    def test_tax_exempt_item(self):
        '''
           tests if no tax (0%) is added on a tax exempt item
           Eg: headache pills (medical product)
        '''

        item = EXPECTED_PARSED_INPUT[2]
        p = PurchaseItem(item['name'], item['category'], item['qty'], item['price'],
                         item['isImported'])
        p.calculate_tax(constants.SALES_TAX, constants.IMPORT_DUTY)

        self.assertEqual(p.tax_on_item, Decimal('0.0'))
        self.assertEqual(p.price, p.total_price_per_item)

    def test_imported_exempt_item(self):
        '''
        tests that only import duty (5%) is added to a tax exempt item
        Eg: imported chocolate (food)
        '''

        item = EXPECTED_PARSED_INPUT[3]
        p = PurchaseItem(item['name'], item['category'], item['qty'], item['price'],
                         item['isImported'])
        p.calculate_tax(constants.SALES_TAX, constants.IMPORT_DUTY)

        self.assertEqual(p.tax_on_item, Decimal('0.6'))
        self.assertEqual(p.total_price_per_item, Decimal('11.85'))

    def test_different_tax_rates(self):
        '''
        tests if the tax is calculated correctly even when
        the tax policy (sales tax, import duty) changes
        '''

        item = EXPECTED_PARSED_INPUT[0]
        p = PurchaseItem(item['name'], item['category'], item['qty'], item['price'],
                         item['isImported'])
        p.calculate_tax(20, 5)
        self.assertEqual(p.total_price_per_item, Decimal('34.99'))
        p.calculate_tax(10, 10)
        self.assertEqual(p.total_price_per_item, Decimal('33.59'))
        p.calculate_tax(20.5, 10.99)
        self.assertEqual(p.total_price_per_item, Decimal('36.84'))

    def test_different_qty(self):
        '''
        tests if the tax is calculated correctly even when the QUANTITY changes
        '''

        input = '10 imported bottles of perfume at 279.90'
        p = PurchaseItem('imported bottles of perfume', None, 10, Decimal('279.90'), True)
        p.calculate_tax(constants.SALES_TAX, constants.IMPORT_DUTY)
        self.assertEqual(p.total_price_per_item, Decimal('321.90'))


    def test_generate_bill(self):
        '''
        tests if the bill is generated properly
        after all the items are added to the bill
        '''
        expected_bill = "1 imported bottle of perfume : 32.19\n1 bottle of perfume : " \
                        "20.89\n1 packet of headache pills : 9.75\n1 box of imported " \
                        "chocolates : 11.85\nSales Taxes: 6.7\nTotal: 74.68"

        bill = Bill(items=None)
        for item in EXPECTED_PARSED_INPUT:
            p = PurchaseItem(item['name'], item['category'], item['qty'], item['price'],
                             item['isImported'])
            p.calculate_tax(constants.SALES_TAX, constants.IMPORT_DUTY)
            bill.add(p)

        actual_bill = bill.generate_bill()
        self.assertEqual(actual_bill, expected_bill)

if __name__ == '__main__':
    unittest.main()
