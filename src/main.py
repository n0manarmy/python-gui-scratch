import sys
import shutil
import tkinter as tk
from tkinter import filedialog
from threading import *
from thread_copy import ThreadCopy
import queue
import re

class AppGUI(tk.Frame):

    JIRA_TICKET_PATTERN = "([A-z]{3}-[0-9]{1,})"
    PAD_SIZE = 5
    dest = None

    def __init__(self):
        super().__init__(master=None)
        self.master.title("Test")
        self.master.maxsize(1280, 900)
        self.config(width=1280, height=900)

        self.init_copy_ui()
        self.build_text_area()
        self.pack(fill=tk.BOTH)


    def build_text_area(self):
        scroll_frame = tk.Frame(master=self, bg="red")

        v_scroll_bar = tk.Scrollbar(scroll_frame, orient=tk.VERTICAL)
        # v_scroll_bar.grid(row=1, rowspan=10, column=11, sticky=tk.E+tk.N+tk.S, padx=self.PAD_SIZE, pady=self.PAD_SIZE, ipadx=2)
        v_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y, padx=self.PAD_SIZE, pady=self.PAD_SIZE, ipadx=5)
        
        h_scroll_bar = tk.Scrollbar(scroll_frame, orient=tk.HORIZONTAL)
        # h_scroll_bar.grid(row=11, column=1, columnspan=10, sticky=tk.E+tk.W, padx=self.PAD_SIZE, pady=self.PAD_SIZE, ipady=2)
        h_scroll_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=self.PAD_SIZE, pady=self.PAD_SIZE, ipady=5)

        self.list_box = tk.Listbox(scroll_frame, xscrollcommand=h_scroll_bar.set, yscrollcommand=v_scroll_bar.set, width=100, height=25)
        # self.list_box.grid(row=1, rowspan=10, column=1, columnspan=10, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=tk.N+tk.S+tk.E+tk.W)
        self.list_box.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=self.PAD_SIZE, pady=self.PAD_SIZE)
        
        v_scroll_bar.config(command=self.list_box.yview)
        h_scroll_bar.config(command=self.list_box.xview)

        scroll_frame.grid(row=1, column=1, padx=self.PAD_SIZE, pady=self.PAD_SIZE)


    def init_copy_ui(self):
        button_frame = tk.Frame(master=self)
        button_frame.config(bg="black")

        self.select_src_button = tk.Button(button_frame, text="src", command=lambda : self.load_files_into_list())
        self.select_src_button.pack(side=tk.TOP, fill=tk.BOTH, padx=self.PAD_SIZE, pady=self.PAD_SIZE)
        # self.select_src_button.grid(row=1, column=0, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=tk.N)

        self.select_dst_button = tk.Button(button_frame, text="dst", command=lambda : self.select_dst_dir())
        self.select_dst_button.pack(side=tk.TOP, fill=tk.BOTH, padx=self.PAD_SIZE, pady=self.PAD_SIZE)
        # self.select_dst_button.grid(row=2, column=0, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=tk.N)

        self.init_copy_button = tk.Button(button_frame, text="copy", command=lambda : self.thread_copy_files(), state=tk.DISABLED)
        self.init_copy_button.pack(side=tk.TOP, fill=tk.BOTH, padx=self.PAD_SIZE, pady=self.PAD_SIZE)
        # self.init_copy_button.grid(row=3, column=0, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=tk.N)

        self.exit_button = tk.Button(button_frame, text="Exit", command=lambda : exit())
        self.exit_button.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=self.PAD_SIZE, pady=self.PAD_SIZE)
        # self.exit_button.grid(row=10, column=0, padx=self.PAD_SIZE, pady=self.PAD_SIZE, sticky=tk.S)

        button_frame.grid(row=1, column=0, rowspan=10, sticky=tk.N+tk.S, padx=self.PAD_SIZE, pady=self.PAD_SIZE)    

    def thread_copy_files(self):
        self.queue = queue.Queue()
        self.select_src_button.config(state=tk.DISABLED)
        self.select_dst_button.config(state=tk.DISABLED)
        self.init_copy_button.config(state=tk.DISABLED)
        ThreadCopy(self.queue, self.list_box, self.dest).start()
        self.master.after(100, self.process_queue)

    
    def collect_meta_data(self):
        return

    
    def process_queue(self):
        try:
            msg = self.queue.get_nowait()
        except queue.Empty:
            self.master.after(100, self.process_queue)
    

    def select_dst_dir(self):
        self.dest = filedialog.askdirectory()
        self.validate_copy()


    def load_files_into_list(self):
        files = filedialog.askopenfilenames()
        for f in files:
            self.list_box.insert(tk.END, f)
        
        self.validate_copy()
        

    def validate_copy(self):
        if len(self.list_box.get(0, tk.END)) > 0 and (self.dest != None and self.dest != ()):
            self.init_copy_button.config(state=tk.ACTIVE)
        else:
            self.init_copy_button.config(state=tk.DISABLED)


    def init_ticket_ui(self):
        validate_jira_reg = (self.register(self.validate_jira_ticket), '%P')

        self.ticket_number_label = tk.Label(self, text="Jira Ticket #")
        self.ticket_number_label.grid(row=1, column=0, padx=1, pady=1)

        self.ticket_number_entry = tk.Entry(self, text="ABC-####")
        self.ticket_number_entry.config(validate='focusout', validatecommand=validate_jira_reg)
        self.ticket_number_entry.grid(row=1, column=1, padx=1, pady=1)

        self.user_sid_label = tk.Label(self, text="User SID")
        self.user_sid_label.grid(row=2, column=0, padx=1, pady=1)

        self.user_sid_entry = tk.Entry(self)
        self.user_sid_entry.grid(row=2, column=1, padx=1, pady=1)

        self.print_values_button = tk.Button(self, text="Print results", command=self.print_results, state=tk.DISABLED)
        self.print_values_button.grid(row=4,column=2,padx=10,pady=10)



my_app = AppGUI()
my_app.mainloop()