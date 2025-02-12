"""
Analyze California Cannabis Lab Results
Copyright (c) 2023 Cannlytics

Authors: Keegan Skeate <https://github.com/keeganskeate>
Created: 12/10/2023
Updated: 1/2/2024
License: MIT License <https://github.com/cannlytics/cannabis-data-science/blob/main/LICENSE>
"""
# Standard imports:
import ast
import json
import matplotlib.pyplot as plt
import seaborn as sns

# External imports:
import pandas as pd
import statsmodels.api as sm

from cannlytics.utils import convert_to_numeric


# TODO: Make these standard functions.


def get_result_value(
        results,
        analyte,
        key='key',
        value='value',
    ):
    """Get the value for an analyte from a list of standardized results."""
    # Ensure that the results are a list.
    try:
        result_list = json.loads(results)
    except:
        try:
            result_list = ast.literal_eval(results)
        except:
            result_list = []
    if not isinstance(result_list, list):
        return None

    # Get the value of interest from the list of results.
    result_data = pd.DataFrame(result_list)
    if result_data.empty:
        return None
    try:
        result = result_data.loc[result_data[key] == analyte, value].iloc[0]
    except:
        return 0
    try:
        return convert_to_numeric(result, strip=True)
    except:
        return result
    

# # Identify all unique cannabinoids and terpenes.
# cannabinoids = []
# terpenes = []
# for item in emerald['results']:
#     lab_results = ast.literal_eval(item)
#     for result in lab_results:
#         if result['analysis'] == 'cannabinoids':
#             cannabinoids.append(result['name'])
#         elif result['analysis'] == 'terpenes':
#             terpenes.append(result['name'])
# cannabinoids = list(set(cannabinoids))
# terpenes = list(set(terpenes))
# print('Cannabinoids:', cannabinoids)
# print('Terpenes:', terpenes)


# === Setup ===

# Setup plotting style.
plt.style.use('fivethirtyeight')
plt.rcParams.update({
    'figure.figsize': (12, 8),
    'font.family': 'Times New Roman',
    'font.size': 24,
})


# === Read the data ===

# Define California datasets.
CA_LAB_RESULTS = {
    'Flower Company': {
        'datafiles': [
            # './data/ca-results-flower-company-2023-12-13.xlsx',
        ],
    },
    'Glass House Farms': {
        'datafiles': [],
    },
    'SC Labs':{
        'datafiles': [
            'D:/data/california/lab_results/datasets/sclabs/ca-lab-results-sclabs-2024-01-02-00-39-36.xlsx',
        ],
    },
}


# Read all datafiles.
all_results = []
for source in CA_LAB_RESULTS:
    for datafile in CA_LAB_RESULTS[source]['datafiles']:
        data = pd.read_excel(datafile)
        all_results.append(data)

# Aggregate results.
results = pd.concat(all_results)


# === Look at the Emerald Cup results ===
emerald_2023 = results.loc[results['producer'] == 'Emerald Cup 2023']
emerald_2022 = results.loc[results['producer'] == 'Emerald Cup 2022']
emerald_2020 = results.loc[results['producer'] == 'Emerald Cup 2020']
emerald_2023['year'] = 2023
emerald_2022['year'] = 2022
emerald_2020['year'] = 2020
emerald = pd.concat([emerald_2023, emerald_2022, emerald_2020])

# TODO: Merge with ranking data.

cannabinoids = [
    'thca',
    'cbga',
    'cbca',
    'delta_9_thc',
    'cbg',
    'thcva',
    'cbda',
    'delta_8_thc',
    'thcv',
    'cbd',
    'cbdv',
    'cbdva',
    'cbl',
    'cbn',
    'cbc',
]
terpenes = [
    'beta_caryophyllene',
    'd_limonene',
    'alpha_humulene',
    'beta_myrcene',
    'beta_pinene',
    'alpha_pinene',
    'beta_ocimene',
    'alpha_bisabolol',
    'terpineol',
    'fenchol',
    'linalool',
    'borneol',
    'camphene',
    'terpinolene',
    'fenchone',
    'nerolidol',
    'trans_beta_farnesene',
    'citronellol',
    'sabinene_hydrate',
    'nerol',
    'valencene',
    'sabinene',
    'alpha_phellandrene',
    'delta_3_carene',
    'alpha_terpinene',
    'p_cymene',
    'eucalyptol',
    'gamma_terpinene',
    'isopulegol',
    'camphor',
    'isoborneol',
    'menthol',
    'pulegone',
    'geraniol',
    'geranyl_acetate',
    'alpha_cedrene',
    'caryophyllene_oxide',
    'guaiol',
    'cedrol'
]

# Get the results for each cannabinoid and terpene.
for a in cannabinoids + terpenes:
    print('Augmenting:', a)
    emerald[a] = emerald['results'].apply(
        lambda x: get_result_value(x, a, key='key')
    )



# TODO: See which strain has the highest terpenes.


# TODO: See which strain has the most diverse terpene profile.


# TODO: See which strain has the most diverse cannabinoid profile.


# TODO: Build an ordered probit model to back-cast 2020 winners.



# === Environment analysis ===

# # Compare indoor vs. outdoor
# indoor = results[results['product_subtype'] == 'Indoor']
# outdoor = results[results['product_subtype'] == 'Full Sun']
# indoor_outdoor_comparison = indoor.describe().join(outdoor.describe(), lsuffix='_indoor', rsuffix='_outdoor')

# # Visualize indoor vs. outdoor cannabis.
# plt.ylabel('Count')
# plt.xlabel('Percent')
# plt.title('Terpene Concentrations in Indoor vs. Full Sun Cannabis in CA')
# indoor['total_terpenes'].hist(bins=40)
# outdoor['total_terpenes'].hist(bins=40)
# plt.legend(['Indoor', 'Outdoor'])
# plt.xlim(0)
# plt.tight_layout()
# # plt.savefig(f'figures/indoor-outdoor-thc.png', bbox_inches='tight', dpi=300)
# plt.show()


# === Chemical Analysis ===

# # Look at total cannabinoids.
# key = 'total_cannabinoids'
# results[key] = pd.to_numeric(results[key], errors='ignore')
# sample = results.dropna(subset=[key])
# sample[key].hist(bins=1000)
# plt.xlim(0, 100)
# plt.show()

# # Look at total terpenes.
# key = 'total_terpenes'
# results[key] = pd.to_numeric(results[key], errors='coerce')
# sample = results.dropna(subset=[key])
# sample[key].hist(bins=40)
# plt.show()

# # Look at moisture content.
# key = 'moisture_content'
# results[key] = pd.to_numeric(results[key], errors='coerce')
# sample = results.dropna(subset=[key])
# sample[key].hist(bins=40)
# plt.show()

# # Look at water activity.
# key = 'water_activity'
# results[key] = pd.to_numeric(results[key], errors='coerce')
# sample = results.dropna(subset=[key])
# sample[key].hist(bins=40)
# plt.show()

# # Look at moisture-adjusted total cannabinoids in flower.
# types = ['Flower', 'Flower, Inhalable']
# sample = results.loc[results['product_type'].isin(types)]
# sample = sample.loc[~sample['total_cannabinoids'].isna()]
# sample = sample.loc[~sample['moisture_content'].isna()]
# sample['wet_total_cannabinoids'] = sample['total_cannabinoids'] / (1 + sample['moisture_content'] * 0.01)
# sample['wet_total_cannabinoids'].hist(bins=1000)
# plt.xlim(0, 100)
# plt.show()

# # Calculate the mean wet total cannabinoids in flower in CA.
# valid = sample['wet_total_cannabinoids'].loc[sample['wet_total_cannabinoids'] < 100]
# valid.mean()


# === Product subtype analysis ===

# # Look at terpene concentrations in concentrate products:
# concentrate_types = [
#     'Badder',
#     'Diamond',
#     'Diamond Infused',
#     'Crushed Diamond',
#     'Liquid Diamonds',
#     'Distillate',
#     'Resin',
#     'Live Resin',
#     'Live Resin Infused',
#     'Live Resin Sauce',
#     'Sauce',
#     'Live Rosin',
#     'Unpressed Hash Green',
#     # 'Fresh Press',
#     # 'Hash Infused',
#     # 'Rosin Infused',
# ]

# # Creating a box plot of total terpenes in concentrates.
# concentrate_data = results.loc[results['product_subtype'].isin(concentrate_types)]
# filtered_data = concentrate_data.loc[~concentrate_data['total_terpenes'].isna()]
# grouped_data = filtered_data.groupby('product_subtype')['total_terpenes'].apply(list)
# mean_terpenes = {subtype: sum(values) / len(values) for subtype, values in grouped_data.items()}
# sorted_subtypes = sorted(mean_terpenes, key=mean_terpenes.get)
# data = [grouped_data[subtype] for subtype in sorted_subtypes]
# labels = sorted_subtypes
# plt.figure(figsize=(15, 11))
# plt.boxplot(data, vert=False, labels=labels)
# plt.xlabel('Total Terpenes (%)', labelpad=20)
# plt.title('Terpene Concentrations in Concentrates in CA', pad=20)
# plt.grid(axis='x', linestyle='--', alpha=0.7)
# plt.tight_layout()
# plt.show()


# === Price analysis ===

# # Clean the price data.
# results['discount_price'] = results['discount_price'].str.replace('$', '').astype(float)
# price_data = results.loc[results['discount_price'] > 0]
# price_data = price_data.loc[~price_data['amount'].isna()]
# price_data['price_per_gram'] = price_data['discount_price'] / price_data['amount']

# # See if THC, terpenes, etc. are correlated with price.
# types = ['Flower', 'Flower, Inhalable']
# # types = [
# #     'Infused Flower/Pre-Roll, Product Inhalable',
# #     'Pre-roll',
# #     'Plant (Preroll)',
# #     'Infused Pre-roll',
# # ]
# # types = [
# #     'Concentrates & Extracts (Other)',
# #     'Concentrates & Extracts (Distillate)',
# #     'Extract',
# #     'Concentrates & Extracts (Diamonds)',
# #     'Concentrates & Extracts (Live Resin)',
# #     'Concentrates & Extracts (Live Rosin)',
# #     'Concentrates & Extracts (Vape)',
# #     'Concentrate, Product Inhalable',
# #     'Distillate',
# # ]
# type_price_data = price_data.loc[price_data['product_type'].isin(types)]
# type_price_data = type_price_data.loc[type_price_data['total_cannabinoids'] < 100]

# # Visualize the relationship between cannabinoids and price.
# plt.figure(figsize=(10, 6))
# sns.regplot(
#     data=type_price_data,
#     x='total_cannabinoids',
#     y='price_per_gram',
# )
# plt.xlabel('Total Cannabinoids')
# plt.ylabel('Price per gram ($)')
# plt.title('Price per gram of flower to total cannabinoids in CA')
# plt.grid(True)
# plt.show()

# # Visualize the relationship between terpenes and price.
# plt.figure(figsize=(10, 6))
# sns.regplot(
#     data=type_price_data,
#     x='total_terpenes',
#     y='price_per_gram',
# )
# plt.xlabel('Total Terpenes')
# plt.ylabel('Price per gram ($)')
# plt.title('Price per gram of flower to total terpenes in CA')
# plt.grid(True)
# plt.show()

# # Price vs. Chemical Properties Regression
# X = type_price_data[['total_cannabinoids', 'total_terpenes']]
# y = type_price_data['price_per_gram']
# X_clean = X.dropna()
# y_clean = y.reindex(X_clean.index)
# X_clean = sm.add_constant(X_clean)
# model = sm.OLS(y_clean, X_clean)
# regression = model.fit()
# print(regression.summary())

# # Look at the average discount.
# results['discount'].hist(bins=40)
# plt.vlines(results['discount'].mean(), 0, 60, color='darkorange')
# plt.show()

# TODO: Look at the average price per product type.



# === Lineage analysis ===

# # Look at the most common parents.
# lineage_data = results['lineage'].dropna()
# unique_parents = pd.Series([parent for lineage in lineage_data for parent in lineage.split(' x ')]).value_counts()
# filtered_strains = unique_parents[unique_parents >= 2]
# plt.figure(figsize=(10, 8))
# filtered_strains.sort_values()[-20:].plot(kind='barh')
# plt.xlabel('Number of Descendants')
# plt.ylabel('')
# plt.title('Number of Descendants by Strain')
# plt.show()


# === Timeseries analysis ===

# # Format the date.
# results['date'] = pd.to_datetime(results['date_tested'])

# TODO: Look at total THC levels over time.


# TODO: Look at total terpene levels over time.



# === Geographic analysis ===

# Note: Mostly missing.

# TODO: Geocode `producer_address`.


# TODO: Compare different regions of CA.
