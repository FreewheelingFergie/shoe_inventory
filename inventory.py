from tabulate import tabulate

#========The beginning of the class==========
class Shoe():

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    # Method for obtaining cost of product.
    def get_cost(self):
        return self.cost

    # Method for obtaining quantity of product.
    def get_quantity(self):
        return (self.quantity)
    
    # String method to ensure data prints out in a way user can understand.
    def __str__(self):
        return 'COUNTRY: ' + str(self.country) + ' CODE: ' + str(self.code) + ' PRODUCT: ' + str(self.product)+ ' COST: £' + str(self.cost) + ' QUANTITY: ' + str(self.quantity)

#=============Shoe list===========
shoe_list = []
#==========Functions outside the class==============

# This function is to pull data from text file and compile list of product details.
def read_shoes_data():
    
    # Use Try/Except method to ensure that the program will remain functioning if the inventory file is missing.
    try:
        with open('inventory.txt', 'r') as f:
            for line in f.readlines()[1:]: # Skip first line using [1:]
                data = (line.strip().split(','))
                shoe_data = Shoe(data[0], data[1], data[2], data[3], data[4])
                shoe_list.append(shoe_data)
                
    except FileNotFoundError as error:
        print('The inventory file appears to be missing.')
        print(error)
       
 # This function is to allow users to add a new product to the inventory.           
def capture_shoes():
   
    product = input('Please enter the product name: ').title()# Use title() to capitalise first letter of each word.

    # Use 'while True' to ensure system does not crash if user inputs anything other than float value.
    while True:
        try:
            cost = float(input('Please enter the cost of the product: '))
        except:
            print('You do not appear to have entered a correct value.')
            continue
        break
    code = input('Please enter the product code: ').upper() # Ensure it is all caps
    
    country = input('Please enter the country: ').title() # Use title() to ensure caps at the start of each word.
    while True:
        try:
            quantity = int(input('Please enter the quantity of the product: '))
        except:
            print('You do not appear to have entered a correct value.')
            continue
        break

    # Create object called 'new_shoe' and append to the list.
    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)
    # Print message to user to confirm item has been added to inventory.
    print('Thank you. The following item has been added to the inventory.')
    print(new_shoe.__str__())

    # Write list to 'inventory.txt'.
    with open('inventory.txt', 'a') as f:
        f.write(f'\n{country},{code},{product},{cost},{quantity}') # Ensure no spaces between items (just a ",") to match format of text file.

# This function should allow user to view all product details.
def view_all():
    # Cannot pull objects from shoe_list with tabulate so create a new list called 'list_of_values' to store values of each object.
    # Use tabulate with (shoe_list, headers, table format code)
    # Ref - https://pypi.org/project/tabulate/
    list_of_values = []
    for line in shoe_list:
        shoe_value = [line.country, line.code, line.product, line.cost, line.quantity]
        list_of_values.append(shoe_value)
    shoe_table = tabulate(list_of_values, headers = ['COUNTRY', 'CODE', 'PRODUCT', 'COST', 'QUANTITY'], tablefmt = 'fancy_grid')
    print(shoe_table)

# This function should allow user to increase stock of products with lowest quantity.
def re_stock():
    # Create a base case where the first product quantity is lowest number.
    lowest_number = shoe_list[0]
    # For each line check if it is lower quantity than first line.
    # If so, make that product's quantity the 'lowest_number'.
    # Esnure values are cast as integers.
    for line in shoe_list:
        if int(line.quantity) < int(lowest_number.quantity):
            lowest_number = line
    
    # Display product with lowest quantity and ask yser how many shoes to add.
    # Inform user they should enter '0' if they do not want to change quantity.
    print(f'The product with the lowest quantity is: {lowest_number.product} with {lowest_number.quantity} shoes.')
    add_quantity = int(input('What quantity of shoes would you like to add to this product? \nEnter 0 if you do not want to add to the quantity:'))
    lowest_number.quantity = int(lowest_number.quantity) + add_quantity
    print(f'The updated quantity for {lowest_number.product} is {lowest_number.quantity}')

    # Update 'inventory.txt' file with new quantity.
    # Write titles first.
    with open('inventory.txt', 'w') as f:
        f.write('Country,Code,Product,Cost,Quantity\n')
    # Now append the actual lines of 'shoe_list'.
    with open('inventory.txt', 'a') as f:
        for line in shoe_list:
            f.write(str(line.country) + ',' + str(line.code) + ',' + str(line.product) + ',' + str(line.cost) + ',' + str(line.quantity) + '\n')

# This function should allow user to search product using product code.
def search_shoe():
    # Request user inputs code of product to begin search.
    search_shoe_code = input('Please input the product code you would like to search for: ').upper()
    # Start a counter for matching search results.
    search_results = 0
    # Loop through each line to check if user input matches product code.   
    for line in (shoe_list):
            # If codes match, then add one to counter and print product details
            if search_shoe_code == line.code:
                search_results += 1
                print (f'\nPlease see product details for item CODE: {search_shoe_code} below:\n{Shoe(line.country, line.code, line.product, line.cost, line.quantity)}')
                
    # If 'search_result' counter is 0, then there have been no matches.
    if search_results == 0:
        print('Cannot find a product with that code.')

# This function should print value of each product.
def value_per_item():
    # Loop through each line of shoe_list and multiply quantity by cost.
    for line in shoe_list:
        shoe_value = int(line.get_quantity()) * float(line.get_cost())
        # Print value of each shoe.
        print(f'PRODUCT: {line.product} -- TOTAL VALUE OF: £{round((shoe_value), 2)}')

# This function find prodcut with highest quantity and place it for sale.
def highest_qty():
    # Create variable called 'largest_quantity'.
    # Start with line[0] being 'largest_quantity' as base condition and loop through each line to see which values are bigger.
    largest_quantity = shoe_list[0]
    for line in shoe_list:
        if int(line.quantity) > int(largest_quantity.quantity):
            largest_quantity = line
    print(f'{largest_quantity.product} is now on sale.')
    
#==========Main Menu=============
# Welcome message for user.
print('WELCOME TO SHOE INVENTORY Version 1.0')

# Use 'read_shoes_data()' function to pupulat the shoe_list. 
# Note - this function is required for other functions to operate correctly...
# ... therefore not in user menu.
read_shoes_data()
while True:
    # Present the menu to the user.
    menu = input('''\nSelect one of the following options below:
1     - Add a new shoe to inventory
2     - View details of all shoes in inventory
3     - Find lowest stock items and arrange stock increase
4     - Search for particular shoe product
5     - Calculate total value of each stock item
6     - Place highest quantity shoe for sale
7     - Exit program
:''').lower() # Use lower() to avoid errors with caps.

    if menu == '1':
        capture_shoes()

    elif menu == '2':
        view_all()
    
    elif menu == '3':
        re_stock()
        
    elif menu == '4':
        search_shoe()

    elif menu == '5':
        value_per_item()

    elif menu == '6':
        highest_qty()

    elif menu == '7':
        print('You are leaving the inventory program. Goodbye.')
        quit()

    else:
        print('You have made a wrong choice, please try again.')