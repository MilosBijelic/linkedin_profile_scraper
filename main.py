import pdb
import re
import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class LinkedinScraper():
    def __init__(self):
        # Creating a webdriver instance
        self.driver = webdriver.Chrome("C:/Users/milos.bijelic/Downloads/chromedriver_win32/chromedriver.exe")
        # This instance will be used to log into LinkedIn
        self.email = input('What is your email?\n')
        self.password = input('What is your password?\n')

    def _create_csv(self):
        # Creates .csv file to write to
        headers = ['Name', 'Job Title', 'Company']
        with open('spire-member-info.csv', 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    def create_member_list(self):
        # If the .csv exists delete the old copy
        if os.path.exists("spire-member-list.csv"):
            os.remove("spire-member-list.csv")
            self._create_csv()
        else:
            self._create_csv()

    def start_chrome(self):
        # Opening linkedIn's login page
        self.driver.get("https://linkedin.com/uas/login")

        # waiting for the page to load
        time.sleep(2)

        # Find the Username box on the webpage
        username = self.driver.find_element(By.ID, "username")

        username.send_keys(self.email)

        # Find the Password box on the webpage
        pword = self.driver.find_element(By.ID, "password")
        # In case of an error, try changing the element
        # tag used here.

        pword.send_keys(self.password)

        # Clicking on the login button
        self.driver.find_element(By.CLASS_NAME, "login__form_action_container").click()

        # Wait 15 seconds in case of security test
        time.sleep(15)

    def scrape_linkedin(self, url_list):
        # Loops through all entries in the spire_linkedin_urls list
        for url in url_list:
            # Opens up the URL
            self.driver.get(url)

            time.sleep(5)
            # Stores the source code of the webpage
            src = self.driver.page_source
            soup = BeautifulSoup(src, 'lxml')

            # Get their headline
            intro = soup.find('div', {'class': 'pv-text-details__left-panel'})

            name_loc = intro.find("h1")

            # Extract the Name
            name = name_loc.get_text().strip()

            works_at_loc = intro.find("div", {'class': 'text-body-medium'})

            # Extracting the persons header
            works_at = works_at_loc.get_text().strip()

            # Empty to store data
            data_row = []

            # Extract the title and company from their headline
            title = re.search("^(.+?),(.*)", works_at)
            company = re.search("(.*) at (.*)", works_at)

            # push the name, title and company to the list
            data_row.append(name)

            if title is None:
                data_row.append(title)
            else:
                data_row.append(title.group(1))

            if company is None:
                data_row.append(company)
            else:
                data_row.append(company.group(2))

            # write the users info to the .csv
            with open('spire-member-info.csv', 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data_row)


if __name__ == "__main__":
    # Get list of URLs from .csv
    with open('spire_urls.csv',  encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        url_list = list(reader)
        url_list = [item for sublist in url_list for item in sublist]

    scraper = LinkedinScraper()

    scraper.create_member_list()
    scraper.start_chrome()
    scraper.scrape_linkedin(url_list)