#!/usr/bin/python 
# -*- coding:utf-8 -*-

import os
import tkinter as tk
import threading
import wave
import pyaudio
import sys # argv

if os.name == 'nt':
    import ctypes
elif os.name == 'posix':
    import gtk

class Notify():
    def __init__(self,str_title_text="",str_show_text="",str_aud_file_name=""):
        self.str_title_text = str_title_text
        self.str_show_text = str_show_text
        if str_aud_file_name == "":
            self.str_aud_file_name = os.path.dirname(__file__) + "/content/main.wav"
            print(self.str_aud_file_name)
        else:
            self.str_aud_file_name = str_aud_file_name

    def __del__(self):
        pass

    def notify(self):
        self.root = tk.Tk()
        self.root.title(self.str_title_text)
        screenwidth,screenheight=self.getMonitorSize()
        dialogwidth=400
        dialogheight=240
        textboxwidth=400
        textboxheight=40
        self.root.geometry("+%d+%d"%(screenwidth-dialogwidth-30,screenheight-dialogheight-105))
        self.root.attributes("-topmost",True)

        self.container = tk.Frame(self.root,width=dialogwidth,height=dialogheight)
        self.container.propagate(0)
        self.canvas = tk.Canvas(self.container)
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.frame2=tk.Frame(self.root,width=400,height=40)
        self.frame2.grid(row=1,column=0,padx=10,pady=5)
        self.frame2.propagate(0)
        self.ary_obj_text=[]
        self.ary_text=[]

    def quit(self):
        self.root.destroy()

    def start(self):
        self.container.grid(row=0,column=0,padx=10,pady=5)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.root.mainloop()

    def setButton(self):
        button = tk.Button(self.frame2,
                            text = 'Click and Quit',
                            command=self.quit)
        button.place(relx=1.0,rely=1.0,anchor='se')

    def setLabel(self,str_text):
        d='\n'.join(textwrap.wrap(str_text,30))
        l=tk.Label(self.scrollable_frame,text=d,relief="solid",width='40',height=str(d.count('\n')+3))
        l.pack()

    def UpdateScrollFrame(self):
        self.scrollable_frame.update_idletasks()

    def setText(self,str_text=""):
        if str_text != "":
            self.str_show_text = str_text

        if len(self.ary_obj_text) > 0:
            map(lambda x: x.destroy(),self.ary_obj_text)
            self.ary_text.insert(0,self.str_show_text)
        else:
            self.ary_text.insert(0,self.str_show_text)
        while len(self.ary_text) > 5:
            self.ary_text.pop()

        for i in range(len(self.ary_text)):
            default_height = 3
            set_height = self.ary_text[i].count('\n')
            if set_height < default_height:
                set_height = default_height
            set_height = str(set_height)

            self.ary_obj_text.insert(len(self.ary_obj_text),tk.Text(self.scrollable_frame,width='40',height=set_height))
            self.ary_obj_text[-1].insert('1.0',self.ary_text[i])
            self.ary_obj_text[-1].pack()

    def getMonitorSize(self,):
        if os.name == 'posix':
            w=gtk.Window()
            s=w.get_screen()
            return [s.get_monitor_geometry(0).width,s.get_monitor_geometry(0).height]
        if os.name == 'nt':
            user32 = ctypes.windll.user32
            return [user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)]

    def wavplay(self,str_aud_file_name=""):
        if str_aud_file_name != "":
            self.str_aud_file_name = str_aud_file_name

        wf = wave.open(self.str_aud_file_name, "r")
    
        # ストリームを開く
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
    
        # チャンク単位でストリームに出力し音声を再生
        chunk = 1024
        data = wf.readframes(chunk)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()

def notify(text):
    obj_notify=Notify('notify')
    obj_notify.notify()
    obj_notify.setText(text)
    obj_notify.setButton()
    obj_notify.wavplay()
    obj_notify.start()

def main():
    print(sys.getdefaultencoding())
    if len(sys.argv) != 2:
        print("Usage: %s message"%(sys.argv[0]))

    str_set_text = sys.argv[1]
    print(str_set_text.encode('utf-8'))
    notify(str_set_text)
    return 0

if __name__ == '__main__':
    main()
