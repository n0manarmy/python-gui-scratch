import threading
import tkinter as tk
import shutil

class ThreadCopy(threading.Thread):
    def __init__(self, queue, list_box, dest_folder):
        super().__init__()
        self.queue = queue
        self.list_box = list_box
        self.dest_folder = dest_folder
    
    def run(self):
        # def copy_files(self):
        # print(self.dest)
        files_list = self.list_box.get(0, tk.END)
        for i, f in enumerate(files_list):
            try:
                shutil.copy2(f, self.dest_folder)
            except Exception as err:
                print("Error copying files: ", err)
            finally:
                if hash(self.list_box.get(i)) == hash(f):
                    self.list_box.delete(i)
                    self.list_box.insert(i, "DONE || " + f)