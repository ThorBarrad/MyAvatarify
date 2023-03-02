from flask import Flask, render_template, request
import cv2
import threading
from moviepy.editor import VideoFileClip

# from cam_fomm_changed_v1 import process_video

app = Flask(__name__)

images = ["static/avatars/einstein.jpg", "static/avatars/eminem.jpg", "static/avatars/jobs.jpg",
          "static/avatars/mona.jpg", "static/avatars/obama.jpg", "static/avatars/potter.jpg",
          "static/avatars/ronaldo.png", "static/avatars/schwarzenegger.png", "static/avatars/zmine.jpg"]

videos = ["static/results/withsound2.mp4", "static/results/withsound5.mp4", "static/results/withsound5.mp4",
          "static/results/withsound3.mp4", "static/results/withsound5.mp4", "static/results/withsound5.mp4",
          "static/results/withsound5.mp4", "static/results/withsound5.mp4", "static/results/withsound5.mp4"]


class VirtualThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.cap = cv2.VideoCapture(0)

    def run(self):
        global active, i, destroy
        while True:
            if active:
                ret, img = self.cap.read()
                img = cv2.flip(img, 1)
                cv2.imwrite('static/cam/image{}.jpg'.format(i), img)
                i += 1
            if destroy:
                break
        self.cap.release()


@app.route("/", methods=['POST', 'GET'])
def index():
    global active, i, image_index, destroy, filename
    if request.method == "POST" and request.form.get("post_type") == "video_upload":
        video = request.files['video_upload']
        if video:
            filename = video.filename
            # print(filename)
            video.save("static/video/" + filename)
            return render_template("index.html", imgsrc="", vdosrc="", uploadvideo="static/video/" + filename)
        else:
            # 开启摄像头进行人脸录制
            active = True
            return render_template("index2.html", imgsrc="", vdosrc="",
                                   uploadvideo="")

    elif request.method == "POST" and request.form.get("post_type") == "video_stop":
        # 停止人脸录制
        active = False

        img = cv2.imread('static/cam/image0.jpg')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        videowriter = cv2.VideoWriter('static/video/original2.mp4', fourcc, 30, (img.shape[1], img.shape[0]), True)
        for j in range(i - 5):
            frame2 = cv2.imread('static/cam/image{}.jpg'.format(j))
            videowriter.write(frame2)
        videowriter.release()
        video_clip = VideoFileClip('static/video/original2.mp4')
        filename = "camcapture" + str(i) + ".mp4"
        video_clip.write_videofile("static/video/" + filename)

        i = 0
        return render_template("index.html", imgsrc="", vdosrc="", uploadvideo="static/video/" + filename)

    # elif request.method == "POST" and request.form.get("post_type") == "video_restart":
    #     return render_template("index.html", imgsrc=images[image_index], vdosrc=videos[image_index])

    # elif request.method == "POST" and request.form.get("post_type") == "video_confirm":
    #     destroy = True
    #     return render_template("index.html", imgsrc=images[image_index], vdosrc=videos[image_index])

    elif request.method == "POST" and request.form.get("post_type") == "image_upload":
        # destroy = True
        image = request.files['image_upload']
        if image:
            image.save("static/avatars/zmine.jpg")
            image_index = 8
        else:
            image_index = int(request.form.get("image_index"))
        return render_template("index.html", imgsrc=images[image_index], vdosrc="",
                               uploadvideo="static/video/" + filename)

    # elif request.method == "POST" and request.form.get("post_type") == "image_restart":
    #     return render_template("index.html", imgsrc=images[image_index], vdosrc=videos[image_index])

    elif request.method == "POST" and request.form.get("post_type") == "image_confirm":
        # process video and image
        # process_video("static/video/original.mp4", image_index)
        return render_template("index.html", imgsrc=images[image_index], vdosrc=videos[image_index],
                               uploadvideo="static/video/" + filename)

    else:
        # return render_template("video_upload.html")
        return render_template("index.html", imgsrc="", vdosrc="", uploadvideo="")


if __name__ == "__main__":
    active = False
    i = 0
    image_index = 0
    destroy = False
    filename = ""
    thread = VirtualThread()
    thread.start()
    app.run()
