import random
import sys

#To show the printout with color
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

#Class User to hold Cart and User Credentials     
class User:
    def __init__(self, username, password,privilege):
        self.privilege = privilege
        self.username = username
        self.password = password
        self.cart = {}
        self.session_id = ""

    def user_get_session_id(self):
        return self.session_id
            
#Class Product to hold the Product info
class Product:
    def __init__(self, product_id, name, category_id, price,count):
        self.product_id = product_id
        self.name = name
        self.category_id = category_id
        self.price = price
        self.count = count

#Class Catalog holds List of products and Categories
class Catalog:
    def __init__(self):
        self.products = {}  # Product ID as key, Product instance as value
        #self.categories = set() #set
        self.categories = [] #List

#Class ECommerceApp to perform operations on Demo Market place 
class ECommerceApp:
    def __init__(self):
        self.users = {}  # Username as key, User instance as value
        self.catalog = Catalog()
        
        #Welcome Message
        print(color.BOLD +color.RED+"Welcome to the Demo Marketplace Dhukan.com !!!"+color.END+" \n\n\n ")
    
    # Method create_demo_data creates a demo data to start the operation(Setup the Online Store) 
    def create_demo_data(self):
        # Add demo users
        user1 = User("user1", "password1","USER")
        user2 = User("user2", "password2","USER")
        user3 = User("admin", "adminpassword","ADMIN")
        self.users[user1.username] = user1 #Add user1
        self.users[user2.username] = user2 #Add user2
        self.users[user3.username] = user3 #Add user3

        # Add demo admin
        #admin = Admin("admin", "adminpassword")
        #self.admin = admin

        # Add demo products to catalog
        product1 = Product(1, "Women Boots", "footwear", 50,10)
        product2 = Product(2, "Rain Strom Waterproof","clothing",80,7)
        product3 = Product(3, "Ladies Jackets", "clothing", 110,10)
        product4 = Product(4, "Stylish Caps", "clothing", 20,18)
        product5 = Product(5, "HP Laptop EliteBook", "electronics", 820,7)
        product6 = Product(6, "Mens Pants", "Clothing", 80,13)
        product7 = Product(7, "ULB Bluetooth speaker", "electronics", 120,7)
        product8 = Product(8, "Women Slippers", "footwear", 70,23)
        product9 = Product(9, "Women Vegan Footwear", "footwear", 150,21)
        product10 = Product(10,"Men Shoes", "footwear", 110,19)
        

        self.catalog.products[product1.product_id] = product1
        self.catalog.products[product2.product_id] = product2
        self.catalog.products[product3.product_id] = product3
        self.catalog.products[product4.product_id] = product4
        self.catalog.products[product5.product_id] = product5
        self.catalog.products[product6.product_id] = product6
        self.catalog.products[product7.product_id] = product7
        self.catalog.products[product8.product_id] = product8
        self.catalog.products[product9.product_id] = product9
        self.catalog.products[product10.product_id] = product10

        # Add categories
        self.catalog.categories.append("footwear")
        self.catalog.categories.append("clothing")
        self.catalog.categories.append("electronics")
        

    #Method user_login check user credentials      
    def user_login(self, username, password):
        if username in self.users and self.users[username].password == password:
            self.users[username].session_id = "{}{:3d}{:0005d}".format(username,random.randint(1,999),random.randint(1,1110))
            print(self.users[username].session_id)
            return self.users[username].privilege
        return "NONE"
    
    #Method checkout make a checkout based on payment option
    def checkout(self, user, payment_option):
        print("------------CHECK OUT --------------")
        total_amount = sum(item["price"] * item["quantity"] for item in user.cart.values())
        if payment_option in ["Net Banking", "PayPal", "UPI"]:
            user.cart.clear() #Clear the Cart after purchase 
            return f"Your order is successfully placed. Payment of Rs. {total_amount} via {payment_option} is pending."
        return "Invalid payment option."
    
    
    #Method display_cart_menu display the Shopping Cart as Menu where user can Add or Remove items from cart
    def display_cart_menu(self,user):
        while True:
            item_list = []
            print("******** CART MENU **********")
            print("----------LIST OF ITEMS---------")
            option = 0
            Total = 0
            item = 0
            del_item = 0
            #List the Items in the CART
            for i in user.cart:
                item_list.append(i)
                item +=1
                print(item,". ",user.cart[i]["name"]," ----- $",user.cart[i]["price"]," ------ QTY: ",user.cart[i]["quantity"],"---->TOTAL :\t\t$",(user.cart[i]["price"] * user.cart[i]["quantity"]) )
                Total = Total + user.cart[i]["price"] * user.cart[i]["quantity"] 
            print("\t\t\t\t\t\t\t\t TOTAL =$",Total) #Show the Total 
            print(item+1,". Continue Shopping...")
            print(item+2,". Remove Item from the CART")
            print(item+3,". Check Out for Payment")
            print("Select Option {} to ".format(item+1),item+2)  
            option = int(input())
            if(option == item+2): #Remove Items from CART
                print("Enter the Item in the menue to be Removed :")
                del_item = int(input())
                if(del_item < item+1 ):
                    self.remove_from_cart(user,item_list[del_item-1])
                else:
                    print("CHOICE OUT OF ITEM RANGE")
            elif(option == item+3): #CHECKOUT
                    print("Placing items for checkout...")
                    print(self.checkout(user, "UPI"))
                    break
            elif(option == item+1): #Continue Shopping
                print("Continue Shopping...")
                break
            else:
                    print("OUT OF MENU RANGE")
                    
    #Method add_to_cart Add Items into Cart                
    def add_to_cart(self, user, product_id, quantity):
        product = self.catalog.products.get(product_id)
        if product:
            user.cart[product_id] = {"name": product.name, "price": product.price, "quantity": quantity}
            return True
        return False

    #Method remove_from_cart Remove Items from the Cart
    def remove_from_cart(self, user, product_id):
        if product_id in user.cart:
            del user.cart[product_id]
            return True
        return False
    
    #Method display_catalog  Display the Catalog for User and Admin depending on the option supplied.
    #Option=0 for Initial full Catalog Display for User, 
    #Option=1  Full Catalog in Menu Form so the and 
    #Option=-1 Full Catalog for Admin   
    def display_catalog(self,user,option):
        
        while True:
            list_in_Menu = []
            i=0
            qty = 0
            print("***********CATALOG************")
            #Option=0 for Initial full Catalog Display , Option=1 for full Catalog in Menu Form and Option=-1 for Full Catalog for Admin  
            if(option == 1 or option == 0 or option == -1):
            
                for prod in self.catalog.products:
                    i+=1
                    if(option == -1): #Option=-1 Full Catalog for Admin 
                        print("{}. PID:  {} --- P_NAME:  {} --- P_CATEGORY: {} --- P_PRICE: ${} --- P_QTY: {}  ".format(i,self.catalog.products[prod].product_id,self.catalog.products[prod].name,self.catalog.products[prod].category_id,self.catalog.products[prod].price,self.catalog.products[prod].count))
                    else:
                        print("\t {}.".format(i),self.catalog.products[prod].name," ---------- $ ",self.catalog.products[prod].price)
                    list_in_Menu.append(self.catalog.products[prod].product_id)
                if(option != 0 and option != -1 ): #dont need EXIT menu for Admin Catalog and User initial Catalog
                    print("\t {}.".format(i+1)," EXIT (Back to Privious Menu)")
                print("\n\n")    
                if(option == 0 or option == -1 ): #Exit the method 
                    break
            elif(option > 1 and option <= len(self.catalog.categories)+1 ):
                print("option : ",option) ##just for Debug Remove
                print("CATEGORY : ",self.catalog.categories[option-2]) #Show the Category 
                i=0
                for prod in self.catalog.products:
                    #Filter out the Product based on Category 
                    if(self.catalog.products[prod].category_id == self.catalog.categories[option-2]):
                        i+=1
                        print("\t {}.".format(i),self.catalog.products[prod].name," ---------- $ ",self.catalog.products[prod].price)
                        list_in_Menu.append(self.catalog.products[prod].product_id)
                print("\t {}.".format(i+1)," EXIT (Back to Privious Menu)\n\n")
            print("Select Option 1 to {} to Shop(Add Items to Cart)".format(i+1))    
            display_option = int(input())
            if(display_option >= 1 and display_option <= i ):
                print("Quantity Needed :")
                qty = int(input()) 
                print("display_option = ",display_option) ##just for Debug Remove
                print("list_in_Menu",list_in_Menu) ##just for Debug Remove
                print("Last Index i= ",i) ##just for Debug Remove
                print("Selected product id from list_in_Menu : ",list_in_Menu[display_option-1])
                print(type(list_in_Menu[display_option-1]))
                self.add_to_cart(user,list_in_Menu[display_option-1],qty) #Add items to Cart
                print("{} --- QTY {} Added to {} Cart ".format(self.catalog.products.get(list_in_Menu[display_option-1]).name,qty,user.username))
            elif(display_option == i+1) : #Back to Privious Menu
                return 9999
            else :    
                print("OUT OF MENU RANGE")
        return i+1
    
    #Method display_category_search_menu Display list of Categories for Category based Catalog   
    def display_category_search_menu(self):
        while True :
            print("******** CATEGORY MENU **********")
            print("1. Complete Catalog") #display Complete Catalog without Filter
            for i in range(len(self.catalog.categories)):
                print(i+2,". Calalog based on ",self.catalog.categories[i]) # Category based Catalog
            print(len(self.catalog.categories)+2,". Way to Check Out (View the CART) ")
            print(len(self.catalog.categories)+3,". EXIT (Done with Shopping)")
            print("Select Option 1 to ",len(self.catalog.categories)+3)
            option = int(input())
            if(option < 0 or option > len(self.catalog.categories)+3 ):
                print("Out of range !!! Please select Option 1 to ",len(self.catalog.categories)+2)
            elif(option == len(self.catalog.categories)+3): #Exit Shopping
                return 9999                                 
            elif(option == len(self.catalog.categories)+2): #View the CART
                return 8888
            else:
                break
        return option      
                                                 
   
    #Method admin_add_product allow Admin to Add the Products 
    def admin_add_product(self, name, category_id, price,count):
        p_id = list(self.catalog.products.keys())
        new_p_id = 0
        if(len(p_id) > 0):
            p_id.sort(reverse=True)
            new_p_id = p_id[0]+1 #Product Id is Auto Generated
        else:
            new_p_id = 1 #When Product is empty value starts from 1
            
        if category_id not in self.catalog.categories:
            return "Invalid category."
        new_product = Product(new_p_id, name, category_id, price,count)
        self.catalog.products[new_p_id] = new_product
        return "Product added successfully."

    #Method admin_modify_product allow Admin to Modify the Product info 
    def admin_modify_product(self, product_id, name, category_id, price,count):
        if category_id not in self.catalog.categories:
            return "Category not found... Enter existing Valid Category or If its a New Category update the Category using Admin ADD Category Menu."
        if product_id in self.catalog.products:
            modified_product = Product(product_id, name, category_id, price,count)
            self.catalog.products[product_id] = modified_product
            return "Product modified successfully."
        return "Product not found."

    #Method admin_remove_product allow Admin to remove the Product from the Inventory
    def admin_remove_product(self, product_id):
        if product_id in self.catalog.products:
            del self.catalog.products[product_id]
            return "Product removed successfully."
        return "Product not found."

    #Method admin_product_menu allow Admin to Manage Products
    def admin_product_menu(self,user):
        while True:
            print("***********ADMIN PRODUCT MENU************")
            print("1. ADD New Product/Item")
            print("2. MODIFY Product/Item")
            print("3. DELETE Product/Item")
            print("4. LIST the Products/Items")
            print("5. EXIT Product/Item Menu")
            print("Select Option 1 to 5")
            option = int(input())
            if(option < 1 or option > 5 ): #Out of Range
                print("Out of range !!! Please select Option 1 to 5")
                continue
            elif(option == 1): #ADD New Product/Item
                print("Enter the New Product Name:")
                name = input()
                print("Enter Category of New Product to be Added :")
                category_id = input()
                print("Enter the Price of New Product to be Added :")
                price = int(input())
                print("Enter the QTY of New Product to be Added :")
                count = int(input())
                print(self.admin_add_product(name,category_id,price,count))
            elif(option == 2): #MODIFY Product/Item
                print("Enter the Product ID to Update:")
                product_id = int(input())
                print("Enter the Product Name to Update:")
                name = input()
                print("Enter Category of the Product to Update :")
                category_id = input()
                print("Enter the Price of the Product to Update :")
                price = int(input())
                print("Enter the QTY of the Product to Update :")
                count = int(input())
                print(self.admin_modify_product(product_id,name,category_id,price,count))
            elif(option == 3): #DELETE Product/Item
                print("Enter the Existing Product ID to Delete:")
                product_id = int(input())
                print(self.admin_remove_product(product_id))
            elif(option == 4): #LIST the Products/Items
                self.display_catalog(user,-1)
            elif(option == 5): #EXIT Product/Item Menu
                break
                
    #Method admin_add_category Allow Admin to Add new Category    
    def admin_add_category(self, category):
        self.catalog.categories.append(category)
        return "New Category added successfully."
    
    #Method admin_modify_category Allow Admin to Modify the Category
    def admin_modify_category(self, old_category_id,new_category_id):
        if old_category_id in self.catalog.categories:
            inx = self.catalog.categories.index(old_category_id)
            self.catalog.categories.pop(inx)
            self.catalog.categories.insert(inx,new_category_id)
            return "Category modified successfully."
        return "Category not found."
    
    #Method admin_remove_category Allow Admin to Remove a Category
    def admin_remove_category(self, category):
        if category in self.catalog.categories:
            self.catalog.categories.remove(category)
            return "Category removed successfully."
        return "Category not found."
    
    #Method admin_list_category Allow Admin to display the Category List
    def admin_list_category(self):
        i = 0
        if len(self.catalog.categories) == 0:
            return "CATEGORY IS EMPTY !!!"
        for category in self.catalog.categories:    
            i+=1
            print("{}. {}".format(i,category))
        return ""
    
    #Method admin_category_menu allow Admin to Manage Category List
    def admin_category_menu(self):
        while True:
            print("***********ADMIN CATEGORY MENU************")
            print("1. ADD New Category")
            print("2. MODIFY Category")
            print("3. DELETE Category")
            print("4. LIST the Categories")
            print("5. EXIT Category Menu")
            print("Select Option 1 to 5")
            option = int(input())
            if(option < 1 or option > 5 ): #Out of Range
                print("Out of range !!! Please select Option 1 to 5")
                continue
            elif(option == 1): #ADD New Category
                print("Enter the New Category to be Added:")
                category_id = input()
                print(self.admin_add_category(category_id))
            elif(option == 2): #MODIFY Category
                print("Enter the Existing Category to Update:")
                old_category_id = input()
                print("Enter the New Category to Update:")
                new_category_id = input()
                print(self.admin_modify_category(old_category_id,new_category_id))
            elif(option == 3): #DELETE Category
                print("Enter the Category to Delete:")
                category_id = input()
                print(self.admin_remove_category(category_id))
            elif(option == 4): #LIST the Categories
                self.admin_list_category()
            elif(option == 5): #EXIT Category Menu
                break

    #Method admin_menu Allow Admin to Manage his/her operations            
    def admin_menu(self,user):
        while True:
            print("***********ADMIN MENU************")
            print("1. CATEGORY")
            print("2. PRODUCT")
            print("3. EXIT ADMIN Menu")
            print("Select Option 1 to 3")
            option = int(input())
            if(option < 1 or option > 3 ): #Out of Range
                print("Out of range !!! Please select Option 1 to 3")
                continue
            elif(option == 1): #Manage CATEGORY
                self.admin_category_menu()
            elif(option == 2): #Manage PRODUCT
                app.admin_product_menu(user)
            elif(option == 3): #EXIT ADMIN Menu
                return 9999
                
# Main Program:
app = ECommerceApp() #Create a ECommerce Application
app.create_demo_data() #Add Demo data(Setup Store) 
app.display_catalog("user1",0) #Display the Catalog with all the Items
shop=''
print("Do you wish to Shop Y/N:")

while True:
    shop = input() #Check User wants to Shop or Admin wants to work on Inventory
    if (shop == 'Y' or shop == 'N' or shop == 'y' or shop == 'n'):
        break
    else:
        print("Please Type Y/N")    
        continue
#Accept User Credentials
print("Please enter the user Name :")
user_name = input()
print("Please print the password :")
password = input()


#If its a User wants to Shop
if (app.user_login(user_name, password) == "USER"):
#if app.user_login(user_name, password):
    user = app.users[user_name]
    #option = 0
    while True:
        #if (user_name == "admin"): #If its Admin exit out
         #   break
        #Search Items based on Category
        option = app.display_category_search_menu()
        if(option == 9999): #Exit out of Shopping
            user.session_id = "" #make the session id blank
            print(color.BOLD +color.RED+"Thank you for shopping with the Demo Marketplace Dhukan.com !!!\n Have a Nice Day !!!"+color.END+" \n\n\n ")
            break
        if(option == 8888): #Display Cart   
            option = app.display_cart_menu(user)
            continue
        #Display Catalog     
        option = app.display_catalog(user,option)
        if(option == 9999):
            continue
# Admin Login to Manage Inventory
elif (app.user_login(user_name, password) == "ADMIN"):
    # Admin actions
    user1 = app.users[user_name]
    while True:
        if(app.admin_menu(user1) == 9999):
            print(color.BOLD +color.RED+"Thank you Admin for updating the shopping Inventory. Hope you enjoyed the Demo Marketplace Dhukan.com !!!\n Have a Nice Day !!!"+color.END+" \n\n\n ")
            break
else:
    print("Sorry Wrong Credentials ...!!!")
