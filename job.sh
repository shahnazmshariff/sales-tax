#!/bin/sh
echo "Output1: "
python sales_tax.py input1.txt
echo "-------"
echo "Output2: "
python sales_tax.py input2.txt
echo "-------"
echo "Output3: "
python sales_tax.py input3.txt
echo "-------"
echo "Running tests..."
python test_sales_tax.py -b
