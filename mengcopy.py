from tkinter import *

window = Tk()
window.geometry("500x500+600+400")
window.title("copy text")

def copy_text():
    text_to_copy = entry.get()
    window.clipboard_clear()
    window.clipboard_append(text_to_copy)
    new_window = Toplevel(window)
    new_window.title("Copied Text")
    new_window.geometry("300x100+600+200")
    label = Label(new_window, text=text_to_copy)
    label.pack()

    def copy_from_new_window():
        new_window.clipboard_clear()
        new_window.clipboard_append(text_to_copy)

    copy_button = Button(new_window, text="copy kalimat", command=copy_from_new_window)
    copy_button.pack()

entry = Entry(window)
entry.pack()

button = Button(window, text="Meluncur", command=copy_text)
button.pack()

window.mainloop()