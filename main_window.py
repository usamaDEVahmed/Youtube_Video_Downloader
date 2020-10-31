from video_downloader import Downloader
import pytube
import tkinter as tk
from tkinter import PhotoImage
from tkinter import filedialog
import tkinter.ttk as ttk
from validator_collection import validators, checkers
import time

class Window():
    def __init__(self):
        self.downloader = None
        self.window = tk.Tk()
        self.icon = PhotoImage(file='data/icon.png')
        self.url_textbox = tk.Entry(self.window, width=60, insertwidth=1)
        self.select_path_button = tk.Button(self.window, image=self.icon, command=self.get_save_directory)
        self.check_button = tk.Button(self.window, text='check', borderwidth=2, command=self.check_url)
        self.invalid_url_label = tk.Label(self.window, text='')

        self.title_label = tk.Label(self.window, text='')
        self.quality_label = tk.Label(self.window, text='')

        self.v = tk.StringVar()
        self.radio_360 = None
        self.radio_480 = None
        self.radio_720 = None
        self.radio_1080 = None

        self.download_button = tk.Button(self.window, text='download', borderwidth=2, command=self.confirm)

        self.save_directory = '/home/usama/Downloads'
        self.URL = None


    def set_constraints_for_main_window(self):
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry('640x360+{}+{}'.format(int((width/2)-(640/2)), int((height/2)-(480/2))))
        self.window.title('Youtube Video Downloader')
        self.window.resizable(False, False)

    def generate_widgets_for_main_window(self):
        enter_url_label = tk.Label(self.window, text='Enter URL')
        enter_url_label.config(font=('Ariel', 15))
        enter_url_label.place(relx=0.43, rely=0.05)

        self.url_textbox.place(relx=0.18, rely=0.14)
        self.select_path_button.place(relx=0.85, rely=0.14)
        self.check_button.place(relx=0.44, rely=0.2)

        self.invalid_url_label.config(font=('Ariel', 10), fg='Red')
        self.invalid_url_label.place(relx=0.3, rely=0.28)

        self.title_label.config(font=('Ariel', 12))
        self.title_label.place(relx=0.18, rely=0.4)

        self.quality_label.config(font=('Ariel', 12))
        self.quality_label.place(relx=0.18, rely=0.45)
    
    def generate_radio_buttons(self, qualities):
        x_placement = 0.3
        if '360p' in qualities:
            self.radio_360 = tk.Radiobutton(self.window, text='360p', variable=self.v, value='360')
            self.radio_360.select()
            self.radio_360.place(relx=x_placement, rely=0.45)
            x_placement += 0.1
        if '480p' in qualities:
            self.radio_480 = tk.Radiobutton(self.window, text='480p', variable=self.v, value='480')
            self.radio_480.place(relx=x_placement, rely=0.45)
            x_placement += 0.1
        if '720p' in qualities:
            self.radio_720 = tk.Radiobutton(self.window, text='720p', variable=self.v, value='720')
            self.radio_720.place(relx=x_placement, rely=0.45)
            x_placement += 0.1
        if '1080p' in qualities:
            self.radio_1080 = tk.Radiobutton(self.window, text='1080p', variable=self.v, value='1080')
            self.radio_1080.place(relx=x_placement, rely=0.45)
            x_placement += 0.1

        self.download_button.place(relx=0.423, rely=0.55)



    def get_save_directory(self):
        path = filedialog.askdirectory(parent=self.window
        , initialdir='/home/usama/Downloads'
        , title='select a directory')
        self.save_directory = str(path)

    def check_url(self):
        URL_flag = False
        url = self.url_textbox.get()
        URL_flag = checkers.is_url(url)
        if len(url) > 43 or len(url) > 28:
            URL_flag = False
        if (url[0:31] == 'https://www.youtube.com/watch?v' and len(url)<=43) or (url[0:17] == 'https://youtu.be/' and len(url)<=28):
            URL_flag = True
        else:
            URL_flag = False
        title = None
        if URL_flag:
            self.invalid_url_label.config(text='')
            self.URL = url
        else:
            self.URL = None
            self.invalid_url_label.config(text='Invalid URL. Don\'t forget to include https:// as well.')
            self.title_label.config(text='')
            self.quality_label.config(text='')
            self.radio_360.place_forget()
            self.radio_480.place_forget()
            self.radio_720.place_forget()
            self.radio_1080.place_forget()
            self.download_button.place_forget()
        if self.URL:
            self.downloader = Downloader(self.URL)
            title = self.downloader.get_title()
            qualities = self.downloader.get_qualities()
            self.title_label.config(text='Title: ' + title)
            self.generate_radio_buttons(qualities)
            self.quality_label.config(text='Quality: ')

    def confirm(self):
        
        self.downloader.get_streams(quality=self.v.get(), save_path=self.save_directory)
        self.downloader.create_download_window(self.window, self.save_directory)
        self.forget_widgets()
        self.window.withdraw()

    def forget_widgets(self):
        self.url_textbox.delete(0, 'end')
        self.title_label.config(text='')
        self.quality_label.config(text='')
        self.radio_360.place_forget()
        self.radio_480.place_forget()
        self.radio_720.place_forget()
        self.radio_1080.place_forget()
        self.download_button.place_forget()

    def on_window_event_quit(self):
        time.sleep(0.2)
        self.window.destroy()

    def create_main_window(self):
        self.set_constraints_for_main_window()
        self.generate_widgets_for_main_window()
        self.window.protocol('WM_DELETE_WINDOW', self.on_window_event_quit)
        try:
            self.window.mainloop()
        except:
            pass

    

if __name__ == "__main__":
    win = Window()
    win.create_main_window()