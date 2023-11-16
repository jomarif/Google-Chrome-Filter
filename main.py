import tkinter as tk
from tkinter import ttk
from random import choice, randint, uniform

import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ScrollOrigin, ActionChains

# global chrome

class Chrome:

    def __init__(self, link):
        self.link = link

        self.chrome_options = Options()

        self.chrome_options.add_argument('--no-sandbox') # Fixed the errors
        self.chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get("https://www.google.com/maps/@49.1536303,-123.1974596,12z/data=!4m3!11m2!2s4oTaOI5R8cNHCLk5gExkBrn-_NaRzw!3e3?entry=ttu")
        # driver.get("https://www.google.com/maps/@48.7726417,-122.499104,14z/data=!4m3!11m2!2sOpyHXndzMsUKQzcKciKrp8HNQM5AXA!3e3?entry=ttu")


        self.name = self.driver.find_elements(By.CLASS_NAME, "kiaEld")
        self.rating = self.driver.find_elements(By.XPATH, "//*[@class = 'U8T7xe']") # Using XPATH
        self.numOfReviews = self.driver.find_elements(By.CLASS_NAME, "ciA11e")

        self.index = 0
        self.list1 = []


        try:
            # while True: # Actual
            while self.index < 10: # DEBUG SO THAT IT DOESN'T GO OVER

                print(f"Name {self.index}: {self.name[self.index].text}.", end = ' ')
                print(f"Rating: {self.rating[self.index].text}.", end = ' ')
                print(f"Num. of Reviews: {self.numOfReviews[self.index].text}.")

                self.list1.append([self.name[self.index].text, self.rating[self.index].text, self.numOfReviews[self.index].text])
                # (Name, Rating, Number of Reviews)

                self.index += 1

                if self.index % 19 == 0:
                    # oldName = name
                    # oldRating = rating

                    self.scroll_origin = ScrollOrigin.from_element(self.name[self.index])
                    ActionChains(self.driver).scroll_from_origin(self.scroll_origin, 0, 1000).perform()
                    time.sleep(8)

                    # re-initialize the name and rating of the two
                    self.name = self.driver.find_elements(By.CLASS_NAME, "kiaEld")
                    self.rating = self.driver.find_elements(By.XPATH, "//*[@class = 'U8T7xe']")
                    self.numOfReviews = self.driver.find_elements(By.CLASS_NAME, "ciA11e")

                if self.name[self.index] == None: # This code had to make me use an try except, other wise it wouldn't just take it. Because it is out of range it would just crash
                    break

                time.sleep(0.1)

        except: # since out of range before it would just crash, look into this more
            print("End of list")


        # REMOVE BRACKETS AND COMMAS FROM STRING
        # CONVERT STRING INTO INTEGERS
        self.counter = 0
        self.listNumOfRev = []
        self.listRating = []
        self.newList = []

        while self.counter < self.index: 
            self.textnumOfReviews = self.list1[self.counter][2]
            self.textnumOfReviews = self.textnumOfReviews.replace('(' , "").replace(')' , "").replace(",", '')
            self.listNumOfRev.append(int(self.textnumOfReviews))
            self.listRating.append(float(self.list1[self.counter][1]))

            self.newList.append([self.list1[self.counter][0], self.listRating[self.counter], self.listNumOfRev[self.counter]])

            self.counter += 1

    def getInformation(self):
        return self.newList

    def getNames(self):
        return self.newList[:][0]

    def getRatings(self):
        return self.newList[:][1]

    def getNumOfReviews(self):
        return self.newList[:][2]

    def sortRating(self):
        return self.newList.sort(key=lambda x: x[1], reverse = True)

    def sortReviews(self):
        return self.newList.sort(key=lambda x: x[2], reverse = True)

    def printList(self):
        for i in self.newList:
            print(f"{i[:][2]} | {i[:][0]} | {i[:][1]}")
            time.sleep(0.01)
        print("")

    def makeCSV(self):
        try: 
            dataframe = pd.DataFrame(self.newList)
            headerList = ["Name Of Restaurant", "Rating", "Number of Reviews"]
            dataframe.to_csv("/Users/jfrancisco/Desktop/Code/Scrape/InformationClass.csv", index = False, header = headerList)
            print("CSV file created...\n")
        except:
            print("Couldn't make CSV file...\n")



class GUI():

    def __init__(self):

        self.window = tk.Tk()
        # chrome = Chrome('TEST')

        # Initialize Tkinter
        self.window.title('Google Maps Filter')
        self.window.geometry('600x400')
        self.window.minsize(600, 400)
        self.window.maxsize(600, 400)

    # widgets

    # Entry
    def createWidgets(self):
        self.entryLinkStringVar = tk.StringVar() # This is the string of the link
        entryLink = ttk.Entry(self.window, textvariable = self.entryLinkStringVar)
        entryLink.bind('<Return>', self.getData)

        enterLinkLabel = ttk.Label(self.window, textvariable = self.entryLinkStringVar)

        # Menu
        menu = tk.Menu(self.window)
        fileMenu = tk.Menu(menu, tearoff = False)

        # Sort Widgets
        sortFrame = ttk.Frame(self.window)
        sortNameButton = ttk.Button(sortFrame, text = 'Sort by Name', command = self.sortByName)
        sortRatingButton = ttk.Button(sortFrame, text = 'Sort by Rating', command = self.sortByRatingTable)
        sortReviewButton = ttk.Button(sortFrame, text = 'Sort by Review', command = self.sortByReviewsTable)

        # Treeview
        self.table = ttk.Treeview(self.window, columns = ('Name', 'Rating', 'Review'), show = 'headings')
        self.table.heading('Name', text = 'Name')
        self.table.heading('Rating', text = 'Rating')
        self.table.heading('Review', text = 'Number Of Reviews')


        #####################
        # Arranging widgets #
        #####################

        # Menu
        menu.add_cascade(label = 'File', menu = fileMenu)
        fileMenu.add_command(label = 'Export to Excel', command = lambda: print('Exporting to Excel...'))
        self.window.configure(menu = menu)

        # Link
        enterLinkLabel.pack()
        entryLink.pack(padx = 50, fill = 'x')

        # Sort Buttons
        sortFrame.pack(fill = 'both', padx = 20, pady = 5)
        sortNameButton.pack(side = 'left', expand = True, fill = 'both', padx = 1)
        sortRatingButton.pack(side = 'left', expand = True, fill = 'both', padx = 1)
        sortReviewButton.pack(side = 'left', expand = True, fill = 'both', padx = 1)

        # Table
        self.table.pack(expand = True, fill = 'both')

    def getData(self, _): # https://stackoverflow.com/questions/23842770/python-function-takes-1-positional-argument-but-2-were-given-how
        self.chromeCall = Chrome(self.entryLinkStringVar.get())
        # self.entryLinkStringVar(value ='Link entered. Enter another one to get retrieve more information')
        self.packInTreeview()
        

    def packInTreeview(self):
        self.clearTreeview() # Clear anything else in the treeview
        self.informationOfRestaurants = self.chromeCall.getInformation()
        for i in self.informationOfRestaurants:
            name = i[:][0]
            rating = i[:][1]
            numOfReviews = i[:][2]
            data = (name, rating, numOfReviews)
            self.table.insert(parent = '', index = tk.END, values = data)

    def sortByRatingTable(self):
        self.clearTreeview() # Clear anything else in the treeview
        # self.informationOfRestaurants = self.chromeCall.sortRating() # WHY DOESN"T THIS WORK
        self.informationOfRestaurants.sort(key=lambda x: x[1], reverse = True)
        for i in self.informationOfRestaurants:
            name = i[:][0]
            rating = i[:][1]
            numOfReviews = i[:][2]
            data = (name, rating, numOfReviews)
            self.table.insert(parent = '', index = tk.END, values = data)

    def sortByReviewsTable(self):
        self.clearTreeview() # Clear anything else in the treeview
        self.informationOfRestaurants.sort(key=lambda x: x[2], reverse = True)
        for i in self.informationOfRestaurants:
            name = i[:][0]
            rating = i[:][1]
            numOfReviews = i[:][2]
            data = (name, rating, numOfReviews)
            self.table.insert(parent = '', index = tk.END, values = data)

    def sortByName(self):
        self.clearTreeview() # Clear anything else in the treeview
        self.informationOfRestaurants.sort(key=lambda x: x[0], reverse = False)
        for i in self.informationOfRestaurants:
            name = i[:][0]
            rating = i[:][1]
            numOfReviews = i[:][2]
            data = (name, rating, numOfReviews)
            self.table.insert(parent = '', index = tk.END, values = data)


    # Clears all of the items in the table
    def clearTreeview(self):
        for item in self.table.get_children():
            self.table.delete(item)
            

if __name__ == "__main__":
    gui = GUI()
    gui.createWidgets() # Create the widgets of the GUI

    gui.window.mainloop()
    