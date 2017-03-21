#!/usr/bin/python
#
# Copyright 2015 Google Inc. All Rights Reserved.
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

"""This code example activates all line items for the given order.
To be activated, line items need to be in the approved state and have at least
one creative associated with them. To approve line items, approve the order to
which they belong by running approve_orders.py. To create LICAs, run
create_licas.py. To determine which line items exist, run
get_all_line_items.py.
"""


# Import appropriate modules from the client library.
from googleads import dfp

# Set the id of the order to get line items from.
ORDER_ID = 573801869 #natl_Ford | New , order 12565


def main(client, order_id):
    # Initialize appropriate service.
    line_item_service = client.GetService('LineItemService', version='v201702')

    # Create query.
    values = [{'key': 'orderId', 'value': {'xsi_type': 'NumberValue',
        'value': order_id}},
        {'key': 'status','value': {'xsi_type': 'TextValue',
        'value': 'INACTIVE'}}]
    query = "WHERE orderId = :orderId AND status = :status"
    statement = dfp.FilterStatement(query, values)

    line_items_activated = 0

    # Get line items by statement.
    while True:
        response = line_item_service.getLineItemsByStatement(
        statement.ToStatement())
        if 'results' in response:
            for line_item in response['results']:
                print('Line item with id \'%s\', in order id \'%s\', and '
                    'named \'%s\' will be activated.' %
                    (line_item['id'], line_item['orderId'], line_item['name']))

                # Perform action.
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

if __name__ == '__main__':
    # Initialize client object.
    dfp_client = dfp.DfpClient.LoadFromStorage()
    main(dfp_client, ORDER_ID)
