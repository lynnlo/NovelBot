# Imports
import tkinter
from PIL import Image, ImageTk
from tkinter.font import Font

# Gui
main = tkinter.Tk()

# Config
main.geometry("640x820+640+320")
main.title("Sythphonic")
#main.iconbitmap("././src/images/icon.png")
main.resizable(False, False)
main.overrideredirect(True)
main.attributes("-alpha", 0.9)
main.attributes("-topmost", True)
main.configure(background="#353535")

# Fonts
titlefont = Font(family="Yu Gothic", size=14)
titletext = tkinter.Text(main, font=titlefont)
buttonfont = Font(family="Cascadia Mono Light", size=12)
buttontext = tkinter.Text(main, font=buttonfont)
textfont = Font(family="Cascadia Mono Light", size=12)
inputfont = Font(family="Cascadia Mono Light", size=16)

# Variables
borderless = True
drag = False

# Functions
def close():
    main.destroy()

def switch_modes():
    global borderless
    borderless = not borderless
    main.overrideredirect(borderless)
    button["activebackground"] = "#303030" if borderless else "#353535"

def drag_start(e):
    global drag
    if borderless:
        drag = True
        main.x = e.x
        main.y = e.y
        titlelabel["background"] = "#303030"
        iconcanvas["background"] = "#303030"

def drag_stop(e):
    global drag
    if borderless:
        drag = False
        titlelabel["background"] = "#353535"
        iconcanvas["background"] = "#353535"

def drag(e):
    if borderless:
        dx = e.x - main.x
        dy = e.y - main.y
        mx = main.winfo_x() + dx
        my = main.winfo_y() + dy
        main.geometry("+"+str(mx)+"+"+str(my))
    

# Move
button = tkinter.Button(main, width=95, height=5, background="#353535", activebackground="#303030", borderwidth=0)

button.bind("<ButtonPress-1>", drag_start)
button.bind("<ButtonRelease-1>", drag_stop)
button.bind("<B1-Motion>", drag)

button.place(x=0, y=0)

# Icon
iconfile = Image.open("././src/images/icon.png").resize((25, 25))
icon= ImageTk.PhotoImage(iconfile)
iconcanvas = tkinter.Canvas(main, width=25, height=25, background="#353535", highlightthickness=0)
iconcanvas.create_image(12.5, 12.5, image=icon)

iconcanvas.place(x=0, y=0)

# Title
titlelabel = tkinter.Label(main, width=10, font=titlefont, height=1, text="Novel Bot", borderwidth=0, background="#353535", foreground="#808080",)

titlelabel.place(x=25, y=0)

# Banner
bannerfile = Image.open("././src/images/banner.png").resize((640, 200))
banner = ImageTk.PhotoImage(bannerfile)
bannercanvas = tkinter.Canvas(main, width=640, height=200, background="#353535", highlightthickness=0)
bannercanvas.create_image(320, 100, image=banner)

bannercanvas.place(x=0, y=25)


# Naivgation
exitbutton = tkinter.Button(main, width=8, height=1, font=buttonfont, text="CLOSE", borderwidth=0, background="#202020", activebackground="#252525", foreground="#808080", activeforeground="#808080", command=close)
switchbutton = tkinter.Button(main, width=8, height=1, font=buttonfont, text="SWITCH", borderwidth=0, background="#202020", activebackground="#252525", foreground="#808080", activeforeground="#808080", command=switch_modes)

exitbutton.place(x=0, y=175)
switchbutton.place(x=100, y=175)

# Settings
lengthlabel = tkinter.Label(main, width=16, height=1, anchor="w", font=textfont, text="Length", background="#353535", foreground="#808080")
lengthinput = tkinter.Entry(main, width=32, font=inputfont, borderwidth=0, background="#202020", foreground="#a0a0a0")

lengthlabel.place(x=25, y=225)
lengthinput.place(x=25, y=250)

# Output
textlabel = tkinter.Label(main, width=16, height=1, anchor="w", font=textfont, text="Output", background="#353535", foreground="#808080")
textarea = tkinter.Text(main, width=65, height=16, font=textfont, borderwidth = 0, background="#202020")

textlabel.place(x=25, y=300)
textarea.place(x=25, y=325)

# Create
createbutton = tkinter.Button(main, width=16, height=1, font=buttonfont, text="CREATE", borderwidth=0, background="#303030", activebackground="#353535", foreground="#b0b0b0", activeforeground="#b0b0b0",)

createbutton.place(x=450, y=750)

main.mainloop()