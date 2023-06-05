"""
Constants | Cannlytics
Copyright (c) 2021-2022 Cannlytics and the Cannabis Data Science Team

Authors: Keegan Skeate <https://github.com/keeganskeate>
Created: 11/8/2021
Updated: 11/28/2022
License: <https://github.com/cannlytics/cannlytics/blob/main/LICENSE>

Description: This module contains useful constants. In particular, there
are maps of encountered `ANALYSES`, `ANALYTES`, `STANDARD_FIELDS`,
`STANDARD_UNITS, `PRODUCT_TYPES`, and `STRAINS` to standard keys.
There are also `CODINGS` to help normalize result values.
The remaining useful constants are: `DECARB`, `DEFAULT_HEADERS`,
`RANDOM_STRING_CHARS`, `states`, `state_names`, `state_time_zones`.
"""

# Standard analysis key map.
# Optional: Load known analyses and analytes from
# the Cannlytics Database via the Cannlytics API.
STANDARD_ANALYSES = {
    'cannabinoids': {'name': 'Cannabinoids'},
    'terpenes': {'name': 'Terpenes'},
    'residual_solvents': {'name': 'Residual Solvents'},
    'pesticides': {'name': 'Pesticides'},
    'microbes': {'name': 'Microbes'},
    'mycotoxins': {'name': 'Mycotoxins'},
    'heavy_metals': {'name': 'Heavy Metals'},
    'foreign_matter': {'name': 'Foreign Matter'},
    'moisture_content': {'name': 'Moisture Content'},
    'water_activity': {'name': 'Water Activity'},
}

# A map of encountered analyses to their standardized analysis.
ANALYSES = {
    'cannabinoids': 'cannabinoids',
    'cannabinoid': 'cannabinoids',
    'Cannabinoid': 'cannabinoids',
    'POT': 'cannabinoids',
    'Potency': 'cannabinoids',
    'Potency Analysis by HPLC': 'cannabinoids',
    'Potency Test Result': 'cannabinoids',
    'CANNABINOID': 'cannabinoids',
    'foreign_materials': 'foreign_matter',
    'foreign_matter': 'foreign_matter',
    'Foreign Material': 'foreign_matter',
    'foreign_material': 'foreign_matter',
    'Filth and Foreign Material': 'foreign_matter',
    'Filth & Foreign Material': 'foreign_matter',
    'Filth and Foreign Material Inspection by Magnification': 'foreign_matter',
    'foreign_material_visual_inspection': 'foreign_matter',
    'FOREIGN MATERIALS': 'foreign_matter',
    'Foreign Materials': 'foreign_matter',
    'metal': 'heavy_metals',
    'MET': 'heavy_metals',
    'heavy_metals': 'heavy_metals',
    'Heavy Metals': 'heavy_metals',
    'Metals Analysis by ICPMS': 'heavy_metals',
    'Heavy Metals Screen': 'heavy_metals',
    'HEAVY METALS': 'heavy_metals',
    'microbial': 'microbes',
    'microbes': 'microbes',
    'microbiological': 'microbes',
    'microbiological_contaminants': 'microbes',
    'Microbiology': 'microbes',
    'microbiology': 'microbes',
    'Compliance Microbial': 'microbes',
    'Microbial Qpcr': 'microbes',
    'Microbial Result': 'microbes',
    'Microbial Screen': 'microbes',
    'MICROBIAL IMPURITIES': 'microbes',
    'Microbials by PCR': 'microbials',
    'moisture': 'moisture',
    'Moisture': 'moisture',
    'MOISTURE': 'moisture',
    'moisture_content': 'moisture',
    'Moisture Content': 'moisture',
    'Moisture by Moisture Balance': 'moisture',
    'Percent Moisture (%)': 'moisture',
    'moisture_analysis': 'moisture',
    'mycotoxins': 'mycotoxins',
    'MYCO': 'mycotoxins',
    'mycotoxin': 'mycotoxins',
    'Mycotoxin': 'mycotoxins',
    'Mycotoxins': 'mycotoxins',
    'Mycotoxins by LCMSMS': 'mycotoxins',
    'Mycotoxin Screen': 'mycotoxins',
    'MYCOTOXIN': 'mycotoxins',
    'PEST': 'pesticides',
    'pesticides': 'pesticides',
    'pesticide': 'pesticides',
    'Category 1 Pesticide': 'pesticides',
    'Category 2 Pesticide': 'pesticides',
    'Chemical Residue': 'pesticides',
    'Chemical Residue GC': 'pesticides',
    'Chemical Residue Gc': 'pesticides',
    'Pesticide Analysis by GCMS/LCMS': 'pesticides',
    'Pesticide Screen': 'pesticides',
    'Pesticide Screen Result - Category 1': 'pesticides',
    'Pesticide Screen Result - Category 2': 'pesticides',
    'PESTICIDES': 'pesticides',
    'solvent': 'residual_solvents',
    'RST': 'residual_solvents',
    'residual_solvents': 'residual_solvents',
    'residual_solvent': 'residual_solvents',
    'Residual Solvent Screen - Category 1': 'residual_solvents',
    'Residual Solvent Screen - Category 2': 'residual_solvents',
    'RESIDUAL SOLVENTS': 'residual_solvents',
    'terpenoids': 'terpenes',
    'TERP': 'terpenes',
    'terpenes': 'terpenes',
    'terpene': 'terpenes',
    'Terpenoid': 'terpenes',
    'terpenoid': 'terpenes',
    'Terpene': 'terpenes',
    'Terpene Analysis by GCMS': 'terpenes',
    'Terpene Test Result': 'terpenes',
    'TERPENES': 'terpenes',
    'WA': 'water_activity',
    'water_activity': 'water_activity',
    'Water Activity': 'water_activity',
    'Water Activity by Aqua Lab': 'water_activity',
    'Water Activity (Aw)': 'water_activity',
    'WATER ACTIVITY': 'water_activity',
    'terpenoid_testing': 'terpenes',
    # Necessary?
    'mycotoxins_status': 'mycotoxins',
    'pesticides_status': 'pesticides',
    'cannabinoids_status': 'cannabinoids',
    'heavy_metals_status': 'heavy_metals',
    'water_activity_status': 'water_activity',
    'Cannabinoid Profile': 'cannabinoids',
    'Microbiological Screen': 'microbes',
    'Mycotoxin Screen': 'mycotoxins',
}

# A map of encountered analytes to their standardized analyte,
# excluding analytes that can be standardized with `snake_case` alone.
# Optional: Create `analyte_details.json`.
ANALYTES = {
    'B1': 'aflatoxin_b1',
    'Aflatoxin B1': 'aflatoxin_b1',
    'B2': 'aflatoxin_b2',
    'Aflatoxin B2': 'aflatoxin_b2',
    'G1': 'aflatoxin_g1',
    'Aflatoxin G1': 'aflatoxin_g1',
    'G2': 'aflatoxin_g2',
    'Aflatoxin G2': 'aflatoxin_g2',
    'a_bisabolol': 'alpha_bisabolol',
    'a_cedrene': 'alpha_cedrene',
    'Ocimene isomer I': 'alpha_ocimene',
    'a_phellandrene': 'alpha_phellandrene',
    'a_pinene': 'alpha_pinene',
    'a_terpinene': 'alpha_terpinene',
    'alphaterpinene': 'alpha_terpinene',
    'A. flavus': 'aspergillus_flavus',
    'A.fumigatus': 'aspergillus_fumigatus',
    'a_fumigatus': 'aspergillus_fumigatus',
    'A. niger': 'aspergillus_niger',
    'a_niger': 'aspergillus_niger',
    'Aspergillus terreus': 'aspergillus_terreus',
    'A. terreus': 'aspergillus_terreus',
    'avermectin_b_1_a_abamectin': 'avermectin_b1b',
    'b_caryophyllene': 'beta_caryophyllene',
    'betacaryophyllene': 'beta_caryophyllene',
    'caryophyliene_oxide': 'caryophyllene_oxide',
    'Ocimene isomer II': 'beta_ocimene',
    'b_pinene': 'beta_pinene',
    'n_butane': 'butane',
    'Δ3-Carene': 'delta_3_carene',
    'Chlorantranil-iprole': 'chlorantraniliprole',
    'cis-Nerolidol': 'cis_nerolidol',
    'cy_uthrin': 'cyfluthrin',
    'delta_limonene': 'd_limonene',
    'limonene': 'd_limonene',
    'r_limonene': 'd_limonene',
    '(R)-(+)-Limonene': 'd_limonene',
    '3-Carene': 'delta_3_carene',
    '3_carene': 'delta_3_carene',
    '4_carene': 'delta_3_carene',
    'Δ8': 'delta_8_thc',
    'D8THC': 'delta_8_thc',
    'd_8_thc': 'delta_8_thc',
    'delta_8_thc_d_8_thc': 'delta_8_thc',
    'Δ9': 'delta_9_thc',
    'D9THC': 'delta_9_thc',
    'd_9_othc': 'delta_9_thc',
    'delta_9_thc_d_9_thc': 'delta_9_thc',
    'd_9_thca': 'thca',
    'd_9_thcva': 'thcva',
    'd_9_thcv': 'thcv',
    'cbca_3': 'cbca',
    'cbna_3': 'cbna',
    'cbl_3': 'cbl',
    'THCA-A': 'thca',
    'thca_a': 'thca',
    'ddvp_dichlorvous': 'dichlorvos',
    'Dichlorvos (DDVP)': 'dichlorvos',
    'dichlorvos_ddvp': 'dichlorvos',
    'DDVP (Dichlorvous)': 'dichlorvos',
    'ddvp_dichlorvos': 'dichlorvos',
    'SSCD': 'soil',
    'Escherichia Coli': 'e_coli',
    'escherichia_coli': 'e_coli',
    'Shiga toxin-producing E. coli': 'e_coli',
    'escherichia_coli_stec': 'e_coli',
    'escherichia_coli_shigella': 'e_coli',
    'STEC': 'e_coli',
    'IFM': 'foreign_matter',
    'Imbedded Foreign Material': 'foreign_matter',
    'IF RH ME': 'foreign_matter',
    'Insect Fragments, Hair, Mammal Excrement': 'foreign_matter',
    'g_terpinene': 'gamma_terpinene',
    'gama_terpinene': 'gamma_terpinene',
    'gammaterpinene': 'gamma_terpinene',
    'α-Humulene': 'alpha_humulene',
    'a_humulene': 'alpha_humulene',
    'alphahumulene': 'alpha_humulene',
    'humulene': 'alpha_humulene',
    'Moisture': 'moisture_content',
    'aflatoxin_b_1_b_2_g_1_g_2_and_ochratoxin_a': 'mycotoxins',
    'Naled': 'naled',
    'Ochratoxin A': 'ochratoxin_a',
    'β-Ocimene': 'beta_ocimene',
    'Oxamyl': 'oxamyl',
    'p-Cymene': 'p_cymene',
    'para_cymene': 'p_cymene',
    'p-Mentha-1,5-diene': 'p_mentha_1_5_diene',
    'p_mentha_15_diene': 'p_mentha_1_5_diene',
    'Piperonylbuto-xide': 'piperonyl_butoxide',
    'r_pulegone': 'pulegone',
    'Salmonella spp.': 'salmonella',
    'Salmonella SPP': 'salmonella',
    'Salmonella spp': 'salmonella',
    'salmonella_specific_gene': 'salmonella',
    'Sand, Soil, Cinders, Dirt': 'soil',
    'Sand': 'soil',
    'SscD': 'soil',
    'spinetoram_j': 'spinetoram',
    'spinetoram_l': 'spinetoram',
    'a_terpineol': 'alpha_terpineol',
    'Terpinen-4-ol': 'terpineol',
    'gammaterpineol': 'gamma_terpineol',
    'Aflatoxins': 'total_aflatoxins',
    'Total CBD(Total CBD = (CBDA x 0.877) + CBD)': 'total_cbd',
    'Total THC(Total THC = (THCA x 0.877) + THC)': 'total_thc',
    'trans_b_farnesene': 'trans_beta_farnesene',
    'trans_beta_famesene': 'trans_beta_farnesene',
    'Trifloxystrob-in': 'trifloxystrobin',
    'AW': 'water_activity',
    '* Beyond scope of accreditation': 'wildcard',
    'afalatoxin_b_2': 'aflatoxin_b2',
    'aflatoxin_b_1': 'aflatoxin_b1',
    'aflatoxin_b_2': 'aflatoxin_b2',
    'aflatoxin_g_1': 'aflatoxin_g1',
    'aflatoxin_g_2': 'aflatoxin_g2',
    'aspergillus_siger': 'aspergillus_niger',
    'avermectin_b_1_b_abamectin': 'avermectin_b1b',
    'b_ocimene': 'beta_ocimene',
    'myrcene': 'beta_myrcene',
    '0_1_guaiol': 'guaiol',
    '0_3_guaiol': 'guaiol',
    '1_2_dichloro_ethane': '1_2_dichloroethane',
    '8_thc': 'delta_8_thc',
    '9_thc': 'delta_9_thc',
    '9_thca': 'thca',
    'a_atoxin_b_1': 'aflatoxin_b1',
    'a_atoxin_g_1': 'aflatoxin_g1',
    'a_atoxin_g_2': 'aflatoxin_g2',
    'carene': 'delta_3_carene',
    'd_3_carene': 'delta_3_carene',
    'd_9_thc': 'delta_9_thc',
    'caryophyllene': 'beta_caryophyllene',
    'chlorantranilip_role': 'chlorantraniliprole',
    'trichloroethene': 'trichloroethylene',
    'xylenes': 'total_xylenes',
    'total_total_xylenes': 'total_xylenes',
    'total_sample_area_covered_by_mold': 'mold',
    'yeast_and_mold': 'mold',
    'total_sample_area_covered_by_sand_soil_cinders_or_dirt': 'soil',
    'total_sample_area_covered_by_an_imbedded_foreign_material': 'foreign_matter',
    'tri_oxystrobin': 'trifloxystrobin',
    'total_aflatoxin': 'total_aflatoxins',
    'spinosad': 'spinosad_a',
    'spinosyn_a_spinosad': 'spinosad_a',
    'spinosyn_d_spinosad': 'spinosad_d',
    'shiga_toxin_producing_escherichia_coli': 'e_coli',
    'sand_soils_cinders_and_dirt': 'soil',
    'salmonella_aoac': 'salmonella',
    'salmonella_spp': 'salmonella',
    'pyrethrins_pyrethrin_i': 'pyrethrins',
    'pyrethrins_pyrethrin_ii': 'pyrethrins',
    'pentachloroni_trobenzene': 'pentachloronitrobenzene',
    'pentachloronitro_benzene': 'pentachloronitrobenzene',
    'mammalian_excreta': 'foreign_matter',
    'mammalian_excreta_count': 'foreign_matter',
    'insect_fragment': 'foreign_matter',
    'insect_fragment_count': 'foreign_matter',
    'imbedded_foreign_material': 'foreign_matter',
    'hair': 'foreign_matter',
    'hair_count': 'foreign_matter',
    'loq_isoborneol': 'isoborneol',
    'loq_terpineol': 'terpineol',
    'l_fenchone': 'fenchone',
    'moisture': 'moisture_content',
    'piperonylbu_toxide': 'piperonyl_butoxide',
    'isopropanol': 'isopropyl_alcohol',
    '2_propanol': 'isopropyl_alcohol',
    'propan_2_ol': 'isopropyl_alcohol',
    'IPA': 'isopropyl_alcohol',
    'lsopropyl_alcohol': 'isopropyl_alcohol',
    'isopropylalcohol': 'isopropyl_alcohol',
    'methyl_parathion': 'parathion_methyl',
    'delta_9_thc_per_packagepackage_3_5_grams': 'total_thc_per_package',
    'n_hexane': 'hexane',
    'mevinphos_i': 'mevinphos',
    'mevinphos_ii': 'mevinphos',
    'permethrin_cis': 'permethrin',
    'permethrin_trans': 'permethrin',
    'permethrins': 'permethrin',
    'chlordane_cis': 'chlordane',
    'chlordane_trans': 'chlordane',
    'trans_geraniol': 'geraniol',
    'cis_geraniol': 'geraniol',
    'geranyl': 'geranyl_acetate',
    'geranylacetate': 'geranyl_acetate',
    'trans_ocimene': 'beta_ocimene',
    'cis_ocimene': 'alpha_ocimene',
    'farnesene': 'trans_beta_farnesene',
    'ethoprop_hos': 'ethoprophos',
    'fenpryoximate': 'fenpyroximate',
    'fludioxanil': 'fludioxonil',
    'thiaclorprid': 'thiacloprid',
    '9_thc_per_serving': 'delta_9_thc_per_serving',
    'd_9_thc_per_serving': 'delta_9_thc_per_serving',
    'n_pentane': 'pentane',
    'n_heptane': 'heptane',
    'carbotfuran': 'carbofuran',
    'lsobomneol': 'isoborneol',
    'lsoborneol': 'isoborneol',
    'lsopulegol': 'isopulegol',
    'methomy': 'methomyl',
    # FIXME: Standardize `fm`, `sscd`, `cep` without messing everything up.
    # 'ocimene': 'alpha_ocimene',
    'Tetrahydrocannabinolic acid': 'thca',
    'D9-Tetrahydrocannabinol': 'delta_9_thc',
    'Cannabidiolic acid': 'cbda',
    'Cannabidiol': 'cbd',
    'Cannabinol': 'cbn',
    'Cannabichromene': 'cbc',
    'Cannabigerolic acid': 'cbga',
    'Cannabigerol': 'cbg',
    'Cannabidivarin': 'cbdv',
    'Tetrahydrocannabivarin': 'thcv',
    'D8-Tetrahydrocannabinol': 'delta_8_thc',
    'Total Yeast and Mold': 'mold',
    'total_yeasttomold': 'mold',
    'Total Yeast/Mold': 'mold',
    'Bile-Tolerant Gram-Neg. Bacteria': 'enterobacteriaceae',
    'btgn': 'enterobacteriaceae',
    'Total Arsenic': 'arsenic',
    'Total Mercury': 'mercury',
    'arsenic_as': 'arsenic',
    'lead_pb': 'lead',
    'cadmium_cd': 'cadmium',
    'mercury_hg': 'mercury',
    'Arsenic (As)': 'arsenic',
    'Lead (Pb)': 'lead',
    'Cadmium (Cd)': 'cadmium',
    'Mercury (Hg)': 'mercury',
    'stec_e_coli': 'e_coli',
    'stec': 'e_coli',
    'escherichia_coli_specific': 'e_coli',
    'iso_butane': 'isobutane',
    'YM': 'mold',
    'CC': 'total_coliforms',
    'TAC': 'total_viable_aerobic_bacteria',
    'total_yeast_and_mold': 'mold',
    'total_bile_tolerant_gram_negative_bacteria': 'enterobacteriaceae',
    'mycotoxin': 'total_aflatoxins',
    'a_bisabolene': 'alpha_bisabolene',
    'a_bulnesene': 'alpha_bulnesene',
    'a_farnesene': 'alpha_farnesene',
    'a_maaliene': 'alpha_maaliene',
    'a_ocimene': 'alpha_ocimene',
    'a_thujone': 'alpha_thujone',
    'b_farnesene': 'trans_beta_farnesene',
    'b_maaliene': 'beta_maaliene',
    'bisabolol': 'alpha_bisabolol',
    'foreign_matter_i_h_e': 'foreign_matter',
}
# TODO: Find out how to map:
# cis_nerolidol vs. nerolidol vs. nerolidol_1 vs. nerolidol_2 vs. trans_nerolidol?

# A map of encountered fields to their standardized field.
# FIXME: Lab's sometimes use sample_id as lab_id.
# 'sample_id': 'lab_id',
STANDARD_FIELDS = {
    'Analyte': 'name',
    'Labeled Amount': 'sample_weight',
    'Limit': 'limit',
    'Detected': 'value',
    'LOD': 'lod',
    'LOQ': 'loq',
    'Pass/Fail': 'status',
    'metrc_src_uid': 'metrc_source_id',
    'matrix': 'product_type',
    'collected_on': 'date_collected',
    'received_on': 'date_received',
    'moisture': 'moisture_content',
    'terpenoids': 'terpenes',
    'foreign_materials': 'foreign_matter',
    'filth_and_foreign_matter': 'foreign_matter',
    'total_terpenoids_mgtog': 'total_terpenes_mg_g',
    'Source Batch ID': 'batch_id',
    'batch_number': 'batch_number',
    'batch_size': 'batch_size',
    '9_thc_per_unit': 'cannabinoids_status',
    'collected': 'date_collected',
    'Collected': 'date_collected',
    'harvesttoprocessing_date': 'date_harvested',
    'Harvest/Processing Date': 'date_harvested',
    'manufacture_date': 'date_produced',
    'received': 'date_received',
    'date_received': 'date_received',
    'date_sampled': 'date_sampled',
    'Date': 'date_tested',
    'date_reported': 'date_tested',
    'dates_of_analysis': 'date_tested',
    'business_name': 'distributor',
    'license_number': 'distributor_license_number',
    'foreign_material_method': 'foreign_matter_method',
    'foreign_material': 'foreign_matter_status',
    'heavy_metals': 'heavy_metals_status',
    'Instrument': 'instrument',
    'coa_id': 'lab_id',
    'sample_no': 'lab_id',
    'lab_sample_id': 'lab_id',
    'Lab Sample ID': 'lab_id',
    'sample_code': 'lab_id',
    'Lab ID': 'lab_id',
    'licensenumber': 'lab_license_number',
    'action-limit': 'limit',
    'action': 'limit',
    'limit': 'limit',
    'LOD mg/g': 'lod',
    'LOD (mg/g)': 'lod',
    'LOD (ug/g)': 'lod',
    'LOD (ug/kg)': 'lod',
    'LOD/LOQ': 'lod',
    'lod': 'lod',
    'LOQ mg/g': 'loq',
    'LOQ (mg/g)': 'loq',
    'LOQ (ug/g)': 'loq',
    'LOQ (ug/kg)': 'loq',
    'loq': 'loq',
    'mu': 'margin_of_error',
    'sample_matrix': 'matrix',
    'Method': 'method',
    'track_and_trace_test_package': 'metrc_lab_id',
    'Test RFID': 'metrc_lab_id',
    'Lab Metrc Id': 'metrc_lab_id',
    'source_metrc_uid': 'metrc_source_id',
    'metrc_uid': 'metrc_source_id',
    'batch_id': 'metrc_source_id',
    'track_and_trace_source_package_s': 'metrc_source_id',
    'Source RFID': 'metrc_source_id',
    'metrc_tag': 'metrc_source_id',
    'Client Metrc Id': 'metrc_source_id',
    'mg/g': 'mg_g',
    'result-mass': 'mg_g',
    'microbiology_status': 'microbes_status',
    'microbial_status': 'microbes_status',
    'microbials_status': 'microbes_status',
    'microbiology': 'microbes_status',
    'mycotoxins': 'mycotoxins_status',
    'Target Analyte': 'name',
    'Microbiological Assay': 'name',
    'compound': 'name',
    'Cannabinoid': 'name',
    'analyte': 'name',
    'name': 'name',
    'Order Number': 'order_number',
    'pesticides': 'pesticides_status',
    'Company': 'producer',
    'client': 'producer',
    'client_address': 'producer_address',
    'client_license_number': 'producer_license_number',
    'sample_name': 'product_name',
    'Sample Name': 'product_name',
    'unit_mass': 'product_size',
    'Type': 'product_type',
    'Matrix': 'product_type',
    'sample_type': 'product_type',
    'Matrix Type': 'product_type',
    'Order ID': 'project_id',
    'residual_solvents': 'residual_solvents_status',
    'sample_size': 'sample_size',
    'Sample Wt': 'sample_weight',
    'total_sample_weight_g': 'sample_weight',
    'product_density': 'sample_weight',
    'Product Density': 'sample_weight',
    'primary_sample': 'sample_weight',
    'Density': 'sample_weight',
    'increment_g': 'sample_weight_used',
    'sampling_method': 'sampling_method',
    'Serving Size': 'serving_size',
    'Servings': 'servings_per_package',
    'overall': 'status',
    'overall_batch': 'status',
    'result-pf': 'status',
    'Status': 'status',
    'level': 'status',
    'status': 'status',
    'sum_of_cannabinoids': 'sum_of_cannabinoids',
    'total_cbc': 'total_cbc',
    'total_cbd': 'total_cbd',
    'total_cbdv': 'total_cbdv',
    'total_cbg': 'total_cbg',
    'total_terpenoids': 'total_terpenes',
    'total_terpenoids_percent': 'total_terpenes',
    'Total Terpenes (%)': 'total_terpenes',
    'total_thc': 'total_thc',
    'total_thcv': 'total_thcv',
    '% Test': 'value',
    'PPM': 'value',
    'PPM (ug/g)': 'value',
    'PPM (ug/kg)': 'value',
    'PPB (ug/g)': 'value',
    'PPB (ug/kg)': 'value',
    'Threshold': 'value',
    'result-percent': 'value',
    'Findings': 'value',
    '%': 'value',
    'result': 'value',
    'value': 'value',
    'cannabinoids': 'cannabinoids_status',
    'water_activity': 'water_activity_status',
    'terpene_analysis_add_on': 'terpenes_status',
    'microbials': 'microbials_status',
    'metals': 'heavy_metals_status',
    'Sampling Method/SOP': 'sampling_method',
    'Batch Size': 'batch_size',
    'Sample Size': 'sample_size',
    'Date Sampled': 'date_sampled',
    'Date Received': 'date_received',
    'total_batch': 'batch_size',
    'total_cannabinoids': 'total_cannabinoids',
    'Total Cannabinoids (%)': 'total_cannabinoids',
    'Total Calculated d9-THC (%)': 'total_thc',
    'Total Calculated CBD (%)': 'total_cbd',
    'batch_size_sample_size': 'batch_size',
    'collected_received': 'date_collected',
    'lloq': 'loq',
    'Anresco ID': 'lab_id',
    'Lot/Batch Number': 'batch_number',
    'cannabinoid_pro_le': 'cannabinoids_status',
    'pesticide_residue_screen': 'pesticides_status',
    'microbiological_screen': 'microbes_status',
    'heavy_metal_screen': 'heavy_metals_status',
    'mycotoxin_screen': 'mycotoxins_status',
    'other_analyses': 'moisture_status',
    'total_active_cannabinoids': 'total_cannabinoids',
    'batch_no': 'batch_number',
    'batch_size_lbs': 'batch_size',
    'cannabinoid_method': 'cannabinoids_method',
    'foreign_matter_status_method': 'foreign_matter_method',
    'heavy_metal_method': 'heavy_metals_method',
    'heavy_metals_status_status': 'heavy_metals_status',
    'moisture_content_method': 'moisture_method',
    'mycotoxin_method': 'mycotoxins_method',
    'mycotoxins_status_status': 'mycotoxins_status',
    'pesticide_method': 'pesticides_method',
    'pesticides_status_status': 'pesticides_status',
    'terpenoid_method': 'terpenes_method',
    'total_a_atoxins': 'total_aflatoxins',
    'water_activity_status_method': 'water_activity_method',
    'water_activity_status_status': 'water_activity_status',
    'moisture_content_status': 'moisture_status',
    'percent_moisture_status': 'moisture_status',
    'total_d_9_thc_mg_per_package': 'total_thc_mg_per_package'
}

# A map of standard units by analysis to use when no units are obtainable.
STANDARD_UNITS = {
    'cannabinoids': 'percent',
    'foreign_matter': 'percent',
    'heavy_metals': 'μg/g',
    'microbes': 'CFU/g',
    'moisture': 'percent',
    'mycotoxins': 'μg/g',
    'pesticides': 'μg/g',
    'terpenes': 'percent',
    'water_activity': 'aW',
}

# A map of encountered product types to their standardized product type.
PRODUCT_TYPES = {
    'Flower & Buds': 'flower',
    'Immature Plants': 'immature_plant',
    'Concentrate (Non-Solvent Based) (Count-Volume)': 'non_solvent_concentrate',
    'Concentrate (Non-Solvent Based) (Count-Weight)': 'non_solvent_concentrate',
    'Concentrate (Weight Based)': 'concentrate',
    'Edibles (Count-Volume)': 'solid_edible',
    'Edibles (Count-Weight)': 'solid_edible',
    'Extracts (Solvent Based) (Count-Volume)': 'concentrate',
    'Extracts (Solvent Based) (Count-Weight)': 'concentrate',
    'Kief': 'kief',
    'Mature Plants': 'mature_plant',
    'Metered Dose Nasal Spray Products': 'nasal_spray',
    'MMJ Waste': 'waste',
    'Pre-Roll (Flower Only)': 'pre_roll',
    'Pre-Roll (Infused)': 'infused_pre_roll',
    'Pressurized Metered Dose Inhaler Products': 'nasal_spray',
    'Rectal/Vaginal Administration Products (Count-Volume)': 'suppository',
    'Rectal/Vaginal Administration Products (Count-Weight)': 'suppository',
    'Seeds': 'seeds',
    'Shake/Trim': 'shake',
    'Shake/Trim (by Strain)': 'shake',
    'Tinctures (Count-Volume)': 'tincture',
    'Tinctures (Count-Weight)': 'tincture',
    'Topicals (Count-Volume)': 'topical',
    'Topicals (Count-Weight)': 'topical',
    'Transdermal Patches': 'transdermal',
    'Vape Cartridges': 'vape_cartridge',
    'Whole Wet Plant': 'plant',
    'Buds': 'flower',
    'Infused': 'solid_edible',
    'InfusedEdible': 'solid_edible',
    'Infused Liquid': 'liquid_edible',
}

# A map of encountered strains to their standardized strain name.
STRAINS = {
    'Cannatonic #4': 'Cannatonic',
    'Cannatonic #4 - RP': 'Cannatonic',
    'GSC': 'Girl Scout Cookies',
    'Gorilla Glue #4': 'Gorilla Glue',
    'GG': 'Gorilla Glue',
    'GG4': 'Gorilla Glue',
    'GG #4': 'Gorilla Glue',
    'GG#4': 'Gorilla Glue',
    'GG 4': 'Gorilla Glue',
    'Gorilla Glue 4': 'Gorilla Glue',
    'Gorilla Glue #4 - 1': 'Gorilla Glue',
    'GDP': 'Grand Daddy Purple',
    'Granddaddy Purple': 'Grand Daddy Purple',
    'SFV': 'SFV OG',
}

# Standard value codings.
CODINGS = {
    'ND': 0.000000001,
    'No detection in 1 gram': 0.000000001,
    'Negative/1g': 0.000000001,
    'PASS': 0.000000001,
    'LOD': 0.00000001,
    '<LOD': 0.00000001,
    '< LOD': 0.00000001,
    '<LOQ': 0.0000001,
    '< LOQ': 0.0000001,
    '<LLoQ': 0.0000001,
    '<LLOQ': 0.0000001,
    'BLQ': 0.0000001,
    '<LLoa': 0.0000001,
    '≥ LOD': 10_001,
    'NR': None,
    'N/A': None,
    'na': None,
    'NT': None,
}

# Cannabinoid decarboxylation rate.
DECARB = 0.877 # Source: <https://www.conflabs.com/why-0-877/>

# Default headers to use for HTTP requests, because we are AI and should not be treated as a bot.
DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'}

# Random characters to use in password generation.
RANDOM_STRING_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# A map of state abbreviations to state names.
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

# A map of state names to state abbreviations.
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

# A map of state abbreviations to timezone.
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


if __name__ == '__main__':

    from cannlytics.utils.utils import snake_case

    # Sort a given dictionary and remove duplicate fields.
    # Also Add snake_case key if not already present.
    # This is useful when adding new fields to a constant in development.
    x = {}
    for k, v in STANDARD_FIELDS.items():
        if k not in x.keys():
            x[k] = v
            x[snake_case(k)] = v
    x = {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
    print(x)
