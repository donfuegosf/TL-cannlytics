"""
Cannabis Licenses | Get Arizona Licenses
Copyright (c) 2022-2023 Cannlytics

Authors:
    Keegan Skeate <https://github.com/keeganskeate>
    Candace O'Sullivan-Sutherland <https://github.com/candy-o>
Created: 9/27/2022
Updated: 8/17/2023
License: <https://github.com/cannlytics/cannlytics/blob/main/LICENSE>

Description:

    Collect Arizona cannabis license data.

Data Source:

    - Arizona Department of Health Services | Division of Licensing
    URL: <https://azcarecheck.azdhs.gov/s/?licenseType=null>

TODO:

    [ ] Separate the functionality into functions.
    [ ] Make the code more robust to errors.
    [ ] Make Google Maps API key optional.    

"""
# Standard imports.
from datetime import datetime
# from dotenv import dotenv_values
import os
import re
from time import sleep
from typing import List, Optional

# External imports.
# from cannlytics.data.gis import geocode_addresses
from cannlytics.data.web import initialize_selenium
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import zipcodes


# Specify state-specific constants.
STATE = 'AZ'
ARIZONA = {
    'licensing_authority_id': 'ADHS',
    'licensing_authority': 'Arizona Department of Health Services',
    'licenses_url': 'https://azcarecheck.azdhs.gov/s/?licenseType=null',
}


def get_county_from_zip(x):
    """Find a county given a zip code. Returns `None` if no match."""
    try:
        return zipcodes.matching(x)[0]['county']
    except KeyError:
        return None
    

def click_load_more(driver, container):
    """Click "Load more" until all of the licenses are visible."""
    more = True
    while(more):
        try:
            button = container.find_element(by=By.TAG_NAME, value='button')
            driver.execute_script('arguments[0].scrollIntoView(true);', button)
            button.click()
            counter = container.find_element(by=By.CLASS_NAME, value='count-text')
            only_digits = re.findall(r'\d+', counter.text)
            more = int(only_digits[0]) if only_digits else False
        except:
            more = False


def get_license_data_from_html(index, el):
    """Get a retailer's data."""
    body = el.find_element(by=By.CLASS_NAME, value='slds-media__body')
    divs = body.find_elements(by=By.TAG_NAME, value='div')
    name = divs[0].text
    legal_name = divs[1].text
    if not name:
        name = legal_name
    address = divs[3].text
    address_parts = address.split(',')
    parts = divs[2].text.split(' · ')
    link = divs[-1].find_element(by=By.TAG_NAME, value='a')
    href = link.get_attribute('href')
    return {
        'address': address,
        'details_url': href,
        'business_legal_name': legal_name,
        'business_dba_name': name,
        'business_phone': parts[-1],
        'license_status': parts[0],
        'license_type': parts[1],
        'premise_street_address': address_parts[0].strip(),
        'premise_city': address_parts[1].strip(),
        'premise_zip_code': address_parts[-1].replace('AZ ', '').strip(),
    }


def get_value_from_links(links: List[str], prefix: str):
    """Get a certain key from given links."""
    for link in links:
        href = link.get_attribute('href')
        if href is None:
            continue
        if href.startswith(prefix):
            return link.text


def get_licenses_az(
        data_dir: Optional[str] = None,
        env_file: Optional[str] = '.env',
    ):
    """Get Arizona cannabis license data."""

    # Create directories if necessary.
    if not os.path.exists(data_dir): os.makedirs(data_dir)

    # Initialize Selenium.
    driver = initialize_selenium()

    # Load the license page.
    driver.get(ARIZONA['licenses_url'])
    detect = (By.CLASS_NAME, 'slds-container_center')
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(detect))

    # Get the map container.
    container = driver.find_element(by=By.CLASS_NAME, value='slds-container_center')

    # Scroll to the bottom of the page.
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', container)
    sleep(1)

    # Click "Load more" until all of the licenses are visible.
    click_load_more(driver, container)

    # Get license data for each retailer.
    data = []
    els = container.find_elements(by=By.CLASS_NAME, value='map-item')
    for index, el in enumerate(els):
        data.append(get_license_data_from_html(index, el))

    # Standardize the retailer data.
    retailers = pd.DataFrame(data)
    retailers = retailers.assign(
        business_email=None,
        business_owner_name=None,
        business_structure=None,
        business_image_url=None,
        business_website=None,
        id=retailers.index,
        licensing_authority_id=ARIZONA['licensing_authority_id'],
        licensing_authority=ARIZONA['licensing_authority'],
        license_designation='Adult-Use',
        license_number=None,
        license_status_date=None,
        license_term=None,
        premise_latitude=None,
        premise_longitude=None,
        premise_state=STATE,
        issue_date=None,
        expiration_date=None,
        parcel_number=None,
        activity=None,
    )

    # Get each retailer's details.
    cultivators = pd.DataFrame(columns=retailers.columns)
    manufacturers = pd.DataFrame(columns=retailers.columns)
    for index, row in retailers.iterrows():

        # Load the licenses's details webpage.
        driver.get(row['details_url'])
        detect = (By.CLASS_NAME, 'slds-container_center')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(detect))
        container = driver.find_element(by=By.CLASS_NAME, value='slds-container_center')
        sleep(4)

        # Get links.
        links = container.find_elements(by=By.TAG_NAME, value='a')

        # Get the `business_email`.
        business_email = get_value_from_links(links, 'mailto:')
        col = retailers.columns.get_loc('business_email')
        retailers.iat[index, col] = business_email

        # Get the `license_number`.
        license_number = get_value_from_links(links, 'https://azdhs-licensing')
        col = retailers.columns.get_loc('license_number')
        retailers.iat[index, col] = license_number

        # Get the `premise_latitude` and `premise_longitude`.
        for link in links:
            href = link.get_attribute('href')
            if href is None:
                continue
            if href.startswith('https://maps.google.com/'):
                coords = href.split('=')[1].split('&')[0].split(',')
                lat_col = retailers.columns.get_loc('premise_latitude')
                long_col = retailers.columns.get_loc('premise_longitude')
                retailers.iat[index, lat_col] = float(coords[0])
                retailers.iat[index, long_col] = float(coords[1])
                break

        # FIXME: Scroll down to the bottom of the page.
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', container)
        sleep(1)

        # Get the `issue_date`.
        key = 'License Effective'
        el = container.find_element('xpath', f"//p[contains(text(),'{key}')]/following-sibling::lightning-formatted-text")
        col = retailers.columns.get_loc('issue_date')
        retailers.iat[index, col] = el.text

        # Get the `expiration_date`.
        key = 'License Expires'
        el = container.find_element('xpath', f"//p[contains(text(),'{key}')]/following-sibling::lightning-formatted-text")
        col = retailers.columns.get_loc('expiration_date')
        retailers.iat[index, col] = el.text

        # Get the `business_owner_name`.
        key = 'Owner / License'
        el = container.find_element('xpath', f"//p[contains(text(),'{key}')]/following-sibling::lightning-formatted-text")
        col = retailers.columns.get_loc('expiration_date')
        retailers.iat[index, col] = el.text

        # Get the `license_designation` ("Services").
        key = 'Services'
        try:
            el = container.find_element('xpath', f"//p[contains(text(),'{key}')]/following-sibling::lightning-formatted-rich-text")
            col = retailers.columns.get_loc('license_designation')
            retailers.iat[index, col] = el.text
        except:
            pass

        # Create entries for cultivations.
        cultivator = retailers.iloc[index].copy()
        key = 'Offsite Cultivation Address'
        try:
            el = container.find_element('xpath', f"//p[contains(text(),'{key}')]/following-sibling::lightning-formatted-text")
            address = el.text
        except:
            address = None
        if address:
            parts = address.split(',')
            cultivator['address'] = address
            cultivator['premise_street_address'] = parts[0]
            cultivator['premise_city'] = parts[1].strip()
            cultivator['premise_zip_code'] = parts[-1].replace(STATE, '').strip()
            cultivator['license_type'] = 'Offsite Cultivation'
            # cultivators.append(cultivator, ignore_index=True)
            cultivators.loc[len(cultivators)] = cultivator

        # Create entries for manufacturers.
        manufacturer = retailers.iloc[index].copy()
        key = 'Manufacture Address'
        try:
            el = container.find_element('xpath', f"//p[contains(text(),'{key}')]/following-sibling::lightning-formatted-text")
            address = el.text
        except:
            address = None
        if address:
            parts = address.split(',')
            manufacturer['address'] = address
            manufacturer['premise_street_address'] = parts[0]
            manufacturer['premise_city'] = parts[1].strip()
            manufacturer['premise_zip_code'] = parts[-1].replace(STATE, '').strip()
            manufacturer['license_type'] = 'Offsite Cultivation'
            # manufacturers.append(manufacturer, ignore_index=True)
            manufacturers.loc[len(manufacturers)] = manufacturer

    # End the browser session.
    try:
        driver.close()
    except:
        pass

    # Drop unnecessary columns.
    retailers.drop(columns=['address', 'details_url'], inplace=True)

    # Lookup counties by zip code.
    retailers['premise_county'] = retailers['premise_zip_code'].apply(get_county_from_zip)
    cultivators['premise_county'] = cultivators['premise_zip_code'].apply(get_county_from_zip)
    manufacturers['premise_county'] = manufacturers['premise_zip_code'].apply(get_county_from_zip)

    # TODO: Setup geocoding
    # config = dotenv_values(env_file)
    # api_key = config['GOOGLE_MAPS_API_KEY']
    # drop_cols = ['state', 'state_name', 'county', 'address', 'formatted_address']
    # gis_cols = {'latitude': 'premise_latitude', 'longitude': 'premise_longitude'}

    # # Geocode cultivators.
    # cultivators = geocode_addresses(cultivators, api_key=api_key, address_field='address')
    # cultivators.drop(columns=drop_cols, inplace=True)
    # cultivators.rename(columns=gis_cols, inplace=True)

    # # Geocode manufacturers.
    # manufacturers = geocode_addresses(manufacturers, api_key=api_key, address_field='address')
    # manufacturers.drop(columns=drop_cols, inplace=True)
    # manufacturers.rename(columns=gis_cols, inplace=True)

    # TODO: Lookup business website and image.

    # Aggregate all licenses.
    licenses = pd.concat([retailers, cultivators, manufacturers])

    # Get the refreshed date.
    timestamp = datetime.now().isoformat()
    licenses['data_refreshed_date'] = timestamp
    retailers['data_refreshed_date'] = timestamp
    cultivators['data_refreshed_date'] = timestamp
    manufacturers['data_refreshed_date'] = timestamp

    # Save and return the data.
    if data_dir is not None:
        date = timestamp[:10]
        labs = licenses.loc[licenses['license_type'] == 'Marijuana Laboratory']
        labs.to_csv(f'{data_dir}/labs-{STATE.lower()}-{date}.csv', index=False)
        retailers.to_csv(f'{data_dir}/retailers-{STATE.lower()}-{date}.csv', index=False)
        cultivators.to_csv(f'{data_dir}/cultivators-{STATE.lower()}-{date}.csv', index=False)
        manufacturers.to_csv(f'{data_dir}/manufacturers-{STATE.lower()}-{date}.csv', index=False)
        licenses.to_csv(f'{data_dir}/licenses-{STATE.lower()}-{date}.csv', index=False)
        licenses.to_csv(f'{data_dir}/licenses-{STATE.lower()}-latest.csv', index=False)

    # Return the licenses.
    return licenses


# === Test ===
# [✓] Tested: 2023-12-17 by Keegan Skeate <keegan@cannlytics>
if __name__ == '__main__':

    # Specify where your data lives.
    DATA_DIR = '../data/az'
    ENV_FILE = '../../../.env'

    # Support command line usage.
    import argparse
    try:
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('--d', dest='data_dir', type=str)
        arg_parser.add_argument('--data_dir', dest='data_dir', type=str)
        arg_parser.add_argument('--env', dest='env_file', type=str)
        args = arg_parser.parse_args()
    except SystemExit:
        args = {'d': DATA_DIR, 'env_file': ENV_FILE}

    # Get licenses, saving them to the specified directory.
    data_dir = args.get('d', args.get('data_dir'))
    env_file = args.get('env_file')
    data = get_licenses_az(data_dir, env_file=env_file)
