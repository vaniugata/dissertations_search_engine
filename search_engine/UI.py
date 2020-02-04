from tkinter import *
from search_engine import engine
class UIMgr:

    window = None
    l_title = None
    e_title = None
    l_university = None
    e_university = None
    b_search = None
    l_name = None
    e_name = None
    l_number = None
    e_number = None
    complexity = 0
    list_result = None
    sb_result = None

    def init(self):
        self.window = Tk()
        self.l_title = Label(self.window, text="Тема: ")
        self.e_title = Entry(self.window)
        self.l_university = Label(self.window, text="Университет: ")
        self.e_university = Entry(self.window)
        self.b_search = Button(self.window, text="Търси")
        self.l_name = Label(self.window, text="Автор: ")
        self.e_name = Entry(self.window)
        self.l_number = Label(self.window, text="Факултетен №: ")
        self.e_number = Entry(self.window)
        self.b_info = Button(self.window, text="Информация")
        self.list_result = Listbox(self.window, height=10, width=100)
        self.sb_result = Scrollbar(self.window)

        Radiobutton(self.window, text="Много сложен", variable=self.complexity, value=5).grid(row=3, column=0)
        Radiobutton(self.window, text="Сложен", variable=self.complexity, value=4).grid(row=3, column=1)
        Radiobutton(self.window, text="Лесен", variable=self.complexity, value=2).grid(row=3, column=3)
        Radiobutton(self.window, text="Нормално сложен", variable=self.complexity, value=3).grid(row=3, column=2)
        Radiobutton(self.window, text="Тривиален", variable=self.complexity, value=1).grid(row=3, column=4)
        Radiobutton(self.window, text="Всички", variable=self.complexity, value=0).grid(row=3, column=5)

        self.l_title.grid(row=1, column=0)
        self.e_title.grid(row=1, column=1)
        self.l_university.grid(row=1, column=3)
        self.e_university.grid(row=1, column=4)
        self.b_search.grid(row=1, column=5, rowspan=2)
        self.b_search.bind()

        self.l_name.grid(row=2, column=0)
        self.e_name.grid(row=2, column=1)
        self.l_number.grid(row=2, column=3)
        self.e_number.grid(row=2, column=4)

        self.b_info.grid(row=5, column=5)

        self.list_result.grid(row=4, column=0, rowspan=10, columnspan=5)
        self.sb_result.grid(row=4, column=4, rowspan=10, sticky=E)
        self.list_result.configure(yscrollcommand=self.sb_result.set)
        self.sb_result.configure(command=self.list_result.yview)

    # temp1=("test 1", "test12", "test13")
    # temp2=("test 2", "test22")
    # list_a =[]
    # list_a.append(temp1)
    # list_a.append(temp2)

    # list_result = Listbox(window, height=10, width=120)
    # sb_result = Scrollbar(window)
    # for item in list_a:
    #     list_result.insert(END, item)

    #l_directory.grid(row=0, column=0)
    #e_directory.grid(row=0, column=1, columnspan=2)
    #b_browse.grid(row=0, column=4, columnspan=2)

   