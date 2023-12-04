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

def not_enough_stock():
    print()
    print('Not enough stock, please RESTOCK')
    print()

def check_stock():
    stock_worksheet = SHEET.worksheet('stock')
    stocks = stock_worksheet.get_all_values()
    if len(stocks) >=2:
        last_stock = stocks[-1]  
        last_stock = [int(x) for x in last_stock]
        return last_stock
    else:
        not_enough_stock()
        restock()

def update_sales(drinks, amount):
    sales = [drinks[0],drinks[1],drinks[2],amount]
    print('updating data')
    daily_sales_worksheet = SHEET.worksheet('daily_sales')
    daily_sales_worksheet.append_row(sales)
    print('Sales Updated')
    
def update_stock(stock):
    print('Updating Stock')    
    last_stock = check_stock()
    print(f'last stock count is {last_stock}')
    for x in range(len(last_stock)):
        last_stock[x] = last_stock[x] - stock[x]
    stock_worksheet = SHEET.worksheet('stock')
    stock_worksheet.append_row(last_stock)
    print('Stock Updated')

def item_added(value, amount):
    if value == '1':
        drinks[0] = drinks[0] + 1
        amount = round(amount + 3.20,2)
        stock[0] = stock[0] + 40
        stock[2] = stock[2] + 10
        sales_menu(drinks, amount)
    elif value == '2':
        drinks[1] = drinks[1] + 1
        amount = round(amount + 4.50,2)
        stock[0] = stock[0] + 30
        stock[1] = stock[1] + 20
        stock[2] = stock[2] + 20
        sales_menu(drinks, amount)
    elif value == '3':
        drinks[2] = drinks[2] + 1
        amount = round(amount + 5.00,2)
        stock[0] = stock[0] + 20
        stock[1] = stock[1] + 40
        stock[2] = stock[2] + 15
        sales_menu(drinks, amount)
    elif value == '4':
        last_stock = check_stock()
        if last_stock[0] > stock[0]:
            if last_stock[1] > stock[1]:
                if last_stock[2] > stock[2]:
                    print()
                    print(f'Order sent & {amount} paid')
                    update_sales(drinks, amount)
                    update_stock(stock)
                    print()
                    main()
                else:
                    not_enough_stock()
                    restock()
    else:
        wrong_selection()
        sales_menu(drinks, amount)
 
def sales_menu(drinks, amount):
    print('Sales Menu')
    print()
    print(f'{drinks[0]} Americano in the cart, Type (1) to add')
    print(f'{drinks[1]} Cappuccino in the cart, Type (2) to add')
    print(f'{drinks[2]} Latte in the cart, Type (3) to add')
    print()
    print(f'Type (4) to Oder send & bill €{amount}.')
    selector = input('Typed: ')
    item_added (selector, amount)

def restock_item(what,how_much):
    if what.lower() == 'coffeebeans':
        last_stock = check_stock()
        last_stock[0] = last_stock[0] + int(how_much)
        stock_worksheet = SHEET.worksheet('stock')
        stock_worksheet.append_row(last_stock)
    elif what.lower() == 'milk':
        last_stock = check_stock()
        last_stock[1] = last_stock[1] + int(how_much)
        stock_worksheet = SHEET.worksheet('stock')
        stock_worksheet.append_row(last_stock)
    elif what.lower() == 'sugar':
        last_stock = check_stock()
        last_stock[2] = last_stock[2] + int(how_much)
        stock_worksheet = SHEET.worksheet('stock')
        stock_worksheet.append_row(last_stock)
    else:
        print('Unknow ERROR')
    restock()
    
def restock():
    print()
    print('Type (1) to restock')
    print('Type (2) return to Main Menu')
    selector = input('Typed: ')
    if selector == '1':
        print('What do you want to restock (list from: CoffeeBeans / Milk / Sugar) and how much?')
        print('Exaple: Milk, 1000')
        what, how_much = input('Type here : ').split(',')
        print()
        restock_item(what,how_much)
    elif selector == '2':
        main()
    else:
        wrong_selection()
        restock()
         
def stock_menu():
    print()
    print('Stock Menu')
    print()
    print('Type (1) to Check Stock')
    print('Type (2) to Restock')
    print('Type (3) to back to Main Menu')
    selector = input('Typed: ')
    if selector == '1':
        print()
        print('Please wait...')
        last_stock = check_stock()
        print(f'Coffee beans remains {last_stock[0]} packs')
        print(f'Milk remains {last_stock[1]} ml')
        print(f'Sugar remains {last_stock[0]} packs')
        stock_menu()
    elif selector == '2':
        restock()
    elif selector == '3':
        main()
    else:
        wrong_selection()

while True:
    main()
    amount = 0
    drinks = [0,0,0]
    stock = [0,0,0]
    selector = main_menu()
    
    if selector == '1':        
        sales_menu(drinks, amount)            
    elif selector == '2':
        stock_menu()
    elif selector == '3':
        print('End of the day count')
    elif selector == '4':
        print('Exit')
        break
    else:
        wrong_selection()
