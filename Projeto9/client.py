import socket
import tkinter as tk
import time

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 5000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.TCP_IP, self.TCP_PORT))

    def create_widgets(self):
         
        self.entermessage = tk.Entry(self, fg="black")

        self.entermessage.pack(side="top")              

        self.sendbutton = tk.Button(self, text="Enviar texto", fg="black",
                              command=self.sendtext)
        self.sendbutton.pack(side="top")

        self.quit = tk.Button(self, text="Fechar janela", fg="black",
                              command=root.destroy)
        self.quit.pack(side="bottom")
        
    def sendtext(self):
        message = self.entermessage.get()
        message = message.encode('utf-8')
        self.s.send(message)
        print("Mensagem enviada")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
app.s.close()

