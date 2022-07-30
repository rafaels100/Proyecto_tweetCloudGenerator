from tkinter import *
from PIL import ImageTk, Image
import os
import pyautogui as pg
from funciones_tweetCloud import tweetcloud


class GUI(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        frame_base = Frame(self)
        self.menu = Menu(master=self)
        self.config(menu=self.menu)
        self.progMenu = Menu(self.menu)
        self.funcMenu = Menu(self.menu)
        self.menu.add_cascade(label="Programa", menu=self.progMenu)
        self.menu.add_cascade(label="Funciones", menu=self.funcMenu)
        self.progMenu.add_command(label="Pagina ppal",
                                  command=lambda:self.mostrar_frame(Pagina_ppal))
        self.funcMenu.add_command(label="Modificar pdfs",
                                 command=lambda:self.mostrar_frame(Pagina_1))
        frame_base.pack()
        
        self.frames = {}

        for F in (Pagina_ppal, Pagina_1):
            frame = F(frame_base, self)
            #Segun estos argumentos que le estoy pasando a las clases
            #del tuple a iterar, el frame_base es el parent y el controller
            #es el objeto de la clase GUI_PSSE que se esta creando.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.mostrar_frame(Pagina_ppal)
    def mostrar_frame(self, frame):
        frame = self.frames[frame]
        frame.tkraise()

class Pagina_ppal(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.config(width=1000, height=300)
        pathFile = os.path.dirname(os.path.realpath(sys.argv[0]))
        imgName = r"logo_twitter.png"
        pathImg = pathFile+ r"\\" + imgName
        self.img = ImageTk.PhotoImage(Image.open(pathImg))
        self.label_1 = Label(self, image=self.img)
        self.label_1.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.button = Button(self, text="TweetCloud",
                             command=lambda:controller.mostrar_frame(Pagina_1))
        self.button.place(relx=0.5, rely=0.5, anchor=CENTER)
            
class Pagina_1(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        """
        De esta forma puedo agregar ventanas dentro de cada ventana definida    
        como clase, en este caso, Pagina_1. Las ventanas que van a estar
        adentro de pagina 1 las voy a ir llamando frame1, frame2, etc
        Tambien es conveniente definir el ancho y largo que tendra la ventana
        asi, cuando la creo, no usando el self.frame1.config(widht=,height=),
        porque trae problemas
        """
        #creo el entry para ingresar el usuario
        self.label_1 = Label(self, text="Usuario")
        self.label_1.grid(row=0,column=0)
        self.e_1 = Entry(self)
        self.e_1.grid(row=0, column=1)
        #creo el dropdown menu
        self.opciones = ["Palabras", "Hashtags", "Emojis", "Links"]
        self.clicked = StringVar()
        self.clicked.set("Elegir wordcloud")
        self.drop = OptionMenu(self, self.clicked, *self.opciones)
        self.drop.grid(row=0, column=2)
        #doy la opcion de guardar o no el wordcloud
        self.var_1 = IntVar()
        self.var_1.set(1)
        self.boton_check_1 = Radiobutton(self, text="No guardar wordcloud",
                                         variable=self.var_1, value=1)
        self.boton_check_1.grid(row=1, column=0)
        self.boton_check_2 = Radiobutton(self, text="Guardar wordcloud",
                                         variable=self.var_1, value=2)
        self.boton_check_2.grid(row=1, column=1)
        #creo boton que imprimira el drop seleccionado
        self.boton = Button(self, text="Generar wordcloud",
                            command=lambda:printSeleccionado(self))
        self.boton.grid(row=2, column=0)

        def printSeleccionado(self):
            print(self.e_1.get(), self.clicked.get(), self.var_1.get())
            tweetcloud(self.e_1.get(), self.clicked.get(), self.var_1.get())
        """
        Asi trabajo con el self (pagina_1) de background y con los frame1,frame2
        etc de ventanitas que voy poniendo en el background. No tiene sentido
        trabajar con un frame1 de fondo si tengo al self como ventana principal
        """

            
   

"""
Al trabajar con clases de este modo, cada vez que crees un objeto de la clase
botones, dicho objeto se va a pasar como self por default y va a hacer lo que
sea que este en el init method, no es necesario llamar a ninguna funcion, ya
que desde el init method se estan llamando a otras funciones.

"""







