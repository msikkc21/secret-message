import string
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import ttk

# Menginisialisasi list karakter, matriks encoder, dan matriks decoder
chars = list(string.ascii_letters + string.digits + string.punctuation + " ") # list karakter
encoder = np.array([[3,9],[7,8]]) # matriks encoder
decoder = np.linalg.inv(encoder) # matriks decoder (invers dari matriks encoder)

# Membagi pesan menjadi beberapa kelompok 
def division(input, x): 
    arr = []
    index = 0
    while index < len(input):
        arr.append(input[index:index+x])
        index += x
    return arr

# Fungsi enkripsi pesan asli
def encode(input):
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

# Fungsi dekripsi pesan rahasia
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

# Fungsi menampilkan popup window yang berisi hasil dari fungsi enkripsi
def encodeClick():
    popup = Toplevel(window)
    popup.title("Pesan Rahasia")
    popup_width = 350
    popup_height = 100
    popup_x = int((window.winfo_screenwidth()/2)-(popup_width/2))
    popup_y = int((window.winfo_screenheight()/2)-(popup_height/2)-260)
    popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")
    frame = Frame(popup)
    frame.pack(padx=10, pady=10)
    pesan_enkripsi = Label(frame, text=encode(pesan.get()))
    pesan_enkripsi.pack(pady=10, padx=10)

    def copy_popup_window():
        popup.clipboard_clear()
        popup.clipboard_append(encode(pesan.get()))

    tombol = Button(frame, text="Copy Text", command=copy_popup_window)
    tombol.pack(padx=10, pady=5)

# Fungsi menampilkan popup window yang berisi hasil dari fungsi dekripsi
def decodeClick():
    popup = Toplevel(window)
    popup.title("Pesan Asli")
    popup_width = 350
    popup_height = 100
    popup_x = int((window.winfo_screenwidth()/2)-(popup_width/2))
    popup_y = int((window.winfo_screenheight()/2)-(popup_height/2)-260)
    popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")
    frame = Frame(popup)
    frame.pack(padx=10, pady=10)
    pesan_dekripsi = Label(frame, text=decode(pesan.get()))
    pesan_dekripsi.pack(pady=10, padx=10)

    def copy_popup_window():
        popup.clipboard_clear()
        popup.clipboard_append(decode(pesan.get()))

    tombol = Button(frame, text="Copy Text", command=copy_popup_window)
    tombol.pack(padx=10, pady=5)

# Membuat window utama
window = tk.Tk()
window.title("Encryption Application")
logo = PhotoImage(file="logo.png")
window.iconphoto(True, logo)
window.configure(bg="white")
width = 350
height = 140
x = int((window.winfo_screenwidth()/2)-(width/2))
y = int((window.winfo_screenheight()/2)-(height/2)-100)
window.geometry(f"{width}x{height}+{x}+{y}")
window.resizable(1,0)

# Membuat frame dan widget
input_frame = ttk.Frame(window)
input_frame.pack(padx=10, pady=10, fill = "x")

pesanLabel = ttk.Label(input_frame, text="Masukkan Pesan : ")
pesanLabel.pack(fill="x", padx=10, pady=5)

pesan = tk.StringVar() # Variabel penampung input pesan

pesanInput = ttk.Entry(input_frame, textvariable=pesan)
pesanInput.pack(fill="x", padx=10, pady=5)

enkripButton = ttk.Button(input_frame,text="Enkripsi", command=encodeClick)
enkripButton.pack(side="left", pady=10, padx=10)

dekripButton = ttk.Button(input_frame,text="Dekripsi", command=decodeClick)
dekripButton.pack(side="right", pady=10, padx=10)

# Start the main event loop
window.mainloop()
