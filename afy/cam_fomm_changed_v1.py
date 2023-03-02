import glob
import yaml

import numpy as np
import cv2

from arguments import opt
from utils import resize

from moviepy.editor import VideoFileClip, AudioFileClip


def load_images(IMG_SIZE=256):
    avatars = []
    filenames = []
    images_list = sorted(glob.glob(f'{opt.avatars}/*'))
    for i, f in enumerate(images_list):
        if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png'):
            img = cv2.imread(f)
            if img is None:
                continue
            if img.ndim == 2:
                img = np.tile(img[..., None], [1, 1, 3])
            img = img[..., :3][..., ::-1]
            img = resize(img, (IMG_SIZE, IMG_SIZE))
            avatars.append(img)
            filenames.append(f)
    return avatars, filenames


def change_avatar(predictor, new_avatar):
    predictor.get_frame_kp(new_avatar)
    predictor.set_source_image(new_avatar)


def process_video(videopath, imageindex):
    with open('../config.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    IMG_SIZE = 256

    predictor_args = {
        'config_path': opt.config,
        'checkpoint_path': opt.checkpoint,
        'relative': opt.relative,
        'adapt_movement_scale': opt.adapt_scale,
        'enc_downscale': opt.enc_downscale
    }

    import predictor_local

    predictor = predictor_local.PredictorLocal(
        **predictor_args
    )

    cap = cv2.VideoCapture(videopath)

    fps = cap.get(cv2.CAP_PROP_FPS)

    video_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    avatars, avatar_names = load_images()

    print("success here")

    cur_ava = imageindex

    change_avatar(predictor, avatars[cur_ava])

    x = 0
    y = 0
    w = 0
    h = 0

    predictor.reset_frames()

    face_cascade = cv2.CascadeClassifier('static/haarcascade_frontalface_default.xml')

    for i in range(int(video_frame_count)):

        print(i)

        ret, frame = cap.read()

        if not ret:
            cv2.imwrite('static/frames/image{}.jpg'.format(i), avatars[cur_ava][..., ::-1])
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            cv2.imwrite('static/frames/image{}.jpg'.format(i), avatars[cur_ava][..., ::-1])
            continue

        frame = frame[..., ::-1]

        if i == 0:
            x, y, w, h = faces[0]

        frame = frame[max(y - h // 2, 0):min(y + h + h // 2, frame.shape[0]),
                max(x - w // 3, 0):min(x + w + w // 3, frame.shape[1])]

        frame = resize(frame, (IMG_SIZE, IMG_SIZE))[..., :3]

        out = predictor.predict(frame)

        if out is not None:
            cv2.imwrite('static/frames/image{}.jpg'.format(i), out[..., ::-1])

        else:
            cv2.imwrite('static/frames/image{}.jpg'.format(i), avatars[cur_ava][..., ::-1])

    cap.release()

    # 添加音频
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    videowriter = cv2.VideoWriter('static/video/nosound.mp4', fourcc, round(fps), (256, 256), True)

    for i in range(int(video_frame_count)):
        print(i)

        frame2 = cv2.imread('static/frames/image{}.jpg'.format(i))

        videowriter.write(frame2)

    videowriter.release()

    # 获取无声视频
    video_clip = VideoFileClip('static/video/nosound.mp4')

    try:
        # 获取音频
        audio_clip = AudioFileClip(videopath)

        # 视频里面添加声音
        final_video = video_clip.set_audio(audio_clip)

        # 保存视频
        final_video.write_videofile("static/video/withsound.mp4")

    except:
        print("warning: no audio detected!")
        video_clip.write_videofile("static/video/withsound.mp4")


if __name__ == "__main__":
    process_video("static/video/original.mp4", 0)
