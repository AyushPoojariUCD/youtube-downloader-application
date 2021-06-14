import pytube
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog, messagebox
file_location = ''

def filelocation():
    global file_location
    file_location = filedialog.askdirectory()

def clear():
    url_entry.delete(0,'end')

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
        try:
            if (quality == '360p'):
                youtube = pytube.YouTube(url)
                video = youtube.streams.filter(res="360p").first()
                video.download(f'{file_location}')
            elif (quality == '480p'):
                youtube = pytube.YouTube(url)
                video = youtube.streams.filter(progressive=True, res="480p").first()
                video.download(f'{file_location}')
            elif (quality == '720p'):
                youtube = pytube.YouTube(url)
                video = youtube.streams.filter(progressive=True, res='720p').first()
                video.download(f'{file_location}')
            elif (quality == '1080p'):
                youtube = pytube.YouTube(url)
                video = youtube.streams.filter(progressive=True, res="1080p").first()
                video.download(f'{file_location}')
        except:
            error = 1
            print(f'Not available in {quality} resolution')
            messagebox.showinfo(title=None, message=f'Not available in {quality} resolution \n *Try Lower Resolution')
    else:
        messagebox.showinfo(title=None, message=f'Mention Save as Location')

    if(url != '' and ((quality == '360p') or (quality == '480p') or (quality == '720p') or (quality == '1080p')) and (error == 0)and(temp!='')):
        messagebox.showinfo(title=None, message=f'Download Complete')


window = Tk()
window.title('Youtube Video Downloader')
window.resizable(height=False,width=False)
window.geometry("600x500")
window.configure(background = 'firebrick3')


#Video Url
video_url = Label(window,text ="Video Url:",bg='gray60',font=('calibre',10,'normal'))
video_url.place(x=30,y=50)
url_entry = Entry(window, font=('calibre',10,'normal'),width=60)
url_entry.place(x=100,y=50)
clear_url = Button(window,text='Clear',font=('calibre',10,'normal'),command=clear)
clear_url.place(x=530,y=50)

#Video Quality
video_quality = Label(window,text= "Choose Quality:",bg='gray60',font=('calibre',10,'normal'))
video_quality.place(x=30,y=100)
choice = ["360p", "480p","720p","1080p"]
combo = Combobox(window,values=choice)
combo.current(0)
combo.place(x=150,y=100)

save_to = Label(window,text ="Save To:",bg='gray60',font=('calibre',10,'normal'))
save_to.place(x=30,y=150)
browse_btn = Button(window,text="Browse Location",font=('calibre',10,'normal'),command = filelocation)
browse_btn.place(x=100,y=150)

download_btn = Button(window,text="Download",font=('calibre',10,'normal'),command = download,bg='gray60',fg='Black')
download_btn.place(x=250,y=300)

window.mainloop()