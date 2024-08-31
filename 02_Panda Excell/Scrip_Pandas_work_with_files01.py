#Install openpyxl for read excell files (pip3 install openpyxl --user)
import numpy as np
import pandas as pd
from matplotlib import pyplot as pltpy

print("Python and Pandas Tutorial:")
print("Work with files 01")

excel_data_df = pd.read_excel('M2_433_ASK_transciever.xlsx', sheet_name='Hoja1')
print(excel_data_df)

#Handling missing values

#Set null values of a a column to 0
excel_data_df.Qty = excel_data_df.Qty.fillna(0)
print(excel_data_df)

excel_data_df.COSTE_UNIDAD = excel_data_df.COSTE_UNIDAD.fillna(0)
print(excel_data_df)

# GET TOTAL COST
Cost_Unit = np.array(excel_data_df.COSTE_UNIDAD)
Qty = np.array(excel_data_df.Qty)

Cost_per_Element = Cost_Unit*Qty
Cost_per_Element = Cost_per_Element.astype(int)

print("Total cost =",Cost_per_Element.sum())
print("Num of elements =",Cost_per_Element.size)
print("Mean cost of element =",Cost_per_Element.mean())

pltpy.bar(x=excel_data_df.Device, height=Cost_per_Element)

pltpy.show()