# Import appropriate modules from the client library.
from googleads import dfp


def main(client):
    # Initialize appropriate service.
    line_item_service = client.GetService('LineItemService', version='v201702')
    query = 'WHERE id = :id'
    values = [
      {'key': 'id',
       'value': {
           'xsi_type': 'NumberValue',
           'value': '291270989'
       }},
    ]
    # Create a statement to select line items.
    statement = dfp.FilterStatement(query, values)

    # Retrieve a small amount of line items at a time, paging
    # through until all line items have been retrieved.
    while True:
        response = line_item_service.getLineItemsByStatement(
        statement.ToStatement())
        if 'results' in response:
            for line_item in response['results']:
                creativePlaceholders = line_item['creativePlaceholders']
                size = creativePlaceholders[0]
            # Print out some information for each line item.
                print('Line Item ID "%d"\nSize = %s\n' %
                (line_item['id'], size))
            statement.offset += dfp.SUGGESTED_PAGE_LIMIT
        else:
            break

    print('\nNumber of results found: %s' % response['totalResultSetSize'])


if __name__ == '__main__':
  # Initialize client object.
  dfp_client = dfp.DfpClient.LoadFromStorage()
  main(dfp_client)
