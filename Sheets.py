import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from Order import *
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
        self._client = gspread.authorize(self._creds)
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
        #this is a map from member name to amount spent
        person2Total : dict[str : float]  = {'Nishant Sinha' : 0, 'Arjun Mitra' : 0, "Param Patel": 0}
        for person in people:
            name : str = person.getName()
            #error checking
            if name not in person2Total:
                print("this member doesnt exist")
                return
            else:
                #adding the value spent by the person to map
                person2Total[name] : str =person.getTotal()
        #getting only the values of amount spent per person
        person2Total_values : list[float]= person2Total.values()
        #putting totals per person in output
        for value in person2Total_values:
            output.append(value)
        #also adding info about the overall order total
        output.append(self._myOrder.getTotal())
        #adding to the sheet
        self._sheet.add_rows(output)




    def format_date(self):
        date: str = ""
        date += self._myOrder.getDate().month
        date += "/"
        date += self._myOrder.getDate().date()
        date += "/"
        date+= self._myOrder.getDate().year
        return date







