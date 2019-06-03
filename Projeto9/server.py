import socket
import tkinter as tk
import time

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 1234
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.TCP_IP, self.TCP_PORT))
        self.s.accept()

    def create_widgets(self):
         
        self.showmessage = tk.Text(self, fg="black")

        #self.showmessage.insert(message)

        self.showmessage.pack(side="top")             

        self.showbutton = tk.Button(self, text="Visualizar texto", fg="black",
                              command=self.getText)
        self.showbutton.pack(side="top") 

        self.quit = tk.Button(self, text="Fechar janela", fg="black",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def getText(self,NData=1024*2):
        try:
            message = self.s.recv(NData)
            message = message.decode('utf-8')
            message = str(message)
            print(message)
        except:
            print("erro")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
app.s.close()

