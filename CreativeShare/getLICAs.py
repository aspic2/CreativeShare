#!/usr/bin/python
#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example gets all line item creative associations for a given line item.
"""

# Import appropriate modules from the client library.
from googleads import dfp
from Spreadsheet import Spreadsheet
from os import getcwd


source_wb = getcwd() + "\\SourceFiles\\testsource.xlsx"

#LINE_ITEM_ID = '44461949'  #multiple creatives, different statuses
#LINE_ITEM_ID = '305376749'  #one creative
#LINE_ITEM_ID = '23'  #one creative

def main(client):
    #Initialize workbooks
    old_workbook = Spreadsheet('old_workbook', False, source_wb)
    #new_workbook = Spreadsheet('LICAResults', True)

    LIDSets = old_workbook.read()
    sourceLIDs = []

    for LIDSet in LIDSets:
        try:
            oldval = int(LIDSet[0])
            newval = int(LIDSet[2])
            sourceLIDs.append(oldval)
        except:
            continue


    sourceLIDs = tuple(sourceLIDs)
    sourceLIDs = str(sourceLIDs)

    # Initialize appropriate service.
    lica_service = client.GetService(
        'LineItemCreativeAssociationService', version='v201702')
    #query = 'WHERE lineItemId = ' + LINE_ITEM_ID # + ' AND status != INACTIVE'
    #query = ('WHERE lineItemId IN ' + sourceLIDs)
    #query = 'WHERE lineItemId IN (249023069, 249022589, 250310789, 229856549, 281174909, 275819069)'
    #query = 'WHERE lineItemId IN (249023069)'
    query = 'WHERE lineItemId = 305376749'     #one creative
    #query = 'WHERE lineItemID = 44461949'       #multiple creatives
    print("Here is my query:\n" + query)
    # Create a statement to select line item creative associations.
    statement = dfp.FilterStatement(query)

    # Retrieve a small amount of line item creative associations at a time, paging
    # through until all line item creative associations have been retrieved.
    newLICAs = []
    while True:
        response = lica_service.getLineItemCreativeAssociationsByStatement(
            statement.ToStatement())
        if 'results' in response:
            #print(response)
            for lica in response['results']:
                if lica['status'] != 'ACTIVE':
                    continue
                # Print out some information for each line item creative association.
                if 'creativeSetId' in lica:
                    #print("LICA with line item ID '%s', creative set ID '%s' and" "status '%s' was found." %
                    #    (lica['lineItemId'], lica['creativeSetId'], lica['status']))
                    for creative in 'creativeSetId':
                        token = (lica['lineItemId'], lica['creativeId'])
                        newLICAs.append(token)
                else:
                    #print("Line item creative association with line item ID '%d' and "
                    #    "creative ID '%d' was found.\n" %
                    #    (lica['lineItemId'], lica['creativeId']))
                    token = (lica['lineItemId'], lica['creativeId'])
                    newLICAs.append(token)
            statement.offset += dfp.SUGGESTED_PAGE_LIMIT
        else:
            break

    print('\nNumber of results found: %s' % response['totalResultSetSize'])
    print(newLICAs)



if __name__ == '__main__':
    # Initialize client object.
    dfp_client = dfp.DfpClient.LoadFromStorage()
    main(dfp_client)
