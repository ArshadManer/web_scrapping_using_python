import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.common.action_chains import ActionChains

class ExtractData(object):
    def __init__(self):
        url = 'https://www.iplt20.com/stats/2022'
        self.driver = webdriver.Chrome()
        #self.driver.maximize_window()
        self.driver.get(url)
        cooke = self.driver.find_element(by=By.CLASS_NAME, value='cookie__accept')
        cooke.click()
        self.soup = None
        self.fliter_value = '/html/body/div[2]/div/div/form/div[2]/div[3]/ul/li'
        self.year = 2022

    def update_page_data(self):
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

    def click_fliter(self):
        fliter = self.driver.find_element(by=By.CLASS_NAME, value='np-battingtable__filter')
        time.sleep(2)
        try:
            # self.driver.execute_script("arguments[0].click();", fliter)
            fliter.click()
        except Exception as e:
            print(e)

    def click_year(self, value):
        value = self.driver.find_element(by=By.XPATH, value=value)
        value.click()

    def click_view(self):
        view = self.driver.find_element(by=By.LINK_TEXT, value='View All')
        while not view.is_displayed():
            ActionChains(self.driver) \
                .scroll_by_amount(0, 5) \
                .perform()
            time.sleep(1)

        time.sleep(1)
        try:
            self.driver.execute_script("arguments[0].click();", view)
        except Exception as e:
            pass

    def exit_driver(self):
        self.driver.quit()

    def batting(self, path, year):
        batting = self.driver.find_element(by=By.LINK_TEXT, value='Batting')
        batting.click()
        self.click_view()
        self.update_page_data()
        table = self.soup.find('table', class_='np-mostruns_table')
        title = table.find_all('th')
        header = []
        for i in title:
            name = i.text
            header.append(name)
        df = pd.DataFrame(columns=header)

        row = table.find_all('tr')
        for i in row[1:]:
            data = i.find_all('td')
            row = [tr.text for tr in data]
            l = len(df)
            df.loc[l] = row
        try:
            df.to_csv(os.path.join(path, f'batting_{self.year}.csv'), index=False)
            print(f'Successfully fetched data for year: {year}')
        except Exception as e:
            print(f'data already exist for year: {year}')
            

    def bowling(self, path, year):
        bowl = self.driver.find_element(by=By.LINK_TEXT, value='Bowling')
        bowl.click()
        self.click_view()
        self.update_page_data()
        table = self.soup.find('table', class_='np-mostruns_table')
        title = table.find_all('th')
        header = []
        for i in title:
            name = i.text
            header.append(name)
        df = pd.DataFrame(columns=header)

        row = table.find_all('tr')
        for i in row[1:]:
            data = i.find_all('td')
            row = [tr.text for tr in data]
            l = len(df)
            df.loc[l] = row

        try:
            df.to_csv(os.path.join(path, f'bowling_{self.year}.csv'), index=False)
            print(f'Successfully fetched data for year: {year}')
        except :
            print('data already exist')

    def run(self):
        for i in range(1, 16):
            path = f'data/{self.year}'
            if not os.path.exists(path):
                os.makedirs(path)

            
            self.click_fliter()
            time.sleep(2)
            self.click_year(self.fliter_value + f"[{i}]")
            time.sleep(2)
            self.batting(path, self.year)
            self.bowling(path, self.year)
            self.year -= 1


extract = ExtractData()
extract.run()