import os
from tkinter import *
from tkinter import filedialog
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from PIL import Image

def select_image():
    # Abre un cuadro de diálogo para seleccionar la imagen
    filename = filedialog.askopenfilename()
    image_entry.delete(0, END)
    image_entry.insert(END, filename)

def generate_output_filename(input_file, operation, mode):
    # Genera el nombre del archivo de salida
    file_name, file_ext = os.path.splitext(input_file)
    return f"{file_name}_{operation}{mode}{file_ext}"

def encrypt():
    # Obtiene los valores de entrada
    key = key_entry.get().encode()
    iv = iv_entry.get().encode()
    plaintext_file = image_entry.get()
    mode = mode_entry.get().upper()

    # Cifra el archivo usando DES en el modo seleccionado
    if mode == 'ECB':
        cipher = DES.new(key, DES.MODE_ECB)
    elif mode == 'CBC':
        cipher = DES.new(key, DES.MODE_CBC, iv)
    elif mode == 'CFB':
        cipher = DES.new(key, DES.MODE_CFB, iv)
    elif mode == 'OFB':
        cipher = DES.new(key, DES.MODE_OFB, iv)
    else:
        raise ValueError("Modo inválido")

    # Lee la imagen original
    im = Image.open(plaintext_file)

    # Convierte la imagen a bytes
    image_bytes = im.tobytes()

    # Rellena los datos de la imagen
    padded_image_bytes = pad(image_bytes, DES.block_size)

    # Cifra los bytes de la imagen
    ciphertext = cipher.encrypt(padded_image_bytes)

    # Crea un objeto de imagen desde los datos cifrados
    im = Image.frombytes(mode="RGB", size=im.size, data=ciphertext)

    # Guarda la imagen cifrada en formato BMP
    output_file = generate_output_filename(plaintext_file, "e", mode)
    im.save(output_file, "bmp")

def decrypt():
    # Obtiene los valores de entrada
    key = key_entry.get().encode()
    iv = iv_entry.get().encode()
    ciphertext_file = image_entry.get()
    mode = mode_entry.get().upper()

    # Descifra el archivo usando DES en el modo seleccionado
    if mode == 'ECB':
        cipher = DES.new(key, DES.MODE_ECB)
    elif mode == 'CBC':
        cipher = DES.new(key, DES.MODE_CBC, iv)
    elif mode == 'CFB':
        cipher = DES.new(key, DES.MODE_CFB, iv)
    elif mode == 'OFB':
        cipher = DES.new(key, DES.MODE_OFB, iv)
    else:
        raise ValueError("Modo inválido")

    # Lee la imagen cifrada
    im = Image.open(ciphertext_file)

    # Convierte la imagen a bytes
    image_bytes = im.tobytes()

    # Descifra los bytes de la imagen
    plaintext = cipher.decrypt(image_bytes)

    # Crea un objeto de imagen desde los datos descifrados
    im = Image.frombytes(mode="RGB", size=im.size, data=plaintext)

    # Guarda la imagen descifrada en formato BMP
    output_file = generate_output_filename(ciphertext_file, "d", mode)
    im.save(output_file, "bmp")


root = Tk()
root.title("DES GUI")

# Etiquetas para cada campo
image_label = Label(root, text="Imagen:")
key_label = Label(root, text="Llave (8 Bytes):")
iv_label = Label(root, text="Vector de Inicialización (8 Bytes):")
mode_label = Label(root, text="Modo:")

# Campos de entrada para cada valor
image_entry = Entry(root)
key_entry = Entry(root)
iv_entry = Entry(root)
mode_entry = Entry(root)

# Botones para seleccionar archivo y ejecutar cifrado/descifrado
image_button = Button(root, text="Seleccionar imagen", command=select_image)
encrypt_button = Button(root, text="Cifrar", command=encrypt)
decrypt_button = Button(root, text="Descifrar", command=decrypt)

# Colocar las etiquetas, campos de entrada y botones en la ventana
image_label.grid(row=0, column=0, sticky=W)
key_label.grid(row=1, column=0, sticky=W)
iv_label.grid(row=2, column=0, sticky=W)
mode_label.grid(row=3, column=0, sticky=W)

image_entry.grid(row=0, column=1)
key_entry.grid(row=1, column=1)
iv_entry.grid(row=2, column=1)
mode_entry.grid(row=3, column=1)

image_button.grid(row=0, column=2)
encrypt_button.grid(row=4, column=0)
decrypt_button.grid(row=4, column=1)

#Iniciar la aplicación
root.mainloop()

