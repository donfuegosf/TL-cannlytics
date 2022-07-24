"""
Constants | Cannlytics
Copyright (c) 2021-2022 Cannlytics and Cannlytics Contributors

Authors: Keegan Skeate <https://github.com/keeganskeate>
Created: 11/8/2021
Updated: 7/16/2022
License: <https://github.com/cannlytics/cannlytics/blob/main/LICENSE>

Description: This module contains useful constant.
"""


# Optional: Load known analyses and analytes from
# the Cannlytics library via the Cannlytics API.
ANALYSES = {
    'cannabinoids': {'names': ['potency', 'POT']},
    'terpenes': {'names': ['terpene', 'TERP', 'terpenoids']},
    'residual_solvents': {'names': ['solvent', 'RST']},
    'pesticides': {'names': ['pesticide', 'PEST']},
    'microbes': {'names': ['microbial', 'MICRO']},
    'mycotoxins': {'names': ['mycotoxins', 'MYCO']},
    'heavy_metals': {'names': ['metal', 'MET']},
    'foreign_matter': {'names': ['foreign_materials']},
    'moisture_content': {'names': ['moisture']},
    'water_activity': {'names': ['WA']},
}

# TODO: Create `analyte_details.json`.

ANALYTES = {
    'CBC': 'cbc',
    'CBCA': 'cbca',
    'CBD': 'cbd',
    'CBDA': 'cbda',
    'CBDV': 'cbdv',
    'CBDVA': 'cbdva',
    'CBG': 'cbg',
    'CBGA': 'cbga',
    'CBL': 'cbl',
    'CBN': 'cbn',
    'CBNA': 'cbna',
    'Δ8': 'delta_8_thc',
    'Δ8 THC': 'delta_8_thc',
    'Δ8-THC': 'delta_8_thc',
    'Δ9 THC': 'delta_9_thc',
    'Δ9-THC': 'delta_9_thc',
    'Δ9': 'delta_9_thc',
    'THCA': 'thca',
    'THCV': 'thcv',
    'THCVA': 'thcva',
    'Total CBD': 'total_cbd',
    'Total CBG': 'total_cbg',
    'Total CBDV': 'total_cbdv',
    'Total CBC': 'total_cbc',
    'Total CBN': 'total_cbn',
    'Total THC': 'total_thc',
    'Total THC(Total THC = (THCA x 0.877) + THC)': 'total_thc',
    'Total CBD(Total CBD = (CBDA x 0.877) + CBD)': 'total_cbd',
    'Total Terpenes *': 'total_terpenes',
    'Terpinolene': 'terpinolene',
    'β-Caryophyllene': 'beta_caryophyllene',
    'α-Humulene': 'humulene',
    'β-Myrcene': 'beta_myrcene',
    'Linalool': 'linalool',
    'β-Pinene': 'beta_pinene',
    'd-Limonene': 'd_limonene',
    'α-Pinene': 'alpha_pinene',
    'β-Ocimene': 'ocimene',
    'cis-Nerolidol': 'cis_nerolidol',
    'α-Bisabolol': 'alpha_bisabolol',
    '3-Carene': 'carene',
    'Δ3-Carene': 'carene',
    'trans-Nerolidol': 'trans_nerolidol',
    'α-Terpinene': 'alpha_terpinene',
    'γ-Terpinene': 'gamma_terpinene',
    'Terpinen-4-ol': 'terpineol',
    'Caryophyllene Oxide': 'caryophyllene_oxide',
    'Geraniol': 'geraniol',
    'Eucalyptol': 'eucalyptol',
    'Camphene': 'camphene',
    'Guaiol': 'guaiol',
    'Isopulegol': 'isopulegol',
    'p-Cymene': 'p_cymene',
    'α-Ocimene': 'alpha_ocimene',
    '* Beyond scope of accreditation': 'wildcard',
    'Moisture': 'moisture_content',
    'Aspergillus flavus': 'aspergillus_flavus',
    'Aspergillus fumigatus': 'aspergillus_fumigatus',
    'Aspergillus niger': 'aspergillus_niger',
    'Aspergillus terreus': 'aspergillus_terreus',
    'Salmonella spp.': 'salmonella',
    'Salmonella': 'salmonella',
    'Shiga toxin-producing E. coli': 'e_coli',
    'Aflatoxin B1': 'aflatoxin_b1',
    'Aflatoxin B2': 'aflatoxin_b2',
    'Aflatoxin G1': 'aflatoxin_g1',
    'Aflatoxin G2': 'aflatoxin_g2',
    'Aflatoxins': 'total_aflatoxins',
    'Ochratoxin A': 'ochratoxin_a',
    'Abamectin': 'abamectin',
    'Acephate': 'acephate',
    'Acequinocyl': 'acequinocyl',
    'Acetamiprid': 'acetamiprid',
    'Aldicarb': 'aldicarb',
    'Azoxystrobin': 'azoxystrobin',
    'Bifenazate': 'bifenazate',
    'Bifenthrin': 'bifenthrin',
    'Boscalid': 'boscalid',
    'Captan': 'captan',
    'Carbaryl': 'carbaryl',
    'Carbofuran': 'carbofuran',
    'Chlorantranil-iprole': 'chlorantraniliprole',
    'Chlordane': 'chlordane',
    'Chlorfenapyr': 'chlorfenapyr',
    'Chlorpyrifos': 'chlorpyrifos',
    'Clofentezine': 'clofentezine',
    'Coumaphos': 'coumaphos',
    'Cyfluthrin': 'cyfluthrin',
    'Cypermethrin': 'cypermethrin',
    'Daminozide': 'daminozide',
    'Diazinon': 'diazinon',
    'Dichlorvos': 'dichlorvos',
    'Dimethoate': 'dimethoate',
    'Dimethomorph': 'dimethomorph',
    'Ethoprophos': 'ethoprophos',
    'Etofenprox': 'etofenprox',
    'Etoxazole': 'etoxazole',
    'Fenhexamid': 'fenhexamid',
    'Fenoxycarb': 'fenoxycarb',
    'Fenpyroximate': 'fenpyroximate',
    'Fipronil': 'fipronil',
    'Flonicamid': 'flonicamid',
    'Fludioxonil': 'fludioxonil',
    'Hexythiazox': 'hexythiazox',
    'Imazalil': 'imazalil',
    'Imidacloprid': 'imidacloprid',
    'Kresoxim-methyl': 'kresoxim_methyl',
    'Malathion': 'malathion',
    'Metalaxyl': 'metalaxyl',
    'Methiocarb': 'methiocarb',
    'Methomyl': 'methomyl',
    'Methyl parathion': 'methyl_parathion',
    'Mevinphos': 'mevinphos',
    'Myclobutanil': 'myclobutanil',
    'Naled': 'naled',
    'Oxamyl': 'oxamyl',
    'Paclobutrazol': 'paclobutrazol',
    'Pentachloroni-trobenzene': 'pentachloroni_trobenzene',
    'Permethrin': 'permethrin',
    'Phosmet': 'phosmet',
    'Piperonylbuto-xide': 'piperonyl_butoxide',
    'Prallethrin': 'prallethrin',
    'Propiconazole': 'propiconazole',
    'Propoxur': 'propoxur',
    'Pyrethrins': 'pyrethrins',
    'Pyridaben': 'pyridaben',
    'Spinetoram': 'spinetoram',
    'Spinosad': 'spinosad',
    'Spiromesifen': 'spiromesifen',
    'Spirotetramat': 'spirotetramat',
    'Spiroxamine': 'spiroxamine',
    'Tebuconazole': 'tebuconazole',
    'Thiacloprid': 'thiacloprid',
    'Thiamethoxam': 'thiamethoxam',
    'Trifloxystrob-in': 'trifloxystrobin',
    'Arsenic': 'arsenic',
    'Cadmium': 'cadmium',
    'Lead': 'lead',
    'Mercury': 'mercury',
    'Water Activity': 'water_activity',
    'Imbedded Foreign Material': 'foreign_matter',
    'Insect Fragments, Hair, Mammal Excrement': 'foreign_matter_fragments',
    'Mold': 'mold',
    'Sand, Soil, Cinders, Dirt': 'soil',
    'Sand': 'soil',
}

DECARB = 0.877 # Source: <https://www.conflabs.com/why-0-877/>

RANDOM_STRING_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

states = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    'DC': 'District of Columbia',
}

state_names = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
    'District of Columbia': 'DC',
    'American Samoa': 'AS',
    'Guam': 'GU',
    'Northern Mariana Islands': 'MP',
    'Puerto Rico': 'PR',
    'United States Minor Outlying Islands': 'UM',
    'U.S. Virgin Islands': 'VI'
}

state_time_zones = {
    'AL': 'America/Chicago',
    'AK': 'America/Anchorage',
    'AZ': 'America/Phoenix',
    'AR': 'America/Chicago',
    'CA': 'America/Los_Angeles',
    'CO': 'America/Denver',
    'CT': 'America/New_York',
    'DC': 'America/New_York',
    'DE': 'America/New_York',
    'FL': 'America/New_York',
    'GA': 'America/New_York',
    'HI': 'Pacific/Honolulu',
    'ID': 'America/Denver',
    'IL': 'America/Chicago',
    'IN': 'America/Indiana/Indianapolis',
    'IA': 'America/Chicago',
    'KS': 'America/Chicago',
    'KY': 'America/New_York',
    'LA': 'America/Chicago',
    'ME': 'America/New_York',
    'MD': 'America/New_York',
    'MA': 'America/New_York',
    'MI': 'America/New_York',
    'MN': 'America/Chicago',
    'MS': 'America/Chicago',
    'MO': 'America/Chicago',
    'MT': 'America/Denver',
    'NE': 'America/Chicago',
    'NV': 'America/Los_Angeles',
    'NH': 'America/New_York',
    'NJ': 'America/New_York',
    'NM': 'America/Denver',
    'NY': 'America/New_York',
    'NC': 'America/New_York',
    'ND': 'America/North_Dakota/Center',
    'OH': 'America/New_York',
    'OK': 'America/Chicago',
    'OR': 'America/Los_Angeles',
    'PA': 'America/New_York',
    'RI': 'America/New_York',
    'SC': 'America/New_York',
    'SD': 'America/Chicago',
    'TN': 'America/Chicago',
    'TX': 'America/Chicago',
    'UT': 'America/Denver',
    'VT': 'America/New_York',
    'VA': 'America/New_York',
    'WA': 'America/Los_Angeles',
    'WV': 'America/New_York',
    'WI': 'America/Chicago',
    'WY': 'America/Denver',
}
