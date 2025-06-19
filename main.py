# pip install opencv-python pillow
# importar bibliotecas
from tkinter import*
from tkinter import Tk, ttk, filedialog
from PIL import ImageTk, Image, ImageEnhance
import cv2
import os

# cores
co0 = "#f0f3f5"  # Preto
co1 = "#feffff"  # Branco
co2 = "#4fa882"  # Verde
co3 = "#38576b"  # Valor
co4 = "#403d3d"  # Letra
co5 = "#e06636"  # Profit
co6 = "#038cfc"  # Azul

# criando janela
janela = Tk()
janela.title("Conversor para Desenho a Lapis")
janela.geometry('450x550')
janela.configure(bg=co1)
janela.resizable(width=FALSE, height=FALSE)

# Variaveis globais
global imagem_original, imagem_convertida
imagem_original = None
imagem_convertida = None



# Funcao para escolher imagem
def escolher_imagem():
    global imagem_original
    caminho = filedialog.askopenfilename()
    if caminho:
        imagem_original = Image.open(caminho)
        imagem_preview = imagem_original.resize((200,200))
        imagem_preview = ImageTk.PhotoImage(imagem_preview)
        l_preview_original.configure(image=imagem_preview)
        l_preview_original.image = imagem_preview

# Funcao para converter a imagem
def converter_imagem(event=None):
    global imagem_original, imagem_convertida

    if imagem_original is None:
        return
    #Ajustes do usuario
    r = s_intensidade.get()
    brilho = s_brilho.get() / 100
    contraste = s_contraste.get() / 100

    # conversao para desenho a lapis
    imagem_cv = cv2.cvtColor(cv2.imread(imagem_original.filename), cv2.COLOR_BGR2GRAY) 
    blur = cv2.GaussianBlur(imagem_cv, (21,21), 0)
    sketch = cv2.divide(imagem_cv, blur, scale=r)

    # Ajustar brilho e contraste
    pil_sketch = Image.fromarray(sketch)
    enhancer_brilho = ImageEnhance.Brightness(pil_sketch)
    pil_sketch = enhancer_brilho.enhance(brilho)
    enhancer_contraste = ImageEnhance.Contrast(pil_sketch)
    pil_sketch = enhancer_contraste.enhance(contraste)


    imagem_convertida = pil_sketch    
    imagem_preview = imagem_convertida.resize((200,200))
    imagem_preview = ImageTk.PhotoImage(imagem_preview)
    l_preview_convertida.configure(image=imagem_preview)
    l_preview_convertida.image = imagem_preview

# Função para salvar a imagem convertida
def salvar_imagem():
    if imagem_convertida:
        caminho = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if caminho:
            imagem_convertida.save(caminho) 

frame_top = Frame(janela, width=450, height=50, bg=co1)
frame_top.grid(row=0, column=0, padx=10, pady=5)

frame_preview = Frame(janela, width=450, height=220, bg=co1)
frame_preview.grid(row=1, column=0, padx=10, pady=5)

frame_controls = Frame(janela, width=450, height=225, bg=co1)
frame_controls.grid(row=2, column=0, padx=10, pady=5)

# Logo e Titulo
logo = Label(frame_top, text="Conversor para Desenho a Lapis", font=("Arial", 16, "bold"), bg=co1, fg=co4)
logo.pack()

# Previews
l_preview_original = Label(frame_preview, text="Previa Original", font=("Arial", 12), bg=co1, fg=co3)
l_preview_original.place(x=30, y=10)

l_preview_convertida = Label(frame_preview, text="Previa Convertida", font=("Arial", 12), bg=co1, fg=co3)
l_preview_convertida.place(x=240, y=10)

# Controles
ttk.Label(frame_controls, text="Intensidade", background=co1).place(x=10, y=10)
s_intensidade = Scale(frame_controls, command=converter_imagem, from_=50, to=300, orient=HORIZONTAL, leng=200, bg=co1, fg=co4)
s_intensidade.set(120)
s_intensidade.place(x=10, y=30)

ttk.Label(frame_controls, text="Brilho", background=co1).place(x=10, y=80)
s_brilho = Scale(frame_controls, command=converter_imagem, from_=50, to=200, orient=HORIZONTAL, leng=200, bg=co1, fg=co4)
s_brilho.set(100)
s_brilho.place(x=10, y=100)

ttk.Label(frame_controls, text="Contraste", background=co1).place(x=10, y=150)
s_contraste = Scale(frame_controls, command=converter_imagem, from_=50, to=200, orient=HORIZONTAL, leng=200, bg=co1, fg=co4)
s_contraste.set(100)
s_contraste.place(x=10, y=170)

# Botões
b_escolher = Button(janela, command=escolher_imagem, text="Escolher Imagem", bg=co6, fg=co1, font=("Arial", 10,), width=15)
b_escolher.place(x=20, y=500)

b_converter = Button(janela, text="Converter", bg=co2, fg=co1, font=("Arial", 10,), width=15)
b_converter.place(x=160, y=500)

b_salvar = Button(janela, command=salvar_imagem, text="Salvar Imagem", bg=co2, fg=co1, font=("Arial", 10,), width=15)
b_salvar.place(x=300, y=500)




janela.mainloop()



