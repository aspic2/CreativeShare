#coding equivalent of sratch paper.

from os import getcwd
from Spreadsheet import Spreadsheet

source_wb = getcwd() + "\\SourceFiles\\testsource.xlsx"

old_workbook = Spreadsheet('old_workbook', False, source_wb)
#new_workbook = Spreadsheet('LICAResults', True)

LIDSets = old_workbook.read()
source_LIDs = []

for LIDSet in LIDSets:
    try:
        oldval = int(LIDSet[0])
        newval = int(LIDSet[2])
    except:
        continue
    source_LIDs.append(oldval)

print("Here is each value in source_LIDs:")
for value in (source_LIDs):
    print(value)

source_LIDs = tuple(source_LIDs)
print("\nHere they are as tuples:")
print(source_LIDs)

print("\nAnd now a string:")
source_LIDs = str(source_LIDs)
print(source_LIDs)
