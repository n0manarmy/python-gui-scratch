import threading
import tkinter as tk
import queue
import shutil

class ThreadCopy(threading.Thread):
    def __init__(self, queue, files_list, list_box, dest_folder, transmit_button):
        super().__init__()
        self.queue = queue
        self.list_box = list_box
        self.files_list = files_list
        self.dest_folder = dest_folder
        self.transmit_button = transmit_button
    
    def run(self):
        # def copy_files(self):
        # print(self.dest)
        for i, f in enumerate(self.files_list):
            try:
                shutil.copy2(f, self.dest_folder)
            except Exception as err:
                print("Error copying files: ", err)
            finally:
                if hash(self.list_box.get(i)) == hash(f):
                    self.list_box.delete(i)
                    self.list_box.insert(i, "DONE || " + f)
                self.process_queue()
        
        self.transmit_button.config(state=tk.ACTIVE)



    def process_queue(self):
        try:
            msg = self.queue.get_nowait()
            print(msg)
        except queue.Empty:
            print("queue.Empty")
            print(self.queue)
            # self.master.after(100, self.process_queue)