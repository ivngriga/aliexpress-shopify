import GUI_product_browse
import GUI_product_download

import tkinter as tk
from PIL import ImageTk, Image

import os
from os import path
import requests

import base64
import json
import requests

from base64 import b64encode

def exitProg():
    exit()

def saveDir(dirEntry):
    if(path.isdir(dirEntry.get())):
        sep = "  -_-_- "
        newtxt = dirEntry.get()
        for x in data[1:10]:
            newtxt+=sep+x

        newtxt = newtxt.replace("  -_-_- ", " -_-_- ")
        file= open("assets/data.txt","w+")
        file.write(newtxt)
        file.close()
    else:
        
        dirEntry.delete(0,"end")
        dirEntry.insert(0, "invalid directory!")
        
    
    
def export(directory, exportText):
    #print(directory)
    products=[]
    for filename in os.listdir(data[0]):
        if(path.isdir(os.path.join(directory, filename))):
            products.append(os.path.join(directory, filename))

    finalfile=open("final.txt", "w")
    finalfile.write("Handle,Title,Body (HTML),Vendor,Type,Tags,Published,Option1 Name,Option1 Value,Option2 Name,Option2 Value,Option3 Name,Option3 Value,Variant SKU,Variant Grams,Variant Inventory Tracker,Variant Inventory Qty,Variant Inventory Policy,Variant Fulfillment Service,Variant Price,Variant Compare At Price,Variant Requires Shipping,Variant Taxable,Variant Barcode,Image Src,Image Position,Image Alt Text,Gift Card,SEO Title,SEO Description,Variant Image,Variant Weight Unit,Variant Tax Code,Cost per item,Status,Collection\n")
    i=1
        
    for product in products:
        images=[]
        info=[]
        curproduct=directory+product
        file=open(product+"/data.txt", "r")
        info=file.read().split(" -_-_- ")
        file.close()
        
        row = ["" for x in range(36)]

        for filename in os.listdir(product):
            if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"): 
                filedir=os.path.join(product, filename)
                txt="Exporting "+product
                exportText.config(text=txt)
                window.update()
                url = "https://api.imgur.com/3/upload.json"
                header = {"Authorization": "Client-ID 3904240a07c1017"}
                fields = {
                        "image":b64encode(open(filedir, 'rb').read()),
                        'type': 'base64',
                        'name': '1.jpg',
                        'title': 'Picture no. 1'
                    }
                r = requests.post(
                    url,
                    headers=header,
                    data=fields
                )

                response = json.loads(r.text)
                try:
                    images.append(response['data']['link'])
                except Exception as e:
                    print(response)

    
        #Handle
        handle="product-"+str(i)
        row[0]=handle
        
        #Title
        row[1]=str(info[0]).replace(","," ")
        
        #Description
        row[2]=str(info[1]).replace("\n", " ").replace(","," ")
        
        #Vendor
        row[3]="myStore"
        
        #Tags
        row[5]=str(info[2]).replace(","," ")
        
        #Published
        row[6]="TRUE"
        
        #Option1 Name
        row[7]="Title"

        #Option1 Value
        row[8]="Default Title"

        #Weight
        row[14]="0"
        
        #Variant inventory policy
        row[17]="deny"

        #Variant fulfillment
        row[18]="manual"

        #Sale Price
        row[19]=str(info[5]).replace(","," ")

        #Price
        row[20]=str(info[4]).replace(","," ")

        #Image
        
        row[24]=str(images[0]).replace(","," ")
        

        #Image Pos
        row[25]=str(1)

        #Status
        row[34]="draft"

        #Collection
        row[35]=str(info[3])

        row = ",".join(row)+"\n"
        finalfile.write(row)

        j=2
        for image in images[1:len(images)-1]:
            imgRow=["" for x in range(36)]
            imgRow[0]=handle
            imgRow[24]=image
            imgRow[25]=str(j)
            imgRow = ",".join(imgRow)+"\n"
            finalfile.write(imgRow)
            j+=1

        i+=1

    finalfile.close()
    fileName = "final.txt"
    base = os.path.splitext(fileName)[0]
    os.rename(fileName, base + ".csv")
    txt="Export Finished!"
    exportText.config(text=txt)
    window.update()

def goBrowse():
    global window
    window.destroy()
    GUI_product_browse.startProductBrowse()

def goDownload():
    global window
    window.destroy()
    GUI_product_download.startProductDownload()

window=0
data=[]

def startMainMenu():
    global page
    global window
    global data
    
    page=0

    window = tk.Tk()
    window.geometry('650x550')
    window.eval('tk::PlaceWindow . center')

    file = open("assets/data.txt", "r")
    data = file.read().split(" -_-_- ")
    file.close()

    titleFrame=tk.Frame(master=window)
    buttonsFrame=tk.Frame(master=window)



    titleLabel = tk.Label(master=titleFrame,text="Aliexpress Editor/Exporter Tool", font=("Arial", 20))# Browse

    # Browse
    browseButton = tk.Button(
        text="Product Overview Page",
        width=30,
        height=3,
        bg="white",
        fg="purple",
        master=buttonsFrame,
        command = goBrowse
    )

    # Download
    downloadButton = tk.Button(
        text="Download Products Page",
        width=30,
        height=3,
        bg="white",
        fg="purple",
        master=buttonsFrame,
        command = goDownload
    )

    # Directory Enter
    dirName = tk.Label(master=buttonsFrame, text="Enter Directory Location:")
    dirEntry = tk.Entry(
        fg="purple",
        bg="white",
        width=40,
        master=buttonsFrame
        
    )
    dirEntry.insert(0, data[0])

    # Save Directory
    saveButton = tk.Button(
        text="Save Directory",
        width=30,
        height=3,
        bg="white",
        fg="purple",
        master=buttonsFrame,
        command = lambda: saveDir(dirEntry)
    )

    # Export
    exportButton = tk.Button(
        text="Export to CSV",
        width=30,
        height=3,
        bg="white",
        fg="purple",
        master=buttonsFrame,
        command = lambda: export(data[0], exportText)
    )
    exportText = tk.Label(master=buttonsFrame,text="Export Not Started")

    # Exit
    exitButton = tk.Button(
        text="Exit",
        width=30,
        height=3,
        bg="white",
        fg="purple",
        master=buttonsFrame,
        command = exitProg
    )

    page=0

    titleLabel.pack(pady=10)
    browseButton.pack(pady=10)
    downloadButton.pack(pady=10)
    dirName.pack()
    dirEntry.pack()
    saveButton.pack(pady=10)
    exportButton.pack(pady=10)
    exportText.pack(pady=10)
    exitButton.pack(pady=10)

    titleFrame.pack()
    buttonsFrame.pack()

    window.mainloop()
