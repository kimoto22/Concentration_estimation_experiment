from tkinter import *
from tkinter import ttk
import tkinter as tk
import time
import threading
import video
import audio
from tkinter import messagebox
import datetime
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
global interval
from log_for_CSV import Log

interval = 120
task_count = 7

video = video.Video()
audio = audio.Audio()

def click_close():
    if messagebox.askokcancel("確認", "本当に閉じていいですか？"):
        close()
        return 0

def close():
    root.destroy()

####課題選択####
def change():
    v1 = StringVar()
    global canvas2
    canvas2 = tk.Canvas(root, highlightthickness=0)
    canvas2.pack(
        fill=tk.BOTH, expand=True
    )  # configure canvas to occupy the whole main window
    # 各種ウィジェットの作成
    label1_frame_app = tk.Label(canvas2, text="数本の映像を見てもらいます", font=("", 40))
    button_change_frame_app = tk.Button(
        canvas2, text="進む", font=("", 40), bg="grey", command=lambda: task_select(canvas2,v1),relief="solid"
    )

    # 各種ウィジェットの設置
    label1_frame_app.pack(anchor="center", expand=1)
    button_change_frame_app.pack(anchor="center", expand=1)
    print("count:" + str(count))

def task_select(canvas,v1):
    print("集中度:%s" % v1.get())
    ans = v1.get()
    # logに書き込み
    log.logging(situation="アンケート解答", questionnaire=str(ans))
    canvas.destroy()
    canvas2.destroy()

    canvas1 = tk.Canvas(root, highlightthickness=0)  # ,bg = "cyan")
    canvas1.pack(
        fill=tk.BOTH, expand=True
    )  # configure canvas to occupy the whole main window
    if count == task_count:
        end(canvas1)
    else:
        watch_movie(master=canvas1)


####アンケート評価####
def questionnaire():
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)  # configure canvas to occupy the whole main window

    # Style - Theme
    ttk.Style().configure('MyWidget.TRadiobutton' ,font=(None,30))
    ttk.Style().map('MyWidget.TRadiobutton',foreground=[ ('active', 'blue')],background=[ ('active', 'white')])
    label = tk.Label(canvas, text="課題を通して自分の集中度を評価してください", font=("", 30))

    # Radiobutton 1
    v1 = StringVar()
    rb1 = ttk.Radiobutton(
        canvas,
        text="1.集中していた",
        value='1',
        style='MyWidget.TRadiobutton',
        variable=v1, command =lambda: change_state(button1))

    # Radiobutton 2
    rb2 = ttk.Radiobutton(
        canvas,
        text='2.少し集中していた',
        value='2',
        style='MyWidget.TRadiobutton',
        variable=v1, command = lambda: change_state(button1))

    # Radiobutton 2
    rb3 = ttk.Radiobutton(
        canvas,
        text='3.どちらでもない',
        value='3',
        style='MyWidget.TRadiobutton',
        variable=v1, command = lambda: change_state(button1))

    # Radiobutton 2
    rb4 = ttk.Radiobutton(
        canvas,
        text='4.少し集中できなかった',
        value='4',
        style='MyWidget.TRadiobutton',
        variable=v1, command = lambda: change_state(button1))

    # Radiobutton 2
    rb5 = ttk.Radiobutton(
        canvas,
        text='5.全く集中できなかった',
        value='5',
        style='MyWidget.TRadiobutton',
        variable=v1, command = lambda: change_state(button1))

    # Button
    button1 = tk.Button(
        canvas,
        text='OK',
        font=("", 30),
        command=lambda: task_select(canvas,v1),
        state=tk.DISABLED,relief="solid",
        bg="grey")


    label.pack(anchor="center",expand=1)
    rb1.pack(anchor="center",pady=20)
    rb2.pack(anchor="center",pady=20)
    rb3.pack(anchor="center",pady=20)
    rb4.pack(anchor="center",pady=20)
    rb5.pack(anchor="center",pady=20)
    button1.pack(anchor="center", expand=1)


def change_state(button1):
    if button1["state"] == tk.DISABLED:
        button1["state"] = tk.NORMAL

def end(canvas):
    label = tk.Label(canvas, text="課題は終了です。", font=("", 40))
    label1 = tk.Label(canvas, text="お疲れ様でした。", font=("", 40))
    label.pack(anchor="center", expand=1)
    label1.pack(anchor="center", expand=1)

    root.after(3000,close)
    # logに書き込み
    log.logging(situation="実験終了", questionnaire="-")

####映像####
class watch_movie(tk.Frame):
    def __init__(self, master):
        if (count %2 == 0):
            self.txt = "リラックス動画が流れます"

            self.video_path = "./video/relax.mp4"
            self.audio_path="./video/relax.wav"
        else:
            if count == 1:
                movie_name = "1"
            elif count == 3:
                movie_name = "2"
            elif count == 5:
                movie_name = "3"

            self.txt = "映画予告の動画が流れます"
            self.video_path = "./video/" + movie_name + ".mp4"
            self.audio_path="./video/" + movie_name + ".wav"


        super().__init__(master)
        self.pack()

        # 各種ウィジェットの作成
        self.label1_frame_app = tk.Label(self.master, text=str(self.txt),font=("", 40))#,fg="red")
        self.button_change_frame_app = tk.Button(
            self.master, text="再生", font=("", 40), bg="grey", command=lambda: self.rocate(),relief="solid")
        # 各種ウィジェットの設置
        self.label1_frame_app.pack(anchor="center", expand=1)
        self.button_change_frame_app.pack(anchor="center", expand=1)

    def rocate(self):
        self.label1_frame_app.pack_forget()
        self.button_change_frame_app.pack_forget()
        #self.create_widgets()

        # 経過時間スレッドの開始
        self.t = threading.Thread(target=self.timer, daemon=True)
        self.t.start()

        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.frame = tk.Label(self.canvas)
        self.canvas.frame.pack(side=tk.BOTTOM)

        video.openfile(self.video_path, self.canvas.frame)
        audio.openfile(self.audio_path)

        self.master.destroy()
        audio.play()
        video.play()


        if (count %2 == 0):
            # logに書き込み
            log.logging(situation="リラックスビデオスタート", questionnaire="-")
        else:
            # logに書き込み
            log.logging(situation="集中ビデオスタート", questionnaire="-")


    def timer(self):
        self.second = 0
        self.flg = True
        while self.flg:
            print(self.second)
            self.second += 1
            #self.time_label.configure(text=f"経過時間：{self.second}秒")
            time.sleep(1)

            # 2分経ったら
            if self.second == interval:
                #self.q_label2.configure(text="")

                # logに書き込み
                log.logging(situation="ビデオ終了", questionnaire="-")

                self.second = 0
                video.stop()
                audio.stop()
                self.canvas.destroy()

                global count
                count += 1
                questionnaire()
                # logに書き込み
                log.logging(situation="アンケート解答画面", questionnaire="-")
                return 0

if __name__ == "__main__":
    root = tk.Tk()
    global count
    count = 1
    root.attributes("-fullscreen", True)
    root.title("視聴実験")
    
    # logを取る
    dt_now = datetime.datetime.now()
    now = dt_now.strftime('%Y_%m_%d_%H.%M.%S')[:-3]
    global log
    log = Log()
    log.first_log(now)
    # logに書き込み
    log.logging(situation="実験スタート", questionnaire="-")
    
    change()
    root.protocol("WM_DELETE_WINDOW", click_close)
    root.mainloop()