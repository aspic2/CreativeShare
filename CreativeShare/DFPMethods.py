from googleads import dfp
from collections import defaultdict
import googleads
import logging

class DFPMethods(object):

    def __init__(self):
        self.client = dfp.DfpClient.LoadFromStorage()
        self.failed_lines = []

    #TODO: build method to find LIDs, provided a list of PLIDs (6 digit #)
    #TODO: at the beginning of Line Item names
    '''Method under construction'''
    def getLIDs(self):
        line_item_service = self.client.GetService('LineItemService')
        query = "WHERE name like '523092%'"
        statement = dfp.FilterStatement(query)
        PLIDs_LIDs = []
        while True:
            response = line_item_service.getLineItemsByStatement(statement.ToStatement(
            ))
            if 'results' in response:
                for line_item in response['results']:
                    # Print out some information for each line item.
                    print('Line item with ID "%d" and name "%s" was found.\n' %
                    (line_item['id'], line_item['name']))
                    #TODO: fix token range to stop right before
                    #TODO: first '-' or '_' in line_item['name']
                    token = (line_item['name'][0:6], line_item['id'])
                    PLIDs_LIDs.append(token)
                statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
                break
        print('\nNumber of results found: %s' % response['totalResultSetSize'])
        print(PLIDs_LIDs)

    def getLineSizes(self, LIDs):
        #TODO: get ONLY width and height from size aspect of Line_item
        LIDs = tuple(LIDs)
        LIDs = str(LIDs)
        query = ('WHERE id IN ' + LIDs)
        statement = dfp.FilterStatement(query)
        LIDs_and_sizes = defaultdict(list)
        line_item_service = self.client.GetService('LineItemService')
        while True:
            response = line_item_service.getLineItemsByStatement(
            statement.ToStatement())
            if 'results' in response:
                for line_item in response['results']:
                    if 'creativePlaceholders' in line_item:
                        for Placeholder in line_item['creativePlaceholders']:
                            LIDs_and_sizes[line_item['id']].append(
                            Placeholder['size'])
                    else:
                        LIDs_and_sizes[line_item['id']].append(line_item ['CreativePlaceholder'['size']])
                statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
                break
        return LIDs_and_sizes



    def getLICAs(self, oldLIDs):
        #oldLIDs must be in string format to work with query
        oldLIDs = tuple(oldLIDs)
        oldLIDs = str(oldLIDs)
        #TODO: adjust this to read single LIDs, too. Currently fails
        query = ('WHERE lineItemId IN ' + oldLIDs)
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
                        oldLICAs[lica['lineItemId']].append(
                        lica['creativeId'])
                statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
                break

        print('\nNumber of LICAs found: %s' % response['totalResultSetSize'])
        return oldLICAs


    def createLICAs(self, LID_sets, old_LICAs):
        licas = []
        #TODO: add logic to confirm that creative sizes match before adding
        #TODO: new LICAs to list. Currently crashes when sizes do not match

        #TODO: add logic to skip when LICA already exists. Currently crashes
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
        updatedLIDs = []
        if newLICAs:
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
        #TODO: add logic to accept single LID also. Currently crashes.
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


    """Ad Hoc Method: Pulls all currently active templates in DFP, as well
    as the trafficker-filled fields and help text info"""
    def getTemplates(self):
        newfile = open('test_file_write.txt', 'w')
        creative_template_service = self.client.GetService('CreativeTemplateService')
        query = "WHERE type = 'USER_DEFINED' AND status = 'ACTIVE'"
#        query = "WHERE id = 10126109"
        statement = dfp.FilterStatement(query)
        while True:
            count = 1
            response = creative_template_service.getCreativeTemplatesByStatement(
            statement.ToStatement())
            if 'results' in response:
                line_break = ("\n")
                for creative_template in response['results']:
                    title = ('%d. %s' %
                    (count, creative_template['name']))
                    newfile.write(title)
                    newfile.write(line_break)
#                    print('%d. %s' % (count, creative_template['name']))
                    if creative_template['description']:
                        template_description = ("\tDescription: %s " % creative_template['description'])
                        newfile.write(template_description)
                        newfile.write(line_break)
                        newfile.write(line_break)
#                        print("\tDescription: %s " % creative_template['description'])
                    if 'variables' in creative_template:
                        for variable in creative_template['variables']:
                            field_name = ("\tField: %s" % variable['label'])
                            newfile.write(field_name)
                            newfile.write(line_break)
    #                        print("\tField: %s" % variable['label'])
                            required_field = ("\tRequired Field: %s" % variable['isRequired'])
                            newfile.write(required_field)
                            newfile.write(line_break)
    #                        print("\tRequired Field: %s" % variable['isRequired'])
                            help_text = None
                            if 'description' in variable:
                                help_text = ("\tHelp Text: %s" % variable['description'])

    #                            print("\tHelp Text: %s\n" % variable['description'])
                            else:
                                help_text = ("\tHelp Text: None")
                            newfile.write(help_text)
                            newfile.write(line_break)

                            newfile.write(line_break)
                        newfile.write(line_break)
                        newfile.write(line_break)
#                        print("\n")

                    count += 1
#                print(response)
                statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
                break
        newfile.close()
        print('\nNumber of results found: %s' %
        response['totalResultSetSize'])
