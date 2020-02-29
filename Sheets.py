import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from Order import *
from googleapiclient import discovery
# import Order
# from datetime import datetime
class Sheets:
    def __init__(self, new_order : Order):
        # storing the order
        self._myOrder : Order = new_order
        # this specifies the scope for the actual google sheet
        self._scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        #get authentification for working with the google sheet
        self._creds= ServiceAccountCredentials.from_json_keyfile_name("doordash_creds.json",self._scope)
        #checking if we have correct authentification
        self._client : gspread.Client = gspread.authorize(self._creds)
        # getting access to the sheet
        self._sheet = self._client.open("Doordash_Records").sheet1
        #storing the data within the sheet
        self._data = self._sheet.get_all_records()
        #going to add the order

        self.add()

    def add(self):
        #output is going to store the row which we are going to append to the sheet
        output=[]
        #stores the date of transaction
        date : str= self.format_date()
        output.append(date)
        #Stores restaraunt name
        restaurant : str= self._myOrder.getRestaurant()
        output.append(restaurant)
        #gets all the people who ordered and money spent
        people : list[Member] = self._myOrder.getMembers()

        #adding value of total
        output.append(self._myOrder.getTotal())

        #this is going to be used to get all names in the sheet by retrieving the header row in the sheet
        headings : list[str] = self._sheet.row_values(1)
        #removing the date, transaction and total headings
        del headings[0:3]
        # print(headings)

        # this is a map from member name to amount spent
        person2Total : dict[str : float]= {}
        #initializing values per person to 0
        for name in headings:
            person2Total[name]=0

        for person in people:
            name : str = person.getName()
            #error checking
            if name not in person2Total:
                # getting total
                person2Total[name]: str= person.getTotal()
                #adding name to the sheet
                self._sheet.update_cell(1, 3+ len(person2Total),name)
                #print(name, "is not a member")
            else:
                #adding the value spent by the person to map
                person2Total[name] : str =person.getTotal()
        #getting only the values of amount spent per person
        person2Total_values : list[float]= person2Total.values()
        #putting totals per person in output
        for value in person2Total_values:
            output.append(value)
        #also adding info about the overall order total

        #adding to the sheet


        self._sheet.insert_row(output,2)

        # self.format()



    def remove(self, initial: int, end:int):
        for row in range(initial,end+1):
            self._sheet.delete_row(row)
        print("size=",self.getSize())
    def getSize(self):
        return len(self._data)

    def format_date(self):
        # date: str = ""
        # date += str(self._myOrder.getDate().month)
        # date += "/"
        # date += str(self._myOrder.getDate().date())
        # date += "/"
        # date+= str(self._myOrder.getDate().year)


        date= str(self._myOrder.getDate().date()).replace("-","/")
        #return self._myOrder.getDate()
        return date


    def format(self):
        service = discovery.build('sheets', 'v4', credentials=self._creds)
        
        # The spreadsheet to apply the updates to.
        spreadsheet_id = "https://docs.google.com/spreadsheets/d/1uRxor97NVAKBnljaOHr8SiJJfzN2UzQpUK8nkOTIQ5o/edit#gid=0" # TODO: Update placeholder value.

        batch_update_spreadsheet_request_body = {
            # A list of updates to apply to the spreadsheet.
            # Requests will be applied in the order they are specified.
            # If any request is not valid, no requests will be applied.

            'requests': [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId" : spreadsheet_id,
                            "startRowIndex": 1,
                            "endRowIndex": 1000,
                            "startColumnIndex": 0,
                            "endColumnIndex": 1
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "numberFormat": {
                                    "type": "DATE",
                                    "pattern": "yyyy-mm-dd"
                                }
                            }
                        },
                        "fields": "userEnteredFormat.numberFormat"
                    }
                }

            ],  # TODO: Update placeholder value.

            # TODO: Add desired entries to the request body.
        }

        request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                     body=batch_update_spreadsheet_request_body)
        response = request.execute()

        # TODO: Change code below to process the `response` dict:

        pprint(response)






