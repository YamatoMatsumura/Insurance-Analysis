import csv
import pandas as pd
import re

Names_row = []
Split_name = []
Full_name = []

Master_File = open("Master CSV File.csv", "r")
Master_File_read = csv.reader(Master_File)

#Blue Cross Blue Shield Info
#split names into first and last
for row in Master_File_read:
    Names_row.append(row[2])
#-5 because white space at bottom
for x in range(1, len(Names_row) - 5):
    Names = Names_row[x]
    Split_name = (Names.rsplit(" ", 1))
    #check for no middle initial
    res = any(bool(re.search(r"\s", ele)) for ele in Split_name)
    if res == True:
        Full_name.append(Split_name[0])
    else:
        Full_name.append(Names)
#make into csv and take out white space
DFFull_name = pd.DataFrame(Full_name, columns = ["Full Name"])
DFFull_name["Full Name"] = DFFull_name["Full Name"].str.replace(" ", "")
DFFull_name.to_csv("Blue Name")
Coverage = pd.read_csv("Master CSV File.csv", usecols = ["Coverage"])
x = pd.read_csv("Blue Name")
x = x.join(Coverage["Coverage"], how = "right")
x.to_csv("Blue Name")
Master_File.close()

#Off-site on-site info
File1 = pd.read_csv("Compare CSV File 1.csv", usecols = ["Last", "First", "Plan"])
DFile1 = File1.dropna(how = "all")
File2 = pd.read_csv("Compare CSV File 2.csv", usecols = ["Last", "First", "Plan"])
DFile2 = File2.dropna(how = "all")

pd.concat([DFile1, DFile2]).to_csv("Combined Compare CSV File", index = False)
Temp_File = pd.read_csv("Combined Compare CSV File")
for index, row in Temp_File.iterrows():
    Temp_File["Full Name"] = (Temp_File["Last"] + ", " + Temp_File["First"])

#all upper case, remove non names and white space
Temp_File["Full Name"] = Temp_File["Full Name"].str.upper()
Temp_File = Temp_File[Temp_File["Full Name"].str.contains("EMPLOYEE|SPOUSE|BCBS|FAMILY|TOTAL") == False]
Temp_File["Full Name"] = Temp_File["Full Name"].str.replace(" ", "")
#Format plan/coverage correctly
Temp_File["Plan"] = Temp_File["Plan"].replace({"E" : "EMP", "E+C" : "EMP+C", "E+F": "EMP+F", "E+S" : "EMP+S"})
#export to csv
Temp_File[["Plan"] + ["Full Name"]].to_csv("Off On Site Name + Plan")

Offon_siteN = set(pd.read_csv("Off On Site Name + Plan", index_col = False, header = None)[2])
Blue_crossN = set(pd.read_csv("Blue Name", index_col = False, header = None)[2])
Offon_siteC = set(pd.read_csv("Off On Site Name + Plan", index_col = False, header = None)[1])
Blue_CrossC = set(pd.read_csv("Blue Name", index_col = False, header = None)[3])

print("Not on Bcbs file: ", Offon_siteN - Blue_crossN)
print("\n")
print("Not on off/on site file: ", Blue_crossN -  Offon_siteN)
print("\n")
print("Plan/coverage wrong: ", Offon_siteC - Blue_CrossC)
