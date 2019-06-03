import setSound

class Frequencia():
    def __init__(self):
        
        self.keypadF =[[1209, 1336, 1477, 1633],
                        [697, 770, 852, 941]]

        self.one = [self.keypadF[0][0],self.keypadF[1][0]]
        self.two = [self.keypadF[0][1],self.keypadF[1][0]]
        self.three = [self.keypadF[0][2],self.keypadF[1][0]]
        self.four = [self.keypadF[0][0],self.keypadF[1][1]]
        self.five = [self.keypadF[0][1],self.keypadF[1][1]]
        self.six = [self.keypadF[0][2],self.keypadF[1][1]]
        self.seven = [self.keypadF[0][0],self.keypadF[1][2]]
        self.eight = [self.keypadF[0][1],self.keypadF[1][2]]
        self.nine = [self.keypadF[0][2],self.keypadF[1][2]]
        self.zero = [self.keypadF[0][1],self.keypadF[1][3]]

frequencia = Frequencia()

while True:
    print ("Input number:")
    num = int(input(""))
    if num == 1:
        setSound.som(frequencia.one)
    if num == 2:
        setSound.som(frequencia.two)
    if num == 3:
        setSound.som(frequencia.three)
    if num == 4:
        setSound.som(frequencia.four)
    if num == 5:
        setSound.som(frequencia.five)
    if num == 6:
        setSound.som(frequencia.six)
    if num == 7:
        setSound.som(frequencia.seven)
    if num == 8:
        setSound.som(frequencia.eight)
    if num == 9:
        setSound.som(frequencia.nine)
    if num == 0:
        setSound.som(frequencia.zero)
   