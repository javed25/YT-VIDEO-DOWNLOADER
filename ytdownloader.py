from tkinter import *
from tkinter import ttk
import os
from tkinter import filedialog
from tkinter import messagebox as msg
from pytube import YouTube
from pytube.cli import on_progress
from moviepy.editor import *

video_size=0
############### FUNCTIONS ###############

def download():
    global video_size,final_mb
    url=e.get()
    resolution=c.get()
    resolution=resolution.lower()
    resolution=resolution.replace(" ","")
    audio_check=var1.get()

    try:
        yt=YouTube(url,on_progress_callback=progress_check)
        title=yt.title
    except Exception as ex:
        print(ex)
        msg.showerror("URL Error","URL INVALID")

    if "audio" in audio_check:
        # try:
        video=yt.streams.filter(only_audio=True).first()
        video_size=video.filesize
        mb=(video_size/(1024*1024))
        final_mb=round(mb,2)
        video.download(se.get())
        mp4path=f"{title}.mp4"
        mp3path=f"{title} audio.mp3"
        mp4=VideoFileClip(filename=mp4path)
        mp4.audio.write_audiofile(filename=mp3path)
        msg.showinfo("Download Completed",f"Audio Downloaded at {se.get()}")
        dp['value']=0
        # except Exception as ex:
        #     print(ex)
    else:
        try:
            video=yt.streams.filter(res=resolution).first()
            video_size=video.filesize
            mb=(video_size/(1024*1024))
            final_mb=round(mb,2)
            video.download(se.get())
            l1.config(text="DOWNLOAD DONE")
            msg.showinfo("Download Completed",f"Video Downloaded at {se.get()}")
            dp['value']=0
        except Exception as ex:
            print(ex)
            msg.showerror("Download Error","Video is Not available in this resolution,try with different resolution")

def progress_check(streams,chunk,bytes_remaining):
    global video_size,final_mb
    l1.config(text=f"DOWNLOADING  {round((video_size-bytes_remaining)/(1024*1024),2)} MB of {final_mb} MB")
    percent = ((video_size-bytes_remaining)/video_size)*100
    percentage=round(percent,2)
    dp["value"]=percentage
    dp.update()
    if int(percentage)==100:
        l1.config(text="DOWNLOAD DONE")
        # download_button.config(state=DISABLED)




def opendir():
    try:
        os.startfile(se.get())
    except:
        msg.showerror("Path Error","Please Enter Valid Path")

def browse():
    path=filedialog.askdirectory()
    if path:
        se.set(path)


root=Tk()
root.title("YOUTUBE DOWNLOADER")
root.geometry("800x500")

######### LABELS  ##########

title=Label(root,text="YOUTUBE VIDEO DOWNLOADER",font=("",20,"bold"),fg="red",bg="white",relief="groove")
title.place(x=170,y=10)

url_label=Label(root,text="Video URL: ",font=("",12,"bold"),fg="black")
url_label.place(x=20,y=80)

quality_label=Label(root,text="Video Quality: ",font=("",12,"bold"),fg="black")
quality_label.place(x=20,y=140)

Save_label=Label(root,text="Save To: ",font=("",12,"bold"),fg="black")
Save_label.place(x=20,y=200)

status_label=Label(root,text="STATUS: ",font=("",12,"bold"),fg="black",bg="white",relief="groove",anchor=W)
status_label.pack(side=BOTTOM,fill=X)

l1=Label(status_label,text="waiting",font=("",12),bg="white")
l1.pack()


########################### WIDGETS  #############
def audio():
    quality_combobox.config(state=DISABLED)
def video():
    quality_combobox.config(state=NORMAL)

e=StringVar()
url_entry=Entry(root,textvariable=e,width=70,bd=2,font=("",10))
url_entry.place(x=150,y=80)

c=StringVar()
l=["360 P","480 P","720 P","1080 P"]
quality_combobox=ttk.Combobox(root,values=l,textvariable=c,width=25)
c.set("SELECT")
quality_combobox.place(x=150,y=140)


se=StringVar()
se.set("C:\\Users\\khana_asisvkp\\Downloads\\Video")
save_entry=Entry(root,textvariable=se,width=70,bd=2,font=("",10))
save_entry.place(x=150,y=200)

var1=StringVar()
var1.set(" ")
Radiobutton(root,text="Download Audio",variable=var1,value="audio",font=("",10),command=audio).place(x=325,y=140)
Radiobutton(root,text="Download Video",variable=var1,value="video",font=("",10),command=video).place(x=450,y=140)

################## BUTTONS ###############
browse_button=Button(root,text="BROWSE",font=("",14),bg="#fcba03",fg="black",width=10,command=browse)
browse_button.place(x=670,y=190)

# search_button=Button(root,text="SEARCH",font=("",14),bg="#fcba03",fg="black",width=10)
# search_button.place(x=670,y=80)

download_button=Button(root,text="DOWNLOAD",font=("",14),bg="#fcba03",fg="black",command=download)
download_button.place(x=320,y=250)

open_button=Button(root,text="OPEN",font=("",14),bg="#fcba03",fg="black",width=10,command=opendir)
open_button.place(x=670,y=250)

############ PROGRESS BAR ##########

frame_label=Label(root,text="",bg="blue",bd=2,relief="groove")
frame_label.pack(side=BOTTOM,fill=X)

dp=ttk.Progressbar(frame_label,orient=HORIZONTAL,mode="determinate",length=450,maximum=100)
dp.pack(side=TOP,padx=12)

Label(root,anchor=W,text="PROGRESS: ",font=("",10,"bold"),fg="white",bg="blue").place(x=10,y=449)



root.mainloop()