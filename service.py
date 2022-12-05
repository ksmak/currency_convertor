from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


from config import JUSANBANK_URL, EXCHANGE_RATE_TYPES

def format_float(string_value: str) -> float:
    """Function for get float from string"""
    if string_value == '':
        return 0
    digits = "0123456789"
    dot = ["."]
    num_list = []
    for s in string_value:
        if s in digits:
            num_list.append(s)
        if s in dot:
            dot.pop()
            num_list.append(s)

    return float(''.join(num_list))
    

def load_for_individual(driver: webdriver, currency_list: list) -> None:
    """Load echange rate for individual"""
    elements = driver.find_elements(By.CLASS_NAME, "exchange-cardbody")
    for element in elements:
        sub_elements = element.find_elements(By.CLASS_NAME, "currency-main-text")
        it = iter(sub_elements)
        for _ in range(3):
            data = {}
            el = next(it)
            data["convert_type"] = EXCHANGE_RATE_TYPES[0]
            data["name"] = el.text
            el = next(it)
            data["sale"] = format_float(el.text)
            el = next(it)
            data["buy"] = format_float(el.text)
            currency_list.append(data)    

def load_other(driver: webdriver, currency_list: list) -> None:
    """Load exchange rate for other"""
    exchange_rate_index = 1
    elements = driver.find_elements(By.CLASS_NAME, "exchange-tablebody")
    for element in elements:
        sub_elements = element.text.split('\n')
        step = 1
        data = {}
        for el in sub_elements:
            if step == 1:
                data = {}
                data["convert_type"] = EXCHANGE_RATE_TYPES[exchange_rate_index]
                step += 1
            elif step == 2:
                step += 1    
            elif step == 3:
                data["name"] = el.split('/')[0]
                step += 1
            elif step == 4:
                step += 1
            elif step == 5:    
                data['sale'] = format_float(el)
                step += 1
            elif step == 6:
                data['buy'] = format_float(el)
                currency_list.append(data)
                step = 3
                data = {}
                data["convert_type"] = EXCHANGE_RATE_TYPES[exchange_rate_index]

        exchange_rate_index += 1   
        
        if exchange_rate_index >= len(EXCHANGE_RATE_TYPES):
            break
    
def load_all_currency() -> list:
    """Load all data from url"""
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
    driver.get(JUSANBANK_URL)
    
    currency_list = []
    
    load_for_individual(driver, currency_list)
    load_other(driver, currency_list)
    
    return currency_list

def get_currency(currency_list: list, convert_type: str, convert_name: str) -> dict:
    """Get currency from currency list"""
    for currency in currency_list:
        if currency["convert_type"] == convert_type and currency["name"] == convert_name:
            return currency