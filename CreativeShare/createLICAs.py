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

"""This code example creates new line item creative associations (LICAs) for an
existing line item and a set of creative ids.
To determine which LICAs exist, run get_all_licas.py.
"""


# Import appropriate modules from the client library.
from googleads import dfp
import googleads
import logging

#sample tuples of (oldLID, newLID)
LIDSets = [(249022589, 321876269),
(250310789, 321876629), (281174909, 321876269),
(275819069, 321876629)]

#sample dictionary containing oldLID: [associated_creatives]
oldLICAs = {250310789: [117616760909], 249022589: [117639032189],
281174909: [117629193149, 117629193389], 275819069: [117620642189],
249023069: [117641202509], 229856549: [117617567309]}

def createLICAs(client, LID_sets, old_LICAs):
    logging.basicConfig(level=logging.INFO, format=googleads.util.LOGGER_FORMAT)
    logging.getLogger('suds.transport').setLevel(logging.DEBUG)
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
  createLICAs(dfp_client, LIDSets, oldLICAs)
