""""Create a python GUI for Game inventory system. Create buttons and functions for searchGame, UpdataGame , ViewAll , AddGame, LogIn (users should login with a userName and Password to access the system).

"""
from tabulate import tabulate
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

conn = sqlite3.connect('gameInventory.db')
c = conn.cursor()
# Create table
c.execute('''CREATE TABLE IF NOT EXISTS users
             (userName text  PRIMARY KEY, password varchar, EmployeeId integer REFERENCES employees(id))''')

c.execute('''CREATE TABLE IF NOT EXISTS games
             (name text, price real, quantity integer, id integer PRIMARY KEY, categoryID integer, description text)''')

c.execute('''CREATE TABLE  IF NOT EXISTS employees
             (id integer PRIMARY KEY, fname text, lname text, role text, email varchar, phone integer)''')

c.execute('''CREATE TABLE IF NOT EXISTS categories
             (id integer PRIMARY KEY, name text, description text)''')
c.execute('''CREATE TABLE IF NOT EXISTS zip
             (zipcode integer PRIMARY KEY, city text, state text)''')

#insert values into the tables
c.execute("INSERT or REPLACE into users VALUES ('admin1', 'water', 1)")
c.execute("INSERT or REPLACE into users VALUES ('admin2', 'password', 2)")
c.execute("INSERT or REPLACE into games VALUES ('GTA V', 50, 100, 1, 1, 'Action')")
c.execute("INSERT or REPLACE into games VALUES ('FIFA 18', 20, 18, 2, 1, 'Sports')")
c.execute("INSERT or REPLACE into games VALUES ('NBA 2K18', 30, 22, 3, 1, 'Sports')")
c.execute("INSERT or REPLACE into games VALUES ('Call of Duty: WWII', 45, 40, 4, 1, 'Shooter')")
c.execute("INSERT or REPLACE into games VALUES ('Assassin''s Creed: Origins', 36, 50, 5, 1, 'RPG')")
c.execute("INSERT or REPLACE into games VALUES ('Destiny 2', 60, 80, 6, 1, 'RPG')")
c.execute("INSERT or REPLACE into games VALUES ('Wolfenstein II: The New Colossus', 15, 4, 7, 1, 'Shooter')")
c.execute("INSERT or REPLACE into games VALUES ('The Evil Within 2', 22, 16, 8, 1, 'Horror')")
c.execute("INSERT or REPLACE into games VALUES ('Middle-earth: Shadow of War', 54, 2, 9, 1, 'RPG')")
c.execute("INSERT or REPLACE into games VALUES ('Need for Speed: Payback', 10, 1, 10, 1, 'Racing')")
c.execute("INSERT or REPLACE into games VALUES ('Forza Motorsport 7', 60, 10, 11, 1, 'Racing')")
c.execute("INSERT or REPLACE into games VALUES ('Super Mario Odyssey', 60, 60, 12, 1, 'Platformer')")
c.execute("INSERT or REPLACE into games VALUES ('The Legend of Zelda: Breath of the Wild', 60, 40, 13, 1, 'Action')")
c.execute("INSERT or REPLACE into games VALUES ('Horizon Zero Dawn', 35, 17, 14, 1, 'Action')")
c.execute("INSERT or REPLACE into games VALUES ('Uncharted: The Lost Legacy', 30, 37, 15, 1, 'Action')")
c.execute("INSERT or REPLACE into games VALUES ('Crash Bandicoot N. Sane Trilogy', 40, 71, 16, 1, 'Platformer')")
c.execute("INSERT or REPLACE into games VALUES ('Nioh', 44, 10, 17, 1, 'RPG')")
c.execute("INSERT or REPLACE into games VALUES ('Persona 5', 25, 23, 18, 1, 'RPG')")
c.execute("INSERT or REPLACE into games VALUES ('Nier: Automata', 15, 14, 19, 1, 'RPG')")
c.execute("INSERT or REPLACE into games VALUES ('Resident Evil 7: Biohazard', 10, 3, 20, 1, 'Horror')")
c.execute("INSERT or REPLACE into games VALUES ('The Witcher 3: Wild Hunt', 24, 60, 21, 1, 'RPG')")
c.execute("INSERT or REPLACE into employees VALUES (1, 'admin', 'admin', 'admin', 'admin@admin.com', 1234567890)")
c.execute("INSERT or REPLACE into categories VALUES (1, 'Action', 'Action')")
c.execute("INSERT or REPLACE into zip VALUES (12345, 'New York', 'NY')")
conn.commit()


class Login:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        self.userName = StringVar()
        self.password = StringVar()
        self.lbl_userName = Label(self.frame, text="User Name: ")
        self.lbl_userName.grid(row=0, column=0, sticky=W)
        self.lbl_password = Label(self.frame, text="Password: ")
        self.lbl_password.grid(row=1, column=0, sticky=W)
        self.entry_userName = Entry(self.frame, textvariable=self.userName)
        self.entry_userName.grid(row=0, column=1)
        self.entry_password = Entry(self.frame, textvariable=self.password)
        self.entry_password.grid(row=1, column=1)
        self.btn_login = Button(self.frame, text="Login", command=self.login)
        self.btn_login.grid(row=2, column=1, sticky=E)

    def login(self):
        userName = self.userName.get()
        password = self.password.get()
        c.execute(("SELECT * FROM users WHERE userName = ?"), (userName,))
        result = c.fetchone()
        c.execute(("SELECT * FROM users WHERE password = ?"), (password,))
        result2 = c.fetchone()

        if (result and result2)and(result[1] == result2[1]):
            self.newWindow = Toplevel(self.master)
            self.app = Main(self.newWindow)
        else:
            messagebox.showerror("Login error", "Incorrect username or password")


class Main:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        self.btn_searchGame = Button(self.frame, text="Search Game", command=self.searchGame)
        self.btn_searchGame.grid(row=0, column=0, sticky=W)
        self.btn_updateGame = Button(self.frame, text="Update Game", command=self.updateGame)
        self.btn_updateGame.grid(row=1, column=0, sticky=W)
        self.btn_viewAll = Button(self.frame, text="View All", command=self.viewAll)
        self.btn_viewAll.grid(row=2, column=0, sticky=W)
        self.btn_addGame = Button(self.frame, text="Add Game", command=self.addGame)
        self.btn_addGame.grid(row=3, column=0, sticky=W)
        self.btn_deleteGame = Button(self.frame, text="Delete Game", command=self.deleteGame)
        self.btn_deleteGame.grid(row=4, column=0, sticky=W)
        self.btn_flagGame = Button(self.frame, text="Flag Game", command=self.flagGame)
        self.btn_flagGame.grid(row=5, column=0, sticky=W)
        self.btn_dataAnalytics = Button(self.frame, text="Data Analytics", command=self.dataAnalytics)
        self.btn_dataAnalytics.grid(row=6, column=0, sticky=W)
        self.btn_logOut = Button(self.frame, text="Log Out", command=self.logOut)
        self.btn_logOut.grid(row=7, column=0, sticky=W)

    def searchGame(self):
        self.newWindow = Toplevel(self.master)
        self.app = SearchGame(self.newWindow)

    def updateGame(self):
        self.newWindow = Toplevel(self.master)
        self.app = UpdateGame(self.newWindow)

    def viewAll(self):
        self.newWindow = Toplevel(self.master)
        self.app = ViewAll(self.newWindow)

    def addGame(self):
        self.newWindow = Toplevel(self.master)
        self.app = AddGame(self.newWindow)

    def deleteGame(self):
        self.newWindow = Toplevel(self.master)
        self.app = DeleteGame(self.newWindow)

    def flagGame(self):
        self.newWindow = Toplevel(self.master)
        self.app = FlagGame(self.newWindow)

    def dataAnalytics(self):
        self.newWindow = Toplevel(self.master)
        self.app = DataAnalytics(self.newWindow)

    def logOut(self):
        self.master.destroy()



class SearchGame:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        self.gameName = StringVar()
        self.lbl_gameName = Label(self.frame, text="Game Name: ")
        self.lbl_gameName.grid(row=0, column=0, sticky=W)
        self.entry_gameName = Entry(self.frame, textvariable=self.gameName)
        self.entry_gameName.grid(row=0, column=1)
        self.btn_search = Button(self.frame, text="Search", command=self.search)
        self.btn_search.grid(row=1, column=1, sticky=E)
        self.btn_back = Button(self.frame, text="Back", command=self.back)
        self.btn_back.grid(row=1, column=0, sticky=W)

    def search(self):
        gameName = self.gameName.get()
        c.execute("SELECT * FROM games WHERE name = ?", (gameName,))
        result = c.fetchall()
        print(result)
        if result:
            self.newWindow = Toplevel(self.master)
            self.app = SearchResult(self.newWindow, tabulate(result, headers=['Name', 'Price', "Quantity", "ID", "Category ID", "Description"], tablefmt='psql'))
        else:
            messagebox.showerror("Search error", "Game not found")

    def back(self):
        self.master.destroy()

class SearchResult:
    def __init__(self, master, result):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        self.lbl_result = Label(self.frame, text=result)
        self.lbl_result.grid(row=0, column=0, sticky=W)
        self.btn_back = Button(self.frame, text="Back", command=self.back)
        self.btn_back.grid(row=1, column=0, sticky=W)

    def back(self):
        self.master.destroy()


class UpdateGame:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        self.gameName = StringVar()
        self.gamePrice = StringVar()
        self.gameQuantity = StringVar()
        self.gameCategory = StringVar()
        self.gameDescription = StringVar()
        self.lbl_gameName = Label(self.frame, text="Game Name: ")
        self.lbl_gameName.grid(row=0, column=0, sticky=W)
        self.lbl_gamePrice = Label(self.frame, text="Game Price: ")
        self.lbl_gamePrice.grid(row=1, column=0, sticky=W)
        self.lbl_gameQuantity = Label(self.frame, text="Game Quantity: ")
        self.lbl_gameQuantity.grid(row=2, column=0, sticky=W)
        self.lbl_gameCategory = Label(self.frame, text="Game Category: ")
        self.lbl_gameCategory.grid(row=3, column=0, sticky=W)
        self.lbl_gameDescription = Label(self.frame, text="Game Description: ")
        self.lbl_gameDescription.grid(row=4, column=0, sticky=W)
        self.entry_gameName = Entry(self.frame, textvariable=self.gameName)
        self.entry_gameName.grid(row=0, column=1)
        self.entry_gamePrice = Entry(self.frame, textvariable=self.gamePrice)
        self.entry_gamePrice.grid(row=1, column=1)
        self.entry_gameQuantity = Entry(self.frame, textvariable=self.gameQuantity)
        self.entry_gameQuantity.grid(row=2, column=1)
        self.entry_gameCategory = Entry(self.frame, textvariable=self.gameCategory)
        self.entry_gameCategory.grid(row=3, column=1)
        self.entry_gameDescription = Entry(self.frame, textvariable=self.gameDescription)
        self.entry_gameDescription.grid(row=4, column=1)
        self.btn_update = Button(self.frame, text="Update", command=self.update)
        self.btn_update.grid(row=5, column=1, sticky=E)
        self.btn_back = Button(self.frame, text="Back", command=self.back)
        self.btn_back.grid(row=5, column=0, sticky=W)

    def update(self):
        gameName = self.gameName.get()
        gamePrice = self.gamePrice.get()
        gameQuantity = self.gameQuantity.get()
        gameCategory = self.gameCategory.get()
        gameDescription = self.gameDescription.get()
        c.execute("SELECT * FROM games WHERE name = ?", (gameName,))
        result = c.fetchone()
        if result:
            c.execute("UPDATE games SET price = ?, quantity = ?, categoryID = ?, description = ? WHERE name = ?",
                      (gamePrice, gameQuantity, gameCategory, gameDescription, gameName))
            conn.commit()
            messagebox.showinfo("Update info", "Game updated")
        else:
            messagebox.showerror("Update error", "Game not found")

    def back(self):
        self.master.destroy()
class ViewAll:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        self.btn_view = Button(self.frame, text="View", command=self.view)
        self.btn_view.grid(row=0, column=1, sticky=W)
        self.btn_back = Button(self.frame, text="Back", command=self.back)
        self.btn_back.grid(row=0, column=0, sticky=W)

    def view(self):
        c.execute("SELECT * FROM games")
        result = c.fetchall()
        if result:
            self.newWindow = Toplevel(self.master)
            self.app = ViewResult(self.newWindow, tabulate(result, headers=['Name', 'Price', "Quantity", "ID", "Category ID", "Description"], tablefmt="psql"))
            print(tabulate(result, headers=['Name', 'Price', "Quantity", "ID", "Category ID", "Description"], tablefmt="psql"))
        else:
            messagebox.showerror("View error", "No games found")

    def back(self):
        self.master.destroy()

class ViewResult:
    def __init__(self, master, result):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        self.lbl_result = Label(self.frame, text=result)
        self.lbl_result.grid(row=0, column=0, sticky=W)
        self.btn_back = Button(self.frame, text="Back", command=self.back)
        self.btn_back.grid(row=1, column=0, sticky=W)

    def back(self):
        self.master.destroy()



class AddGame:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        self.gameName = StringVar()
        self.gamePrice = StringVar()
        self.gameQuantity = StringVar()
        self.gameid = StringVar()
        self.gameCategory = StringVar()
        self.gameDescription = StringVar()
        self.lbl_gameName = Label(self.frame, text="Game Name: ")
        self.lbl_gameName.grid(row=0, column=0, sticky=W)
        self.lbl_gamePrice = Label(self.frame, text="Game Price: ")
        self.lbl_gamePrice.grid(row=1, column=0, sticky=W)
        self.lbl_gameQuantity = Label(self.frame, text="Game Quantity: ")
        self.lbl_gameQuantity.grid(row=2, column=0, sticky=W)
        self.lbl_gameid = Label(self.frame, text="Game id: ")
        self.lbl_gameid.grid(row=3, column=0, sticky=W)
        self.lbl_gameCategory = Label(self.frame, text="Game Category: ")
        self.lbl_gameCategory.grid(row=4, column=0, sticky=W)
        self.lbl_gameDescription = Label(self.frame, text="Game Description: ")
        self.lbl_gameDescription.grid(row=5, column=0, sticky=W)
        self.entry_gameName = Entry(self.frame, textvariable=self.gameName)
        self.entry_gameName.grid(row=0, column=1)
        self.entry_gamePrice = Entry(self.frame, textvariable=self.gamePrice)
        self.entry_gamePrice.grid(row=1, column=1)
        self.entry_gameQuantity = Entry(self.frame, textvariable=self.gameQuantity)
        self.entry_gameQuantity.grid(row=2, column=1)
        self.entry_gameid = Entry(self.frame, textvariable=self.gameid)
        self.entry_gameid.grid(row=3, column=1)
        self.entry_gameCategory = Entry(self.frame, textvariable=self.gameCategory)
        self.entry_gameCategory.grid(row=4, column=1)
        self.entry_gameDescription = Entry(self.frame, textvariable=self.gameDescription)
        self.entry_gameDescription.grid(row=5, column=1)
        self.btn_add = Button(self.frame, text="Add", command=self.add)
        self.btn_add.grid(row=6, column=1, sticky=E)
        self.btn_back = Button(self.frame, text="Back", command=self.back)
        self.btn_back.grid(row=6, column=0, sticky=W)

    def add(self):
        gameName = self.gameName.get()
        gamePrice = self.gamePrice.get()
        gameQuantity = self.gameQuantity.get()
        gameid = self.gameid.get()
        gameCategory = self.gameCategory.get()
        gameDescription = self.gameDescription.get()
        c.execute("SELECT * FROM games WHERE name = ?", (gameName,))
        result = c.fetchone()
        if result:
            messagebox.showerror("Add error", "Game already exists")
        else:
            c.execute("INSERT INTO games VALUES (?, ?, ?, ?, ?, ?)",
                      (gameName, gamePrice, gameQuantity, gameid, gameCategory, gameDescription))
            conn.commit()
            messagebox.showinfo("Add info", "Game added")

    def back(self):
        self.master.destroy()

class DeleteGame:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        self.gameName = StringVar()
        self.lbl_gameName = Label(self.frame, text="Game Name: ")
        self.lbl_gameName.grid(row=0, column=0, sticky=W)
        self.entry_gameName = Entry(self.frame, textvariable=self.gameName)
        self.entry_gameName.grid(row=0, column=1)
        self.btn_delete = Button(self.frame, text="Delete", command=self.delete)
        self.btn_delete.grid(row=1, column=1, sticky=E)
        self.btn_back = Button(self.frame, text="Back", command=self.back)
        self.btn_back.grid(row=1, column=0, sticky=W)


    def delete(self):
        gameName = self.gameName.get()
        c.execute("SELECT * FROM games WHERE name = ?", (gameName,))
        result = c.fetchall()
        if result:
            c.execute("DELETE FROM games WHERE name = ?", (gameName,))
            conn.commit()
            messagebox.showinfo("Delete info", "Game deleted")
        else:
            messagebox.showerror("Delete error", "Game not found")

    def back(self):
        self.master.destroy()

class FlagGame:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        self.btn_flagGame = Button(self.frame, text="Flagged Games", command=self.flagGame)
        self.btn_flagGame.grid(row=0, column=0, sticky=W)
        self.btn_back = Button(self.frame, text="Back", command=self.back)
        self.btn_back.grid(row=1, column=0, sticky=W)

    def flagGame(self):
        c.execute("SELECT * FROM games WHERE quantity < 20")
        results = c.fetchall()
        if results:
            self.newWindow = Toplevel(self.master)
            self.app = ViewResult(self.newWindow, tabulate(results, headers=['Name', 'Price', "Quantity", "ID", "Category ID", "Description"], tablefmt='psql'))

    def back(self):
        self.master.destroy()


class DataAnalytics:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        self.btn_dataAnalytics = Button(self.frame, text="Count Plot: Number of Games", command=self.dataAnalytics)
        self.btn_dataAnalytics.grid(row=0, column=0, sticky=W)
        self.btn_dataAnalytics2 = Button(self.frame, text="Pie Chart: Genres", command=self.dataAnalytics2)
        self.btn_dataAnalytics2.grid(row=1, column=0, sticky=W)
        self.btn_back = Button(self.frame, text="Back", command=self.back)
        self.btn_back.grid(row=2, column=0, sticky=W)

    def dataAnalytics(self):
        c.execute("SELECT * FROM games")
        result = c.fetchall()

        game_name = []
        game_quantity = []

        for i in result:
            game_name.append(i[0])
            game_quantity.append(i[2])

        print("Name of Game = ", game_name)
        print("Quantity of Games = ", game_quantity)

        # Visulizing Data using Matplotlib
        plt.figure(figsize=(40, 3), dpi=100)
        plt.bar(game_name, game_quantity)
        plt.ylim(0, 105)
        plt.xlim(0, 20)
        plt.xlabel("Games")
        plt.ylabel("Quantity")
        plt.title("Number of Games")
        plt.show()

    def dataAnalytics2(self):
        c.execute("SELECT * FROM games")
        result = c.fetchall()

        game_desc = []

        for i in result:
            game_desc.append(i[-1])

        action = 0
        horror = 0
        rpg = 0
        racing = 0
        platformer = 0
        shooter = 0
        sports = 0

        for genre in game_desc:
            if genre == "Action":
                action += 1
            if genre == "Horror":
                horror += 1
            if genre == "RPG":
                rpg += 1
            if genre == "Shooter":
                shooter += 1
            if genre == "Platformer":
                platformer += 1
            if genre == "Sports":
                sports += 1
            if genre == "Racing":
                racing += 1

        genre_array = np.array([action, horror, rpg, racing, shooter, platformer, sports])
        mylabels = ["Action", "Horror", "RPG", "Racing", "Shooter", "Platformer", "Sports"]
        mycolors = ["Red", "Blue", "Green", "Purple", "Pink", "Yellow", "Brown"]
        plt.title("Genre Pie Chart")
        plt.pie(genre_array, labels=mylabels, colors=mycolors)
        plt.show()

    def back(self):
        self.master.destroy()

def main():
    root = Tk()
    root.title("Game Inventory System")
    root.geometry("600x450")
    app = Login(root)
    root.mainloop()

if __name__ == '__main__':
    main()

