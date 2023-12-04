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
    
def main():
    print()
 
def main_menu():
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

def update_sales(drinks, amount):
    sales = [drinks[0],drinks[1],drinks[2],amount]
    print('updating data')
    daily_sales_worksheet = SHEET.worksheet('daily_sales')
    daily_sales_worksheet.append_row(sales)
    print('Sales Updated')
    
def update_stock(stock):
    print('Updating Stock')
    stock_worksheet = SHEET.worksheet('stock')
    stocks = stock_worksheet.get_all_values()
    last_stock = stocks[-1]    
    last_stock = [int(x) for x in last_stock]
    for x in range(len(last_stock)):
        last_stock[x] = last_stock[x] - stock[x]
    stock_worksheet.append_row(last_stock)
    print('Stock Updated')

def item_added(value, amount):
    if value == '1':
        drinks[0] = drinks[0] + 1
        amount = amount + 3
        stock[0] = stock[0] + 40
        stock[2] = stock[2] + 10
        sales_menu(drinks, amount)
    elif value == '2':
        drinks[1] = drinks[1] + 1
        amount = amount + 4
        stock[0] = stock[0] + 30
        stock[1] = stock[1] + 20
        stock[2] = stock[2] + 20
        sales_menu(drinks, amount)
    elif value == '3':
        drinks[2] = drinks[2] + 1
        amount = amount + 4
        stock[0] = stock[0] + 20
        stock[1] = stock[1] + 40
        stock[2] = stock[2] + 15
        sales_menu(drinks, amount)
    elif value == '4':
        print()
        print(f'Order sent & {amount} paid')
        update_sales(drinks, amount)
        update_stock(stock)
        print()
        main()
    else:
        wrong_selection()
        sales_menu(drinks, amount)
 
def sales_menu(drinks, amount):
    print('Sales Menu')
    print()
    print(f'{drinks[0]} Americano in Cart, Type (1) to add')
    print(f'{drinks[1]} Cappuccino in cart, Type (2) to add')
    print(f'{drinks[2]} Latte in cart, Type (3) to add')
    print()
    print(f'Type (4) to Oder send & bill €{amount}.')
    selector = input('Typed: ')
    item_added (selector, amount)

while True:
    main()
    amount = 0
    drinks = [0,0,0]
    stock = [0,0,0]
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
