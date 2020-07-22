import cv2
import pafy
import time
import pytesseract

from moviepy.editor import VideoFileClip
from PIL import Image

video_path = "/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/satsang_test.mov"
video_path2 = "/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/clip_1.avi"



cap = cv2.VideoCapture(video_path)



cap.set(cv2.CAP_PROP_POS_FRAMES, 0)



fps = cap.get(cv2.CAP_PROP_FPS)
success,image = cap.read()

totalTime = (cap.get(cv2.CAP_PROP_FRAME_COUNT)/fps)
print(totalTime)
num=0
frame_rate = 100
prev = 0

count = 0
startTime = 0
endTime = 0
ds_factor = 0.5

startTimeSet = []
endTimeSet = []

now = time.perf_counter()
timeStamps = []
start_time = time.time()
finalTime = 0
times = []

count2=0
x = 0
faleSafe = 0

while (count/fps) < totalTime - 20:
    count+=2
    print(count/fps)
    time_elapsed = time.time() - prev
    _, img = cap.read()
    _, img2 = cap.read()

    count2 += 1
    if (count2 == 1):
        currentTime = time.time()
        finalTime = currentTime + 3
    elif time.time() >= finalTime:
        img2[img2 >= 200] = 76
        img2[img2 != 76] = 255
        img2[img2 == 76] = 0
        img3 = Image.fromarray(img2).convert('L')
        img3 = img3.crop((0, 330, 168, 357))
        print(img3)
        result = pytesseract.image_to_string(img3, lang='eng')
        print(result.lower())
        count2 = 0
        if num == 0:
            if result.lower().find("amma") != -1:
                startTime = int(count/fps)
                times.append(startTime)
                print("talking")
                num += 1
            elif result.lower().find("ashram") != -1:
                startTime = int(count/fps)
                print("talking")
                times.append(startTime)
                num += 1
            print(times)
        else:
            if result.lower().find("amma") != -1:
                times.append(count/fps)
                print("talking")
                faleSafe = 0
            elif result.lower().find("ashram") != -1:
                times.append(count/fps)
                print("talking")
                faleSafe = 0
            elif result.lower().find("amma") == -1:
                faleSafe += 1
                if faleSafe > 2:
                    times.append(count/fps)
                    print("done")
                    endTime = count/fps
                    if(startTime - 10 >= 0):
                        startTime -= 10
                        clip = VideoFileClip(video_path).subclip(startTime, endTime + 40)
                        clip.to_videofile("/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/ammVidNum" +
                                      str(x) + ".mp4", codec="libx264", temp_audiofile='temp-audio.m4a',
                                      remove_temp=True, audio_codec='aac')
                    else:
                        clip = VideoFileClip(video_path).subclip(startTime, endTime + 40)
                        clip.to_videofile("/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/ammVidNum" +
                                      str(x) + ".mp4", codec="libx264", temp_audiofile='temp-audio.m4a',
                                      remove_temp=True, audio_codec='aac')
                    x+=1
                    startTime = 0
                    endTime = 0
                    num = 0
                    faleSafe = 0
                    times.clear()
            elif result.lower().find("ashram") == -1:
                faleSafe += 1
                if faleSafe > 2:
                    times.append(count/fps)
                    print("done")
                    endTime = count/fps
                    if (startTime - 10 >= 0):
                        startTime -= 10
                        clip = VideoFileClip(video_path).subclip(startTime, endTime + 40)
                        clip.to_videofile("/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/ammVidNum" +
                                          str(x) + ".mp4", codec="libx264", temp_audiofile='temp-audio.m4a',
                                          remove_temp=True, audio_codec='aac')
                    else:
                        clip = VideoFileClip(video_path).subclip(startTime, endTime + 40)
                        clip.to_videofile("/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/ammVidNum" +
                                      str(x) + ".mp4", codec="libx264", temp_audiofile='temp-audio.m4a',
                                      remove_temp=True, audio_codec='aac')
                    x += 1
                    startTime = 0
                    endTime = 0
                    num = 0
                    faleSafe = 0
                    times.clear()
            print(times)


    cv2.imshow('img', img)

    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

clip = VideoFileClip(video_path).subclip(startTime, endTime)
clip.to_videofile("/Users/ananthgoyal/PycharmProjects/recognition_test/Resources/ammVidNum" +
                    str(x) + ".mp4", codec="libx264", temp_audiofile='temp-audio.m4a',
                    remove_temp=True, audio_codec='aac')
cap.release()