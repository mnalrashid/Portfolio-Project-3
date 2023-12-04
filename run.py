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
    '''
    The app will start from the main also in the middle of using the app,
    if the User wants to back to the Main menu, Main() will reset all the variables.
    '''
    print()
 
def main_menu():
    '''
    The main menu will show the options where the User can redirect to the Sales Menu, Stock Menu, and check the Balance.
    '''
    print('X Coffee')
    print('Select the menu')
    print('Type (1) for Sales Menu')
    print('Type (2) for Stock Menu')
    print('Type (3) for Closing Day Menu')
    print('Type (4) for Exit')
    print()
    selector = input('Typed: \n')
    return selector
 
def wrong_selection():
    '''
    If the User typed the wrong value/key, this function will show the message. and return a True value to keep while loop active.
    '''
    print('Wrong selection, try again')
    print()
    return True

def not_enough_stock():
    '''
    If there is less stock than the order created, Apps will call this function to show a message.
    '''
    print()
    print('Not enough stock, please RESTOCK')
    print()

def check_stock():
    '''
    By this function, Apps will get the data from the worksheet and return the last count of the stock, If the stock is empty,
    The function will ask for a restocking.
    '''
    stock_worksheet = SHEET.worksheet('stock')
    stocks = stock_worksheet.get_all_values()
    if len(stocks) >=2:
        last_stock = stocks[-1]  
        last_stock = [int(x) for x in last_stock]
        return last_stock
    else:
        last_stock = [0,0,0]
        return last_stock

def update_sales(drinks, amount):
    '''
    When any sales, this function will update the worksheet (will add sales item and add the sale amount)
    '''
    sales_item = [drinks[0],drinks[1],drinks[2]]
    sale[0] = amount
    print('updating data')
    daily_sales_worksheet = SHEET.worksheet('daily_sales')
    daily_sales_worksheet.append_row(sales_item)
    expense_worksheet = SHEET.worksheet('z_count')
    expense_worksheet.append_row(sale)
    print('Sales Updated')
    
def update_stock(stock):
    '''
    When this function is called with a restock value, this will update the worksheet.
    '''
    print('Updating Stock')    
    last_stock = check_stock()
    for x in range(len(last_stock)):
        last_stock[x] = last_stock[x] - stock[x]
    stock_worksheet = SHEET.worksheet('stock')
    stock_worksheet.append_row(last_stock)
    print('Stock Updated')

def item_added(value, amount):
    '''
    This function will add items to the shopping cart until the user selects to place an order the function will check the stock,
    if we have enough stock to ready the order, this will update sales and stock, else will request the user to restock.
    '''
    if value == '1':
        drinks[0] = drinks[0] + 1
        amount = amount + 3.20
        stock[0] = stock[0] + 40
        stock[2] = stock[2] + 10
        sales_menu(drinks, amount)
    elif value == '2':
        drinks[1] = drinks[1] + 1
        amount = amount + 4.50
        stock[0] = stock[0] + 30
        stock[1] = stock[1] + 20
        stock[2] = stock[2] + 20
        sales_menu(drinks, amount)
    elif value == '3':
        drinks[2] = drinks[2] + 1
        amount = amount + 5.00
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
                not_enough_stock()
                restock()
        else:
            not_enough_stock()
            restock()
    else:
        wrong_selection()
        sales_menu(drinks, amount)
 
def sales_menu(drinks, amount):
    '''
    This is a Sales Menu, Users can choose what drinks they want to add and the User can see the shopping cart and place an order from here.
    '''
    print('Sales Menu')
    print()
    print(f'{drinks[0]} Americano in the cart, Type (1) to add')
    print(f'{drinks[1]} Cappuccino in the cart, Type (2) to add')
    print(f'{drinks[2]} Latte in the cart, Type (3) to add')
    print()
    print(f'Type (4) to Oder send & bill €{amount}.')
    selector = input('Typed: \n')
    item_added (selector, amount)
    
def update_expenses_worksheet(last_stock,how_much):
    '''
    This fucntion will update all the expenses including stocks
    '''
    expense[1] = how_much
    stock_worksheet = SHEET.worksheet('stock')
    stock_worksheet.append_row(last_stock)
    expense_worksheet = SHEET.worksheet('z_count')
    expense_worksheet.append_row(expense)

def restock_item(what,how_much):
    '''
    This function will sort what items will be added to the stock.
    '''
    if what.lower() == 'coffeebeans':
        last_stock = check_stock()
        stock = how_much * 80
        last_stock[0] = last_stock[0] + stock
        update_expenses_worksheet(last_stock,how_much)
    elif what.lower() == 'milk':
        last_stock = check_stock()
        stock = how_much * 200
        last_stock[1] = last_stock[1] + stock
        update_expenses_worksheet(last_stock,how_much)
    elif what.lower() == 'sugar':
        last_stock = check_stock()
        stock = how_much * 120
        last_stock[2] = last_stock[2] + stock
        update_expenses_worksheet(last_stock,how_much)
    else:
        print('Unknown ERROR')
    restock()
    
def restock():
    '''
    This is the restock menu, the user can go ahead to add items or can go back to the main menu from here.
    '''
    print()
    print('Type (1) to restock')
    print('Type (2) return to Main Menu')
    selector = input('Typed: \n')
    if selector == '1':
        print('What do you want to restock (list from: CoffeeBeans / Milk / Sugar) and how much €?')
        print('Exaple: Milk, 100')
        what, how_much = input('Type here : \n').split(',')
        print()
        how_much = int(how_much)
        restock_item(what,how_much)
    elif selector == '2':
        main()
    else:
        wrong_selection()
        restock()
         
def stock_menu():
    '''
    From this function. Users can see what stock is available, restock and can able to back to the main menu.
    '''
    print()
    print('Stock Menu')
    print()
    print('Type (1) to Check Stock')
    print('Type (2) to Restock')
    print('Type (3) to back to Main Menu')
    selector = input('Typed: \n')
    if selector == '1':
        print()
        print('Please wait...')
        last_stock = check_stock()
        print(f'Coffee beans remains {last_stock[0]} packs')
        print(f'Milk remains {last_stock[1]} ml')
        print(f'Sugar remains {last_stock[2]} packs')
        stock_menu()
    elif selector == '2':
        restock()
    elif selector == '3':
        main()
    else:
        wrong_selection()
        
# def end_of_day():
    

while True:
    main()
    amount = 0
    drinks = [0,0,0]
    stock = [0,0,0]
    expense = [0,0]
    sale = [0,0]
    selector = main_menu()
    
    if selector == '1':        
        sales_menu(drinks, amount)            
    elif selector == '2':
        stock_menu()
    elif selector == '3':
        # end_of_day()
        print('Under dev')
    elif selector == '4':
        print('Exit')
        break
    else:
        wrong_selection()
