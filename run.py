import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('x_coffee')

amount = 0
drinks = [0,0,0]

def main():
    print()
 
def main_menu():
    amount = 0
    drinks = [0,0,0]
    print('X Coffee')
    print('Select the menu')
    print('Type (1) for Sales')
    print('Type (2) for Stock')
    print('Type (3) for Closing count')
    print('Type (4) for Exit')
    print()
    selector = input('Typed: ')
    return selector
 
def wrong_selection():
    print('Wrong selection, try again')
    print()
    return True

def item_added(value, amount):
    if value == 1:
        drinks[0] = drinks[0] + 1
        amount = amount + 3
        sales_menu(drinks, amount)
    elif value == 2:
        drinks[1] = drinks[1] + 1
        amount = amount + 4
        sales_menu(drinks, amount)
    elif value == 3:
        drinks[2] = drinks[2] + 1
        amount = amount + 4
        sales_menu(drinks, amount)
    elif value == 4:
        print()
        print(f'Order sent & {amount} paid')
        print()
        main()
    else:
        wrong_selection()
        sales_menu(drinks, amount)
 
def sales_menu(drinks, amount):
    print('Sales Menu')
    print()
    print(f'{drinks[0]} Americano in Cart, Type (1) to add')
    print(f'{drinks[1]} Cuppuccino in cart, Type (2) to add')
    print(f'{drinks[2]} Latte in cart, Type (3) to add')
    print()
    print(f'Type (4) to Oder send & bill €{amount}.')
    selector = input('Typed: ')
    item_added(int(selector), amount)

while True:
    main()
    selector = main_menu()
    
    if selector == '1':        
        sales_menu(drinks, amount)            
    elif selector == '2':
        print('Stock Menu')
    elif selector == '3':
        print('End of the day count')
    elif selector == '4':
        print('Exit')
        break
    else:
        wrong_selection()
