import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from Order import *
from googleapiclient import discovery

class Sheets:
    def __init__(self):
        # this specifies the scope for the actual google sheet
        self._scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        #get authentification for working with the google sheet
        self._creds= ServiceAccountCredentials.from_json_keyfile_name("doordash_creds.json",self._scope)
        #checking if we have correct authentification
        self._client : gspread.Client = gspread.authorize(self._creds)

        self._test= None

        self._sheet = self._client.open("Doordash_Records").sheet1
        self._sh = self._client.open("Doordash_Records")

        #storing the data within the sheet
        self._data = self._sheet.get_all_records()


    def add(self,order):

        # used to store value of updated balances after incorporating new order
        updated_balance : dict[str : float]= {}
        if(order == None ):
            print('order doesnt exist')
            return
        # output is going to store the row which we are going to append to the sheet
        output : list=[]
        #stores the date of transaction
        date : str = str(order.getDate().date()).replace("-", "/")
        output.append(date)
        #Stores restaraunt name
        restaurant : str = order.getRestaurant()
        output.append(restaurant)
        #gets all the people who ordered and money spent
        people : list[Member] = order.getMembers()

        #adding value of total
        output.append(order.getTotal())

        #this is going to be used to get all names in the sheet by retrieving the header row in the sheet
        headings : list[str] = self._sheet.row_values(1)[3:]

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


            else:
                #adding the value spent by the person to map
                person2Total[name] : str =person.getTotal()

        #getting only the values of amount spent per person

        person2Total_values : list[float]= person2Total.values()

        #putting totals per person in output
        index=1
        headings = self._sheet.row_values(1)[3:]
        for heading in headings:
            inside= False
            if heading not in person2Total:
                output.append(0)
            else:
                output.append(person2Total[heading])
                inside= True
            if inside:
                myCell = self._sh.worksheets()[1].find(heading)
                original_balance= float(self._sh.worksheets()[1].cell(myCell.row+1,myCell.col).value)
                self._sh.worksheets()[1].update_cell(myCell.row+1,myCell.col, original_balance + person2Total[heading])
            index+=1


        #adding to the sheet
        self._sheet.insert_row(output,2, value_input_option = 'USER_ENTERED')




    def remove(self, initial: int, end:int):
        for row in range(initial,end+1):
            self._sheet.delete_row(row)
        print("size=",self.getSize())

    def getSize(self):
        return len(self._data)





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





