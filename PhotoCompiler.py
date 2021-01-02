import os
import pathlib
import datetime
import shutil
from tkinter import filedialog
import tkinter
from tkinter import messagebox
import multiprocessing
from tkinter import ttk
def StartSort(locationToWrite,direct,topic):
    tW = tkinter.Tk()
    tW.withdraw()
    if direct=="" or locationToWrite == "" or topic=="" or locationToWrite == direct:
        messagebox.showerror("Something went wrong!","Something went wrong..\n1.Check whether the paths and topics arent null\n2.Check whether ther results path and image path isnt the same.")
        tW.destroy()
        return
    if list(direct)[len(direct)-1] in ["\\","/"]:
        direct = list(direct)
        del direct[len(direct)-1]
        direct = ''.join(x for x in direct)
    if list(locationToWrite)[len(locationToWrite)-1] in ["\\","/"]:
        locationToWrite = list(locationToWrite)
        del locationToWrite[len(locationToWrite)-1]
        locationToWrite = ''.join(x for x in locationToWrite)
    

    fetched = os.listdir(direct)
    fetched.sort()
    listOfFiles = []
    for x in fetched:
        try:
            newx = os.path.basename(x)
            if " " in list(newx):
                convertx = x.replace(" ","_")
                os.rename(direct+"\\"+x,direct+"\\"+convertx)
                newx.replace(" ","_")
                x = x.replace(" ","_")
            pre,post = newx.split('.')
        except:
            continue
        if post in ["heic","HEIC"]:        
            x = direct+"\\"+x
            listOfFiles.append(x)
        elif post in ["jpeg","JPEG","mov","mp4","JPG","jpg","MOV","MP4","PNG","png"]:
            x = direct+"\\"+x
            listOfFiles.append(x)
    weekDayInterpret = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    uniqueDays = []
    YoungestMonth = 12
    MonthInterpret = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    listOfOldProcessed = []
    YoungestYear = datetime.date.today().year
    uniqueMonths = []
    uniqueYears = []
    for x in listOfFiles:
        if x[-3:] in ["jpg","JPG","PNG","png"]:
            ret = os.popen("exiftool -time:all "+x)
            data = ret.read()
            data = data.split('\n')
            data = [x.split(':') for x in data]
            newdata = []
            for x in data:
                sub = []
                for y in x:
                    sub.append(y.strip())
                newdata.append(sub)
            del newdata[0]
            del newdata[0]
            del newdata[1]
            use,notuseful = newdata[0][3].split(' ')
            newdata[0][3] = use
            try:
                ProcessedDate = datetime.datetime(int(newdata[0][1]),int(newdata[0][2]),int(newdata[0][3]))
            except:
                messagebox.showerror("Error","FILE : "+x+" is missing metadata! This file will be skipped by the program")
                listOfFiles = [y for y in listOfFiles if y!=x]
                continue
        else:
            ret = os.popen("exiftool -CreateDate -m "+x)
            data = ret.read()
            data = [x.strip() for x in data.strip().split(':')]
            del data[0]
            del data[len(data)-1]
            del data[len(data)-1]
            useful,notuseful = data[len(data)-1].split(' ')
            del data[len(data)-1]
            data.append(useful)
            data = [int(x) for x in data]
            try:
                ProcessedDate = datetime.datetime(data[0],data[1],data[2])
            except:
                messagebox.showerror("Error","FILE : "+x+" is missing metadata! This file will be skipped by the program")
                listOfFiles = [y for y in listOfFiles if y!=x]
                continue
        listOfOldProcessed.append(ProcessedDate)
        if (ProcessedDate.day,ProcessedDate.weekday(),ProcessedDate.month,ProcessedDate.year) not in uniqueDays:
            uniqueDays.append((ProcessedDate.day,ProcessedDate.weekday(),ProcessedDate.month,ProcessedDate.year))
        if ProcessedDate.month < YoungestMonth and ProcessedDate.year<=YoungestYear:
            YoungestMonth = ProcessedDate.month
        if ProcessedDate.year<YoungestYear:
            YoungestYear = ProcessedDate.year
        if (ProcessedDate.month,ProcessedDate.year) not in uniqueMonths:
            uniqueMonths.append((ProcessedDate.month,ProcessedDate.year))
        if ProcessedDate.year not in uniqueYears:
            uniqueYears.append(ProcessedDate.year)
    YoungestYear = str(YoungestYear)
    TrueMonth = MonthInterpret[YoungestMonth-1]
    try:
        os.mkdir(locationToWrite+"\\"+topic+" "+TrueMonth+" "+str(YoungestYear)+"\\")
    except FileExistsError:
        pass
    basePath = locationToWrite+"\\"+topic+" "+TrueMonth+" "+YoungestYear
    listOfYearsPaths = []
    for x in uniqueYears:
        try:
            os.mkdir(basePath+"\\"+str(x))
        except: 
            pass
        listOfYearsPaths.append((basePath+"\\"+str(x),x))
    listOfMonthsPaths = []
    for x in uniqueMonths:
        month,year = x
        for y in listOfYearsPaths:
            path,_year = y
            if int(_year) == year:
                try:
                    os.mkdir(path+"\\"+str(year)+" "+MonthInterpret[month-1])
                except FileExistsError:
                    pass
                listOfMonthsPaths.append((path+"\\"+str(year)+" "+MonthInterpret[month-1],year,month))
    listOfUniqueDaysPaths = []
    for x in uniqueDays:
        day,weekID,month,year = x
        for y in listOfMonthsPaths:
            path,_year,_month = y
            if int(_year) == year and int(_month) == month:
                try:
                    os.mkdir(path+"\\"+str(day)+" "+weekDayInterpret[weekID])
                except FileExistsError:
                    pass
                listOfUniqueDaysPaths.append((path+"\\"+str(day)+" "+weekDayInterpret[weekID],year,month,day))
    i = 0
    while i<len(listOfFiles):
        fileName = os.path.basename(listOfFiles[i])
        for x in listOfUniqueDaysPaths:
            basePath,_year,_month,_day = x
            if int(_year) == listOfOldProcessed[i].year and _month == listOfOldProcessed[i].month and _day == listOfOldProcessed[i].day:
                shutil.move(listOfFiles[i],basePath+"\\"+fileName)
        i+=1
    messagebox.showinfo("Processing completed","Your files have been sorted!")
    os.system("start "+locationToWrite)
    tW.destroy()
direct = ""
topic = ""
locationToWrite = ""
direct=""
locationToWrite=""
if __name__ == "__main__":
    MainWindow = tkinter.Tk()
    MainWindow.title("iOS Photo Sorter")
    tkinter.Label(MainWindow,text="iOS Photo Sorter",underline=16,font="arial",justify=tkinter.CENTER).grid(column=1,row=0)
    OptionsForm = tkinter.Frame(MainWindow)
    OptionsForm.grid(column=1,row=1)
    tkinter.Label(OptionsForm,text="Path to search for images").grid(column=0,row=0)
    tkinter.Label(OptionsForm,text="Path to place the results(must be empty)").grid(column=0,row=1)
    TopicVar = tkinter.StringVar()
    tkinter.Label(OptionsForm,text="Topic:").grid(column=0,row=2)
    TopicEntry = tkinter.Entry(OptionsForm,textvariable=TopicVar)
    TopicEntry.grid(column=1,row=2)
    def TopicChanged(a,b,c):
        global topic
        topic = TopicEntry.get()
        if TopicEntry.get() == "":
            TopicPreviewLabel.config(text="Folder preview will show here")
        elif set(TopicEntry.get()).intersection(set(["\\","/",":","?","\"","<",">","|"," "])) or len(TopicEntry.get()) >= 200:
            TopicPreviewLabel.config(text="Invalid Topic")
            topic=""
        else:
            if locationToWrite != "":
                TopicPreviewLabel.config(text=f"{locationToWrite}/{TopicEntry.get()} <month> <year>")
            else:
                TopicPreviewLabel.config(text="Set a results path")
    TopicVar.trace('w',TopicChanged)
    def PathForImages():
        global direct
        direct = filedialog.askdirectory(initialdir="/",title="Select a folder")
        if direct == "":
            ImagePreviewLabel.config(text="Selected Image Path will show here")
        elif " " in direct:
            ImagePreviewLabel.config(text="Please pick a path that doesnt have spaces in its name!")
            direct = ""
        else:
            ImagePreviewLabel.config(text="Selected Image Path:"+direct)
        
    def PathForResults():
        global locationToWrite
        locationToWrite = filedialog.askdirectory(initialdir="/",title="Select a folder")
        if locationToWrite == "":
            ResultPreviewLabel.config(text="Selected Results Path will show here")
        elif " " in list(locationToWrite):
            ResultPreviewLabel.config(text="Please pick a path that doesnt have spaces in its name!")
            locationToWrite = ""
        else:
            ResultPreviewLabel.config(text="Selected Results Path:"+locationToWrite)
    ButtonForImages = tkinter.Button(OptionsForm,text="Select Path...",command=PathForImages)
    ButtonForImages.grid(column=1,row=0)
    ButtonForResults = tkinter.Button(OptionsForm,text="Select Path...",command=PathForResults)
    ButtonForResults.grid(column=1,row=1)
    TopicPreviewLabel = tkinter.Label(MainWindow,text="Folder preview will show here")
    TopicPreviewLabel.grid(column=1,row=2)
    ImagePreviewLabel = tkinter.Label(MainWindow,text="Selected Image Path will show here")
    ImagePreviewLabel.grid(column=1,row=3)
    ResultPreviewLabel = tkinter.Label(MainWindow,text="Selected Results Path will show here")
    ResultPreviewLabel.grid(column=1,row=4)
    def StartProcess():
        global locationToWrite,direct,topic
        StartButton.config(state=tkinter.DISABLED)
        MainWindow.update_idletasks()
        process = multiprocessing.Process(target=StartSort,args=[locationToWrite,direct,topic])
        process.start()
        ProgressBar.start(20)
        MainWindow.update_idletasks()
        while process.is_alive():
            ProgressBar.update()
            ProgressBar.update_idletasks()
            MainWindow.update_idletasks()
        ProgressBar.stop()
        MainWindow.update_idletasks()
        ProgressBar['value']=0
        StartButton.config(state=tkinter.NORMAL)
    StartButton = tkinter.Button(MainWindow,text="Begin Sort",command=StartProcess)
    ProgressBar = ttk.Progressbar(MainWindow,orient=tkinter.HORIZONTAL,length=100,mode='indeterminate')
    ProgressBar.grid(column=1,row=5)
    StartButton.grid(column=1,row=6)
    tkinter.Button(MainWindow,text="Help",command=lambda:messagebox.showinfo("Help","Path to search for images is the folder where all the imported images should be kept.\n Path to place the results is the folder where the program will generate a new folder in which your images will be sorted\nTopic is the topic of the images which will be used to generate a main folder named following the format <topic> <year> <month> , you can view the preview of the folder name which is displayed on the screen. \n For more help consult the README")).grid(column=2,row=2)

    MainWindow.mainloop()