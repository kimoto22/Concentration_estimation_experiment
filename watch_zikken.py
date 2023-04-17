from tkinter import *
from tkinter import ttk
import tkinter as tk
import time
import threading
import datetime
import pandas as pd
import video
import audio
import random
from tkinter import messagebox
import pyautogui as pag
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
global interval

interval = 120

video = video.Video()
audio = audio.Audio()

def click_close():
    if messagebox.askokcancel("確認", "本当に閉じていいですか？"):
        root.destroy()
        return 0

####リラックス####
class relax_movie(tk.Frame):
    def __init__(self, master):

        super().__init__(master)
        self.pack()

        # 各種ウィジェットの作成
        self.label1_frame_app = tk.Label(self.master, text="リラックス動画",font=("", 40))#,fg="red")
        self.button_change_frame_app = tk.Button(
            self.master, text="課題に進む", font=("", 40), bg="grey", command=lambda: self.rocate(),relief="solid"
        )
        # 各種ウィジェットの設置
        self.label1_frame_app.pack(anchor="center", expand=1)
        self.button_change_frame_app.pack(anchor="center", expand=1)


    def rocate(self):
        self.label1_frame_app.pack_forget()
        self.button_change_frame_app.pack_forget()
        self.create_widgets()

        # 経過時間スレッドの開始
        self.t = threading.Thread(target=self.timer, daemon=True)
        self.t.start()

        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.frame = tk.Label(self.canvas)
        self.canvas.frame.pack(side=tk.BOTTOM)

        video.openfile("./video/1.mp4", self.canvas.frame)
        audio.openfile("./video/1.wav")

        audio.play()
        video.play()

        # Tkインスタンスに対してキーイベント処理を実装
        # self.master.bind("<KeyPress>", self.type_event)

    # ウィジェットの生成と配置
    def create_widgets(self):
        # # 時間計測用のラベル
        self.time_label = tk.Label(self, text="", font=("", 20))
        self.time_label.grid(row=4, column=0, columnspan=2)

    def timer(self):
        self.second = 0
        self.flg = True
        while self.flg:
            print(self.second)
            self.second += 1
            self.time_label.configure(text=f"経過時間：{self.second}秒")
            time.sleep(1)

            # 2分経ったら
            if self.second == interval:
                #self.q_label2.configure(text="")

                self.second = 0
                video.stop()
                audio.stop()
                self.destroy()
                self.master.destroy()

                global count
                count += 1
                root.destroy()
                return 0

if __name__ == "__main__":
    root = tk.Tk()
    # root.geometry("1280x720")
    # root.state("zoomed")
    global count
    count = 1
    root.attributes("-fullscreen", True)
    root.title("タイピングゲーム！")

    canvas1 = tk.Canvas(root, highlightthickness=0)  # ,bg = "cyan")
    canvas1.pack(
        fill=tk.BOTH, expand=True
    )  # configure canvas to occupy the whole main window
    relax_movie(master=canvas1)

    # change(eye_task)
    root.protocol("WM_DELETE_WINDOW", click_close)
    root.mainloop()