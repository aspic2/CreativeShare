'''old form of CreativeShare Script. use main.py to run the updated
OO version of the script
'''
#CreativeShare script. Designed to share creative from one Line Item to another
# Import appropriate modules from the client library.
from googleads import dfp
from Spreadsheet import Spreadsheet
from os import getcwd
from collections import defaultdict
import googleads
import logging


source_wb = getcwd() + "\\SourceFiles\\testsource.xlsx"

#LINE_ITEM_ID = '44461949'  #multiple creatives, different statuses
#LINE_ITEM_ID = '305376749'  #one creative
#LINE_ITEM_ID = '23'  #one creative

def return_LID_sets():
    #Initialize workbooks
    old_workbook = Spreadsheet('old_workbook', False, source_wb)
    #new_workbook = Spreadsheet('LICAResults', True)

    wbdata = old_workbook.read()
    #dict pairs of oldLIDs and newLIDs. For matching values in createLICAs
    LIDSets = []
    for row in wbdata:
        try:
            oldval = int(row[0])
            newval = int(row[2])
            LIDSets.append((oldval, newval))
        except:
            continue
    print("Here is list LIDSets:")
    print(LIDSets)
    return LIDSets

def return_source_LIDs(sets):
    #oldLIDs as string for query
    sourceLIDs = []
    for group in sets:
            sourceLIDs.append(group[0])
    print("\nHere is list sourceLIDs:")
    print(sourceLIDs)
    sourceLIDs = tuple(sourceLIDs)
    sourceLIDs = str(sourceLIDs)
    return sourceLIDs

def main(client, query_end):
    # Initialize appropriate service.
    lica_service = client.GetService(
        'LineItemCreativeAssociationService', version='v201702')
    query = ('WHERE lineItemId IN ' + query_end)
    #query = 'WHERE lineItemId IN (249023069, 249022589, 250310789, 229856549, 281174909, 275819069)'
    #query = 'WHERE lineItemId IN (249023069)'
    #query = 'WHERE lineItemId = 305376749'     #one creative
    #query = 'WHERE lineItemID = 44461949'       #multiple creatives
    print("Here is my query:\n" + query)
    # Create a statement to select line item creative associations.
    statement = dfp.FilterStatement(query)

    # Retrieve a small amount of line item creative associations at a time, paging
    # through until all line item creative associations have been retrieved.
    oldLICAs = defaultdict(list)
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
                        oldLICAs[lica['lineItemId']].append(lica['creativeId'])
                        #token = (lica['lineItemId'], lica['creativeId'])
                        #oldLICAs.append(token)

                else:
                    #print("Line item creative association with line item ID '%d' and "
                    #    "creative ID '%d' was found.\n" %
                    #    (lica['lineItemId'], lica['creativeId']))
                    #token = (lica['lineItemId'], lica['creativeId'])
                    #oldLICAs.append(token)
                    oldLICAs[lica['lineItemId']].append(lica['creativeId'])
            statement.offset += dfp.SUGGESTED_PAGE_LIMIT
        else:
            break

    print('\nNumber of results found: %s' % response['totalResultSetSize'])
    print("Here is a default dict of oldLICAs:")
    print(oldLICAs)
    return oldLICAs

def createLICAs(client, LID_sets, old_LICAs):
    #logging.basicConfig(level=logging.INFO, format=googleads.util.LOGGER_FORMAT)
    #logging.getLogger('suds.transport').setLevel(logging.DEBUG)
    # Initialize appropriate service.
    lica_service = client.GetService('LineItemCreativeAssociationService',
    version='v201702')

    #testing licas
#    licas = [{'lineItemId': 321876629, 'creativeId': 117616760909},
#             {'lineItemId': 307238069, 'creativeId': 117644870909}]
    licas = []
    for LID in LID_sets:
        for value in old_LICAs[LID[0]]:
            creative_id = value
            line_item_id = LID[1]
            queryset = {'creativeId': creative_id,
                          'lineItemId': line_item_id}
            licas.append(queryset)


    print("Here are the new LID and Creative pairs, as variable licas:\n")
    print(licas)


    # Create the LICAs remotely.
    newLICAs = lica_service.createLineItemCreativeAssociations(licas)

    # Display results.
    if newLICAs:
        for lica in newLICAs:
            print('LICA with line item id \'%s\', creative id \'%s\', and '
            'status \'%s\' was created.' %
            (lica['lineItemId'], lica['creativeId'], lica['status']))
    else:
        print('No LICAs created.')



if __name__ == '__main__':
    # Initialize client object.
    dfp_client = dfp.DfpClient.LoadFromStorage()
    LID_sets = return_LID_sets()
    source_LIDs = return_source_LIDs(LID_sets)
    old_LICAs = main(dfp_client, source_LIDs)
    createLICAs(dfp_client, LID_sets, old_LICAs)
