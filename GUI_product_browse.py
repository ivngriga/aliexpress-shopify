import GUI_main_menu
import GUI_product_edit

import tkinter as tk
from PIL import ImageTk, Image
import os
from os import path

def goBack():
    global window
    
    window.destroy()
    GUI_main_menu.startMainMenu()

def updateDisplay(displayFrame, products, addon, titleLabel):
    for child in list(displayFrame.children.values()):
        child.pack_forget()
        child.destroy()

    for i in range(len(products)):
        if(i==8 or addon+i==len(products)):
            break
        createPreview(products[addon+i], i//4, i%4, displayFrame)

    txt="Browse Products, page: " + str(addon//8+1)
    titleLabel.config(text=txt)
    
def goLeft(displayFrame, products, titleLabel):
    global addon
    
    if(addon-8>=0):
        addon-=8
        updateDisplay(displayFrame, products, addon, titleLabel)

def goRight(displayFrame, products, titleLabel):
    global addon
    
    if(addon+8<len(products)):
        addon+=8
        updateDisplay(displayFrame, products, addon, titleLabel)

def redirect(directory):
    file= open("assets/temp.txt","w+")
    file.write(directory)
    file.close()

    window.destroy()
    GUI_product_edit.goto=0
    GUI_product_edit.startProductEdit()
    

def resizeIMG(img):
    w,h = img.size
    if(w>h):
        ratio=w/150
        w=150
        h=round(h/ratio)
    elif(w<h):
        ratio=h/150
        h=150
        w=round(w/ratio)
    else:
        w=150
        h=150
    img = img.resize((w,h), Image.ANTIALIAS)
    return img

def createPreview(directory, gridrow, gridcolumn, displayFrame):
    global window

    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"): 
            imagename=os.path.join(directory, filename)
            break
        
    file = open(directory+"/data.txt", "r")
    data = file.read().split(" -_-_- ")
    file.close

    name=data[0]
        
    productFrame=tk.Frame(master=displayFrame)
    img = Image.open(imagename)
    w, h = img.size
    previewimg = resizeIMG(img)
    previewimg = ImageTk.PhotoImage(previewimg)

    imageLabel = tk.Label(image=previewimg, master=productFrame, width= 155, height=175)
    imageLabel.image = previewimg

    redirectButton = tk.Button(
                text=name[0:18],
                width=15,
                bg="white",
                fg="purple",
                master=productFrame,
                command = lambda: redirect(directory)
            )

    imageLabel.pack(side=tk.TOP)
    redirectButton.pack()

    productFrame.grid(row=gridrow, column=gridcolumn)

window = 0
addon=0

def startProductBrowse():
    global window
    global page
    
    page=1

    window = tk.Tk()
    window.geometry('650x550')

    window.eval('tk::PlaceWindow . center')

    titleFrame=tk.Frame(master=window)
    displayFrame=tk.Frame(master=window)
    buttonsFrame=tk.Frame(master=window)
    headerFrame=tk.Frame(master=window)

    products=[]

    file = open("assets/data.txt", "r")
    data = file.read().split(" -_-_- ")
    file.close
        
    directory=data[0]

    for filename in os.listdir(directory):
        if(path.isdir(os.path.join(directory, filename))):
            products.append(os.path.join(directory, filename))

    products.sort()

    txt="Browse Products, page: " + str(addon+1)
    titleLabel = tk.Label(master=titleFrame,text=txt, font=("Arial", 20))

    updateDisplay(displayFrame, products, addon, titleLabel)

    # Return Button
    returnButton = tk.Button(
        text="Return",
        width=8,
        bg="white",
        fg="purple",
        master=headerFrame,
        command = goBack
    )

    arrowright = Image.open("assets/arrowright.png")
    arrowright = arrowright.resize((35, 35), Image.ANTIALIAS)
    arwright = ImageTk.PhotoImage(arrowright)
    arw1button = tk.Button(image=arwright,command= lambda: goRight(displayFrame, products, titleLabel), borderwidth=0, master=buttonsFrame)

    arrowleft = Image.open("assets/arrowleft.png")
    arrowleft = arrowleft.resize((35, 35), Image.ANTIALIAS)
    arwleft = ImageTk.PhotoImage(arrowleft)
    arw2button = tk.Button(image=arwleft,command= lambda: goLeft(displayFrame, products, titleLabel), borderwidth=0, master=buttonsFrame)

    returnButton.pack(side=tk.LEFT)
    titleLabel.pack()
    arw1button.pack(side=tk.RIGHT, padx=75)
    arw2button.pack(side=tk.LEFT, padx=75)

    headerFrame.pack(side=tk.TOP, anchor=tk.NW)
    titleFrame.pack()
    displayFrame.pack(pady=15)
    buttonsFrame.pack()

    window.mainloop()

