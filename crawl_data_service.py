from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

class CrawlDataService:

    @staticmethod
    def crawl_data_from_target_lazada_page():
        DICT_KEYS = ['product_name', 'sale_price', 'original_price', 'sale_percentage', 'sold_number', 'review_number', 'vendor_location']
        result = []
        urlpage = 'https://www.lazada.vn/locklock-flagship-store/?q=All-Products&from=wangpu&langFlag=vi&pageTypeId=2'
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome()
        driver.get(urlpage)
        for i in range(24):
            time.sleep(10)
            print(f'===================CRAWLING DATA PAGE {i+1} BEGIN================')
            products_raw_data = driver.find_elements(By.XPATH, "//*[@class='qmXQo']//*[@class='buTCk']")
            print(f'===================CRAWLING DATA PAGE {i+1} FINISH================')

            for product in products_raw_data:
                product_split = product.text.split('\n')

                if len(product_split) == 7:
                    product_dict = {DICT_KEYS[index]: product_split[index] for index in range(len(product_split))}
                    result.append(product_dict)
                else:
                    product_dict = {DICT_KEYS[index]: product_split[index] for index in range(4)}
                    for index in range(-1 ,-4, -1):
                        product_dict[DICT_KEYS[index]] = product_split[index]
                    result.append(product_dict)

            next_button = driver.find_element(By.XPATH, '//li[@class="ant-pagination-next"]//button[@class="ant-pagination-item-link"]')
            next_button.click()
            driver.refresh()

        driver.quit()

        return result