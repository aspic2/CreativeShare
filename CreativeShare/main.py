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
        source_wb = getcwd() + "\\SourceFiles\\11998_LIDSheet_first2.xlsm"
        old_workbook = Spreadsheet('old_workbook', False, source_wb)
        wb_data = old_workbook.read()
        dfp = DFPMethods()


        LIDSets = Helper.return_LID_sets(wb_data)
        sourceLIDs = Helper.return_source_LIDs(LIDSets)
#        targetLIDs = Helper.return_target_LIDs(LIDSets)
#        target_LID_slots = dfp.getLineSizes(targetLIDs)
        oldLICAs = dfp.getLICAs(sourceLIDs)

        trafficked_LIDs = dfp.createLICAs(LIDSets, oldLICAs)
        print("Here are the failed LIDs, if any:\n")
        for LID in LIDSets:
            if LID[1] not in trafficked_LIDs:
                dfp.failed_lines.append(LID[1])
        print(dfp.failed_lines)
        dfp.activateLineItems(trafficked_LIDs)




if __name__ == '__main__':
    CreativeShare.main()
