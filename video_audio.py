import cv2
from playsound import playsound
import threading

# 音声ファイルの再生を行う関数
def play_audio(file):
    playsound(file)

# 動画ファイルの読み込み
cap = cv2.VideoCapture('.\\face_landmark\\video\\video\\1.mp4')

# 音声ファイルの再生を開始する
audio_thread = threading.Thread(target=play_audio, args=('.\\face_landmark\\video\\video\\1.mp3',))
audio_thread.start()

# 動画の再生
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv2.imshow('frame',frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

# スレッドを停止し、リソースを解放する
audio_thread.join()
cap.release()
cv2.destroyAllWindows()
