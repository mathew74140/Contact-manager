from tkinter import *
from tkinter import messagebox
from contact_db import *
import random

#----- UI
sample = Tk()
sample.geometry('550x350')
sample.resizable(0, 0)
sample.title('Contact Manager')

def hex_color():
    hex_num = '0123456789ABCDEF'
    return '#' + ''.join(random.choice(hex_num) for _ in range(6))

bg_color = hex_color()
sample.configure(bg=bg_color)

cdb = ContactDB('d:/mycontacts.db')

#----- Functions
data = None  # Global variable for selected contact

def add_item():
    fname = name_entry.get().strip()
    lname = family_entry.get().strip()
    address = address_entry.get().strip()
    phone = phone_entry.get().strip()
    if fname and lname:
        cdb.insert(fname, lname, address, phone)
        show_list()
        clear()
    else:
        messagebox.showwarning("Input Error", "Name and Family are required.")

def show_list():
    contact_list.delete(0, END)
    for rec in cdb.select():
        contact_list.insert(END, rec)

def clear():
    name_entry.delete(0, END)
    family_entry.delete(0, END)
    address_entry.delete(0, END)
    phone_entry.delete(0, END)
    name_entry.focus_set()

def remove_item():
    global data
    index = contact_list.curselection()
    if not index:
        messagebox.showwarning("Warning", "Select a contact to delete.")
        return
    data = contact_list.get(index)
    result = messagebox.askquestion('Delete', f'Delete {data[1]} {data[2]}?')
    if result == 'yes':
        cdb.delete(data[0])
        show_list()
        clear()

def select_item(event):
    global data
    index = contact_list.curselection()
    if not index:
        return
    data = contact_list.get(index)
    clear()
    name_entry.insert(0, data[1])
    family_entry.insert(0, data[2])
    address_entry.insert(0, data[3])
    phone_entry.insert(0, data[4])

def update_item():
    global data
    if not data:
        messagebox.showwarning("Warning", "Select a contact to update.")
        return
    cdb.update(data[0], name_entry.get(), family_entry.get(), address_entry.get(), phone_entry.get())
    show_list()
    clear()

def cancel():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        sample.destroy()

def search_item():
    sample.withdraw()  # Hide main window

    search_win = Toplevel()
    search_win.title("جستجوی مخاطب")
    search_win.geometry("300x150")
    search_win.resizable(0, 0)

    search_label = Label(search_win, text="Enter your data")
    search_label.pack(pady=10)

    search_var = StringVar()
    search_entry = Entry(search_win, textvariable=search_var, width=30)
    search_entry.pack(pady=5)
    search_entry.focus_set()

    def perform_search():
        query = search_var.get().strip().lower()
        contact_list.delete(0, END)
        for rec in cdb.select():
            if any(query in str(field).lower() for field in rec[1:]):
                contact_list.insert(END, rec)
        search_win.destroy()
        sample.deiconify()

    search_btn = Button(search_win, text="search", command=perform_search)
    search_btn.pack(pady=10)

    search_win.protocol("WM_DELETE_WINDOW", lambda: [search_win.destroy(), sample.deiconify()])

def open_toplevel():
    sample.withdraw()
    show_toplevel()

def back_to_main(top):
    top.destroy()
    sample.deiconify()

def show_toplevel():
    top = Toplevel()
    top.title("پنجره دوم")

    back_btn = Button(top, text="Return to main window", command=lambda: back_to_main(top))
    back_btn.pack(padx=20, pady=20)

#----- Labels & Entries
name_text = StringVar()
family_text = StringVar()
address_text = StringVar()
phone_text = StringVar()

Label(sample, text="Name:", bg=bg_color, font=('Arial', 14)).place(x=10 , y=5)
name_entry = Entry(sample, textvariable=name_text)
name_entry.place(x=90, y=10)

Label(sample, text="Family:", bg=bg_color, font=('Arial', 14)).place(x=10 , y=35)
family_entry = Entry(sample, textvariable=family_text)
family_entry.place(x=90, y=35)

Label(sample, text="Address:", bg=bg_color, font=('Arial', 14)).place(x=10 , y=65)
address_entry = Entry(sample, textvariable=address_text)
address_entry.place(x=90, y=65)

Label(sample, text="Phone:", bg=bg_color, font=('Arial', 14)).place(x=10 , y=95)
phone_entry = Entry(sample, textvariable=phone_text)
phone_entry.place(x=90, y=95)

#----- Listbox & Scrollbar
contact_list = Listbox(sample, height=10, width=80, bd=3)
contact_list.place(x=10, y=180)
scrollbar = Scrollbar(sample)
scrollbar.place(x=500, y=180, height=165)
contact_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=contact_list.yview)
contact_list.bind('<<ListboxSelect>>', select_item)

#----- Buttons
Button(sample, text='Show', bg=bg_color, command=show_list, width=18).place(x=385, y=1)
Button(sample, text='Update', bg=bg_color, width=18, command=update_item).place(x=385, y=26)
Button(sample, text='Insert', bg=bg_color, width=18, command=add_item).place(x=385, y=51)
Button(sample, text='Delete', bg=bg_color, width=18, command=remove_item).place(x=385, y=76)
Button(sample, text='Delete Inputs', bg=bg_color, width=18, command=clear).place(x=385, y=101)
Button(sample, text='Cancel', bg=bg_color, width=18, command=cancel).place(x=385, y=126)
Button(sample, text='Search', bg=bg_color, width=18, command=search_item).place(x=385, y=151)

#----- Start
show_list()
sample.mainloop()