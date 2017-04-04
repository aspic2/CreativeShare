#main class. 1) Reads excel file for old LIDs (source) and new LIDs (target)
# 2) gets the Line Item Creative Associations for the source LIDs,
# 3) then adds a new association for the target LID
# 4) Activates all newly trafficked Line Items that are not in 'Ready' status

from DFPMethods import DFPMethods
from Helper import Helper
from Spreadsheet import Spreadsheet
from os import getcwd
import logging

#TODO: add list (set) of failed updates and reason for failure.
#TODO: add logic in each updating method to add to this list

class CreativeShare:

    def main():
        #update the filepath to the name of your workbook
        source_wb = getcwd() + "\\SourceFiles\\12733_Hyu CPO LIDs.xlsx"
        old_workbook = Spreadsheet('old_workbook', False, source_wb)
        wb_data = old_workbook.read()
        dfp = DFPMethods()


        LIDSets = Helper.return_LID_sets(wb_data)
        sourceLIDs = Helper.return_source_LIDs(LIDSets)
        oldLICAs = dfp.getLICAs(sourceLIDs)
        trafficked_LIDs = dfp.createLICAs(LIDSets, oldLICAs)
        print("createLICAs worked. Here are your trafficked_LIDs:\n")
        print(trafficked_LIDs)
        dfp.activateLineItems(trafficked_LIDs)



if __name__ == '__main__':
    CreativeShare.main()
