
import tkinter as tk

# Configuração da janela
WIDTH = 600
HEIGHT = 400
STEP = 10  # pixels por movimento

root = tk.Tk()
root.title("Rectângulo com Teclas Direcionais")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()
pic=tk.PhotoImage(file="bit.gif")
# Criar rectângulo (x1, y1, x2, y2)
rect = canvas.create_image(50, 50, image=pic)

def move(event):
    if event.keysym == "Up":
        canvas.move(rect, 0, -STEP)
    elif event.keysym == "Down":
        canvas.move(rect, 0, STEP)
    elif event.keysym == "Left":
        canvas.move(rect, -STEP, 0)
    elif event.keysym == "Right":
        canvas.move(rect, STEP, 0)

# Capturar teclas
root.bind("<Up>", move)
root.bind("<Down>", move)
root.bind("<Left>", move)
root.bind("<Right>", move)

root.mainloop()
