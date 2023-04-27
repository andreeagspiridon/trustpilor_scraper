import re
import tkinter as tk
import sqlite3
from tkinter import END

sql_path = "trustpilot.db"
with sqlite3.connect(sql_path) as db:
    cursor = db.cursor()
    print('Connected to db')
# location = cursor.execute("""SELECT location FROM trustpilot_table""").fetchall()


class TrustPilotTK:
    def __init__(self, master):
        self.list3 = None
        self.entry3 = None
        self.trust_score = None
        self.entry3_str = None
        self.services = None
        self.location = None
        self.label2 = None
        self.label1 = None
        self.list2 = None
        self.entry2 = None
        self.entry2_str = None
        self.value = None
        self.selected_item = None
        self.entry1_str = None
        self.entry1 = None
        self.list1 = None
        self.master = master
        self.render_main_page()

    @staticmethod
    def get_data(elements, entry_name, list_name):
        search_str = entry_name.get()  # string that the user enters
        list_name.delete(0, END)  # clear the content of the Entry widget in this range
        for element in elements:  # for each element in my list of elements
            if isinstance(element, float):
                element = str(element)
            if re.search(search_str, element, re.IGNORECASE):  # searches for all of the instances of the pattern in
                # the given string/ by contrast, .match will check if the pattern is found at the beginning of the string
                list_name.insert(END, element.title())  # display data, first parameter is the index position and the
                # second parameter is the info to be inserted

    @staticmethod
    def search_item(widget_search, entry_name, list_name):
        selected_item = widget_search.widget
        index = int(selected_item.curselection()[0])  # function used to fetch multiple values and display them
        selected_value = selected_item.get(index)  # get the value at the index position
        entry_name.set(selected_value.title())  # move the selected value at the entry box
        list_name.delete(0, END)


    def render_main_page(self):
        self.master.resizable(False, False)
        self.master.title("UK services")
        self.master.eval("tk::PlaceWindow . center")  # place window at center of screen
        self.master.geometry('700x400')
        self.master.config(background="#B4B4EE")
        font1 = ('Times', 20, 'bold')

        # Labels
        self.label1 = tk.Label(self.master, text="Select location", font=font1, bg="#B4B4EE", fg='black')
        self.label1.grid(row=0, column=1, padx=20, pady=5)
        self.label2 = tk.Label(self.master, text="Select services", font=font1, bg="#B4B4EE", fg='black')
        self.label2.grid(row=0, column=2, padx=20, pady=5)
        self.label3 = tk.Label(self.master, text="Select trust score", font=font1, bg="#B4B4EE", fg='black')
        self.label3.grid(row=0, column=3, padx=30, pady=5)



        # Entry 1 - LOCATION
        self.entry1_str = tk.StringVar(self.master)  # value holder for string variables and can be used for an
        # Entry/Label widget

        self.location = set([x[0] for x in cursor.execute("""SELECT location FROM trustpilot_table""").fetchall()])
        # returns a deduplicated list;(x[0] for x is used to return a list of elements, not a tuple

        self.entry1 = tk.Entry(self.master, font=font1, textvariable=self.entry1_str)
        self.entry1.grid(row=1, column=1, padx=20,pady=5)
        self.list1 = tk.Listbox(self.master, height=6, font=font1, relief='flat',
                             bg="#B4B4EE", highlightcolor="#B4B4EE")
        self.list1.grid(row=2, column=1)

        self.entry1_str.trace('w', lambda *args:  self.get_data(self.location,
                                                                self.entry1,
                                                                self.list1))
        # tracing the value of the Entry widget that gets updated when the user enters a value in it
        self.list1.bind("<<ListboxSelect>>", lambda event: self.search_item(event,
                                                                            self.entry1_str,
                                                                            self.list1))
        # execute the search_item function when the selected items in the listbox change


        # Entry 2 - SERVICES
        self.entry2_str = tk.StringVar(self.master)
        # self.service = ['fitness', 'restaurant', 'spa', 'nail salon']
        # query = "SELECT title FROM trustpilot_table WHERE services LIKE ?"
        # rez = cursor.execute(query, ("%{}%".format(self.entry2),))
        # self.services = set([x[0] for x in rez.fetchall()])

        self.services = set([x[0] for x in cursor.execute("""SELECT services FROM trustpilot_table""").fetchall()])

        self.entry2 = tk.Entry(self.master, font=font1, textvariable=self.entry2_str)
        self.entry2.grid(row=1, column=2)
        self.list2 = tk.Listbox(self.master, height=6, font=font1, relief='flat',
                                bg="#B4B4EE", highlightcolor="#B4B4EE")
        self.list2.grid(row=2, column=2)



        self.entry2_str.trace('w', lambda *args:  self.get_data(self.services,
                                                                self.entry2,
                                                                self.list2))
        self.list2.bind("<<ListboxSelect>>", lambda event: self.search_item(event,
                                                                            self.entry2_str,
                                                                            self.list2))

        # Entry 3 - TrustScore
        self.entry3_str = tk.StringVar(self.master)
        self.trust_score = set([x[0] for x in cursor.execute("""SELECT trust_score FROM trustpilot_table""").fetchall()])
        print(self.trust_score)

        self.entry3 = tk.Entry(self.master, width=10, font=font1, textvariable=self.entry3_str)
        self.entry3.grid(row=1, column=3)
        self.list3 = tk.Listbox(self.master, height=6, font=font1, relief='flat',
                                bg="#B4B4EE", highlightcolor="#B4B4EE")
        self.list3.grid(row=2, column=3)
        self.entry3_str.trace('w', lambda *args:  self.get_data(self.trust_score,
                                                                    self.entry3,
                                                                    self.list3))
        self.list3.bind("<<ListboxSelect>>", lambda event: self.search_item(event,
                                                                            self.entry3_str,
                                                                            self.list3))
        # TODO
        '''
        de adaugat un buton pentru returnarea rezultatului
        si de adaugat un textbox in care vor fi enumerate rezultatele in
        urma combinarii celor 3 entry-uri 
        '''




if __name__ == '__main__':
    root = tk.Tk()
    app = TrustPilotTK(root)
    root.mainloop()
