# encoding: UTF-8
# Authors: Luis / Bobby

from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.filedialog import askopenfilename


# textbook matrix multiplication algorithm
def multiplyText(A, B):

    m = len(A)
    k = len(B)
    n = len(A[0])

    C = [[0 for j in range(k)] for i in range(m)]

    for i in range(m):
        for j in range(k):
            for step in range(n):
                C[i][j] += A[i][step]*B[step][j]
    return C
    #print(prodCount)


# auxiliary methods for strassen()

def matrixAdd(A,B):
    rows = len(A)
    columns = len(A[0])
    C = [[0 for j in range(columns)] for i in range(rows)]

    for i in range(rows):
        for j in range(columns):
            C[i][j] += A[i][j]+B[i][j]
    return C


def matrixSubstract(A, B):
    rows = len(A)
    columns = len(A[0])
    C = [[0 for j in range(columns)] for i in range(rows)]

    for i in range(rows):
        for j in range(columns):
            C[i][j] = A[i][j] - B[i][j]

    return C


def strassen(A,B):

    # Base case
    if len(A) == 2:
        return multiplyText(A,B)
    else:
        # The following will be done recursively until length of matrix equals 2
        shift = len(A) // 2
        length = len(A)

        a11 = [[A[i][j] for j in range(shift)] for i in range(shift)]
        a12 = [[A[i][j] for j in range(shift, length)] for i in range(shift)]
        a21 = [[A[i][j] for j in range(shift)] for i in range(shift, length)]
        a22 = [[A[i][j] for j in range(shift, length)] for i in range(shift,length)]

        b11 = [[B[i][j] for j in range(shift)] for i in range(shift)]
        b12 = [[B[i][j] for j in range(shift, length)] for i in range(shift)]
        b21 = [[B[i][j] for j in range(shift)] for i in range(shift, length)]
        b22 = [[B[i][j] for j in range(shift, length)] for i in range(shift, length)]


        # First, calculate M1, M2, M3, M4, M5, M6 and M7
        # m1 = (a11 + a22) * (b11+b22)
        m1 = strassen(matrixAdd(a11,a22), matrixAdd(b11,b22))

        # m2 = (a21 + a22) * b11
        m2 = strassen(matrixAdd(a21, a22), b11)

        # m3 = a11 * (b12 - b22)
        m3 = strassen(a11, matrixSubstract(b12, b22))

        # m4 = a22 * (b21 - b11)
        m4 = strassen(a22, matrixSubstract(b21, b11))

        # m5 = (a11 + a12) * b22
        m5 = strassen(matrixAdd(a11, a12), b22)

        # m6 = (a21 - a11) * (b11 + b12)
        m6 = strassen(matrixSubstract(a21, a11), matrixAdd(b11, b12))

        # m7 = (a12 - a22) * (b21 + b22)
        m7 = strassen(matrixSubstract(a12, a22), matrixAdd(b21, b22))


        # Now calculate C11, C12, C21 and C22
        # c11 = m1 + m4 - m5 + m7
        c11 =  matrixAdd(matrixSubstract(matrixAdd(m1,m4),m5), m7)
        c12 = matrixAdd(m3, m5)
        c21 = matrixAdd(m2, m4)
        c22 = matrixAdd(matrixAdd(matrixSubstract(m1, m2), m3), m6)

        C = [[0 for i in range(length)] for j in range(length)]

        for i in range(shift):
            for j in range(shift):
                C[i][j] = c11[i][j]
                C[i][j+shift] = c12[i][j]
                C[i+shift][j] = c21[i][j]
                C[i+shift][j+shift] = c22[i][j]
        return C


# master method: select the files and run both matrix multiplication algorithms
def multiplyMatrices():
    # we DON'T want home window at the very top anymore
    window.attributes('-topmost', False)

    # open matrix 1
    pathA = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"),      # path to file 1
                                                     ("All files", "*.*")))
    matrixA = open(pathA, 'r').read().splitlines()
    A = []
    for line in matrixA:
        A.append([int(x) for x in line.rstrip().split(",")])
    #print(A)
    messagebox.showinfo("Success", "Matrix A loaded")

    # open matrix 2
    pathB = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"),      # path to file 2
                                                     ("All files", "*.*")))
    matrixB = open(pathB, 'r').read().splitlines()
    B = []
    for line in matrixB:
        B.append([int(x) for x in line.rstrip().split(",")])
    #print(B)
    messagebox.showinfo("Success", "Matrix B loaded")

    if len(A[0]) != len(B):
        print("Can't have multiplication!")
        exit()

    #print("Basic", multiplyText(A, B))

    if len(A) != len(A[0]):
        print("Strassen's Algorithm requires two square matrixes")
        exit()


    textInMatForm = ''
    for mat in multiplyText(A,B):
        textInMatForm = textInMatForm + str(mat) + "\n"

    strassenInMatForm = ''
    for mat in strassen(A,B):
        strassenInMatForm = strassenInMatForm + str(mat) + "\n"


    # print resulting matrices to the console
    print("Textbook matrix multiplication:")
    print(textInMatForm)
    print("Strassen's algorithm matrix multiplication:")
    print(strassenInMatForm)

    # write on the file (if we decide to take this approach)
    salida = open("matrices.txt", "w", encoding="UTF-8")
    salida.write("\n***In order for the matrices to display properly, it is recommended to make the TextEdit or other\n"
                 "window where you're watching them as large as you can on your computer monitor.\n")
    salida.write("\nMatrix multiplication by textbook:\n")
    salida.write(textInMatForm)
    salida.write("\n\t--------------------------\n\n")
    salida.write("Matrix multiplication by Strassen's algorithm:\n")
    salida.write(strassenInMatForm)
    salida.close()



    solutionWindow = Tk()
    solutionWindow.title("Solutions")
    solutionWindow.geometry("1000x840")
    ANCHO = 1000
    ALTO = 840
    solutionWindow.attributes('-topmost', True)

    tagTextbook = Label(solutionWindow, text="Textbook solution", justify = LEFT).grid(row = 1, column = 1)
    tagSolTextbook = Label(solutionWindow, text=textInMatForm).grid(row = 2, column = 1)
    tagMultipCountTe = Label(solutionWindow, text="number of scalar multiplications: ", justify=LEFT).grid(row=3, column=1)
    whitspc = Label(solutionWindow, text="", justify=LEFT).grid(row=4, column=1)
    tagStrassen = Label(solutionWindow, text="Strassen's algorithm solution", justify = LEFT).grid(row = 5, column = 1)
    tagSolStrassen = Label(solutionWindow, text=strassenInMatForm).grid(row = 6, column = 1)
    tagMultipCountSt = Label(solutionWindow, text="number of scalar multiplications: ", justify=LEFT).grid(row=7, column=1)

    altCloseTab = Label(solutionWindow, text="Click on the close button on the window's top left corner to exit.",
                        justify=LEFT).place(x = 10, y = ALTO - 40)

    # REVISAR, hay que clicar dos veces y a la 2da cierra las 2 ventanas
    #exitButton = Button(solutionWindow, text="Close this window", command=solutionWindow.quit).place(x=450, y=565) # REVISAR

    solutionWindow.mainloop()







# home window and its contents
window = Tk()
window.title("1st term project - Luis / Roberto")
window.geometry("600x600")
ANCHO = 600
ALTO = 600
window.attributes('-topmost', True)

tagInfo = Label(window, text = "Luis Alfonso Alcántara López-Ortega - A01374785\n"
                               "Roberto Téllez Perezyera - A01374866", justify = RIGHT).place(x = ANCHO - 345, y = 5)
tag1 = Label(window, text = "Welcome to our program.").place(x = 10, y = 60)
tag2 = Label(window, text = "Here you can run the textbook and the Strassen algorithms for matrix multiplication.").place(x = 10, y = 90)
tag3 = Label(window, text = "Click on the Start button to begin.").place(x = 10, y = 120)
tag4 = Label(window, text = "You will be asked to open the files and the solutions will be displayed in another window.").place(x = 10, y = 150)
tagn = Label(window, text = "You can close that new window and repreat the process from this one.").place(x = 10, y = 180)
tagn1 = Label(window, text = "Click on Quit on the lower right corner to close this window.").place(x = 10, y = 210)

startButton = Button(window, text = "Start", command = multiplyMatrices).place(x = (ANCHO // 2)-30, y = ALTO // 2)
exitButton = Button(window, text = "Quit", command = window.quit).place(x = 540, y = 565)

window.mainloop()
