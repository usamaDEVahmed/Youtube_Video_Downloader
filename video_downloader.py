import tkinter as tk
from tkinter import ttk
import threading
import subprocess
import os
import time
from pytube import YouTube, request
import ffmpeg

class Downloader():
    def __init__(self, url):
        self.downloader = YouTube(url)
        self.video = None
        self.audio = None
        self.title = None

        self.root_window = None
        self.download_window = None
        self.is_paused = False
        self.is_canceled = False

    def get_qualities(self):
        qualities = []

        for stream in self.downloader.streams.filter(adaptive=True):
            q = stream.resolution
            if (q not in qualities) and (q is not None):
                if q is not '144p' and q is not '240p':
                    qualities.append(q)
        return qualities
    
    def get_title(self):
        self.title = self.downloader.streams.first().title
        return self.title    
            
    def get_streams(self, quality, save_path):

        self.video = self.downloader.streams.filter(adaptive=True, only_video=True, res=quality+'p').first()
        self.audio = self.downloader.streams.filter(adaptive=True
        , only_audio=True
        , is_dash=True
        , file_extension='mp4').first()
    
    def on_window_event_quit(self):
        time.sleep(0.2)
        self.download_window.destroy()
        self.root_window.deiconify()
    
    def create_download_window(self, root_window, save_path):
        self.root_window = root_window
        self.download_window = tk.Toplevel(root_window)
        width = root_window.winfo_screenwidth()
        height = root_window.winfo_screenheight()
        self.download_window.geometry('400x200+{}+{}'.format(int((width/2)-(400/2)), int((height/2)-(200/2))))
        self.download_window.title('Youtube Video Downloader')
        self.download_window.resizable(False, False)

        download_status_label = tk.Label(self.download_window, text='downloading...')
        download_status_label.place(relx=0.13, rely=0.2)
        download_progress_label = tk.Label(self.download_window, text='0.0%')
        download_progress_label.place(relx=0.775, rely=0.2)
        progress_bar = ttk.Progressbar(self.download_window
        , orient=tk.HORIZONTAL
        , length=300)
        progress_bar.place(relx=0.135, rely=0.3)

        pause_button = tk.Button(self.download_window, text='pause', borderwidth=2, command=self.on_pause)
        pause_button.place(relx=0.52, rely=0.5)
        cancel_button = tk.Button(self.download_window, text='cancel', borderwidth=2, command=self.on_cancel)
        cancel_button.place(relx=0.695, rely=0.5)

        pause_button.config(width=5)
        cancel_button.config(width=5)

        self.download_window.protocol('WM_DELETE_WINDOW', self.on_window_event_quit)

        self.initiate(download_status_label, download_progress_label, progress_bar, pause_button, cancel_button, save_path)
    
    def on_pause(self):
        if self.is_paused:
            self.is_paused = False
        else:
            self.is_paused = True
    def on_cancel(self):
        self.is_canceled = True
    
    def initiate(self, speed_label, status_label, progress_bar, pause_button, cancel_button, save_path):
        # self.download(self.video, self.audio, self.download_window, speed_label, status_label, progress_bar, pause_button, cancel_button, save_path)
        threading.Thread(target=self.download, args=(self.video, self.audio, self.download_window, speed_label, status_label, progress_bar, pause_button, cancel_button, save_path)).start()


    def download(self, video, audio, download_window, speed_label, status_label, progress_bar, pause_button, cancel_button, save_path):
        filesize = video.filesize + audio.filesize
        with open(save_path+'/video.mp4', 'wb') as f:
            f2 = open(save_path+'/audio.mp4', 'wb')
            stream = request.stream(video.url)
            audio_stream = request.stream(audio.url)
            downloaded = 0
            while True:
                if self.is_canceled:
                    status_label.config(text='cancelled')
                    if os.path.isfile(os.path.join(save_path, 'audio.mp4')):
                        os.remove(os.path.join(save_path, 'audio.mp4'))
                    if os.path.isfile(os.path.join(save_path, 'video.mp4')):
                        os.remove(os.path.join(save_path, 'video.mp4'))

                    self.download_window.destroy()
                    self.root_window.deiconify()
                    break
                if self.is_paused:
                    pause_button['text'] = 'continue'
                    speed_label.config(text='paused')
                    continue
                else:
                    pause_button['text'] = 'pause'
                    speed_label.config(text='downloading...')
                chunk = next(stream, None)
                audio_chunk = next(audio_stream, None)
                if audio_chunk:
                    f2.write(audio_chunk)
                    downloaded += len(audio_chunk)
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                progress = downloaded/filesize
                status_label.config(text=f'{round(progress*100, 2)}%')
                progress_bar['value'] = int(progress*100)
                if not audio_chunk and not chunk:
                    # no more data
                    f2.close()
                    speed_label.config(text='merging...')
                    pause_button['state'] = 'disabled'
                    cancel_button['text'] = 'ok'
                    video_path = save_path+'/video.mp4'
                    audio_path = save_path+'/audio.mp4'
                    try:                 
                        command = 'ffmpeg -y -i '+ video_path +' -i '+  audio_path + ' -c copy '+ save_path +'/output.mp4'
                        subprocess.call(command.split())
                    except:
                        speed_label.config(text='couldn\t download...')
                    if os.path.isfile(os.path.join(save_path, 'output.mp4')):
                        speed_label.config(text='compelete')
                        os.rename(os.path.join(save_path, 'output.mp4'), os.path.join(save_path, self.title))
                    else:
                        speed_label.config(text='can\'t download')
                        status_label.config(text='error')
                    os.remove(os.path.join(save_path, 'audio.mp4'))
                    os.remove(os.path.join(save_path, 'video.mp4'))
                    while True:
                        if self.is_canceled:
                            self.download_window.destroy()
                            self.root_window.deiconify()
                            break
                    
                    break
                download_window.update_idletasks()
        
        try:
            download_window.mainloop()
        except:
            pass
        




# import time
# def button():
#     for i in range(1, 11):
#         bar['value'] = (i*10)
#         window.update_idletasks()
#         time.sleep(0.5)



# if __name__ == "__main__":
#     # downloader = Downloader('https://www.youtube.com/watch?v=o_v9MY_FMcw')

#     window = tk.Tk()
#     width = window.winfo_screenwidth()
#     height = window.winfo_screenheight()
#     window.geometry('640x360+{}+{}'.format(int((width/2)-(640/2)), int((height/2)-(480/2))))
#     window.title('Youtube Video Downloader')
#     window.resizable(False, False)

#     bar = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=400, mode='determinate')
#     bar.place(relx=0.2, rely=0.5)

#     btn = tk.Button(window, text='start', command=button)
#     btn.place(relx=0.4, rely=0.6)

#     window.mainloop()


