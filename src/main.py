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
    PAD_SIZE = 10
    dest = None

    def __init__(self):
        super().__init__(master=None)
        self.init_copy_ui()
        self.build_text_area()
        self.pack(fill=tk.BOTH)
        # self.grid(columnspan=10)


    def build_text_area(self):
        v_scroll_bar = tk.Scrollbar(self)
        # v_scroll_bar.grid(row=1, rowspan=4, column=4)
        v_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        
        h_scroll_bar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        # h_scroll_bar.grid(row=4, column=0, columnspan=4)
        h_scroll_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.list_box = tk.Listbox(self, xscrollcommand=h_scroll_bar.set, yscrollcommand=v_scroll_bar.set)
        # self.list_box.grid(row=1, rowspan=4, column=1, columnspan=4)
        self.list_box.pack(side=tk.BOTTOM, fill=tk.BOTH)
        
        v_scroll_bar.config(command=self.list_box.yview)
        h_scroll_bar.config(command=self.list_box.xview)
        
        # scroll_frame.grid(row=5, column=0, columnspan=4, padx=self.PAD_SIZE, pady=self.PAD_SIZE)
        self.pack(side=tk.BOTTOM, fill=tk.BOTH)
        

    def init_copy_ui(self):
        this_frame = tk.Frame(master=self)
        self.select_src_button = tk.Button(this_frame, text="src", command=lambda : self.load_files_into_list())
        self.select_src_button.pack(side=tk.TOP, fill=tk.BOTH)

        self.select_dst_button = tk.Button(this_frame, text="dst", command=lambda : self.select_dst_dir())
        self.select_dst_button.pack(side=tk.TOP, fill=tk.BOTH)

        self.init_copy_button = tk.Button(this_frame, text="copy", command=lambda : self.thread_copy_files(), state=tk.DISABLED)
        self.init_copy_button.pack(side=tk.TOP, fill=tk.BOTH)

        this_frame.pack(side=tk.LEFT, padx=10, pady=10)
        # select_source_button.grid(row=0, column=0)


    def thread_copy_files(self):
        # t1=Thread(target=self.copy_files)
        # t1.start()
        self.queue = queue.Queue()
        self.select_src_button.config(state=tk.DISABLED)
        self.select_dst_button.config(state=tk.DISABLED)
        self.init_copy_button.config(state=tk.DISABLED)
        ThreadCopy(self.queue, self.list_box, self.dest).start()
        self.master.after(100, self.process_queue)

    
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

        # self.ticket_number_label.pack()
        self.print_values_button = tk.Button(self, text="Print results", command=self.print_results, state=tk.DISABLED)
        # self.print_values_button.bind("<<valid_ticket>>", self.activate_print_results)
        self.print_values_button.grid(row=4,column=2,padx=10,pady=10)

        self.exit_button = tk.Button(self,text="Exit", command=self.exit_app)
        self.exit_button.grid(row=3, column=2, padx=10, pady=10)
        # self.exit_button.pack()
    
    
    def validate_jira_ticket(self, input):
        print("validate_jira_ticket, input: ", input)
        if re.match(self.JIRA_TICKET_PATTERN, input):
            print("validate_jira_ticket TRUE")
            self.print_values_button.config(state=tk.ACTIVE)
            return True
        else:
            print("validate_jira_ticket FALSE")
            self.print_values_button.config(state=tk.DISABLED)
            return False
    

    def exit_app(self):
        sys.exit()


    def print_results(self):
        self.validate_jira_ticket(self.ticket_number_entry.get())
        # print()
        print("ticket: ", self.ticket_number_entry.get())
        print("sid: ", self.user_sid_entry.get())


    def activate_print_results(self, event):
        event.widget["state"] = tk.ACTIVE


my_app = AppGUI()
my_app.master.title("Test")
my_app.master.maxsize(800, 600)
my_app.config(width=800, height=600)
my_app.mainloop()