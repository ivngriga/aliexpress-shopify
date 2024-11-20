import GUI_product_browse
import GUI_product_download
import shutil

import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import os

def resizeIMG(img):
    w,h = img.size
    if(w>h):
        ratio=w/250
        w=250
        h=round(h/ratio)
    elif(w<h):
        ratio=h/250
        h=250
        w=round(w/ratio)
    else:
        w=250
        h=250
    img = img.resize((w,h), Image.ANTIALIAS)
    return img

def delProduct(selected):
    global window

    answer=messagebox.askyesno(title='Confirm', message='Are you sure you want to delete?')

    if(answer==True):
        shutil.rmtree(selected)

        window.destroy()
        if(goto==0):
            GUI_product_browse.startProductBrowse()
        else:
            GUI_product_download.startProductDownload()

def delIMG(selected, label1, curimg):
    global images
    global image
    
    answer=messagebox.askyesno(title='Confirm', message='Are you sure you want to delete?')

    if(answer==True):
        os.remove(images[image])

    image=0
    images=[]
    for filename in os.listdir(selected):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"): 
            images.append(os.path.join(selected, filename))

    changeIMG(images,label1,curimg)
        

def previewIMG(imagename,left,top,right,bottom, frame1):
    global cropImage
    img = Image.open(imagename)
    croppedimg=img.crop((int(left), int(top), int(right), int(bottom)))
    croppedimg = resizeIMG(croppedimg)
    croppedimg = ImageTk.PhotoImage(croppedimg)

    labeltemp=tk.Label(image=croppedimg, master=frame1)
    labeltemp.image=croppedimg

    cropImage.config(image=croppedimg)
    cropImage.image = croppedimg


def saveIMG(imagename,left,top,right,bottom, images, label1, curimg):
    global cropImage
    img = Image.open(imagename)
    img=img.crop((int(left), int(top), int(right), int(bottom)))

    img = img.save(imagename)
    changeIMG(images,label1,curimg)

def cropIMG(newWindow, images, curimg, window, label1):
    global cropImage
    global image
    #global newWindow

    if (newWindow.winfo_exists()==0):
    
        imagename=images[image]
        temp=curimg

        newWindow=tk.Toplevel(window)
        newWindow.title("Crop Image")
        newFrame=tk.Frame(master=newWindow)
        buttonsFrame=tk.Frame(master=newWindow)
        
        txt=tk.Label(text=imagename, master=newWindow)
        
        img = Image.open(imagename)
        w, h = img.size
        previewimg = resizeIMG(img)
        previewimg = ImageTk.PhotoImage(previewimg)

        cropImage = tk.Label(image=previewimg, master=newWindow)
        cropImage.image = previewimg

        leftName = tk.Label(master=newFrame, text="Left")
        leftEntry = tk.Text(
            fg="purple",
            bg="white",
            width=5,
            height=1,
            master=newFrame
        )
        leftEntry.insert("1.0","0")

        rightName = tk.Label(master=newFrame, text="Right")
        rightEntry = tk.Text(
            fg="purple",
            bg="white",
            width=5,
            height=1,
            master=newFrame
        )
        rightEntry.insert("1.0",w)

        bottomName = tk.Label(master=newFrame, text="Bottom")
        bottomEntry = tk.Text(
            fg="purple",
            bg="white",
            width=5,
            height=1,
            master=newFrame
        )
        bottomEntry.insert("1.0",h)

        topName = tk.Label(master=newFrame, text="Top")
        topEntry = tk.Text(
            fg="purple",
            bg="white",
            width=5,
            height=1,
            master=newFrame
        )
        topEntry.insert("1.0","0")

        previewButton = tk.Button(
            text="Preview Changes",
            width=15,
            bg="white",
            fg="purple",
            master=buttonsFrame,
            command = lambda: previewIMG(imagename,
                                 leftEntry.get("1.0",'end-1c'),
                                 topEntry.get("1.0",'end-1c'),
                                 rightEntry.get("1.0",'end-1c'),
                                 bottomEntry.get("1.0",'end-1c'),
                                 newWindow
                                 )
        )

        savingButton = tk.Button(
            text="Save Changes",
            width=15,
            bg="white",
            fg="purple",
            master=buttonsFrame,
            command = lambda: saveIMG(imagename,
                                 leftEntry.get("1.0",'end-1c'),
                                 topEntry.get("1.0",'end-1c'),
                                 rightEntry.get("1.0",'end-1c'),
                                 bottomEntry.get("1.0",'end-1c'),
                                 images,
                                 label1,
                                 curimg
                                 )
        )

        leftName.grid(row=0, column=0)
        leftEntry.grid(row=0, column=1)

        rightName.grid(row=0, column=3)
        rightEntry.grid(row=0, column=2)

        bottomName.grid(row=1, column=0)
        bottomEntry.grid(row=1, column=1)

        topName.grid(row=1, column=3)
        topEntry.grid(row=1, column=2)
        
        txt.pack()
        cropImage.pack()

        previewButton.pack(side=tk.LEFT)
        savingButton.pack(side=tk.RIGHT)

        newFrame.pack()
        buttonsFrame.pack()

def goBack():
    global window
    global images

    images=[]
    
    window.destroy()
    if(goto==0):
        GUI_product_browse.startProductBrowse()
    else:
        GUI_product_download.startProductDownload()

def changeIMG(images,label1,curimg):
    global image

    img = Image.open(images[image])
    img = resizeIMG(img)
    curimg = ImageTk.PhotoImage(img)

    label1.config(image=curimg)
    label1.image = curimg

    
def goRight(images, label1, curimg):
    global image

    if(image<len(images)-1):
        image+=1
        changeIMG(images,label1,curimg)
        

def goLeft(images, label1, curimg):
    global image
    
    if(image>0):
        image-=1
        changeIMG(images,label1,curimg)

def saveChanges(titleEntry, descEntry, tagEntry, colEntry, priceEntry, salepriceEntry, selected):
    sep = " -_-_- "
    newtitle = titleEntry.get()
    newdesc = descEntry.get("1.0",'end-1c')
    newtag = tagEntry.get()
    newcol = colEntry.get()
    newprice = priceEntry.get()
    newsaleprice = salepriceEntry.get()
    newdata = newtitle + sep + newdesc + sep + newtag + sep + newcol + sep + newprice + sep + newsaleprice
    dir = selected+"/data.txt"
    file= open(dir,"w+")
    file.write(newdata)
    file.close()

image = 0
window = 0
goto = 1
images=[]
# Create window
def startProductEdit():
    global page
    global image
    global window
    global images
    
    page=0
    window = tk.Tk() 
    window.geometry('650x550')
    window.eval('tk::PlaceWindow . center')
    newWindow=tk.Toplevel(window)
    newWindow.destroy()


    file = open("assets/temp.txt", "r")
    selected = file.read()
    file.close()

    window.title(selected)

    for filename in os.listdir(selected):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"): 
            images.append(os.path.join(selected, filename))

    dir = selected + "/data.txt"
    file = open(dir, "r")
    data = file.read().split(" -_-_- ")
    file.close()

    #frame=tk.Frame(master=window,relief=tk.RIDGE)

    frameall = tk.Frame(relief=tk.RIDGE)
    framehead = tk.Frame(master=frameall,relief=tk.RIDGE)
    frame1 = tk.Frame(master=frameall,relief=tk.RIDGE)
    frameimg = tk.Frame(master=frameall,relief=tk.RIDGE)
    framearrows = tk.Frame(master=frameimg, relief=tk.RIDGE)
    framegrid = tk.Frame(master=frame1, relief=tk.RIDGE)
    framebottom = tk.Frame(master=window, relief=tk.RIDGE)

    # Return Button
    returnButton = tk.Button(
        text="Return",
        width=8,
        bg="white",
        fg="purple",
        master=framehead,
        command = lambda: goBack()
    )


    # Back Front Arrows
    arrowright = Image.open("assets/arrowright.png")
    arrowright = arrowright.resize((35, 35), Image.ANTIALIAS)
    arwright = ImageTk.PhotoImage(arrowright)
    arw1button = tk.Button(image=arwright,command= lambda: goRight(images, label1, curimg), borderwidth=0, master=framearrows)

    arrowleft = Image.open("assets/arrowleft.png")
    arrowleft = arrowleft.resize((35, 35), Image.ANTIALIAS)
    arwleft = ImageTk.PhotoImage(arrowleft)
    arw2button = tk.Button(image=arwleft,command= lambda: goLeft(images, label1, curimg), borderwidth=0, master=framearrows)

    # Image
    image = 0;
    image1 = Image.open(images[image])
    image1 = resizeIMG(image1)
    curimg = ImageTk.PhotoImage(image1)

    label1 = tk.Label(image=curimg, master=frameimg, width= 250, height=250)

    # Crop Button
    cropButton = tk.Button(
        text="Crop Image",
        width=15,
        bg="white",
        fg="purple",
        master=frameimg,
        command = lambda: cropIMG(newWindow, images, curimg, window, label1)
    )

    # Delete Image Button
    delIMGButton = tk.Button(
        text="Delete Image",
        width=15,
        bg="white",
        fg="purple",
        master=frameimg,
        command = lambda: delIMG(selected, label1, curimg)
    )

    # Save Button
    saveButton = tk.Button(
        text="Save Product",
        width=25,
        bg="white",
        fg="purple",
        master=framebottom,
        command = lambda: saveChanges(titleEntry, descEntry, tagEntry, colEntry, priceEntry, salepriceEntry, selected)
    )

    # Delete Button
    deleteButton = tk.Button(
        text="Delete Product",
        width=25,
        bg="white",
        fg="purple",
        master=framebottom,
        command = lambda: delProduct(selected)
    )

    # Title Entry
    titleName = tk.Label(master=frame1, text="Title")
    titleEntry = tk.Entry(
        fg="purple",
        bg="white",
        width=40,
        master=frame1
        
    )
    titleEntry.insert(0, data[0])

    # Sale Price Entry
    salepriceName = tk.Label(master=framegrid, text="Sale Price")
    salepriceEntry = tk.Entry(
        fg="purple",
        bg="white",
        width=20,
        master=framegrid
    )
    salepriceEntry.insert(0, data[5])

    # Price Entry
    priceName = tk.Label(master=framegrid, text="Price")
    priceEntry = tk.Entry(
        fg="purple",
        bg="white",
        width=20,
        master=framegrid
    )
    priceEntry.insert(0, data[4])

    # Description Entry
    descName = tk.Label(master=frame1, text="Description")
    descEntry = tk.Text(
        fg="purple",
        bg="white",
        width=51,
        master=frame1
    )
    descEntry.insert("1.0",data[1])

    # Tag Entry
    tagName = tk.Label(master=framegrid, text="Tags")
    tagEntry = tk.Entry(
        fg="purple",
        bg="white",
        width=20,
        master=framegrid
    )
    tagEntry.insert(0, data[2])

    # Collection Entry
    colName = tk.Label(master=framegrid, text="Collections")
    colEntry = tk.Entry(
        fg="purple",
        bg="white",
        width=20,
        master=framegrid
    )
    colEntry.insert(0, data[3])


    # Add it to window

    # pack widgets
    returnButton.pack(side=tk.LEFT)

    label1.pack(side=tk.TOP)

    arw1button.pack(side=tk.RIGHT)
    arw2button.pack(side=tk.LEFT)

    cropButton.pack(side=tk.BOTTOM)
    delIMGButton.pack(side=tk.BOTTOM, pady=25)

    titleName.pack()
    titleEntry.pack()

    descName.pack()
    descEntry.pack()

    tagName.grid(row=0,column=0)
    tagEntry.grid(row=1,column=0)
    colName.grid(row=0,column=1)
    colEntry.grid(row=1,column=1)
    salepriceName.grid(row=2,column=0)
    salepriceEntry.grid(row=3, column=0)
    priceName.grid(row=2, column=1)
    priceEntry.grid(row=3, column=1)

    saveButton.pack(side=tk.RIGHT)
    deleteButton.pack(side=tk.LEFT)



    # pack frames
    frameall.pack()
    framehead.pack(side=tk.TOP, anchor=tk.NW)
    frame1.pack(side=tk.RIGHT)
    framegrid.pack(side=tk.RIGHT)
    frameimg.pack(side=tk.LEFT)
    framearrows.pack()
    framebottom.pack()


    window.bind("<Return>", changeIMG)
    window.mainloop()
