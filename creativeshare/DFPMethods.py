#CreativeShare script. Designed to share creative from one Line Item to another
# Import appropriate modules from the client library.
from googleads import dfp
from collections import defaultdict
import googleads
import logging

class DFPMethods(object):

    def __init__(self):
        self.client = dfp.DfpClient.LoadFromStorage()

    def getLICAs(self, oldLIDs):
        #oldLIDs must be in string format to work with query
        oldLIDs = tuple(oldLIDs)
        oldLIDs = str(oldLIDs)
        query = ('WHERE lineItemId IN ' + oldLIDs)
        # Create a statement to select line item creative associations.
        statement = dfp.FilterStatement(query)
        # Retrieve a small amount of line item creative associations at a time, paging
        # through until all line item creative associations have been retrieved.
        oldLICAs = defaultdict(list)
        lica_service = self.client.GetService(
        'LineItemCreativeAssociationService', version='v201702')
        while True:
            response = lica_service.getLineItemCreativeAssociationsByStatement(
                statement.ToStatement())
            if 'results' in response:
                for lica in response['results']:
                    if lica['status'] != 'ACTIVE':
                        continue
                    if 'creativeSetId' in lica:
                        for creative in 'creativeSetId':
                            oldLICAs[lica['lineItemId']].append(
                            lica['creativeId'])
                    else:
                        oldLICAs[lica['lineItemId']].append(lica['creativeId'])
                statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
                break

        print('\nNumber of results found: %s' % response['totalResultSetSize'])
        return oldLICAs

    def createLICAs(self, LID_sets, old_LICAs):
        licas = []
        for LID in LID_sets:
            for value in old_LICAs[LID[0]]:
                creative_id = value
                line_item_id = LID[1]
                queryset = {'creativeId': creative_id,
                              'lineItemId': line_item_id}
                licas.append(queryset)
        lica_service = self.client.GetService(
        'LineItemCreativeAssociationService', version='v201702')
        # Create the LICAs remotely.
        newLICAs = lica_service.createLineItemCreativeAssociations(licas)
        # Display results.
        if newLICAs:
            updatedLIDs = []
            for lica in newLICAs:
                #print('LICA with line item id \'%s\', creative id \'%s\', and '
                #'status \'%s\' was created.' %
                #(lica['lineItemId'], lica['creativeId'], lica['status']))
                updatedLIDs.append(lica['lineItemId'])
        else:
            print('No LICAs created.')
        #remove duplicates
        updatedLIDs = list(set(updatedLIDs))
        return updatedLIDs


    def activateLineItems(self, newLIDs):
        newLIDs = tuple(newLIDs)
        newLIDs = str(newLIDs)
        values = [{'key': 'status','value': {'xsi_type': 'TextValue',
        'value': 'READY'}}]
        query = "WHERE NOT status = :status AND id IN " + newLIDs
        statement = dfp.FilterStatement(query, values)
        line_item_service = self.client.GetService(
        'LineItemService', version='v201702')
        line_items_activated = 0
        while True:
            response = line_item_service.getLineItemsByStatement(
            statement.ToStatement())
            if 'results' in response:
                result = line_item_service.performLineItemAction(
                    {'xsi_type': 'ActivateLineItems'}, statement.ToStatement())
                if result and int(result['numChanges']) > 0:
                    line_items_activated += int(result['numChanges'])
                statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
                break
        # Display results.
        if line_items_activated > 0:
            print('Number of line items activated: %s' % line_items_activated)
        else:
            print('No line items were activated.')
        #TODO Have activateLineItems return a list of successful activations
        #TODO Then print these to screen or export as excel file
