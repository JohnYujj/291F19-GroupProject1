import tkinter

window = tkinter.Tk()
window.title("Window")

userNameLabel = tkinter.Label(window, text="Username:")
userNameLabel.pack()

loginTextBox = tkinter.Text(window, height = 2, width = 10)
loginTextBox.pack()

loginButton = tkinter.Button(window, text="Login")
loginButton.pack()

window.mainloop()