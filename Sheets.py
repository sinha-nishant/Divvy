import gspread, os, json
from oauth2client.service_account import ServiceAccountCredentials
from Order import *
from typing import Dict

class Sheets:
    def __init__(self):
        # this specifies the scope for the actual google sheet
        self._scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                       "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        # get authentication for working with the google sheet
        self._creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(os.environ.get("SHEET_CREDS")), self._scope)
        # checking if we have correct authentication
        self._client: gspread.Client = gspread.authorize(self._creds)

        self._order_record = self._client.open_by_key("1uRxor97NVAKBnljaOHr8SiJJfzN2UzQpUK8nkOTIQ5o").get_worksheet(0)
        self._balances = self._client.open_by_key("1uRxor97NVAKBnljaOHr8SiJJfzN2UzQpUK8nkOTIQ5o").get_worksheet(1)

    def add(self, new_order):
        # storing the order
        order = new_order
        # used to store value of updated balances after incorporating new order
        updated_balance: dict[str: float] = {}
        if not order:
            print('order doesnt exist')
        else:
            # output is going to store the row which we are going to append to the sheet
            output: list = []
            # stores the date of transaction
            date : str = str(order.getDate().date()).replace("-", "/")
            output.append(date)
            # Stores restaurant name
            restaurant: str = order.getRestaurant()
            output.append(restaurant)
            # gets all the people who ordered and money spent
            members: List[Member] = order.getMembers()

            # adding value of total
            output.append(order.getTotal())

            # this is going to be used to get all names in the sheet by retrieving the header row in the sheet
            headings: List[str] = self._order_record.row_values(1)[3:]

            memberToTotal = dict()
            for member in members:
                memberToTotal[member.getName()] = member.getTotal()

            new_member_names = []
            for key in memberToTotal:
                if key not in headings:
                    new_member_names.append(key)

            if new_member_names:
                new_member_range : List[gspread.Cell] = self._order_record.range(1, 3 + len(headings) + 1, 1, 3 + len(headings) + len(new_member_names))
                for i, cell in enumerate(new_member_range):
                    cell.value = new_member_names[i]
                self._order_record.update_cells(new_member_range)

            headings.extend(new_member_names)
            for heading in headings:
                if heading in memberToTotal.keys():
                    output.append(memberToTotal[heading])
                else:
                    output.append(0)

            self._order_record.insert_row(output, 2, value_input_option = 'USER_ENTERED')

            # Now need to update balances
            if new_member_names:
                new_member_range: List[gspread.Cell] = self._balances.range(1, len(headings) - len(new_member_names) + 1, 1, len(headings))
                for i, cell in enumerate(new_member_range):
                    cell.value = new_member_names[i]
                self._balances.update_cells(new_member_range)

            balance_range : List[gspread.Cell] = self._balances.range(2, 1, 2, len(headings))
            for balance in balance_range:
                if not balance.value:
                    balance.value = 0

            balance_dict : Dict[str : gspread.Cell] = dict()
            updated_cells : List[gspread.Cell] = list()
            for i, heading in enumerate(headings):
                balance_dict[heading] = balance_range[i]

            for key in memberToTotal:
                print(balance_dict[key].value)
                if balance_dict[key].value:
                    balance_dict[key].value = float(balance_dict[key].value) + memberToTotal[key]
                else:
                    balance_dict[key].value = memberToTotal[key]
                updated_cells.append(balance_dict[key])

            self._balances.update_cells(balance_dict.values(), value_input_option = "USER_ENTERED")

    def remove(self, initial: int, end: int):
        for row in range(initial, end + 1):
            self._order_record.delete_row(row)

    def withdraw(self, name: str, value: float):
        cell_list = self._balances.findall(name.title())
        if len(cell_list) == 0:
            print('Name does not exist')
        else:
            row = cell_list[0].row
            col = cell_list[0].col
            initial_val = float(self._balances.cell(row + 1, col).value)
            self._balances.update_cell(row + 1, col, initial_val - value)