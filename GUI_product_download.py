import GUI_main_menu
import GUI_product_edit

import tkinter as tk
from PIL import ImageTk, Image
import os
from bs4 import BeautifulSoup
import requests
import re
import json
import urllib.request
from os import path

def redirect(directory):
    global window
    
    file= open("assets/temp.txt","w+")
    file.write(directory)
    file.close()

    window.destroy()
    GUI_product_edit.startProductEdit()
    

def resizeIMG(img):
    w,h = img.size
    if(w>h):
        ratio=w/130
        w=130
        h=round(h/ratio)
    elif(w<h):
        ratio=h/130
        h=130
        w=round(w/ratio)
    else:
        w=130
        h=130
    img = img.resize((w,h), Image.ANTIALIAS)
    return img

def updateDisplay(historyFrame):
    file = open("assets/data.txt", "r")
    data = file.read().split(" -_-_- ")[1:10]
    file.close()

    for child in list(historyFrame.children.values()):
        child.pack_forget()
        child.destroy()

    for i in range(len(data)-1):
        if(path.isdir(os.path.join(data[i]))):
            createPreview(data[i], i//4, i%4, historyFrame)
        else:
            createPreview("noproduct", i//4, i%4, historyFrame)

def createPreview(directory, gridrow, gridcolumn, historyFrame):
    #global window
    #global historyFrame
    if(directory!="noproduct"):
        for filename in os.listdir(directory):
            if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"): 
                imagename=os.path.join(directory, filename)
                break
        
        file = open(directory+"/data.txt", "r")
        data = file.read().split(" -_-_- ")
        file.close

        name=data[0]
    else:
        name="Product Not Found"

    productFrame=tk.Frame(master=historyFrame)
    if(directory!="noproduct"):
        img = Image.open(imagename)
        w, h = img.size
        previewimg = resizeIMG(img)
        previewimg = ImageTk.PhotoImage(previewimg)
    else:
        img = Image.open("assets/no_product.png")
        w, h = img.size
        previewimg = resizeIMG(img)
        previewimg = ImageTk.PhotoImage(previewimg)

    imageLabel = tk.Label(image=previewimg, master=productFrame, width= 135, height=145)
    imageLabel.image = previewimg

    if(directory!="noproduct"):
        redirectButton = tk.Button(
                    text=name[0:18],
                    width=15,
                    bg="white",
                    fg="purple",
                    master=productFrame,
                    command = lambda: redirect(directory)
                )
    else:
        redirectButton = tk.Button(
                    text=name[0:18],
                    width=15,
                    bg="white",
                    fg="purple",
                    master=productFrame,
                )

    imageLabel.pack(side=tk.TOP)
    redirectButton.pack()
    productFrame.grid(row=gridrow, column=gridcolumn)

def goBack():
    global window
    
    window.destroy()
    GUI_main_menu.startMainMenu()

def dlProduct(dlEntry, statusCanvas, statusBG, statusTXT, directory, historyFrame):
    url = dlEntry.get()
    
    statusCanvas.itemconfig(statusBG,fill="lightblue")
    statusCanvas.itemconfig(statusTXT,text="Downloading...")
    window.update()

    if(url == ""):
        statusCanvas.itemconfig(statusBG,fill="#FF7F7F")
        statusCanvas.itemconfig(statusTXT,text="Enter URL")
        window.update()
        return

    if(url.find("aliexpress") == -1):
        statusCanvas.itemconfig(statusBG,fill="#FF7F7F")
        statusCanvas.itemconfig(statusTXT,text="URL must contain AliExpress")
        window.update()
        return
    
    if(url.find(".com") == -1):
        statusCanvas.itemconfig(statusBG,fill="#FF7F7F")
        statusCanvas.itemconfig(statusTXT,text="URL must contain .com")
        window.update()
        return

    if(url.find("https") == -1):
        statusCanvas.itemconfig(statusBG,fill="#FF7F7F")
        statusCanvas.itemconfig(statusTXT,text="URL must contain https")
        window.update()
        return

    try:
        r = requests.get(url)
        jsonData = re.search(r'data: ({.+})', r.text)
        temp=jsonData.group().replace("data: ", "")
        jsonData = json.loads(temp)

        price=jsonData['priceModule']['minAmount']['formatedAmount']+"-"+jsonData['priceModule']['maxAmount']['formatedAmount']
        title = jsonData['titleModule']['subject']
        images=jsonData['imageModule']['imagePathList']
        
        page = requests.get(jsonData['descriptionModule']['descriptionUrl'])
        soup = BeautifulSoup(page.content, 'html.parser')
        description = soup.find('p',"detail-desc-decorate-content")
        if(description!=None):
            description=description.getText()
        else:
            description=" "
    except Exception as e:
        statusCanvas.itemconfig(statusBG,fill="#FF7F7F")
        statusCanvas.itemconfig(statusTXT,text="Try another URL")
        window.update()
        return

    if(len(title)>50):
        dirName=(directory+title[0:50]).replace(" ","_")
    else:
        dirName=(directory+title).replace(" ","_")

    if(path.isdir(os.path.join(dirName)) == False):
        os.makedirs(dirName)

        sep = " -_-_- "
        data=title+sep+description+sep+" "+sep+" "+sep+price+sep+price
        file=open(dirName+"/data.txt","w+")
        file.write(data)
        file.close()

        i=0
        for image in images:
            extension = os.path.splitext(image)[1]
            urllib.request.urlretrieve(image, dirName+"/"+str(i)+extension)
            i+=1

        file = open("assets/data.txt", "r")
        history = file.read().split(" -_-_- ")[0:10]
        file.close()
        history[2:10]=history[1:9]
        history[1]=dirName

        newtxt=history[0]
        for x in history[1:10]:
            newtxt+=sep+x
        
        newtxt = newtxt.replace("  -_-_- ", " -_-_- ")

        file= open("assets/data.txt","w+")
        file.write(newtxt)
        file.close()

        updateDisplay(historyFrame)
        
        statusCanvas.itemconfig(statusBG,fill="lightgreen")
        statusCanvas.itemconfig(statusTXT,text="Success!")
        window.update()
    else:
        statusCanvas.itemconfig(statusBG,fill="#FF7F7F")
        statusCanvas.itemconfig(statusTXT,text="Product Already Downloaded")
        window.update()
    

window = 0

def startProductDownload():
    global page
    global window
    
    page=2
    
    window = tk.Tk()
    window.geometry('650x550')
    window.eval('tk::PlaceWindow . center')

    headerFrame=tk.Frame(master=window)
    mainFrame=tk.Frame(master=window)
    histnameFrame=tk.Frame(master=window)
    historyFrame=tk.Frame(master=window)

    file = open("assets/data.txt", "r")
    data = file.read().split(" -_-_- ")
    file.close
        
    directory=data[0]

    # Return Button
    returnButton = tk.Button(
        text="Return",
        width=8,
        bg="white",
        fg="purple",
        master=headerFrame,
        command = goBack
    )

    # Download Entry
    dlName = tk.Label(master=mainFrame, text="Enter Aliexpress Link:")
    dlEntry = tk.Entry(
        fg="purple",
        bg="white",
        width=80,
        master=mainFrame
    )

    # Status Bar
    statusCanvas = tk.Canvas(mainFrame, background = "#FFFFFF", width=200,height=50)
    statusBG = statusCanvas.create_rectangle(0, 0, 200, 50, fill="grey80", outline="grey60")
    statusTXT = statusCanvas.create_text(100, 25, text="Not Started")

    # Download Button
    dlButton = tk.Button(
        text="Download Product",
        width=25,
        bg="white",
        fg="purple",
        master=mainFrame,
        command = lambda: dlProduct(dlEntry, statusCanvas, statusBG, statusTXT, directory, historyFrame)
    )

    # History Label
    historyName = tk.Label(master=histnameFrame, text="History of Downloaded Products:")

    returnButton.pack(side=tk.LEFT)

    file = open("assets/data.txt", "r")
    data = file.read().split(" -_-_- ")[1:10]
    file.close()

    updateDisplay(historyFrame)

    dlName.pack()
    dlEntry.pack()
    statusCanvas.pack(side=tk.LEFT)
    dlButton.pack(side=tk.RIGHT)
    historyName.pack()

    headerFrame.pack(side=tk.TOP, anchor=tk.NW)
    mainFrame.pack()
    histnameFrame.pack()
    historyFrame.pack()


    window.mainloop()
