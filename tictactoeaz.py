import turtle
import subprocess
import tkinter
import sys
import time

# The following program will play tic tac toe. This
# program and a back end program communicate through pipes (both input and output)
# according to this architecture. When a command is sent to the back end it is indicated
# with a right arrow indicating something is written to the back end program's
# standard input. When the back end program sends something to this Python Program
# it is indicated with a left arrow. That means it is written to the standard
# output of the back end program.

# Front End    Back End
#   0 ----------->     # New Game is initiated by the back end Code
#   <----------- 0     # Back End Code says OK.
#   2 M --------->     # Human Move followed by Move Value M which is 0-8.
#                      # Move Value M will be on separate line.
#   <----------- 0     # Back End Code says OK.
#   1 ----------->     # Computer Move is indicated to Back End Code
#   <--------- 0 M     # Status OK and Move Value M which is 0-8.
#   3 ----------->     # Game Over?
#   <--------- Val     # Val is 0=Not Over, 1=Computer Won, 2=Human Won, 3=Tie.

# This architecture must be adhered to strictly for this program to work. Here
# is sample Lisp code that will handle this interaction.

#(defun play ()
  #(let ((gameBoard (make-hash-table :size 10))
        #(memo (make-hash-table :size 27 :test #'equalp)))

    #(do () (nil nil)
        #(let ((msgId (read)))
          #(cond ((equal msgId 2) ;; Human turn to call human turn function
                 #(humanTurn gameBoard))

                #((equal msgId 0) ;; New Game message
                 #(progn
                   #(setf gameBoard (make-hash-table :size 10))
                   #(setf memo (make-hash-table :size 27 :test #'equalp))
                   #(format t "0~%")))
                   #;; Return a 0 to indicate the computer is ready

                #((equal msgId 1) ;; Computer Turn message
                 #(computerTurn gameBoard memo))

                #((equal msgId 3) ;; Get Game Status

                 #(cond ((equal (evalBoard gameBoard) 1) (format t "1~%"))
                       #;; The Computer Won

                       #((equal (evalBoard gameBoard) -1) (format t "2~%"))
                       #;; The Human Won

                       #((fullBoard gameBoard) (format t "3~%"))
                       #;; It's a draw

                       #(t (format t "0~%"))))
                       #;; The game is not over yet.

                #(t (format t "-1~%")))))))

Computer = 1
Human = -1

class Tile(turtle.RawTurtle):
    def __init__(self,canvas,row,col,app):
        super().__init__(canvas)
        self.shape("tile.gif")
        self.val = 0
        self.row = row
        self.col = col
        self.tttApplication = app
        self.penup()
        self.goto(col*200+100,row*200+100)

    def setShape(self,horc):
        self.val = horc

        if horc == Computer:
            self.shape("X.gif") # You fill this in
        else:
            self.shape("O.gif") # You fill this in

    def getOwner(self):
        return self.val

    def clicked(self):
        print(self.row,self.col)

class TicTacToeApplication(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.buildWindow()
        self.running = False

    def buildWindow(self):

        self.master.title("Tic Tac Toe")

        bar = tkinter.Menu(self.master)
        fileMenu = tkinter.Menu(bar,tearoff=0)

        fileMenu.add_command(label="Exit",command=self.master.quit)

        bar.add_cascade(label="File",menu=fileMenu)

        self.master.config(menu=bar)

        canvas = tkinter.Canvas(self,width=600,height=600)
        canvas.pack(side=tkinter.LEFT)

        theTurtle = turtle.RawTurtle(canvas)
        theTurtle.ht()
        screen = theTurtle.getscreen()
        screen.setworldcoordinates(0,600,600,0)
        screen.register_shape("tile.gif")
        screen.register_shape("X.gif")
        screen.register_shape("O.gif")
        screen.tracer(0)

        def checkStatus():
            toBackEnd.write("3\n")
            toBackEnd.flush()

            status = int(fromBackEnd.readline().strip())

            if status == 1:
                tkinter.messagebox.showinfo("Game Over", "I Won!!!!!")
            elif status == 2:
                tkinter.messagebox.showinfo("Game Over", "You Won!!!!!")
            elif status == 3:
                 tkinter.messagebox.showinfo("Game Over", "It's a tie.")

            print("Status is ", status)
            return status

        def ComputerTurn():
            print("In Computer Turn")
            toBackEnd.write("1\n")
            toBackEnd.flush()
            status = int(fromBackEnd.readline().strip())
            print("Computer Turn Back End Status = ", status)
            if status == 0:
                move = int(fromBackEnd.readline())
                print("Move is", move)
                row = move // 3
                col = move % 3

                matrix[row][col].setShape(Computer)
                screen.update()

        def HumanTurn(x,y):
            if self.running:
                return

            status = checkStatus()

            if status != 0:
                return

            self.running = True
            col = int(x) // 200
            row = int(y) // 200
            print(row,col)
            val = row * 3 + col

            # Do the Human Turn
            toBackEnd.write("2\n")
            toBackEnd.flush()
            toBackEnd.write(str(val) + "\n")
            toBackEnd.flush()

            status = fromBackEnd.readline().strip()
            print("Status is ",status)

            matrix[row][col].setShape(Human)
            screen.update()

            # Check the status of the game
            status = checkStatus()

            if status == 0:
                # Do a Computer Turn
                ComputerTurn()
                checkStatus()

            self.running = False


        matrix = []

        for i in range(3):
            row = []
            for j in range(3):
                t = Tile(canvas,i,j,self)
                t.onclick(HumanTurn)
                row.append(t)
            matrix.append(row)

        screen.update()

        sideBar = tkinter.Frame(self,padx=5,pady=5, relief=tkinter.RAISED,borderwidth="5pt")
        sideBar.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)



        kb = tkinter.Button(sideBar,text="Pass",command=ComputerTurn)
        kb.pack()

        proc = subprocess.Popen(["python3","tictactoebackendaz.py"],stdout=subprocess.PIPE,stdin=subprocess.PIPE,universal_newlines=True)
        fromBackEnd = proc.stdout
        toBackEnd = proc.stdin

        # To write to back end you should use commands like this
        # toBackEnd.write(val+"\n")
        # Don't forget to flush the buffer
        # toBackEnd.flush()

        # To read from back end you write
        # line = fromBackEnd.readline().strip()



def main():
    root = tkinter.Tk()
    animApp = TicTacToeApplication(root)

    animApp.mainloop()
    print("Program Execution Completed.")

if __name__ == "__main__":
    main()
