import json
from googleapiclient.discovery import build

def get_values(credentials, sheet_id, sheet_range):
  service = build('sheets', 'v4', credentials=credentials)
   # Call the Sheets API
  sheet = service.spreadsheets()
  result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_range).execute()
  return result.get('values', [])

def get_party(party):
  return 'Democratic' if party.strip().lower() == 'd' else 'Republican'

def get_name(f_name, l_name): 
  return f'{f_name} {l_name}'

def get_member_name_and_district(value):
  array = value.split('-')
  name = array[1] 
  #check if hyphenated last name has been split
  if len(array) > 2: 
    name = f"{array[1]}-{array[2]}"
  return [array[0].strip(), name]

def filter_senate(data):
  return filter(lambda x: len(x) > 6 and x[5].lower().strip() == 'yes', data)

def add_council_member_info_to_branches_list(branches, council_members):
  new_member_list = []
  count = 0
  for branch in branches:
    found = False
    for member_to_add in council_members[1:]:
      last_name = branch['council_member'].split()
       #look for names that end with "Jr."
      if last_name[-1].lower == 'jr.':
        last_name = last_name[:-1]
      last_name = last_name[-2] if len(last_name) > 2 else last_name[-1]
      if member_to_add[4].lower().find(last_name.lower()) != -1:
        if (last_name.lower() == "la"):
          print(member_to_add, "LASTNAME LOWER", last_name.lower())
        record = {}
        record = branch
        council_name = f"{member_to_add[3].strip()} {member_to_add[4].strip()}"
        council_address = f"{member_to_add[21]} - {member_to_add[22]}, {member_to_add[23]}"
        # print(council_address, council_name)
        council_party = get_party(member_to_add[6]) 
        record['council_address'] = council_address
        record['council_party'] = council_party
        record['council_member'] == council_name
        new_member_list.append(record)
  return new_member_list

def add_assembly_member_info_to_branches_list(branch_data, assembly_members):
  pass


def add_senate_member_info_to_branches_list(branch_data, senate_members):
  new_member_list = []
  count = 0
  for branch in branch_data: 
    found = False
    for member_to_add in senate_members[1:]:
      if member_to_add[3].lower().find(branch['senate_member'].split()[-1].lower()) != -1:
        found = True
        senate_name = f"{member_to_add[2].strip()} {member_to_add[3].strip()}"
        senate_address = f"{member_to_add[20]} - {member_to_add[21]} - {member_to_add[22]}, {member_to_add[23]} {member_to_add[22]}"
        senate_party = get_party(member_to_add[8])
    if not found:
      print(branch["senate_member"])    
  
  print(count)

    
def wrangle_branches_and_members_into_json_file(values, file_name):
  branches_with_members = []
  for member in values[1:]:
    branch = {}
    branch["council_member"] = get_member_name_and_district(member[3] if member[3] else member[2])[1]
    branch["council_district"] = get_member_name_and_district(member[3] if member[3] else member[2])[0]
    branch["assembly_member"] = get_member_name_and_district(member[4])[1]
    branch["assembly_district"] = get_member_name_and_district(member[4])[0]
    branch["senate_member"] = get_member_name_and_district(member[6])[1]
    branch["senate_district"] = get_member_name_and_district(member[6])[0]
    branch["branch_name"]  = member[1]
    branch["borough"] = member[0]
    branches_with_members.append(branch)
  out_file = open(file_name, "w")
  json.dump(branches_with_members, out_file, indent=6)
  return branches_with_members

