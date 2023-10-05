import os, json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from data_utils import get_values, wrangle_branches_and_members_into_json_file, add_council_member_info_to_branches_list, add_senate_member_info_to_branches_list, add_assembly_member_info_to_branches_list, filter_senate
from file_utils import open_sheet

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "1N8k9O_GIzdlaXvSdjsTTatv1oYaSvM6ZgCd7FBdPjSI"

CITY_COUNCIL_RANGE = 'City Council!A1:Z52'
ASSEMBLY_RANGE = 'NY State Assembly!A1:Z61'
SENATE_RANGE = 'NY State Senate!A1:AB63'

def main():
    creds = open_sheet(creds=None, scopes=SCOPES)
    try:
        branches = get_values(creds, "1JhfGhCE7CYGNhUdmKFAgW3h_qq4pmIUWj0rKON1cbfM", "Master List!A3:G94" )
        council_officials = get_values(creds, SPREADSHEET_ID, CITY_COUNCIL_RANGE)
        senate_officials = get_values(creds, SPREADSHEET_ID, SENATE_RANGE)
       
        data = wrangle_branches_and_members_into_json_file(branches, "test.json")
      
        branches_data_with_council_info = add_council_member_info_to_branches_list(data ,council_officials)

        with open("test_council.json", "w") as f: 
            json.dump(branches_data_with_council_info, f, indent=6)

        # with open('council_and_branches.json') as f: 
        #     council_branches_json_data = json.load(f)
        #     data = add_senate_member_info_to_branches_list(council_branches_json_data, list(filter_senate(senate_officials)))
     
      
    except HttpError as err:
        print(err)
main()

