import re
import tkinter as tk
import sqlite3
from tkinter import END


class TrustPilotTK:
    def __init__(self, master):
        self.query_execute = None
        self.menu = None
        self.selected = None
        self.types = None
        self.result_box = None
        self.cursor = None
        self.location_get = None
        self.services_get = None
        self.trust_score_str = None
        self.services_str = None
        self.location_str = None
        self.trust_score = None
        self.services = None
        self.location = None
        self.label1 = None
        self.value = None
        self.selected_item = None
        self.entry1_str = None
        self.entry1 = None
        self.list1 = None
        self.master = master
        self.entry_dictionary = dict()
        self.render_main_page()

    @staticmethod
    def connect_to_database():
        sql_path = "trustpilot.db"
        db = sqlite3.connect(sql_path)
        cursor = db.cursor()
        return cursor

    """The get_data method is used to get the user input and searches for all of the instances
     of the pattern in the given string"""

    @staticmethod
    def get_data(elements, entry_name, list_name):
        search_str = entry_name.get()
        list_name.delete(0, END)
        for element in elements:
            if isinstance(element, float):
                element = str(element)
            if search_str and re.search(search_str, element, re.IGNORECASE):
                list_name.insert(END, element.title())

    """The search_item method is used to fetch multiple values and display them, get the selected item, and move it 
    to the entry box"""

    def search_item(self, widget_search, entry_name, list_name, dict_key=None):
        selected_item = widget_search.widget
        index = int(selected_item.curselection()[0])
        selected_value = selected_item.get(index)
        entry_name.set(selected_value.title())
        list_name.insert(0, selected_value)
        list_name.delete(0, END)
        if dict_key:
            self.entry_dictionary[dict_key] = selected_value

    def get_results(self):

        if self.menu_select() == 'location':
            query = "select distinct title,services,trust_score from trustpilot_table where location like ?"
            self.query_execute = self.cursor.execute(query, [self.entry_dictionary['query']]).fetchall()
            print(self.query_execute)
            return self.query_execute
        elif self.menu_select() == 'services':
            query = "select distinct title,location,trust_score from trustpilot_table where services like ?"
            self.query_execute = self.cursor.execute(query, [self.entry_dictionary['query']]).fetchall()
            print(self.query_execute)
            return self.query_execute
        elif self.menu_select() == 'trust_score':
            query = "select distinct title,location,services from trustpilot_table where trust_score like ?"
            self.query_execute = self.cursor.execute(query, [self.entry_dictionary['query']]).fetchall()
            print(self.query_execute)
            return self.query_execute

    def post_results(self):
        print(self.menu.get())
        results = self.get_results()
        self.result_box.insert(END, results)

    def clear_text(self):
        self.entry1.delete(0, END)
        self.result_box.delete("1.0", END)
        self.menu.set(self.types[0])

    def get_entry_list(self, entry):
        return set([str(x[0]) for x in self.cursor.execute(f"""SELECT {entry} FROM trustpilot_table""").fetchall()])

    def menu_select(self):
        return self.menu.get()

    def render_main_page(self):
        self.master.resizable(False, False)
        self.master.title("UK services")
        self.master.eval("tk::PlaceWindow . center")
        self.master.geometry('450x500')
        self.master.config(background="#B4B4EE")
        self.cursor = self.connect_to_database()
        font1 = ('Times', 20, 'bold')

        # dropdown menu
        self.label1 = tk.Label(self.master, text="Filter results by:", font=font1, bg="#B4B4EE", fg='black')
        self.label1.grid(row=0, column=1, padx=20, pady=5)
        self.types = ['Select', 'location', 'services', 'trust_score']
        self.menu = tk.StringVar()
        self.menu.set(self.types[0])
        dropdown_select = tk.OptionMenu(self.master, self.menu, *self.types)
        dropdown_select.grid(row=1, column=1)
        dropdown_select.config(width=15, height=2, bg="#B4B4EE", font=font1, fg='black')

        self.entry1_str = tk.StringVar(self.master)
        self.entry1 = tk.Entry(self.master, width=40, font=font1, textvariable=self.entry1_str)
        self.entry1.grid(row=2, column=1, padx=20, pady=5)

        self.selected = self.menu.get()
        self.list1 = tk.Listbox(self.master, width=40, height=6, font=font1, relief='flat',
                                bg="#B4B4EE", highlightcolor="#B4B4EE")
        self.list1.grid(row=3, column=1)

        """tracing the value of the Entry widget that gets updated when the user enters a value in it
        and executing the search_item function when the selected items in the listbox change"""
        self.entry1_str.trace('w', lambda *args: self.get_data(self.get_entry_list(self.menu_select()),
                                                               self.entry1,
                                                               self.list1))
        self.list1.bind("<<ListboxSelect>>", lambda event: self.search_item(event,
                                                                            self.entry1_str,
                                                                            self.list1,
                                                                            'query'))
        # Result
        self.result_box = tk.Text(root, height=10, width=60)
        self.result_box.grid(row=7, column=1, padx=10)

        # Buttons
        tk.Button(root, text="Submit", command=lambda: self.post_results(), bg="#B4B4EE").grid(row=5, column=1)
        tk.Button(root, text="Click Here to Reset", command=self.clear_text).grid(row=6, column=1)


if __name__ == '__main__':
    root = tk.Tk()
    app = TrustPilotTK(root)
    root.mainloop()
