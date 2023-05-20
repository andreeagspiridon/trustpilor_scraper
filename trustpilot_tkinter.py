import re
import tkinter as tk
import sqlite3
from tkinter import END

class TrustPilotTK:
    def __init__(self, master):
        self.result_box = None
        self.cursor = None
        self.trustscore_get = None
        self.location_get = None
        self.services_get = None
        self.trust_score_str = None
        self.services_str = None
        self.location_str = None
        self.label3 = None
        self.entry4 = None
        self.label4 = None
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
        self.list1_value = None
        self.master = master
        self.all_dict_lists = dict()
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
            if re.search(search_str, element, re.IGNORECASE):
                list_name.insert(END, element.title())

    """The search_item method is used to fetch multiple values and display them, get the slected item, and move it 
    to the entry box"""
    def search_item(self, widget_search, entry_name, list_name, dict_key=None):
        selected_item = widget_search.widget
        index = int(selected_item.curselection()[0])
        selected_value = selected_item.get(index)
        entry_name.set(selected_value.title())
        list_name.delete(0, END)
        if dict_key:
            self.all_dict_lists[dict_key] = selected_value

    def get_results(self, loc, score, serv):
        # query = "SELECT title FROM trustpilot_table WHERE location = ? AND trust_score = ? AND services LIKE ?"
        # query1 = "select distinct * from trustpilot_table where location = ? AND trust_score = ? AND services IN ({seq})"
        # serv_query = ','.join(["?"] * len(serv.split(',')))
        # query1 = query1.format(seq=serv_query)
        # print(query1)
        # self.result = self.cursor.execute(query1, (loc, float(score)) + tuple(serv.split(','))).fetchall()
        # print(self.result)
        # query = "select * from trustpilot_table where services in ({seq})"
        query = "select distinct title from trustpilot_table where services like ?"
        execute_query = self.cursor.execute(query, [self.all_dict_lists['list2']]).fetchall()
        # query = query.format(seq=serv_query)
        print(execute_query)
        print(query)

        # self.result = self.cursor.execute(query, servs).fetchall()
        # print(self.result)

        # serv = serv.replace('[', '').replace(']', '').replace('"', '')
        # serv = ', '.join([x.strip() for x in serv.split(',')])
        # print(serv)
        # query1 = query1 % ', '.join(['?']*len(serv.split(',')))
        # serv2 = ','.join(['?']*len(serv.split(',')))
        # print(serv2)
        # serv = serv.split(',')
        # print(serv)
        # self.result = self.cursor.execute(query1, serv).fetchall()
        # print(self.result)
        # self.result = [element[0] for element in self.result]
        # print(self.result)
        return execute_query

    def post_results(self):
        self.location_get = self.all_dict_lists.get('list1')
        self.services_get = self.all_dict_lists.get('list2')
        self.trustscore_get = self.all_dict_lists.get('list3')

        final_result = self.get_results(self.location_get, self.trustscore_get, self.services_get)
        self.result_box.insert(tk.END, final_result)

    def clear_text(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)


    def render_main_page(self):
        self.master.resizable(False, False)
        self.master.title("UK services")
        self.master.eval("tk::PlaceWindow . center")
        self.master.geometry('900x450')
        self.master.config(background="#B4B4EE")
        self.cursor = self.connect_to_database()
        font1 = ('Times', 20, 'bold')

        # Labels
        self.label1 = tk.Label(self.master, text="Select location", font=font1, bg="#B4B4EE", fg='black')
        self.label1.grid(row=0, column=1, padx=20, pady=5)

        self.label2 = tk.Label(self.master, text="Select services", font=font1, bg="#B4B4EE", fg='black')
        self.label2.grid(row=0, column=2, padx=20, pady=5)

        self.label3 = tk.Label(self.master, text="Select trust score", font=font1, bg="#B4B4EE", fg='black')
        self.label3.grid(row=0, column=4, padx=30, pady=5)

        self.label4 = tk.Label(self.master, text="Result:", font=font1, bg="#B4B4EE", fg='black')
        self.label4.grid(row=6, column=1, padx=5, pady=5)

        # Entry 1 - LOCATION
        self.entry1_str = tk.StringVar(self.master)

        """return a deduplicated list;(x[0] for x is used to return a list of elements, not a tuple"""
        self.location = set([x[0] for x in self.cursor.execute("""SELECT location FROM trustpilot_table""").fetchall()])
        self.location = list(self.location)

        self.entry1 = tk.Entry(self.master, font=font1, textvariable=self.entry1_str)
        self.entry1.grid(row=1, column=1, padx=20,pady=5)
        self.list1 = tk.Listbox(self.master, height=6, font=font1, relief='flat',
                             bg="#B4B4EE", highlightcolor="#B4B4EE")
        self.list1.grid(row=2, column=1)

        """tracing the value of the Entry widget that gets updated when the user enters a value in it
        and executing the search_item function when the selected items in the listbox change"""
        self.entry1_str.trace('w', lambda *args:  self.get_data(self.location,
                                                                self.entry1,
                                                                self.list1))
        self.list1.bind("<<ListboxSelect>>", lambda event: self.search_item(event,
                                                                            self.entry1_str,
                                                                            self.list1,
                                                                            'list1'))


        # Entry 2 - SERVICES
        self.entry2_str = tk.StringVar(self.master)
        self.services = set([x[0] for x in self.cursor.execute("""SELECT services FROM trustpilot_table""").fetchall()])
        self.services = list(self.services)

        self.entry2 = tk.Entry(self.master, width=30, font=font1, textvariable=self.entry2_str)
        self.entry2.grid(row=1, column=2)
        self.list2 = tk.Listbox(self.master, width=30, height=6, font=font1, relief='flat',
                                bg="#B4B4EE", highlightcolor="#B4B4EE")
        self.list2.grid(row=2, column=2)

        self.entry2_str.trace('w', lambda *args:  self.get_data(self.services,
                                                                self.entry2,
                                                                self.list2))
        self.list2.bind("<<ListboxSelect>>", lambda event: self.search_item(event,
                                                                            self.entry2_str,
                                                                            self.list2,
                                                                            'list2'))


        # Entry 3 - TrustScore
        self.entry3_str = tk.StringVar(self.master)
        self.trust_score = set([str(x[0]) for x in self.cursor.execute("""SELECT trust_score FROM trustpilot_table""").fetchall()])
        # self.trust_score_str = '? '.join(self.trust_score)

        self.entry3 = tk.Entry(self.master, width=10, font=font1, textvariable=self.entry3_str)
        self.entry3.grid(row=1, column=4)
        self.list3 = tk.Listbox(self.master, height=6, font=font1, relief='flat',
                                bg="#B4B4EE", highlightcolor="#B4B4EE")
        self.list3.grid(row=2, column=4)
        self.entry3_str.trace('w', lambda *args:  self.get_data(self.trust_score,
                                                                    self.entry3,
                                                                    self.list3))
        self.list3.bind("<<ListboxSelect>>", lambda event: self.search_item(event,
                                                                            self.entry3_str,
                                                                            self.list3,
                                                                            'list3'))



        #Result
        self.result_box = tk.Text(root, height=9, width=60)
        self.result_box.grid(row=6, column=2)

        B = tk.Button(root, text="Submit", command=lambda: self.post_results(), bg="#B4B4EE").grid(row=4, column=2)
        ResetB = tk.Button(root, text="Click Here to Reset", command=self.clear_text).grid(row=5, column=2)
        # # query = """SELECT title FROM trustpilot_table WHERE location = ? AND services = ? AND trust_score = ?"""
        # # query = """SELECT title FROM trustpilot_table WHERE location IN (%s) AND services IN (%s) AND trust_score IN (%s)""" % (self.location_str, self.services_str, self.trust_score_str)
        # # self.result = cursor.execute(query, (self.location_str, self.services_str, self.trust_score_str))
        #
        # self.result = cursor.execute(query)
        query = "SELECT title FROM trustpilot_table WHERE location = ? AND trust_score = ? AND services LIKE ?"
        # result = cursor.execute(query, (str(x), str(y), str(z)))
        # T.insert(tk.END, result)
        # print(x,y,z)

        # TODO
        '''
        de adaugat un buton pentru returnarea rezultatului
        si de adaugat un textbox in care vor fi enumerate rezultatele in
        urma combinarii celor 3 entry-uri 
        '''

        """
        ADD CLOSE BUTTON -> CLOSES DB CONNECTION & APP
        """




if __name__ == '__main__':
    root = tk.Tk()
    app = TrustPilotTK(root)
    root.mainloop()
