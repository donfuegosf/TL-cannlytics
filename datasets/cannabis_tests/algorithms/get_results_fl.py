"""
Florida cannabis lab results
Copyright (c) 2023 Cannlytics

Authors:
    Keegan Skeate <https://github.com/keeganskeate>
    Candace O'Sullivan-Sutherland <https://github.com/candy-o>
Created: 5/18/2023
Updated: 12/31/2023
License: <https://github.com/cannlytics/cannlytics/blob/main/LICENSE>

Description:

    Archive Florida cannabis lab result data.

Data Sources:

    - [Florida Labs](https://knowthefactsmmj.com/cmtl/)
    - [Florida Licenses](https://knowthefactsmmj.com/mmtc/)
    - [Kaycha Labs](https://yourcoa.com)
    - [The Flowery](https://support.theflowery.co)
    - [TerpLife Labs](https://www.terplifelabs.com)

Resources:

    - https://www.reddit.com/r/FLMedicalTrees/search/?q=COA
    - https://www.reddit.com/r/FLMedicalTrees/comments/11hfwjl/question_on_dispensaries_and_coas/
    - https://www.reddit.com/r/FLMedicalTrees/comments/1272per/anyone_have_batch_s_they_can_share_for_our/
    - https://www.reddit.com/r/FLMedicalTrees/comments/vdnpqf/coa_accumulation/
    - https://www.reddit.com/r/FLMedicalTrees/comments/13jizze/vidacann_finally_put_all_coas_up/
    - https://www.reddit.com/r/FLMedicalTrees/comments/13j1tua/rick_james_coa/
    - https://www.reddit.com/r/FLMedicalTrees/comments/13d7bwb/can_someone_explain_some_terps_to_me/
    - https://www.reddit.com/r/FLMedicalTrees/comments/11v4pa5/holy_farnesene_batman/

"""
# Standard imports:
from datetime import datetime
import os
import random
import tempfile
from time import sleep
from typing import Optional

# External imports:
from bs4 import BeautifulSoup
from cannlytics.data.coas.coas import CoADoc
from cannlytics.data.web import initialize_selenium
from cannlytics.utils.constants import DEFAULT_HEADERS
import pandas as pd
import requests

# Selenium imports.
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


#-----------------------------------------------------------------------
# Parse Kaycha Labs COAs.
#-----------------------------------------------------------------------

# Get a list of Florida companies.
# Note: It may be best to retrieve this list dynamically.
# TODO: Keep track of the last page of results for each company.
# TODO: Try to find COAs for the remaining companies.
# - Plant 13 Florida, Inc.
# - House of Platinum Cannabis
# - Cookies Florida, Inc.
FLORIDA_LICENSES = {
    'MMTC-2015-0002': {
        'business_dba_name': 'Ayr Cannabis Dispensary',
        'business_legal_name': 'Liberty Health Sciences, FL',
        'slug': 'Liberty+Health+Sciences%2C+FL',
        'total': 3924,
    },
    'MMTC-2017-0011': {
        'business_dba_name': 'Cannabist',
        'slug': 'Cannabist',
        'total': 3,
    },
    'MMTC-2019-0018': {
        'business_dba_name': 'Cookies Florida, Inc.',
        'slug': '',
        'total': 0,
    },
    'MMTC-2015-0001': {
        'business_dba_name': 'Curaleaf',
        'slug': 'CURALEAF+FLORIDA+LLC',
        'total': 8905,
    },
    'MMTC-2015-0003': {
        'business_dba_name': 'Fluent ',
        'slug': 'Fluent',
        'total': 70,
    },
    'MMTC-2019-0019': {
        'business_dba_name': 'Gold Leaf',
        'slug': 'Gold+Leaf',
        'total': 6,
    },
    'MMTC-2019-0021': {
        'business_dba_name': 'Green Dragon',
        'slug': 'Green+Dragon',
        'total': 0,
    },
    'MMTC-2016-0007': {
        'business_dba_name': 'GrowHealthy',
        'slug': 'GrowHealthy',
        'total': 28,
    },
    'MMTC-2017-0013': {
        'business_dba_name': 'GTI (Rise Dispensaries)',
        'slug': 'GTI',
        'total': 0,
    },
    'MMTC-2018-0014': {
        'business_dba_name': 'House of Platinum Cannabis',
        'slug': '',
        'total': 0,
    },
    'MMTC-2019-0016': {
        'business_dba_name': 'Insa - Cannabis for Real Life',
        'slug': 'Insa',
        'total': 9,
    },
    'MMTC-2019-0015': {
        'business_dba_name': 'Jungle Boys',
        'slug': 'Jungle+Boys',
        'total': 2,
    },
    'MMTC-2017-0010': {
        'business_dba_name': 'MüV',
        'slug': 'Altmed+Florida',
        'total': 1633,
    },
    'MMTC-2016-0006': {
        'business_dba_name': 'Planet 13 Florida, Inc.',
        'slug': '',
        'total': 0,
    },
    'MMTC-2019-0022': {
        'business_dba_name': 'Revolution Florida',
        'slug': 'Revolution',
        'total': 0,
    },
    'MMTC-2019-0017': {
        'business_dba_name': 'Sanctuary Cannabis',
        'slug': 'Sanctuary',
        'total': 581,
    },
    'MMTC-2017-0012': {
        'business_dba_name': 'Sunburn',
        'slug': '',
        'total': 0,
    },
    'MMTC-2017-0008': {
        'business_dba_name': 'Sunnyside*',
        'slug': 'Sunnyside',
        'total': 886,
    },
    'MMTC-2015-0004': {
        'business_dba_name': 'Surterra Wellness',
        'slug': 'Surterra+Wellness',
        'total': 1,
    },
    'MMTC-2019-0020': {
        'business_dba_name': 'The Flowery',
        'slug': 'The+Flowery',
        'total': 0,
    },
    'MMTC-2015-0005': {
        'business_dba_name': 'Trulieve',
        'slug': 'Trulieve',
        'total': 0,
    },
    'MMTC-2017-0009': {
        'business_dba_name': 'VidaCann',
        'slug': 'VidaCann',
        'total': 4,
    },
}


def download_coas_kaycha(
        data_dir: str,
        slug: str,
        dba: Optional[str] = None,
        producer_license_number: Optional[str] = None,
        overwrite: Optional[bool] = False,
        base: Optional[str] = 'https://yourcoa.com',
        columns: Optional[list] = None,
    ):
    """Download Kaycha Labs COAs uploaded to the public web."""

    # Initialize COA URL collection.
    if columns is None:
        columns = ['lab_id', 'batch_number', 'product_name']

    # Create an output directory.
    datasets_dir = os.path.join(data_dir, '.datasets')
    if not os.path.exists(datasets_dir):
        os.makedirs(datasets_dir)

    # Request each page until the maximum is reached.
    page = 0
    observations = []
    iterate = True
    while iterate:

        # Get the first/next page of COAs.
        page += 1
        url = f'{base}/company/company?t={slug}&page={page}'
        response = requests.get(url, headers=DEFAULT_HEADERS)
        if response.status_code != 200:
            print(f"Request failed with status {response.status_code}")

        # Get the download URLs.
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        links = [x['href'] for x in links if 'coa-download' in x['href']]
        links = list(set(links))
        links = [base + x for x in links]

        # Get the details from the page.
        divs = soup.find_all(class_='pdf_box')
        print('Found %i samples on page %i.' % (len(divs), page))
        for n, div in enumerate(divs):
            observation = {}
            spans = div.find_all('span')[:len(columns)]
            values = [x.text for x in spans]
            for k, value in enumerate(values):
                observation[columns[k]] = value
            try:
                observation['download_url'] = links[n]
            except:
                continue
            if dba is not None:
                observation['business_dba_name'] = dba
            if producer_license_number is not None:
                observation['producer_license_number'] = producer_license_number
            observations.append(observation)

        # See if the next button is disabled to know when to stop iterating.
        next_element = soup.find(class_='next')
        if not next_element:
            iterate = False
        elif next_element and 'disabled' in next_element.get('class', []):
            iterate = False

        # Otherwise pause to respect the server.
        sleep(0.3)

    # Save the observed lab result URLs.
    date = datetime.now().isoformat()[:19].replace(':', '-')
    df = pd.DataFrame(observations)
    df.to_excel(f'{datasets_dir}/fl-lab-result-urls-{slug}-{date}.xlsx', index=False)
    print('Saved %i lab result URLs for %s' % (len(df), slug))

    # Create a directory for COA PDFs.
    pdf_dir = os.path.join(datasets_dir, 'pdfs')
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    # Create a directory for each licensees COAs.
    license_pdf_dir = os.path.join(pdf_dir, producer_license_number)
    if not os.path.exists(license_pdf_dir):
        os.makedirs(license_pdf_dir)

    # Download the PDFs.
    for _, row in df.iterrows():
        sleep(0.3)
        sample_id = row['lab_id']
        outfile = os.path.join(license_pdf_dir, f'{sample_id}.pdf')
        if os.path.exists(outfile) and not overwrite:
            continue
        # FIXME: Handle URLs without a base URL.
        download_url = row['download_url']
        if not download_url.startswith('http'):
            download_url = base + download_url
        response = requests.get(download_url, headers=DEFAULT_HEADERS)
        with open(outfile, 'wb') as pdf:
            pdf.write(response.content)
        print('Downloaded: %s' % outfile)

    # Return the COA URLs.
    return df


def get_results_kaycha(data_dir: str, licenses=None, **kwargs):
    """Get lab results published by Kaycha Labs on the public web."""

    # Sort licenses by the number of COAs.
    if licenses is None:
        licenses = FLORIDA_LICENSES
    licenses = dict(sorted(licenses.items(), key=lambda x: x[1]['total']))

    # Iterate over each producer.
    coa_urls = []
    for license_number, licensee in licenses.items():
        # expected_total = licensee['total']
        # if expected_total == 0:
        #     continue
        print('Preparing to download COAs for %s' % licensee['business_dba_name'])
        urls = download_coas_kaycha(
            data_dir,
            slug=licensee['slug'],
            dba=licensee['business_dba_name'],
            producer_license_number=license_number,
        )
        coa_urls.append(urls)

    # Save and return all of the COA URLs.
    date = datetime.now().isoformat()[:19].replace(':', '-')
    data = pd.concat(coa_urls)
    datasets_dir = os.path.join(data_dir, '.datasets')
    data.to_excel(f'{datasets_dir}/fl-lab-result-urls-{date}.xlsx', index=False)
    print('Saved %i lab result URLs for Kaycha Labs.' % len(data))
    return data


def parse_results_kaycha(
        data_dir: str,
        outfile: Optional[str] = None,
        temp_path: Optional[str] = None,
        reverse: Optional[bool] = True,
        completed: Optional[list] = [],
        license_number: Optional[str] = None,
    ):
    """Parse lab results from Kaycha Labs COAs."""
    # Initialize a parser.
    parser = CoADoc()

    # Create the output data directory if it does not exist.
    if outfile:
        output_dir = os.path.dirname(outfile)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    # Get a temporary path for storing images.
    if temp_path is None:
        temp_path = tempfile.gettempdir()

    # Iterate over PDF directory.
    all_data = []
    for path, _, files in os.walk(data_dir):
        if reverse:
            files = reversed(files)

        # Iterate over all files.
        for filename in list(iter(files))[550:1_000]:

            # Skip all files except PDFs.
            if not filename.endswith('.pdf'):
                continue

            # Skip parsed files.
            if filename in completed:
                continue

            # Parse COA PDFs one by one.
            try:
                doc = os.path.join(path, filename)
                data = parser.parse(doc, temp_path=temp_path)
                if license_number is not None:
                    data['license_number'] = license_number
                all_data.extend(data)
                print('Parsed:', doc)
            except:
                print('Error:', doc)

    # Save the data.
    if outfile:
        try:
            parser.save(all_data, outfile)
            print('Saved COA data:', outfile)
        except:
            print('Failed to save COA data.')

    # Return the data.
    return all_data


# === Test ===
if __name__ == '__main__':

    # Specify where your data lives.
    DATA_DIR = 'D://data/florida/lab_results'
    # DATA_DIR = r'C:\.datasets\data\florida\lab_results'

    # [✓] TEST: Get Kaycha COAs.
    kaycha_coas = get_results_kaycha(DATA_DIR)

    # [✓] TEST: Parse Kaycha COAs.
    # Note: This is a super, super long process
    # pdf_dir = 'D://data/florida/lab_results/.datasets/pdfs'
    # date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    # for folder in os.listdir(pdf_dir):
    #     if folder.startswith('MMTC-2015-0002'):
    #         data_dir = os.path.join(pdf_dir, folder)
    #         outfile = os.path.join(DATA_DIR, '.datasets', f'{folder}-lab-results-{date}.xlsx')
    #         print('Parsing:', folder)
    #         coa_data = parse_results_kaycha(
    #             data_dir,
    #             outfile,
    #             reverse=True,
    #             completed=[]
    #         )


#-----------------------------------------------------------------------
# The Flowery (892+ results).
# TODO: Automate to be a daily script.
#-----------------------------------------------------------------------

def get_results_the_flowery(
        data_dir: str,
        slug = 'the-flowery',
        producer_license_number = 'MMTC-2019-0020',
        lists_url = 'https://support.theflowery.co/hc/en-us/sections/7240468576283-Drop-Information',
        overwrite = False,
    ):
    """Get lab results published by The Flowery on the public web."""

    # Initialize the web driver.
    driver = initialize_selenium()

    # Load the lists page to get each list of COAs.
    coa_lists = []
    driver.get(lists_url)
    links = driver.find_elements(by=By.TAG_NAME, value='a')
    for link in links:
        if 'COAs' in link.text:
            coa_lists.append(link.get_attribute('href'))

    # Get COA URLs.
    coa_urls = []
    for coa_list in coa_lists:
        driver = initialize_selenium()
        driver.get(coa_list)
        links = driver.find_elements(by=By.TAG_NAME, value='a')
        for link in links:
            href = link.get_attribute('href')
            if href and href.endswith('.pdf'):
                coa_urls.append(href)
        driver.quit()

    # Close the browser.
    driver.quit()

    # Create an output directory.
    datasets_dir = os.path.join(data_dir, '.datasets')
    if not os.path.exists(datasets_dir):
        os.makedirs(datasets_dir)

    # Save the COA URLs.
    date = datetime.now().isoformat()[:19].replace(':', '-')
    df = pd.DataFrame(coa_urls)
    df.to_excel(f'{datasets_dir}/fl-lab-result-urls-{slug}-{date}.xlsx', index=False)
    print('Saved %i lab result URLs for %s' % (len(df), slug))

    # Create a directory for COA PDFs.
    pdf_dir = os.path.join(datasets_dir, 'pdfs')
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    # Create a directory for each licensees COAs.
    license_pdf_dir = os.path.join(pdf_dir, producer_license_number)
    if not os.path.exists(license_pdf_dir):
        os.makedirs(license_pdf_dir)

    # Download the COA PDFs.
    for coa_url in coa_urls:
        sample_id = coa_url.split('/')[-1].split('.')[0]
        batch_id = coa_url.split('/')[-2]
        outfile = os.path.join(license_pdf_dir, f'{batch_id}-{sample_id}.pdf')
        if os.path.exists(outfile) and not overwrite:
            continue
        sleep(0.3)
        response = requests.get(coa_url, headers=DEFAULT_HEADERS)
        with open(outfile, 'wb') as pdf:
            pdf.write(response.content)
        print('Downloaded: %s' % outfile)

    # TODO: Save details about each COA, including The Flowery company data.

    # Return the COA URLs.
    return df


def get_product_results_the_flowery(data_dir: str, overwrite = False, **kwargs):
    """Get product results from The Flowery website."""
    # Initialize a web driver.
    driver = initialize_selenium()

    # Iterate over all of the product types.
    observations = []
    categories = ['Flower', 'Concentrates', 'Pre-Rolls', 'Vaporizers', 'Tinctures']
    for category in categories:

        # Load the category page.
        url = f'https://theflowery.co/shop?categories[]={category}'
        driver.get(url)
        sleep(3.33)

        # Get all of the product cards.
        divs = driver.find_elements(by=By.CSS_SELECTOR, value='a.s-shop-product-card')
        for div in divs:
            
            # Extract product name.
            product_name = div.find_element(by=By.CLASS_NAME, value='title').text

            # Extract product image URL.
            product_image = div.find_element(by=By.TAG_NAME, value='img').get_attribute('src')

            # Extract product price.
            product_price = float(div.find_element(by=By.CLASS_NAME, value='full-price').text.strip('$'))

            # Extract strain type.
            strain_type = div.find_element(by=By.CLASS_NAME, value='sort').text

            # Extract product URL (assuming the URL is stored in the href attribute of a link)
            product_url = div.get_attribute('href')

            # Store the extracted data in a dictionary
            obs = {
                'product_name': product_name,
                'image_url': product_image,
                'product_price': product_price,
                'strain_type': strain_type,
                'product_url': product_url
            }
            observations.append(obs)

    # Get the COA URL for each product.
    # TODO: Also get the image_url.
    for i, obs in enumerate(observations):
        coa_url = ''
        driver.get(obs['product_url'])
        sleep(3.33)
        links = driver.find_elements(by=By.TAG_NAME, value='a')
        for link in links:
            if link.get_attribute('href') and '.pdf' in link.get_attribute('href'):
                coa_url = link.get_attribute('href')
                break
        observations[i]['coa_url'] = coa_url
        print('Found COA URL: %s' % coa_url)

    # Close the driver.
    driver.close()

    # Download the COA PDFs.
    license_pdf_dir = os.path.join(data_dir, '.datasets', 'pdfs', 'MMTC-2019-0020')
    for obs in observations:
        coa_url = obs['coa_url']

        # Get the sample ID
        sample_id = coa_url.split('/')[-1].split('.')[0]

        # Format the file.
        outfile = os.path.join(license_pdf_dir, f'{sample_id}.pdf')
        if os.path.exists(outfile) and not overwrite:
            print('Cached: %s' % outfile)
            continue
        sleep(0.3)

        # Download the PDF.
        try:
            response = requests.get(coa_url, headers=DEFAULT_HEADERS)
            with open(outfile, 'wb') as pdf:
                pdf.write(response.content)
            print('Downloaded: %s' % outfile)
            sleep(3.33)
        except:
            print('Failed to download: %s' % coa_url)

    # Merge The Flowery data with the COA data.
    the_flowery = FLORIDA_LICENSES['MMTC-2019-0020']
    observations = [{**the_flowery, **x} for x in observations]

    # Save the data.
    date = datetime.now().isoformat()[:19].replace(':', '-')
    data = pd.DataFrame(observations)
    datasets_dir = os.path.join(DATA_DIR, '.datasets')
    data.to_excel(f'{datasets_dir}/the-flowery-lab-result-urls-{date}.xlsx', index=False)
    print('Saved %i lab result URLs for The Flowery.' % len(data))
    return data


# === Test ===
if __name__ == '__main__':

    # Specify where your data lives.
    DATA_DIR = 'D://data/florida/lab_results'
    
    # [✓] TEST: Get The Flowery COAs.
    the_flowery_products = get_product_results_the_flowery(DATA_DIR)
    the_flowery_coas = get_results_the_flowery(DATA_DIR)


#-----------------------------------------------------------------------
# Download TerpLife Labs COAs.
#-----------------------------------------------------------------------

class TerpLifeLabs:
    """Download lab results from TerpLife Labs."""

    def __init__(self, data_dir):
        """Initialize the driver and directories."""
        self.data_dir = data_dir
        self.datasets_dir = os.path.join(data_dir, '.datasets')
        self.pdf_dir = os.path.join(self.datasets_dir, 'pdfs')
        self.license_pdf_dir = os.path.join(self.pdf_dir, 'terplife')
        if not os.path.exists(self.datasets_dir): os.makedirs(self.datasets_dir)
        if not os.path.exists(self.pdf_dir): os.makedirs(self.pdf_dir)
        if not os.path.exists(self.license_pdf_dir): os.makedirs(self.license_pdf_dir)
        self.driver = initialize_selenium(
            download_dir=r'D:\data\florida\lab_results\.datasets\pdfs\terplife',
        )

    def get_results_terplife(
            self,
            queries: list,
            url='https://www.terplifelabs.com/coa/',
            wait=30,
        ):
        """Get lab results published by TerpLife Labs on the public web."""
        start = datetime.now()
        self.driver.get(url)
        sleep(1)
        for query in queries:
            print('Querying: %s' % query)
            self.query_search_box(query)
            self.download_search_results(wait=wait)
        end = datetime.now()
        print('Finished downloading TerpLife Labs COAs.')
        print('Time elapsed: %s' % str(end - start))

    def download_search_results(self, wait=30):
        """Download the results of a search."""
        # FIXME: Wait for the table to load instead of simply waiting.
        sleep(wait)
        load = EC.presence_of_element_located((By.CLASS_NAME, 'file-list'))
        table = WebDriverWait(self.driver, wait).until(load)
        rows = table.find_elements(By.CLASS_NAME, 'file-item')
        print('Found %i rows.' % len(rows))
        for row in rows:

            # Skip if the file has already be downloaded.
            try:
                file_name = row.find_element(By.CLASS_NAME, 'file-item-name').text
                if file_name == 'COAS':
                    continue
                outfile = os.path.join(self.license_pdf_dir, file_name)
                if os.path.exists(outfile):
                    print('Cached: %s' % outfile)
                    continue
            except:
                print('ERROR FINDING: %s' % file_name)
                sleep(60)
                break

            # Click on the icons for each row.
            try:
                self.driver.execute_script('arguments[0].scrollIntoView();', row)
                sleep(3.33)
                row.click()
            except:
                print('ERROR CLICKING: %s' % file_name)
                continue

            # Click the download button.
            try:
                sleep(random.uniform(30, 31))
                download_button = self.driver.find_element(By.CLASS_NAME, 'lg-download')
                download_button.click()
                print('Downloaded: %s' % file_name)
                # FIXME: Properly wait for the download to finish.
                sleep(random.uniform(30, 31))
            except:
                print('ERROR DOWNLOADING: %s' % file_name)
                continue

            # Click the close button.
            try:
                close_button = self.driver.find_element(By.CLASS_NAME, 'lg-close')
                close_button.click()
            except:
                print('ERROR CLOSING: %s' % file_name)

    def query_search_box(self, character):
        """Find the search box and enter text."""
        search_box = self.get_search_box()
        self.driver.execute_script('arguments[0].scrollIntoView();', search_box)
        sleep(0.3)
        search_box.clear()
        search_box.send_keys(character)
        sleep(0.3)
        search_button = search_box.find_element(By.XPATH, 'following-sibling::*[1]')
        search_button.click()

    def get_search_box(self):
        """Find the search box and enter text."""
        inputs = self.driver.find_elements(By.TAG_NAME, 'input')
        for input in inputs:
            if input.get_attribute('placeholder') == 'Enter a keyword to search':
                return input
        return None

    def quit(self):
        """Close the driver."""
        self.driver.quit()


# === Test ===
if __name__ == '__main__':

    import itertools

    # # Drill down on:
    # long_letters = [ 'wu', 'us', 'tp', 'qd', 'oo', 'og', 'nd', 'mh', 'it',
    #                 'io', 'ie', 'fm', 'bu', 'bf', 'at', 'aq', 'ao']
    # long_digits = ['81', '61', '51', '41', '40', '30', '20']

    # # Function to add digits 0-9 to each string in a list
    # def add_digits(strings):
    #     return [s + str(digit) for s in strings for digit in range(10)]

    # # Function to add letters a-z to each string in a list
    # def add_letters(strings):
    #     return [s + letter for s in strings for letter in string.ascii_lowercase]

    # # Create new lists with the combinations
    # combined_letters = add_letters(long_letters)
    # combined_digits = add_digits(long_digits)

    # # Printing the result
    # print("Combinations with letters:")
    # print(combined_letters)
    # print("\nCombinations with digits:")
    # print(combined_digits)

    def get_day_month_combinations():
        """Get all day-month combinations."""
        day_month_combinations = []
        for month in range(1, 13):
            if month in [4, 6, 9, 11]:
                days_in_month = 30
            elif month == 2:
                days_in_month = 29
            else:
                days_in_month = 31
            for day in range(1, days_in_month + 1):
                formatted_month = f'{month:02d}'
                formatted_day = f'{day:02d}'
                combination = formatted_month + formatted_day
                day_month_combinations.append(combination)
        return day_month_combinations

    # Download TerpLife Labs COAs by digit combinations.
    day_month_combinations = get_day_month_combinations()
    queries = [''.join(map(str, x)) for x in itertools.product(range(10), repeat=2)]

    # Download TerpLife Labs COAs by alphabetic combinations.
    # specific_letters = [x for x in string.ascii_lowercase]
    # queries = [a + b for a in specific_letters for b in string.ascii_lowercase]
    # queries.reverse()

    DATA_DIR = 'D://data/florida/lab_results'
    downloader = TerpLifeLabs(DATA_DIR)
    downloader.get_results_terplife(queries)
    downloader.quit()


# Optional: Search TerpLife for known strains.
