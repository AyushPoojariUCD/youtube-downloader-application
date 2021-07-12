import pytube
from tkinter import *
from tkinter.ttk import Combobox, Progressbar,Style
from tkinter import filedialog, messagebox
import os
from moviepy.editor import *
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import ImageTk, Image
import time



file_location = ''

def filelocation():
    global file_location
    file_location = filedialog.askdirectory()

def clear():
    url_entry.delete(0,'end')


def cut(editor, event=None):
    editor.event_generate("<<Cut>>")


def copy(editor, event=None):
    editor.event_generate("<<Copy>>")


def paste(editor, event=None):
    editor.event_generate('<<Paste>>')


def rightKey(event, editor):
    menubar.delete(0, END)
    menubar.add_command(label='shear', command=lambda: cut(editor))
    menubar.add_command(label='copy', command=lambda: copy(editor))
    menubar.add_command(label='paste', command=lambda: paste(editor))
    menubar.post(event.x_root, event.y_root)



def merge(temp,n):
    videoclip = VideoFileClip(f"{temp}/video.mp4")
    audioclip = AudioFileClip(f"{temp}/audio.mp3")
    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    name = save_as_entry.get()

    if (name !=''):
        videoclip.write_videofile(f'{temp}/{name}.mp4')
    else:
        videoclip.write_videofile(f'{temp}/{n}.mp4')


def download():
    temp = file_location
    print(temp)
    url = url_entry.get()
    print(url)
    quality = str(combo.get())
    print(quality)
    error = 0

    if (temp != ''):

        messagebox.showinfo(title=None, message=f'Downloading at location:{file_location}')
        download_update = Label(window, text=f"Downloading at {file_location}", bg='gray14', fg='goldenrod2', font=('calibre', 12, 'normal'))
        download_update.place(x=150,y=300)
        #1
        window.update()
        try:
            if (quality == '360p'):
                progress['value'] = 20
                percent.set("20%")

                window.update_idletasks()
                youtube = pytube.YouTube(url)

                progress['value'] += 40
                percent.set("60%")
                window.update_idletasks()

                video = youtube.streams.filter(res="360p").first()
                video.download(f'{file_location}')


            if (quality == '480p'):
                progress['value'] = 40
                percent.set("40%")
                window.update_idletasks()

                youtube = pytube.YouTube(url)

                progress['value'] += 20
                percent.set("60%")
                window.update_idletasks()

                video = youtube.streams.filter(adaptive=True, res="480p").first()
                video.download(f'{file_location}',filename='video')




            if(quality == '480p'):
                youtube = pytube.YouTube(url)
                n = youtube.title
                print(n)
                audio = youtube.streams.filter(only_audio=True).first()
                ad = audio.download(f'{file_location}',filename='audio')
                base, ext = os.path.splitext(ad)
                new_file = base + '.mp3'
                os.rename(ad, new_file)
                merge(temp,n)


            if (quality == '720p'):
                progress['value'] = 40
                percent.set("40%")
                window.update_idletasks()

                youtube = pytube.YouTube(url)

                progress['value'] += 20
                percent.set("60%")
                window.update_idletasks()

                video = youtube.streams.filter(adaptive=True, res='720p').first()
                video.download(f'{file_location}',filename='video')

            if(quality == '720p'):
                youtube = pytube.YouTube(url)
                n = youtube.title
                print(n)
                audio = youtube.streams.filter(only_audio=True).first()
                ad = audio.download(f'{file_location}',filename='audio')
                base, ext = os.path.splitext(ad)
                new_file = base + '.mp3'
                os.rename(ad, new_file)
                merge(temp,n)

            if (quality == 'Only Audio'):
                progress['value'] = 40
                percent.set("40%")

                youtube = pytube.YouTube(url)
                progress['value'] += 20
                percent.set("60%")

                audio = youtube.streams.filter(only_audio=True).first()
                ad = audio.download(f'{file_location}')
                base, ext = os.path.splitext(ad)
                new_file = base + '.mp3'
                os.rename(ad, new_file)


        except:
            error = 1
            print(f'Not available in {quality} resolution')
            messagebox.showinfo(title=None, message=f'Not available in {quality} resolution \n *Try Lower Resolution')
    else:
        messagebox.showinfo(title=None, message=f'Mention Save as Location')

    if(url != '' and ((quality == '360p') or (quality == '480p') or (quality == '720p') or (quality == 'Only Audio')) and (error == 0)and(temp!='')):
        #Removing Extra Files
        if((quality == '480p') or (quality == '720p')):
            os.remove(f"{temp}/video.mp4")
            os.remove(f"{temp}/audio.mp3")
        progress['value'] += 40
        percent.set("100%")
        window.update_idletasks()
        messagebox.showinfo(title=None, message=f'Download Complete')



window = Tk()
window.title('Youtube Downloader')
window.resizable(height=False,width=False)
window.geometry("650x600")
window.configure(background = 'gray14')

photo = PhotoImage(file = "logo.png")
window.iconphoto(False, photo)

#Variables
percent = StringVar()
text = StringVar()

#Title
title = Label(window,text= "Youtube Downloader",fg='goldenrod2',bg='gray14',font=('calibre',20,'normal'))
title.place(x=200,y=40)

canvas = Canvas(window, width = 60, height = 60)
canvas.place(x=125,y=20)
img = PhotoImage(file="logo.png")
canvas.create_image(1,0, anchor=NW, image=img)

#Video Url
video_url = Label(window,text ="Video Url:",fg='goldenrod2',bg='gray14',font=('calibre',12,'bold'))
video_url.place(x=30,y=100)
url_entry = Entry(window, font=('calibre',10,'normal'),width=60,highlightthickness=1)
url_entry.config(highlightcolor= "goldenrod2")
url_entry.place(x=120,y=100)
url_entry.bind("<Button-3>", lambda x: rightKey(x,url_entry))
menubar = Menu(window, tearoff=False)

#Clear Url
clear_url = Button(window,text='Clear',font=('calibre',8,'bold'),command=clear)
clear_url.place(x=550,y=100)

#Video Quality
video_quality = Label(window,text= "Choose Quality:",bg='gray14',fg='goldenrod2',font=('calibre',12,'bold'))
video_quality.place(x=30,y=150)


#Combo Box
choice = ["360p", "480p","720p","Only Audio"]
combo = Combobox(window,values=choice,font=('calibre',10,'bold'))
combo.current(0)
combo.place(x=180,y=150)

#Save To
save_to = Label(window,text ="Choose File Location:",bg='gray14',fg='goldenrod2',font=('calibre',12,'bold'))
save_to.place(x=30,y=200)
browse_btn = Button(window,text="Browse Location",font=('calibre',10,'bold'),command = filelocation)
browse_btn.place(x=220,y=200)

#Save as
save_as = Label(window,text ="Save as:",bg='gray14',fg='goldenrod2',font=('calibre',12,'bold'))
save_as.place(x=30,y=250)
save_as_entry = Entry(window, font=('calibre',10,'normal'),width=60,highlightthickness=1)
save_as_entry.config(highlightcolor= "goldenrod2")
save_as_entry.place(x=120,y=250)

#Progress Bar
status = Label(window,text="Download\nStatus",bg='gray14',fg='goldenrod2',font=('calibre',12,'bold'))
status.place(x=30,y=335)
percent = StringVar()
style = Style()
style.theme_use('default')
style.configure("grey.Horizontal.TProgressbar", background='goldenrod2')
progress = Progressbar(window, orient=HORIZONTAL,length=400,style="grey.Horizontal.TProgressbar")
progress.place(x=135,y=350)
percentLabel = Label(window,textvariable=percent,bg='gray14',fg='goldenrod2',font=('calibre',10,'bold'))
percentLabel.place(x=540,y=350)

#Download Button
download_btn = Button(window,text="Download",font=('calibre',12,'bold'),command = download,bg='snow',fg='black')
download_btn.place(x=260,y=420)
           
note = Label(window,text='WAIT IF WINDOW SHOWS NOT RESPONDING',bg='gray10',fg='goldenrod2',font=('calibre',10,'bold'))
note.place(x=160,y=520)

window.mainloop()