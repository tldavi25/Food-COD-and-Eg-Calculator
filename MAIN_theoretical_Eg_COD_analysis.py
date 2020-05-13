# -*- coding: utf-8 -*-
"""
Eg and COD data analysis in python
Author: Taylor Davis
Creation date: 3/5/2020
"""

# Load packages
import pandas as pd
from Theoretical_Eg_COD_calculator_functions import API_extraction
from Theoretical_Eg_COD_calculator_functions import calcitall


# =============================================================================
# Step 1: Get a list of food items and FDC IDs from spreadsheet
# =============================================================================
fdcIDlist_FILE = r"FoodData_Central_ID_Lists.xlsx"
COD_exp_data = pd.read_excel(fdcIDlist_FILE,sheet_name = "Training Set") # Unit: mgCOD/L


# =============================================================================
# Step 2: Load all literature data from spreadsheet
# =============================================================================
nutlit_FILE = r"Nutrient_Literature_EmpFormula_EnthalpyComb.xlsx"
nut_lit_data = pd.read_excel(nutlit_FILE,sheet_name = "Nutrient_lit_data") # Unit: C,H,O,N - mol, MW - g/mol, and delta_Hc - kJ/mol


# =============================================================================
# Step 3: Load nutrient amounts from API FoodCentral Database, calcualte Eg and
# COD things and save to dataframe
# =============================================================================
# API key
API = "imoqAI08iPXwN3pd4oKTHIHFqnODxnQqOcvr4wBh"

# initialize empty dataframe with lit list nutrients as columns
saveCOL = ["Food descr","FDC ID","Total COD (gCOD/g)","Carb COD (gCOD/g)",\
           "Prot COD (gCOD/g)","Fat COD (gCOD/g)","Total Eg (kcal/g)",\
           "Carb Eg (kcal/g)","Prot Eg (kcal/g)","Fat Eg (kcal/g)"]
FOOD_Eg_COD = pd.DataFrame(columns = saveCOL)

# loop through and calculate Eg and COD parameters for all food items
for x in range (0,len(COD_exp_data)):
    # use api extraction function to get data for the ID
    ID = str(COD_exp_data.loc[x,"FDC ID"])
    [food_descr,df_nut_wt] = API_extraction(ID, API)
    
    
    # calculate 
    updateLIST = calcitall(food_descr,ID,nut_lit_data,df_nut_wt)

    FOOD_Eg_COD = FOOD_Eg_COD.append(pd.Series(updateLIST, index = saveCOL), ignore_index = "True")
    del updateLIST


# =============================================================================
# Step 4: Send resulting dataframe to a csv 
# =============================================================================
FOOD_Eg_COD.to_csv(r"Results COD and Eg.csv")


