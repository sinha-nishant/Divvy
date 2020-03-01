import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from Order import *
from googleapiclient import discovery
# import Order
# from datetime import datetime
class Sheets:
    def __init__(self, new_order : Order = None):
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
        #self._ids= []

        self._test= None

        self._sheet = self._client.open("Doordash_Records").sheet1
        self._sh = self._client.open("Doordash_Records")

        #self._ids.append(self._sheet.id)
        #storing the data within the sheet
        self._data = self._sheet.get_all_records()
        #going to add the order

        #self.add()

    def add(self):
        #output is going to store the row which we are going to append to the sheet
        if(self._myOrder == None ):
            print('order doesnt exist')
            return
        output=[]
        #stores the date of transaction
        date : str = self.format_date()
        output.append(date)
        #Stores restaraunt name
        restaurant : str = self._myOrder.getRestaurant()
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
        person2Total : dict[str : float] = {}
        #initializing values per person to 0
        for name in headings:
            person2Total[name] = 0

        for person in people:
            name : str = person.getName()
            #error checking
            if name not in person2Total:
                # getting total
                person2Total[name]: str= person.getTotal()
                #adding name to the sheet
                self._sheet.update_cell(1, 3+ len(person2Total),name)
                self._sh.worksheets()[1].update_cell(1,len(person2Total), name)
                self._sh.worksheets()[1].update_cell(2, len(person2Total), 0)
                #print(name, "is not a member")

            else:
                #adding the value spent by the person to map
                person2Total[name] : str =person.getTotal()
        #getting only the values of amount spent per person
        person2Total_values : list[float]= person2Total.values()
        #putting totals per person in output
        index=1
        for value in person2Total_values:
            output.append(value)
            self._sh.worksheets()[1].update_cell(2,index,value+ float(self._sh.worksheets()[1].cell(2,index).value))
            index+=1
        #also adding info about the overall order total

        #adding to the sheet
        self._sheet.insert_row(output,2, value_input_option = 'USER_ENTERED')


    def remove(self, initial: int, end:int):
        for row in range(initial,end+1):
            self._sheet.delete_row(row)
        print("size=",self.getSize())
    def getSize(self):
        return len(self._data)

    def format_date(self):
        date = str(self._myOrder.getDate().date()).replace("-","/")
        return date

    def add_sheet(self, title: str):
        service = discovery.build('sheets', 'v4', credentials=self._creds)

        # The spreadsheet to apply the updates to.
        spreadsheet_id = '1uRxor97NVAKBnljaOHr8SiJJfzN2UzQpUK8nkOTIQ5o' # TODO: Update placeholder value.
        # print(spreadsheet_id)

        batch_update_spreadsheet_request_body = {
            # A list of updates to apply to the spreadsheet.
            # Requests will be applied in the order they are specified.
            # If any request is not valid, no requests will be applied.
            'requests': [
                {
                    "addSheet": {
                        "properties": {
                            "title": title,
                            "gridProperties": {
                                "rowCount": 1000,
                                "columnCount": 1000
                            },

                        }
                    }
                }




            ],  # TODO: Update placeholder value.

            # TODO: Add desired entries to the request body.
        }

        request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                     body=batch_update_spreadsheet_request_body)

        response = request.execute()
        print(response['replies'][0]['addSheet']['properties']['sheetId'])

    def create(self, name:str):
        gc = gspread.authorize(self._creds)
        sh = gc.create('Test')
        self._test= sh
        sh.share('mitraarj@usc.edu', perm_type='user', role='writer')
        return sh


    def get_all_sheets(self):
        return self._sh.worksheets()

    def withdraw(self, name :str, value : float):
        cell_list= self._sh.worksheets()[1].findall(name.title())
        if len(cell_list) == 0:
            print('Name does not exist')
            return
        row= cell_list[0].row
        col= cell_list[0].col
        initial_val= float(self._sh.worksheets()[1].cell( row +1 , col ).value)
        self._sh.worksheets()[1].update_cell(row+1,col,initial_val - value )

    def add_order(self,new_order):
            self._myOrder= new_order




