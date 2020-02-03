from tkinter import *

window = Tk()

#l_directory = Label(window, text="Директория: ")
#e_directory = Entry(window)
#b_browse = Button(window, text="Избери")


l_title = Label(window, text="Тема: ")
e_title = Entry(window)
l_university = Label(window, text="Университет: ")
e_university = Entry(window)
b_search = Button(window, text="Търси")

l_name = Label(window, text="Автор: ")
e_name = Entry(window)
l_number = Label(window, text="Факултетен №: ")
e_number = Entry(window)

b_info = Button(window, text="Информация")

complexity = IntVar()

Radiobutton(window, text="Много сложен", variable=complexity, value=5).grid(row=3, column=0)
Radiobutton(window, text="Сложен", variable=complexity, value=4).grid(row=3, column=1)
Radiobutton(window, text="Нормално сложен", variable=complexity, value=3).grid(row=3, column=2)
Radiobutton(window, text="Лесен", variable=complexity, value=2).grid(row=3, column=3)
Radiobutton(window, text="Тривиален", variable=complexity, value=1).grid(row=3, column=4)
Radiobutton(window, text="Всички", variable=complexity, value=0).grid(row=3, column=5)

list_result = Listbox(window, height=10, width=100)
sb_result = Scrollbar(window)

#l_directory.grid(row=0, column=0)
#e_directory.grid(row=0, column=1, columnspan=2)
#b_browse.grid(row=0, column=4, columnspan=2)

l_title.grid(row=1, column=0)
e_title.grid(row=1, column=1)
l_university.grid(row=1, column=3)
e_university.grid(row=1, column=4)
b_search.grid(row=1, column=5, rowspan=2)

l_name.grid(row=2, column=0)
e_name.grid(row=2, column=1)
l_number.grid(row=2, column=3)
e_number.grid(row=2, column=4)

b_info.grid(row=5, column=5)

list_result.grid(row=4, column=0, rowspan=10, columnspan=5)
sb_result.grid(row=4, column=4, rowspan=10, sticky=E)

list_result.configure(yscrollcommand=sb_result.set)
sb_result.configure(command=list_result.yview)
window.mainloop()