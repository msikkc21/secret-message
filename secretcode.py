import string
import numpy as np

chars = list(string.ascii_letters + string.digits + string.punctuation + " ") # list karakter
encoder = np.array([[1,2],[4,5]]) # matriks encoder
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



pesan = input("Masukkan pesan : ") 
print(f"encrypted text : {encode(pesan)}")

chiper = input("Masukkan pesan : ") 
print(f"decrypted text : {decode(chiper)}")


