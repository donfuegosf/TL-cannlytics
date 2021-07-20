"""
Worksheets | Cannlytics

Author: Keegan Skeate <keegan@cannlytics.com>
Created: 7/18/2021
Updated: 7/20/2021
License: MIT License <https://opensource.org/licenses/MIT>
"""
# Standard packages
from ast import literal_eval
import os

# External packages.
from dotenv import load_dotenv
from pandas import DataFrame
import requests
import xlwings as xw
from xlwings.utils import rgb_to_int

# Internal packages.
from cannlytics.utils.utils import snake_case


def get_data_block(sheet, coords, expand=None):
    """Get a data block.
    Args:
        sheet (Sheet): The worksheet containing the data block.
        coords (str): The inclusive coordinates of the data block.
        expand (str): Optionally expand the range of values.
    Returns
        (dict): A dictionary of the data in the data block.
    """
    data = {}
    values = sheet.range(coords).options(expand=expand).value
    for item in values:
        key = snake_case(item[0])
        value = item[1]
        data[key] = value
    return data


def increment_row(coords):
    """Increment a row given its starting coordinates.
    Args:
        coords (str):
    Returns:
        (str): The incremented row coordinates.
    """
    column = ''.join([i for i in coords if not i.isdigit()])
    seq_type = type(coords)
    row = int(seq_type().join(filter(seq_type.isdigit, coords))) + 1
    return column + str(row)


def show_status_message(sheet, coords, message, background=None, color=None):
    """Show a status message in an Excel spreadsheet.
    Args:
        sheet (Sheet): The sheet where the status message will be written.
        coords (str): The location of the status message.
        message (str): A status message to write to Excel.
        background (tuple): Optional background color.
        color (tuple): Optional font color.
    """
    sheet.range(coords).value = message
    if background:
        sheet.range(coords).color = literal_eval(background)
    if color:
        sheet.range(coords).api.Font.Color = rgb_to_int(literal_eval(color))


@xw.sub
def import_worksheet_data(model_type):
    """A function called from Excel to import data by ID
    from Firestore into the Excel workbook.
    Args:
        model_type (str): The data model at hand.
    """

    # Initialize the workbook.
    book = xw.Book.caller()
    worksheet = book.sheets.active
    config_sheet = book.sheets['cannlytics.conf']
    config = get_data_block(config_sheet, 'A1', expand='table')
    show_status_message(
        worksheet,
        coords=config['status_cell'],
        message='Importing %s data...' % model_type,
        background=config['success_color'],
    )

    # Read the IDs.
    id_cell = increment_row(config['table_cell'])
    ids = worksheet.range(id_cell).options(expand='down').value

    # Get Cannlytics API key from .env.
    load_dotenv(config['env_path'])
    api_key = os.getenv('CANNLYTICS_API_KEY')

    # Get the worksheet columns.
    columns = worksheet.range(config['table_cell']).options(expand='right').value
    columns = [snake_case(x) for x in columns]

    # Get data using model type and ID through the API.
    base = config['api_url']
    org_id = worksheet.range(config['org_id_cell']).value
    headers = {
        'Authorization': 'Bearer %s' % api_key,
        'Content-type': 'application/json',
    }
    for model_id in ids:
        if not model_id:
            continue # Skip empty rows.
        url = f'{base}/{model_type}/{model_id}?organization_id={org_id}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Once the data is retrieved, iterate over columns to get values.
            values = []
            data = response.json()['data']
            for column in columns:
                values.append(data.get(column))
            worksheet.range(id_cell).value = values
            id_cell = increment_row(id_cell)
        else:
            show_status_message(
                worksheet,
                coords=config['status_cell'],
                message='Error importing %s %s.' % (model_type, model_id),
                background=config['error_color']
            )
            return

    # Show success status message.
    show_status_message(
        worksheet,
        coords=config['status_cell'],
        message='Imported %s data.' % model_type,
    )


@xw.sub
def upload_worksheet_data(model_type):
    """A function called from Excel to import data by ID
    from Firestore into the Excel workbook."""

    # Initialize the workbook.
    book = xw.Book.caller()
    worksheet = book.sheets.active
    config_sheet = book.sheets['cannlytics.conf']
    config = get_data_block(config_sheet, 'A1', expand='table')
    show_status_message(
        worksheet,
        coords=config['status_cell'],
        message='Uploading %s data now...' % model_type,
        background=config['success_color'],
    )

    # Read table data, cleaning the column names.
    table = worksheet.range(config['table_cell'])
    data = table.options(DataFrame, index=False, expand='table').value
    data.columns = list(map(snake_case, data.columns))
    show_status_message(
        worksheet,
        coords=config['status_cell'],
        message='Imported data: %i observations' % len(data),
        background=config['success_color'],
    )

    # Determine the model type and organization.
    org_id = worksheet.range(config['org_id_cell']).value
    model_singular = data.columns[0].replace('_id', '')

    # Get Cannlytics API key from .env using env_path in config.
    load_dotenv(config['env_path'])
    api_key = os.getenv('CANNLYTICS_API_KEY')

    # Upload data using model type, ID, and data through the API.
    headers = {
        'Authorization': 'Bearer %s' % api_key,
        'Content-type': 'application/json',
    }
    base = config['api_url']
    for _, row in data.iterrows():
        json = row.to_dict()
        doc_id = json[f'{model_singular}_id']
        if not doc_id:
            continue
        url = f'{base}/{model_type}?organization_id={org_id}'
        response = requests.post(url, json=json, headers=headers)
        if response.status_code == 200:
            show_status_message(
                worksheet,
                coords=config['status_cell'],
                message='Uploaded %s %s' % (model_type, doc_id),
            )
        else:
            show_status_message(
                worksheet,
                coords=config['status_cell'],
                message='Error uploading %s %s. Check your internet connection and API key.' % (model_type, doc_id), # pylint:disable=line-too-long
                background=config['error_color']
            )
            return

    # Show success status message.
    show_status_message(
        worksheet,
        coords=config['status_cell'],
        message='Uploaded %s data.' % model_type,
    )
