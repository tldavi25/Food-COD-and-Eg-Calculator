# -*- coding: utf-8 -*-
"""
COD and Eg Calculator for Food Items
Author: Taylor Davis
Date created: 10/31/19
Date last edited: 10/31/19
"""

"""
API_extraction file

Purpose: to extract the desired data from the USDA database
"""
# Import required packages
import requests
import json
import pandas as pd


# =============================================================================
# Function to create a formatted string of the Python JSON object
# =============================================================================
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


# =============================================================================
# Function to extract the nutrient names and amounts for a food item using an api
# for the FoodCentral database.
# =============================================================================
def API_extraction(ID, API):
    # API request
    API_request = "https://api.nal.usda.gov/fdc/v1/food/"+ID+"?api_key=" + API 
    response = requests.get(API_request)

    food_descr = response.json()["description"]
    # Load nutrient data using json
    pass_times = response.json()["foodNutrients"]
    # Initialize lists for desired data        
    Nutrient_amounts = []
    Nutrient = []
    Nutrient_names = []
    
    # Loop through nutrient data to get amounts 
    for i in pass_times:
        try:
            amount = i["amount"]
            Nutrient_amounts.append(amount)
            nutrient = i["nutrient"]
            Nutrient.append(nutrient)
        except KeyError:
            pass
    
    # Loop through nutrient data to get names                
    for i in Nutrient:
        try:
            name = i["name"]
            Nutrient_names.append(name)
        except KeyError:
            pass
    
    # Make a dataframe of nutrient amounts
    DF_nut_wt = pd.DataFrame([Nutrient_amounts], columns=Nutrient_names)
    return food_descr,DF_nut_wt


# =============================================================================
# Function to update nutrients listed in columns of a dataframe
# =============================================================================
def update_nutDF(df_update,df_api,row):
    data = []
    for col in df_update.columns:
        try:
            data.append(df_api.loc[row,col])
        except:
            data.append(0.0)
    df_update = df_update.append(pd.Series(data,index=df_update.columns),ignore_index=True)
    df_update = df_update.div(100)
    return df_update


# =============================================================================
# Function to calculate COD from empirical formula
# =============================================================================
def calc_COD(C,H,O,N):
    # Calculate percentage grams of c,h,o, and n per total grams
    CP = C*100*12
    HP = H*100*1
    OP = O*100*16
    NP = N*100*14
    
    # Calculate intermediate availables
    T = CP / 12 + HP + OP / 16 + NP / 14
    n = CP / (12 * T)
    a = HP / T
    b = OP / (16 * T)
    c = NP / (14 * T)
    
    # Calculate COD
    COD = 16 * (2 * n + 0.5 * a - 1.5 * c - b) / (12 * n + a + 16 * b + 14 * c)
    return COD


# =============================================================================
# Function to calculate the empirical formula for each macronutrient
# =============================================================================
def calc_EmpForm(amt_df,lit_data):
    Clist = []
    Hlist = []
    Olist = []
    Nlist = []
    
    amt_df = amt_df.reset_index(drop="True")
    macKind = amt_df.loc[0,"Macronutrient type"]
    
    # calculate amount per macronutrient
    tot_amt = amt_df["Amount (g/g)"].sum()
    amt_df = amt_df["Amount (g/g)"].div(tot_amt)
    lit_data = lit_data.reset_index()
    
    # get moles of c, h, o, and n for each nutrient
    for index, row in amt_df.iteritems():
        Clist.append(row*lit_data.loc[index,"carbon"])
        Hlist.append(row*lit_data.loc[index,"hydrogen"])
        Olist.append(row*lit_data.loc[index,"oxygen"])
        Nlist.append(row*lit_data.loc[index,"nitrogen"])
    
    # sum for empirical formula
    if sum(Clist) > 0:
        ef = [sum(Clist)/sum(Clist), sum(Hlist)/sum(Clist), sum(Olist)/sum(Clist), sum(Nlist)/sum(Clist)]
    else:
        if macKind == "Carbohydrate":
            ef = [1, 1.826, 0.913, 0]
        elif macKind == "Protein":
            ef = [1, 2.063, 0.626, 0.282]
        elif macKind == "Fat":
            ef = [1, 1.838, 0.118, 0]
        else:
            print("No system in place for this macronutrient kind:  " + macKind)
    
    EmpForm = pd.DataFrame([ef], columns=["Carbon","Hydrogen","Oxygen","Nitrogen"])
    return EmpForm
        

# =============================================================================
# Function to calculate the macronutrient gross energy 
# =============================================================================
def calc_Eg(amt_df, lit_data):
    calincomp_df = []
    amt_df = amt_df.reset_index(drop="True")
    macKind = amt_df.loc[0,"Macronutrient type"]
    
    # calculate amount per macronutrient
    tot_amt = amt_df["Amount (g/g)"].sum()
    amt_df = amt_df["Amount (g/g)"].div(tot_amt)
    lit_data = lit_data.reset_index()
    
    # calculate energy for each nutrient
    for index, row in amt_df.iteritems():
        calincomp_df.append(row*lit_data.loc[index,"Δhc (kJ mol-1)"]/lit_data.loc[index,"MW (g mol-1)"])
    
    # sum for Eg value
    if sum(calincomp_df) > 0:
        H = sum(calincomp_df)*0.239
    else:
        if macKind == "Carbohydrate":
            H = 4.1
        elif macKind == "Protein":
            H = 4.3
        elif macKind == "Fat":
            H = 9.3
        else:
            print("No system in place for this macronutrient kind:  " + macKind)
    
    return H


# =============================================================================
# function to calculate everything
# =============================================================================
def calcitall(food_descr,ID,nut_lit_data,df_nut_wt):
# =============================================================================
# Step 1: intialize dataframes and setup specific parameters
# =============================================================================
    amt_df = pd.DataFrame(columns=nut_lit_data["Database ID"])
    mac_comp_df = pd.DataFrame(columns=["Water","Protein","Total lipid (fat)","Carbohydrate, by difference"])

    # get macronutrient fractions of total and nutrient fractions of total
    amt_df = update_nutDF(amt_df,df_nut_wt,0) # Unit: g/g total
    mac_comp_df = update_nutDF(mac_comp_df,df_nut_wt,0) # Unit: g/g total
    totdrywt = mac_comp_df.iloc[0,:].sum() - mac_comp_df.loc[0,"Water"]
    drywt_comp = mac_comp_df.div(totdrywt)
    
    # add macronutrient data info to amount dataframe
    amt_df = amt_df.T
    amt_df.rename(columns = {0 : "Amount (g/g)"}, inplace = True)
    amt_df["Macronutrient type"] = nut_lit_data["Macronutrient type"].values
    
# =============================================================================
# Step 2: Calculate COD for each macronutrient and food item overall
# =============================================================================
    # split lit data into macronutrient data
    carb_lit_data = nut_lit_data[nut_lit_data["Macronutrient type"]=="Carbohydrate"]
    prot_lit_data = nut_lit_data[nut_lit_data["Macronutrient type"]=="Protein"]
    fat_lit_data  = nut_lit_data[nut_lit_data["Macronutrient type"]=="Fat"]
    
    # split amt data into macronutrient data
    carb_amt_df = amt_df[amt_df["Macronutrient type"]=="Carbohydrate"]
    prot_amt_df = amt_df[amt_df["Macronutrient type"]=="Protein"]
    fat_amt_df  = amt_df[amt_df["Macronutrient type"]=="Fat"]
    
    # calculate empirical formulas for each macronutrient
    carbEF = calc_EmpForm(carb_amt_df, carb_lit_data) 
    protEF = calc_EmpForm(prot_amt_df, prot_lit_data)
    fatEF  = calc_EmpForm(fat_amt_df, fat_lit_data)
    
    # calculate the COD for each macronutrient (gCOD/g -dry wt.)
    carbCOD = calc_COD(carbEF.loc[0,"Carbon"],carbEF.loc[0,"Hydrogen"],carbEF.loc[0,"Oxygen"],carbEF.loc[0,"Nitrogen"])*drywt_comp.iloc[0,3]
    protCOD = calc_COD(protEF.loc[0,"Carbon"],protEF.loc[0,"Hydrogen"],protEF.loc[0,"Oxygen"],protEF.loc[0,"Nitrogen"])*drywt_comp.iloc[0,1]
    fatCOD  = calc_COD(fatEF.loc[0,"Carbon"],fatEF.loc[0,"Hydrogen"],fatEF.loc[0,"Oxygen"],fatEF.loc[0,"Nitrogen"])*drywt_comp.iloc[0,2]
    
    # calcualte overall COD (gCOD/g -dry wt.)
    totCOD  = carbCOD + protCOD + fatCOD
    
    
# =============================================================================
# Step 3: Calculate Eg for each macronutrient and food item overall
# =============================================================================
    # calculate the Eg for each macronutrient (kcal/g -dry wt.)
    carbEg = calc_Eg(carb_amt_df, carb_lit_data)*drywt_comp.iloc[0,3]
    protEg = calc_Eg(prot_amt_df, prot_lit_data)*drywt_comp.iloc[0,1]
    fatEg  = calc_Eg(fat_amt_df, fat_lit_data)*drywt_comp.iloc[0,2]
    
    # calcualte overall Eg (kcal/g - dry wt.)
    totEg  = carbEg + protEg + fatEg
    

# =============================================================================
# Step 4: Save all results for food item to a dataframe
# =============================================================================
    updateLIST = [food_descr, ID, totCOD, carbCOD, protCOD, fatCOD, totEg, carbEg, protEg, fatEg]
    return updateLIST

