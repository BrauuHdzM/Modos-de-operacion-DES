from tkinter import *
from tkinter import filedialog
from Crypto.Cipher import DES
from PIL import Image
import os

class DESGUI:
    def __init__(self, master):
        self.master = master
        master.title("DES GUI")

        # Etiquetas para cada campo
        self.image_label = Label(master, text="Imagen:")
        self.key_label = Label(master, text="Llave (8 Bytes):")
        self.iv_label = Label(master, text="Vector de Inicialización (8 Bytes):")
        self.mode_label = Label(master, text="Modo:")

        # Campos de entrada para cada valor
        self.image_entry = Entry(master)
        self.key_entry = Entry(master)
        self.iv_entry = Entry(master)
        self.mode_entry = Entry(master)

        # Botones para seleccionar archivo y ejecutar cifrado/descifrado
        self.image_button = Button(master, text="Seleccionar Imagen", command=self.select_image)
        self.encrypt_button = Button(master, text="Cifrar", command=self.encrypt)
        self.decrypt_button = Button(master, text="Descifrar", command=self.decrypt)

        # Organiza los elementos en la ventana
        self.image_label.grid(row=0, column=0)
        self.image_entry.grid(row=0, column=1)
        self.image_button.grid(row=0, column=2)

        self.key_label.grid(row=1, column=0)
        self.key_entry.grid(row=1, column=1)

        self.iv_label.grid(row=2, column=0)
        self.iv_entry.grid(row=2, column=1)

        self.mode_label.grid(row=3, column=0)
        self.mode_entry.grid(row=3, column=1)

        self.encrypt_button.grid(row=4, column=0)
        self.decrypt_button.grid(row=4, column=1)

    def select_image(self):
        # Abre un cuadro de diálogo para seleccionar la imagen
        filename = filedialog.askopenfilename()
        self.image_entry.insert(END, filename)

    def encrypt(self):
        # Obtiene los valores de entrada
        key = self.key_entry.get().encode()
        iv = self.iv_entry.get().encode()
        plaintext_file = self.image_entry.get()
        mode = self.mode_entry.get().upper()

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

        # Cifra los bytes de la imagen
        ciphertext = cipher.encrypt(image_bytes)

        # Crea un objeto de imagen desde los datos
        # Crea un objeto de imagen desde los datos cifrados
        im = Image.frombytes(mode="RGB", size=im.size, data=ciphertext)

        # Guarda la imagen cifrada en formato BMP
        im.save("ciphertext.bmp", "bmp")

    def decrypt(self):
        # Obtiene los valores de entrada
        key = self.key_entry.get().encode()
        iv = self.iv_entry.get().encode()
        ciphertext_file = self.image_entry.get()
        mode = self.mode_entry.get().upper()

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
        im.save("plaintext.bmp", "bmp")

        

root = Tk()
des_gui = DESGUI(root)
root.mainloop()