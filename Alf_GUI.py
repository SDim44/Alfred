#
#       Alfred Modul - Arduino Connector
#
#       Stefan Dimnik, 09.03.2020
#
#       Mit dieses Programm wird die Grafische Oberflaeche aufgerufen.
# 
#       V0.1 
#       Die Oberflaeche ist fuer einen Touchscreen ausgelegt.
#       Manuelle Steuerung fuer Modus, Tool und Motoren wurde erstellt.
#
#       V0.2
#       Emotionen/Bild im Hauptfenster kann im Betrieb dynamisch angepasst werden

#Libarys
from Tkinter import *
import logging
import time
import Alf_ToolConnect as tool
import RPi.GPIO as GPIO
import Alf_Motor as engin
import os

#---------------------------------------------------------------------------------------
#Variablen definieren
datetime = time.strftime("%d.%m.%Y %H:%M:%S")
mainapp = ''

emo = ''
root = ''
window = ''
img = ''

scvalue1 = 0
scvalue2 = 0
btvalue1 = 0
outtxt = ''
command = {0,0,0}

#---------------------------------------------------------------------------------------
#Start Logging
Version = "V0.1"
logging.basicConfig(filename='logs/Alf_GUI.log',level=logging.DEBUG ,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug("----------- Starte Alfred Modul - GUI {0} ---------------".format(Version))

#---------------------------------------------------------------------------------------
#Funktionen
def setcmd():
    global scvalue1
    global scvalue2
    global btvalue1
    global outtxt
    global command
    
    command = str(btvalue1) + "," + str(scvalue1) + "," + str(scvalue2)
    tool.set(command)
    curtime = time.strftime("%H:%M:%S")
    txt=curtime + " - " + command + "\n"
    outtxt.insert('current',txt)
    

def getvaluebt(twert):
    global btvalue1
    btvalue1 = str(twert)
    setcmd()
    return btvalue1

      
def getvalue1(swert):
    global scvalue1
    scvalue1 = str(swert)
    setcmd()
    return scvalue1
    
    
def getvalue2(swert):
    global scvalue2
    scvalue2 = str(swert)
    setcmd()
    return scvalue2
    
#Modus in Main aendern
def setmode(num): 
    wert = str(num)
    config = open("mode.conf","w")
    config.write(wert)
    config.close
    
#exit function
def restart():
    root.destroy()
    emo.destroy()
    main()

def exit():
    root.destroy()
    emo.destroy()

def alf_sht():
    #try:
    os.system("sudo /etc/init.d/Alfred stop")
    #except:
        #logging.warning("!!!Init-Script nicht konfiguriert - Alfred wird beendent")
    #root.destroy()
    #emo.destroy()
    #os.system("./Alf_Stop.sh")
        
def alf_rst():    
    #try:
    #os.system("sudo /etc/init.d/Alfred restart")
    #except:
        #logging.warning("!!!Init-Script nicht konfiguriert - Alfred wird nur beendent und muss manuell neu gestartet werden")
    root.destroy()
    emo.destroy()
    os.system("./Alf_Stop.sh")
    
def lift_emo():
    root.attributes("-fullscreen", False)
    emo.attributes("-fullscreen", True)

def lift_root():
    root.attributes("-fullscreen", True)
    emo.attributes("-fullscreen", False)

#Config File lesen/aendern
def read_emotionfile():
    config = open("emotion.conf")
    set = config.read()
    config.close()
    set = set.strip(' \n\t')
    
    path = "DATA/emotions/" + set
    return path

#Schleife um das Bild im Betrieb zu aendern 
def update_image():
    global window
    global img
    
    filename = read_emotionfile()    
    img = PhotoImage(file=filename)
     
    window.config(image = img)
    window.after(1000, update_image)

#---------------------------------------------------------------------------------------
#tool menue  
def build():
    
    global emo
    global root
    global outtxt
    
    trow=2
    tcolumn=2
    if tool.get():
        widget=0
        var = tool.get()
        tname=var[0]
        Label (root, text=tname, anchor="center", bg="white", fg="black", font="none 14 bold") .grid(row=trow, column=tcolumn, columnspan=2,padx=20)
        trow+=1
        var.pop(0) #index aus dem array entfernen
        
        for x in var:
            global command
            global scvalue1
            global scvalue2
            
            i=0
            var1 = str(x)
            var2 = var1.split(',')
            type = var2[0]
            name = var2[1]
            arg1 = var2[2]
            arg2 = var2[3]
                
            
            if type == "btn1":
                cmdbt1 = arg1
                btn1 = Button (root, text=name, width=10, height=2, command= lambda: getvaluebt(cmdbt1)) .grid(row=trow, column=tcolumn, rowspan=2, padx=5, pady=5)
                
            if type == "btn2":
                tcolumn+=1
                cmdbt2 = arg1
                btn2 = Button (root, text=name, width=10, height=2, command= lambda: getvaluebt(cmdbt2)) .grid(row=trow, column=tcolumn, rowspan=2, padx=5, pady=5)
                tcolumn-=1
                trow+=2
                
            if type == "scale1":
                lbscale1 = Label (root, text=name, anchor="center", bg="white", fg="black", font="none 10") .grid(row=trow, column=tcolumn, padx=0, pady=0)
                trow+=1
                scale1 = Scale (root, from_=arg1, to=arg2, orient=HORIZONTAL, showvalue=1, command=getvalue1) .grid(row=trow, column=tcolumn, padx=0, pady=0)
                scvalue1 = arg1
                
            if type == "scale2":
                trow-=1
                tcolumn+=1
                lbscale2 = Label (root, text=name, anchor="center", bg="white", fg="black", font="none 10") .grid(row=trow, column=tcolumn, padx=0, pady=0)
                trow+=1
                scale2 = Scale (root, from_=arg1, to=arg2, orient=HORIZONTAL, showvalue=1, command=getvalue2) .grid(row=trow, column=tcolumn, padx=0, pady=5)
                scvalue2 = arg1
                tcolumn-=1
                trow+=1
                
        trow+=1
        Label (root, text="Serial - Output", anchor="center", bg="white", fg="black", font="none 10") .grid(row=trow, column=tcolumn, padx=0, pady=5, columnspan=2)
        trow+=1
        outtxt = Text(root, state='normal', height=1, width=20, bg="white")
        outtxt.grid(row=trow, column=tcolumn, padx=0, pady=0, columnspan=2)
    
    
    else:
        Label (root, text="Tool Settings", anchor="center", bg="white", fg="black", font="none 14 bold") .grid(row=trow, column=tcolumn, columnspan=2,padx=20)
        trow+=1
        Label (root, text="Kein Tool erkannt!", anchor="center", bg="white", fg="black", font="none 10 bold") .grid(row=trow, column=tcolumn, columnspan=2,padx=20)


#---------------------------------------------------------------------------------------
#Main
def main():
    
    global emo
    global root
    global window
    global img
    
    
    #Main Emotion Window
    emo = Tk()
    emo.title('Alfred Emotion')
    emo.attributes("-fullscreen", True)

    filename = read_emotionfile()
    img = PhotoImage(file=filename)

    window = Button(emo, image=img, command=lift_root)

    window.pack()

    emo.after(1000, update_image)
    
    #Main root
    root = Tk()
    root.title("Alfred GUI")
    root.configure(background="white")

    #Header
    Label (root, text="Alfred - Steuerung", bg="white", fg="black", font="none 16 bold") .grid(row=1, column=0, padx=50,columnspan = 3)
    Label (root, text=datetime, bg="white", fg="black", font="none 12 bold") .grid(row=1, column=4, padx=0, columnspan = 2)
    
    
    ##Body
    #1.Spalte - Modus wechseln
    Label (root, text="Modus", anchor="center", bg="white", fg="black", font="none 14 bold") .grid(row=2, column=1, padx=0, pady=20)
    Button(root, text="Verfolgung", width=10, height=2, command= lambda: setmode(1)) .grid(row=3, column=1, padx=5, pady=5, rowspan=2)
    Button(root, text="Ladestation", width=10, height=2, command= lambda: setmode(2)) .grid(row=5, column=1, padx=5, pady=5, rowspan=2)
    Button(root, text="Tool-Modus", width=10, height=2, command= lambda: setmode(3)) .grid(row=7, column=1, padx=5, pady=5, rowspan=2)
    
    Label (root, text="Motor", anchor="center", bg="white", fg="black", font="none 14 bold") .grid(row=9, column=1, padx=0, pady=20)
    Button(root, text="Forwaerts", width=10, height=1, command= lambda: engin.move(1,1,100,100)) .grid(row=10, column=1, padx=0, pady=0, rowspan=2)
    Button(root, text="Drehen", width=10, height=1, command= lambda: engin.move(1,2,50,50)) .grid(row=11, column=1, padx=0, pady=0, rowspan=2)
    
    #2.Spalte - Tool Menue
    build()
    
    #3.Spalte - Ausgabe
    Label (root, text="System", anchor="center", bg="white", fg="black", font="none 14 bold") .grid(row=2, column=4, padx=0, pady=0,columnspan = 2)
    
    #Footer
    btn_rst = Button(root, text="Restart GUI", width=10, height=2,command=restart) .grid(row=3, column=5, padx=0, pady=5, rowspan=2)
    #btn_sht = Button(root, text="Shutdown GUI", width=10, height=2,command=exit) .grid(row=5, column=5, padx=0, pady=5)
    btn_arst = Button(root, text="Restart Alfred", width=10, height=2,command=alf_rst) .grid(row=5, column=5, padx=0, pady=5, rowspan=2)
    btn_asht = Button(root, text="Shutdown Alfred", width=10, height=2,command=alf_sht) .grid(row=7, column=5, padx=0, pady=5, rowspan=2)
    
    Button(root, text="Zurueck", width=8, height=2, command=lift_emo, font="none 12 bold") .grid(row=12, column=4, padx=30, pady=20, rowspan= 2, columnspan = 3)
     
    
    emo.mainloop()

main()