import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class ListFrame(tk.Frame):
    def __init__(self, label=None, default_type=None, file_types=None, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.file_name_list = tk.StringVar()
        self.files = []

        self.default_type = default_type
        self.file_types = file_types

        lf2 = ttk.LabelFrame(self, text=label)
        lf2.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        scroll = ttk.Scrollbar(lf2)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll2 = ttk.Scrollbar(lf2)
        scroll2.pack(side=tk.BOTTOM, fill=tk.X)
        self.file_list = tk.Listbox(lf2, listvariable=self.file_name_list, selectmode=tk.EXTENDED, bd=0,
                                    yscrollcommand=scroll.set, xscrollcommand=scroll2.set)
        self.file_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scroll.config(command=self.file_list.yview)
        scroll2.config(orient=tk.HORIZONTAL, command=self.file_list.xview)
        frame1 = ttk.Frame(self)
        frame1.pack(side=tk.TOP, fill=tk.X, expand=0)  # it's important to set the
        # expand as False to expand file_list
        frame1.columnconfigure(0, weight=1)
        frame1.columnconfigure(1, weight=1)
        frame1.columnconfigure(2, weight=1)
        frame1.columnconfigure(3, weight=1)

        ttk.Button(frame1, text='+', command=self.add_file).grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        ttk.Button(frame1, text='-', command=self.remove_file).grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        ttk.Button(frame1, text='CLR', command=self.clear_list).grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
        ttk.Button(frame1, text='iii', command=self.show_info).grid(row=0, column=3, sticky=tk.N + tk.S + tk.E + tk.W)

    def add_file(self):
        option = dict(defaultextension=self.default_type,
                      filetypes=self.file_types)
        file_names = filedialog.askopenfilenames(**option)
        if len(file_names) != 0:
            self.files.extend(file_names)
            # print(self.files)
            self.file_name_list.set(self.files)
        for i in range(0, len(self.files), 2):
            self.file_list.itemconfigure(i, background='#f0f0ff')

    def remove_file(self):
        l = list(self.file_list.curselection())
        while l:
            self.files.pop(l.pop())
        self.file_name_list.set(self.files)

    def clear_list(self):
        self.files.clear()
        self.file_name_list.set(self.files)

    def show_info(self):
        info = '%i files in this list.' % len(self.files)
        messagebox.showinfo(title='Info', message=info)


if __name__ == '__main__':
    root = tk.Tk()
    f = ListFrame(master=root, default_type='.tif', file_types=[("All Files", "*.*"), ("Images", "*.jpg"),
                                                                ("Images", "*.tif"), ("Images", "*.png")])
    f.pack()
    root.mainloop()