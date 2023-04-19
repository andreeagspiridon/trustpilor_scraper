import re
import tkinter as tk
import sqlite3
from tkinter import END

sql_path = "trustpilot.db"
with sqlite3.connect(sql_path) as db:
    cursor = db.cursor()
    print('Connected to db')
location = cursor.execute("""SELECT location FROM trustpilot_table""").fetchall()


class TrustPilotTK:
    def __init__(self, master):
        self.label2 = None
        self.label1 = None
        self.list2 = None
        self.entry2 = None
        self.service = None
        self.entry2_str = None
        self.value = None
        self.selected_item = None
        self.entry1_str = None
        self.entry1 = None
        self.loc = None
        self.list1 = None
        self.master = master
        self.render_main_page()

    @staticmethod
    def get_data(elements, entry_name, list_name):
        search_str = entry_name.get()  # user entered string
        list_name.delete(0, END)
        for element in elements:
            if re.search(search_str, element, re.IGNORECASE):
                list_name.insert(END, element.title())

    @staticmethod
    def search_item(widget_search, entry_name, list_name):
        selected_item = widget_search.widget
        index = int(selected_item.curselection()[0])
        selected_value = selected_item.get(index)
        entry_name.set(selected_value.title())
        list_name.delete(0, END)

    def render_main_page(self):
        self.master.resizable(False, False)
        self.master.title("UK services")
        self.master.eval("tk::PlaceWindow . center")  # place window at center of screen
        self.master.geometry('560x400')
        self.master.config(background="#B4B4EE")
        font1 = ('Times', 24, 'bold')
        font2 = ('Times', 20, 'bold')

        # Labels
        self.label1 = tk.Label(self.master, text="Select location", font=font2, bg="#B4B4EE", fg='black')
        self.label1.grid(row=0, column=1, padx=20, pady=5)
        self.label2 = tk.Label(self.master, text="Select services", font=font2, bg="#B4B4EE", fg='black')
        self.label2.grid(row=0, column=2, padx=20, pady=5)

        # Entry 1 - LOCATION
        self.entry1_str = tk.StringVar(self.master)
        self.loc = ['Select Location', 'Loc 1 ', 'Loc 2', 'Loc 3', 'Loc 101010']

        self.entry1 = tk.Entry(self.master, font=font1, textvariable=self.entry1_str)
        self.entry1.grid(row=1, column=1, padx=20,pady=5)
        self.list1 = tk.Listbox(self.master, height=6, font=font1, relief='flat',
                             bg="#B4B4EE", highlightcolor="#B4B4EE")
        self.list1.grid(row=2, column=1)

        self.entry1_str.trace('w', lambda *args:  self.get_data(self.loc,
                                                                self.entry1,
                                                                self.list1))
        self.list1.bind("<<ListboxSelect>>", lambda event: self.search_item(event,
                                                                            self.entry1_str,
                                                                            self.list1))

        # Entry 2 - SERVICES
        self.entry2_str = tk.StringVar(self.master)
        self.service = ['fitness', 'restaurant', 'spa', 'nail salon']
        self.entry2 = tk.Entry(self.master, font=font1, textvariable=self.entry2_str)
        self.entry2.grid(row=1, column=2)
        self.list2 = tk.Listbox(self.master, height=6, font=font1, relief='flat',
                                bg="#B4B4EE", highlightcolor="#B4B4EE")
        self.list2.grid(row=2, column=2)
        self.entry2_str.trace('w', lambda *args:  self.get_data(self.service,
                                                                self.entry2,
                                                                self.list2))
        self.list2.bind("<<ListboxSelect>>", lambda event: self.search_item(event,
                                                                            self.entry2_str,
                                                                            self.list2))


if __name__ == '__main__':
    root = tk.Tk()
    app = TrustPilotTK(root)
    root.mainloop()
