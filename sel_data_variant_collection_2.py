from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import xlsxwriter
import lxml.html.clean
import re
import time
import pandas as pd
import numpy as np


# available cars list
cars_lst = ['aston-martin', 'audi', 'bentley', 'bmw', 'citroen', 'datsun', 'dc', 'ferrari', 'fiat', 'force', 'ford',
             'honda', 'hyundai', 'isuzu', 'jaguar', 'jeep', 'kia', 'lamborghini', 'land-rover',
            'lexus', 'mahindra', 'mahindra-electric', 'maruti-suzuki', 'maserati', 'mercedes-benz', 'mg', 'mini',
            'mitsubishi', 'nissan', 'porsche', 'renault', 'rolls-royce', 'skoda', 'tata', 'toyota', 'volkswagen',
            'volvo']

# locate chromedriver and webaddress
web = webdriver.Chrome(executable_path='D:/Python code/chromedriver.exe')
web.get('https://www.autocarindia.com/car-price')

# find make
model_list = []                                               # empty lists for storing data of models and variants
var_list = []

# connect to webadress using selenium and start retriving data
for car_name in range(1, (len(cars_lst)+1)):
    find_var = Select(web.find_element_by_xpath('//*[@id="DrpMake1"]'))
    find_var.select_by_index(car_name)

    # sleep time of 5 seconds
    time.sleep(5)

    # search for car model for the html,  collect all the available models
    find_model = web.find_elements_by_id('DrpModel1')

    # parse the html with beautifulsoup to get only text
    clear_data_lst = []
    clean_text = BeautifulSoup(find_model[0].get_attribute('innerHTML'), 'lxml')
    clean_text_1 = clean_text.find_all('option')
    for model in clean_text_1:
        clear_data_lst.append(model.text)
    print(clear_data_lst)

    # desired length of the next loop
    desired_length = len(clear_data_lst[1:])
    print(desired_length)
    model_list.append(clear_data_lst[1:])

    for var_names in range(desired_length):
        # select model
        select_model = Select(web.find_element_by_xpath('//*[@id="DrpModel1"]'))
        select_model.select_by_index(var_names + 1)

        # add time to sleep
        time.sleep(2)

        # find variant
        find_variant = web.find_elements_by_id('DrpVariants')

        # parse the variant html
        clear_variant_lst = []
        clean_variant = BeautifulSoup(find_variant[0].get_attribute('innerHTML'), 'lxml')
        new_clean_variant = clean_variant.find_all('option')
        for variant in new_clean_variant:
            clear_variant_lst.append(variant.text)
        print(clear_variant_lst)

        var_list.append(clear_variant_lst[1:])

# Create an excel file
excel_sheet = xlsxwriter.Workbook('all_cars_data2.xlsx')

# Create a sheet within the excel
worksheet_1 = excel_sheet.add_worksheet("Sheet1")

# write data in the excel sheet
col_name_1 = 'A'
col_name_2 = 'B'
col_name_3 = 'C'
count_1 = 1
count_2 = 1
count_3 = 1
count_4 = 1
count_5 = 1
count_6 = 1

# create new model list
new_model_list = []
for m in model_list:
    for n in m:
        new_model_list.append(n)

# write models and variants to excel sheet
for x, y in enumerate(new_model_list):
    worksheet_1.write(col_name_1 + str(count_1), y)
    for g in var_list[x]:
        worksheet_1.write(col_name_2 + str(count_1), g)
        count_1 += 1
excel_sheet.close()




