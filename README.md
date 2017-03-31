# CreativeShare
Tool for Google's DFP API that bulk trafficks line items by using already uploaded creative.
CreativeShare works by matching up two Line Items by LIDs, taking active creatives from the source LID and 
associating the creatives with the target LID

# Requirements
This program is written in Python 3 and requires the following packages to run:
- googleads
- openpyxl

# Instructions
This program requires a few prep steps before it can run. 

1. Format your excel file with your LIDs to the following order:
  - Column A = Source LIDs (LIDs containing the creative already)
  - Column C = Target LIDs (LIDs you wish to traffic using creative from Column A LIDs)
  The other columns do not affect the tool.
  
2. Place your excel file in the sourcefiles folder.

3. Update the file path in CreativeShare/main.py to the name of your excel sheet.

Once this is complete, you can run the program at the command line. 

# License
This program was developed using Googleads' examples - https://github.com/googleads/googleads-python-lib/.
CreativeShare is available under Apache License.


