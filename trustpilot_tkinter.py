import tkinter as tk
import sqlite3


sql_path = r"/trustpilot_scraper/trustpilot.db"
with sqlite3.connect(sql_path) as db:
    cursor = db.cursor()
    # print('connected to db')
location = cursor.execute("""SELECT location FROM trustpilot_table""").fetchall()
#print(len(location))

root = tk.Tk()
root.resizable(False, False)
root.title("UK services")
root.eval("tk::PlaceWindow . center")#place window at center of screen
# root.geometry('270x280')
# root.config(background="#B4B4EE")


# Datatype of menu text
menu = tk.StringVar()

# Initial menu text
menu.set("Select location")

# Create dropdown menu
drop_loc = tk.OptionMenu(root, menu, *location)
drop_loc.grid(row=1, column=1)






# greeting = tk.Label(text="Hello, Tkinter")  # widget added
# greeting.pack()  # widget packed into window as small as it can be while still fully encompassing the widget


root.mainloop()


