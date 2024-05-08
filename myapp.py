import string
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

# Create the main window
window = tk.Tk()
window.title("Encryption Application")
window.configure(bg="white")
window.geometry("350x140")
window.resizable(False,False)

pesan = tk.StringVar()

# Add widgets or UI elements here
input_frame = ttk.Frame(window)
input_frame.pack(padx=10, pady=10, fill = "x")

pesanLabel = ttk.Label(input_frame, text="Masukkan Pesan : ")
pesanLabel.pack(fill="x", padx=10, pady=5)

pesanInput = ttk.Entry(input_frame, textvariable=pesan)
pesanInput.pack(fill="x", padx=10, pady=5)

chars = list(string.ascii_letters + string.digits + string.punctuation + " ") # list karakter
encoder = np.array([[3,6],[7,9]]) # matriks encoder
decoder = np.linalg.inv(encoder) # matriks decoder (invers dari matriks encoder)

def division(input, x): # untuk membagi pesan menjadi beberapa kelompok yang berisi 4 karakter
    arr = []
    index = 0
    while index < len(input):
        arr.append(input[index:index+x])
        index += x
    return arr

def encode(input): # untuk mengenkripsi pesan
    # menambahkan karakter jika pesan yang diinput tidak kelipatan 4
    while len(input) % 4 != 0: 
        input += " "
    key = [] 
    # mengubah  pesan menjadi kode 
    for letter in input:
        index = chars.index(letter)
        key.append(index)
    key = division(key,4) # membagi pesan menjadi kelompok
    # algoritma encoding
    chipertext = ""
    for matrix in key:
        # mengubah array python menjadi array numpy
        matriks = np.array(matrix)
        # mengubah array 1D menjadi 2D
        matriks = matriks.reshape(2,2)
        #  memanggil fungsi enkripsi dengan mengalikan dengan matriks encoder
        chipercode = np.dot(matriks, encoder)
        chipercode = chipercode.reshape(1,4)
        # menyederhanakan hasil yang melebihi jumlah karakter dan menyimpannya dalam variabel result
        result = []
        for i in chipercode:
            for j in i:
                number = j
                x = 0
                while number > len(chars):
                    number -= len(chars)
                    x += 1
                result.append(number) 
                result.append(x) 
        # mengubah data yang ada di dalam result menjadi karakter kembali
        for i in result:
            chipertext +=  chars[i]    
    return chipertext

def decode(input):
    key = [] 
    # mengubah  pesan menjadi kode 
    for letter in input:
        index = chars.index(letter)
        key.append(index)
    key = division(key,8) # membagi pesan menjadi kelompok
    # algoritma decoding
    plaintext = ""
    for matrix in key:
        # mengubah array python menjadi array numpy
        matriks = np.array(matrix)
        # mengubah array yang disederhanakan dari hasil encoding
        index = 0
        originMatriks = []
        while index < len(matriks):
            sum = matriks[index]
            mtp = matriks[index + 1]
            while mtp > 0:
                mtp -= 1
                sum += 95
            originMatriks.append(sum)
            index += 2
        # mengubah originMatriks menjadi array numpy
        originMatriks = np.array(originMatriks)
        # mengubah array 1D  menjadi array 2D
        originMatriks = originMatriks.reshape(2,2)
        # mengalikan matriks dengan decoder
        result = np.dot(originMatriks, decoder)
        # mengubah array 2D  ke array 1D
        result = result.reshape(1,4)
        # mengubah isi array menjadi karakter
        for i in result[0]:
            plaintext +=  chars[round(i)]
    return plaintext

def encodeClick():
    popup = Toplevel(window)
    popup.title("Pesan Rahasia")
    popup.geometry("300x100")
    frame = Frame(popup)
    frame.pack(padx=10, pady=10)
    pesan_enkripsi = Label(frame, text=encode(pesan.get()))
    pesan_enkripsi.pack(pady=10, padx=10)

    def copy_popup_window():
        popup.clipboard_clear()
        popup.clipboard_append(encode(pesan.get()))

    tombol = Button(frame, text="Copy Text", command=copy_popup_window)
    tombol.pack(padx=10, pady=5)

def decodeClick():
    popup = Toplevel(window)
    popup.title("Pesan Asli")
    popup.geometry("300x100")
    frame = Frame(popup)
    frame.pack(padx=10, pady=10)
    pesan_dekripsi = Label(frame, text=decode(pesan.get()))
    pesan_dekripsi.pack(pady=10, padx=10)

    def copy_popup_window():
        popup.clipboard_clear()
        popup.clipboard_append(decode(pesan.get()))

    tombol = Button(frame, text="Copy Text", command=copy_popup_window)
    tombol.pack(padx=10, pady=5)

enkripButton = ttk.Button(input_frame,text="Enkripsi", command=encodeClick)
enkripButton.pack(side="left", pady=10, padx=10)

dekripButton = ttk.Button(input_frame,text="Dekripsi", command=decodeClick)
dekripButton.pack(side="right", pady=10, padx=10)

# Start the main event loop
window.mainloop()
