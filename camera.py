import datetime
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2

def record(cap, out, fil):
    tm = cv2.TickMeter()
    tm.start()
    count = 0
    count1 = 0
    max_count = 1
    fps = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            if count == max_count:
                tm.stop()
                fps = max_count / tm.getTimeSec()
                tm.reset()
                tm.start()
                count = 0
            #cv2.putText(frame, 'FPS: {:.2f}'.format(fps),(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), thickness=2)
            #cv2.putText(frame, 'Frame:{:.0f}'.format(count1),(1000, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), thickness=2)
            out.write(frame)
            cv2.imshow('camera', frame)
            dt_now = datetime.datetime.now()
            time = dt_now.strftime('%Y/%m/%d %H.%M.%S.%f')[:-3]
            fil.write(str(count1) + "," + str(fps) +  "," + str(time) +"\n")
            count1 += 1
            count += 1

            k = cv2.waitKey(1)
            if k == 27:    # Esc key to stop
                break
        else:
            break

    fil.close()
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    dt_before = datetime.datetime.now().strftime('%Y/%m/%d %H.%M.%S.%f')[:-3]
    print("Camera start:"+str(dt_before))
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    fps = 30
    w = 1280
    h = 720
    cap.set(cv2.CAP_PROP_FPS, fps)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'));

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(fps)
    print(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    m="test1"
    name="./camera/"+str(m)
    txt_name = str(name)+'.txt'
    fil = open(str(txt_name), 'w')
    #print(f)
    camera_name = str(name)+'_video.mp4'
    out = cv2.VideoWriter(str(camera_name), fourcc, fps, (w, h))
    dt_after = datetime.datetime.now().strftime('%Y/%m/%d %H.%M.%S.%f')[:-3]

    print("Camera after start:"+str(dt_after))
    fil.write("Camera start,"+str(dt_before)+"\nCamera after start,"+str(dt_after)+"\nresolution,"+str(w)+"*"+str(h)+"\nMovie FPS,"+str(fps)+"\n")
    fil.write("frame,FPS,time\n")

    record(cap, out, fil)

    fil.close()
    cap.release()
    out.release()
    cv2.destroyAllWindows()

