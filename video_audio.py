import cv2
from playsound import playsound
import threading

# 音声ファイルの再生を行う関数
def play_audio(file):
    playsound(file)


# 動画の再生
def video_start(file):
    cap = cv2.VideoCapture(file)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('frame',frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            cap.release()
            cv2.destroyAllWindows()
            break
# 動画ファイル読み込み
video_thread = threading.Thread(target=video_start, args=('動画パス\\.mp4',))
# 音声ファイルの再生を開始する
audio_thread = threading.Thread(target=play_audio, args=("音声パス\\.mp3",))

video_thread.start()
audio_thread.start()

# スレッドを停止し、リソースを解放する
video_thread.join()
audio_thread.join()

