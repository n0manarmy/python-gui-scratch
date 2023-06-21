import unittest
import re
import tkinter as tk

class TestListboxEdit(unittest.TestCase):

    def test_listbox_edit(self):
        list_box = tk.Listbox(master=None)
        for x in range(100):
            list_box.insert(tk.END, str(x) + " - A")
        
        temp_list = list_box.get(0, tk.END)
        
        for i, x in enumerate(temp_list):
            print(i)
            y = str(i) + " - B"
            print(hash(list_box.get(i)))
            print(hash(x))
            if hash(list_box.get(i)) == hash(x):
                list_box.delete(i)
                list_box.insert(i, "DONE - " + y)
            # list_box.selection_set(i, i)
            # select = list_box.curselection()
            # list_box.insert(select)
        
        for i, x in enumerate(list_box.get(0, tk.END)):
            print(x)
            # x = i * "B"
        

if __name__ == '__main__':
    unittest.main()