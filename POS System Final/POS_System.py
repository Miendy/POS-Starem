from tkinter import *
import customtkinter
import datetime
from PIL import Image, ImageTk # install pillow

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

self = customtkinter.CTk()

# configure window
self.title("POS System")
width = 1100
height = 620
self.geometry(f"{1100}x{620}")
self.resizable(False,False)
# self.wm_attributes('-transparentcolor', '#ABCDEF')

# configure grid layout (4x4)
self.grid_columnconfigure(1, weight=1)
self.grid_columnconfigure((2, 3), weight=0)
self.grid_rowconfigure((0, 1, 2), weight=1)

# Variables 
item_cost_string = customtkinter.StringVar()
item_cost_string.set("0")

food_item = []
food_price = []

customerCount = 0

global time
entryData = ""
changeLabelData = customtkinter.StringVar()

# Functions
def button_sidebar_food():
        print("Home")

def button_sidebar_drinks():
        print("Transactions")

def button_sidebar_all_catalog():
        print("Settings")

def calculate_change():
        entryData = moneyEntry.get()
        calculated = float(entryData) - float(sum(food_price))
        if calculated < 0:
                changeLabelData.set("Please provide: $" + str(abs(calculated)))
        else:
                changeLabelData.set("Your change is: $" + str(calculated))

def pay_button(): # show this on the video
        global customerCount
        small_date = datetime.datetime.today().date()
        bill = open(f"Bill.txt {small_date}", 'a')
        bill.writelines("Date: " + str(small_date) + "\n")
        current_date = datetime.datetime.now()
        curr_date_str = str(current_date)
        curr_date_strip = curr_date_str.split('.')[0]
        bill.writelines("<-----------------Recept----------------->\n")
        bill.writelines(f"Customer #{customerCount}\n" + str(small_date))
        for i in range(len(food_price)):
                out = str(i+1) + ". " + curr_date_strip+ " - "  + food_item[i] + ": $" + str(food_price[i])
                bill.writelines(out)
                bill.writelines("\n")
        bill.writelines("Total: $" + str(sum(food_price)) + "\n")
        bill.close()
        customerCount = customerCount + 1
        #new window
        newWindow()

def newWindow():
        # New window
        win = customtkinter.CTkToplevel()
        win.attributes('-topmost', 'true')
        win.geometry("650x400")
        win.resizable(False,False)
        win.focus()
        moneyLabel = customtkinter.CTkLabel(win, text=f"Total Cost: ${sum(food_price)}")
        moneyLabel.pack(padx=10, pady=10)
        global moneyEntry
        moneyEntry = customtkinter.CTkEntry(master=win, placeholder_text="Enter Money Given")
        moneyEntry.focus()
        moneyEntry.pack(padx=20, pady=10)
        moneyButton = customtkinter.CTkButton(master=win, text="Calculate Change", command=calculate_change)
        moneyButton.pack(padx=20, pady=5)
        changeLabel = customtkinter.CTkLabel(master=win, textvariable=str(changeLabelData), font=("Segoe UI Bold", 20))
        changeLabel.pack(padx=20, pady=20)
        
        def next_customer():
                clear_function()
                win.destroy()
                win.update()
                changeLabelData.set("")
        
        next_customer_button = customtkinter.CTkButton(master=win, text="Next Customer", command=next_customer)
        next_customer_button.pack(padx=20, pady=20)

def purchase_item(item, cost, self):
        food_item.append(item)
        food_price.append(cost)
        item_info =  item + ": $" + str(cost)
        lable = customtkinter.CTkLabel(master=self, text=item_info)
        item_cost_string.set(str(0))
        for i in range(len(food_item)):
                lable.grid(row=len(food_item), column=0)
        item_cost_string.set(str(sum(food_price)))

def clear_function(): 
        food_item.clear()
        food_price.clear()
        item_cost_string.set("0")
        for label in self.scrollable_frame.winfo_children():
                label.destroy()


# create sidebar frame with widgets
self.sidebar_frame = customtkinter.CTkFrame(self, width=80, corner_radius=15)
self.sidebar_frame.grid(row=0, column=0, padx=(15, 0), pady=15, rowspan=4, sticky="nsew")
self.sidebar_frame.grid_rowconfigure(4, weight=1)

self.sidebar_home_button = customtkinter.CTkButton(self.sidebar_frame, width=90, text="Home", command=button_sidebar_food)
self.sidebar_home_button.grid(row=1, column=0, padx=15, pady=15)
self.sidebar_transactions_button = customtkinter.CTkButton(self.sidebar_frame, width=90, text="Transactions", command=button_sidebar_drinks)
self.sidebar_transactions_button.grid(row=2, column=0, padx=15, pady=10)
self.sidebar_settings_button = customtkinter.CTkButton(self.sidebar_frame, width=90, text="Settings", command=button_sidebar_all_catalog)
self.sidebar_settings_button.grid(row=3, column=0, padx=15, pady=10)

self.main_middle_frame = customtkinter.CTkFrame(self, width=450, corner_radius=15)
self.main_middle_frame.grid(row=0, column=1, padx=20, pady=15, rowspan=4, sticky="nsew")
self.main_middle_frame.grid_columnconfigure(10, weight=1)

self.right_frame = customtkinter.CTkFrame(self.main_middle_frame, width=150, height=100, corner_radius=15)
self.right_frame.grid(row=3, column=4, sticky="nsew",  padx=665, pady=25, rowspan=4)
self.right_frame.grid_columnconfigure(4, weight=4)

self.right_button_frame = customtkinter.CTkFrame(self.right_frame, corner_radius=15)
self.right_button_frame.grid(row=1, column=0, sticky="nsew",  padx=20, pady=(30, 25), rowspan=4)

self.total_text_label = customtkinter.CTkLabel(self, text="Total", font=("Segoe UI",20), bg_color="#2B2B2B", anchor="center")
self.total_text_label.place(x=870, y=405)

self.total_text_label = customtkinter.CTkLabel(self, textvariable = item_cost_string, font=("Segoe UI Bold",30), bg_color="#2B2B2B")
self.total_text_label.place(x=955, y=390)

self.total_text_label = customtkinter.CTkLabel(self, text = "$", font=("Segoe UI Bold",30), bg_color="#2B2B2B")
self.total_text_label.place(x=935, y=390)

self.right_frame_pay_button = customtkinter.CTkButton(self, width=140, height=50, text="CHECK OUT", fg_color='#FF5C5C', bg_color="#2B2B2B", hover_color="#FF8A8A", corner_radius=15, command=pay_button)
self.right_frame_pay_button.place(x=870, y=450)

self.right_frame_clear_button = customtkinter.CTkButton(self, width=110, height=40, text="CLEAR", bg_color="#2B2B2B", corner_radius=15, command=clear_function)
self.right_frame_clear_button.place(x=885, y=510)

# self.right_frame_clear_button = customtkinter.CTkButton(self, width=110, height=40, text="UNDO", bg_color="#2B2B2B", corner_radius=15, command=clear_function)
# self.right_frame_clear_button.place(x=885, y=510)

# self.right_frame_clear_button = customtkinter.CTkButton(self, width=140, height=50, text="CLEAR", fg_color='#FF5C5C', bg_color="#2B2B2B", hover_color="#FF8A8A", corner_radius=15, command=delete)
# self.right_frame_clear_button.place(x=870, y=450)

# Tabview
self.tabview = customtkinter.CTkTabview(self, width=250, height=545, fg_color="#333333", bg_color="#2B2B2B", corner_radius=15)
self.tabview.grid(row=0, column=1, padx=(50, 315), pady=(20, 0), sticky="nsew")
self.tabview.add("Food")
self.tabview.add("Drinks")
self.tabview.tab("Food").grid_columnconfigure(3, weight=1)  # configure grid of individual tabs
self.tabview.tab("Drinks").grid_columnconfigure(3, weight=1)

# This is a scrollable line
self.scrollable_frame = customtkinter.CTkScrollableFrame(self.right_frame, width=120, label_text="Cart", corner_radius=10)
for label in self.scrollable_frame.winfo_children():
        label.destroy()
self.scrollable_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
self.scrollable_frame.grid_columnconfigure(0, weight=1)
self.scrollable_frame_switches = []

# Foods
# Banana ----------------------------------------------------------------
banana_img= customtkinter.CTkImage(Image.open("Images\crop_banana.png"), size=(100, 100))
self.banana_button = customtkinter.CTkButton(self.tabview.tab("Food"), width=130, height=100, image=banana_img, compound="top", text="Bananas\n$4", command=lambda: purchase_item("Banana", 4, self.scrollable_frame))
self.banana_button.grid(row=1, column=0, padx=30, pady=10)
# Banana ----------------------------------------------------------------

# Potato ----------------------------------------------------------------
potato_img= customtkinter.CTkImage(Image.open("Images\crop_potato.png"), size=(100, 100))
self.potato_button = customtkinter.CTkButton(self.tabview.tab("Food"), width=130, height=100, image=potato_img, compound="top", text="Potato\n$2", command=lambda: purchase_item("Potato", 2, self.scrollable_frame))
self.potato_button.grid(row=1, column=1, padx=30, pady=10)
# Potato ----------------------------------------------------------------

# Burger ----------------------------------------------------------------
burger_img= customtkinter.CTkImage(Image.open("Images\crop_burger.png"), size=(100, 100))
self.burger_button = customtkinter.CTkButton(self.tabview.tab("Food"), width=130, height=100, image=burger_img, compound="top", text="Burger\n$5", command=lambda: purchase_item("Burger", 5, self.scrollable_frame))
self.burger_button.grid(row=1, column=2, padx=30, pady=10)
# Burger ----------------------------------------------------------------

# chips ----------------------------------------------------------------
chips_img= customtkinter.CTkImage(Image.open("Images\crop_chips.png"), size=(118, 100))
self.chips_button = customtkinter.CTkButton(self.tabview.tab("Food"), width=130, height=100, image=chips_img, compound="top", text="Chips\n$4", command=lambda: purchase_item("Chips", 4, self.scrollable_frame))
self.chips_button.grid(row=2, column=0, padx=30, pady=10)
# chips ----------------------------------------------------------------

# Popcorn ----------------------------------------------------------------
popcorn_img= customtkinter.CTkImage(Image.open("Images\corp_popcorn.png"), size=(100, 100))
self.popcorn_button = customtkinter.CTkButton(self.tabview.tab("Food"), width=130, height=100, image=popcorn_img, compound="top", text="Popcorn\n$3", command=lambda: purchase_item("Popcorn", 3, self.scrollable_frame))
self.popcorn_button.grid(row=2, column=1, padx=30, pady=10)
# Popcorn ----------------------------------------------------------------

# Garlic Bread ----------------------------------------------------------------
garlicbread_img= customtkinter.CTkImage(Image.open("Images\crop_garlic.png"), size=(100, 100))
self.garlicbread_button = customtkinter.CTkButton(self.tabview.tab("Food"), width=130, height=100, image=garlicbread_img, compound="top", text="Garlic Bread\n$2.50", command=lambda: purchase_item("Garlic Bread", 2.5, self.scrollable_frame))
self.garlicbread_button.grid(row=2, column=2, padx=30, pady=10)
# Garlic Bread ----------------------------------------------------------------

# chicken Wrap ----------------------------------------------------------------
wrap_img= customtkinter.CTkImage(Image.open("Images\crop_wrap.png"), size=(118, 100))
self.chips_button = customtkinter.CTkButton(self.tabview.tab("Food"), width=130, height=100, image=wrap_img, compound="top", text="Chicken Wrap\n$4", command=lambda: purchase_item("Chicken Wrap (Halal)", 4, self.scrollable_frame))
self.chips_button.grid(row=3, column=0, padx=30, pady=10)
# chicken Wrap ----------------------------------------------------------------

# Drinks
# Prime ----------------------------------------------------------------
prime_img= customtkinter.CTkImage(Image.open("Images\crop_brime.png"), size=(100, 100))
self.prime_button = customtkinter.CTkButton(self.tabview.tab("Drinks"), width=130, height=100, image=prime_img, compound="top", text="Brime\n$100", command=lambda: purchase_item("Brime", 100, self.scrollable_frame))
self.prime_button.grid(row=1, column=0, padx=30, pady=(10,0))
# Prime ----------------------------------------------------------------

# Cola ----------------------------------------------------------------
cola_img= customtkinter.CTkImage(Image.open("Images\crop_freeway_cola.png"), size=(100, 100))
self.cola_button = customtkinter.CTkButton(self.tabview.tab("Drinks"), width=130, height=100, image=cola_img, compound="top", text="Freeway Cola\n$2", command=lambda: purchase_item("cola", 2, self.scrollable_frame))
self.cola_button.grid(row=1, column=1, padx=30, pady=10)
# Cola ----------------------------------------------------------------

# King ----------------------------------------------------------------
king_img= customtkinter.CTkImage(Image.open("Images\corp_king.png"), size=(100, 100))
self.king_button = customtkinter.CTkButton(self.tabview.tab("Drinks"), width=130, height=100, image=king_img, compound="top", text="King\n50c", command=lambda: purchase_item("king", .5, self.scrollable_frame))
self.king_button.grid(row=1, column=2, padx=30, pady=10)
# King ----------------------------------------------------------------

# Bebsi ----------------------------------------------------------------
bebsi_img= customtkinter.CTkImage(Image.open("Images\crop_bebsi.png"), size=(100, 100))
self.king_button = customtkinter.CTkButton(self.tabview.tab("Drinks"), width=130, height=100, image=bebsi_img, compound="top", text="Bebsi\n$2.5", command=lambda: purchase_item("Bebsi", 2.5, self.scrollable_frame))
self.king_button.grid(row=2, column=0, padx=30, pady=10)
# Bebsi ----------------------------------------------------------------

# self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
# self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

self.mainloop()
