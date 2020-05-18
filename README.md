# Food-COD-and-Eg-Calculator
Repository containing a macro-enabled excel workbook that calculates the chemical oxygen demand (COD) and gross energy (Eg) of food items. Calculator only works for Windows Excel and not Mac Excel due to a lack of available libraries for the Mac Excel. Additional python code to perform the calculation for lists of food items. 

## Getting Started

These instructions explain how to use both the Food COD and Eg Calculator Macro Workbook for individual food items and the python code for lists of food items. 


### How to use the calculator

1. Download and save the "Food COD and Eg Calculator Macro Workbook.xlsm" as a macro-enabled workbook locally on your computer.

2. Enable macro content within the calculator workbook. 

3. Make sure objects libraries within VBA are available. Directions on how to check if the libraries are available are within the "Get Object Library Directions.pdf" file. 

4. Go to the [USDA FoodData Central](https://fdc.nal.usda.gov/index.html) database website.

5. Search for desired food item and copy the "FDC ID" number.

6. Paste "FDC ID" number within the blue box on the "directions" tab within the calculator workbook.

7. Click the "RUN CALCULATOR" button. Results appear in the "results" tab for total COD and Eg calculations. An additional table for the carbohydrate, protein, and fat COD and Eg calculations are also available. 

### How to use the python code for lists of food items

1. Go to the [USDA FoodData Central](https://fdc.nal.usda.gov/index.html) database website.

2. Copy down a list of the "FDC ID" numbers for all desired food items and save as "FoodData_Central_ID_Lists.xlsx"  (Example provided in repository). 

3. Save locally the following files in the same folder as the food item list:
* Main_theoretical_Eg_COD_analysis.py
* Theoretical_Eg_COD_calculator_functions.py
* Nutrient_Literature_EmpFormula_EnthalpyComb.xlsx

4. Within a python evironment, run "Main_theoretical_Eg_COD_analysis.py". Results are .csv file. 


## Authors

* **Taylor Davis** 

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.


## References

1. Nutrient Data Laboratory (U.S), Consumer and Food Economics Institute (U.S.). USDA Food Composition Databases [Internet]. Riverdale, MD: USDA, Nutrient Data Laboratory, Agricultural Research Service; 1999 [cited 2019 Jul 9]. Available from: https://ndb.nal.usda.gov/ndb/

2. Linstrom PJ, Mallard MG. NIST Standard Reference Database Number 69 [Internet]. Gaithersburg MD: National Institute of Standards and Technology; 2018 [cited 2019 Jul 9]. Available from: https://webbook.nist.gov/chemistry/

3. Yao Y. Use of Carbohydrate , Protein and Fat to Characterise Wastewater in Terms of its Major Elemental Constituents and Energy. The University of Manchester; 2014. 
