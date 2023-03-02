# import cv2
from moviepy.editor import VideoFileClip, AudioFileClip

# cap = cv2.VideoCapture("original.mp4")
#
# fps = cap.get(cv2.CAP_PROP_FPS)
#
# video_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
#
# frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
#
# frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
#
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#
# videowriter = cv2.VideoWriter('nosound.mp4', fourcc, round(fps), (256, 256), True)
#
# for i in range(int(video_frame_count)):
#     print(i)
#
#     frame2 = cv2.imread('frames/image{}.jpg'.format(i))
#
#     videowriter.write(frame2)
#
# videowriter.release()

# 获取无声视频
video_clip = VideoFileClip('static/video/nosound.mp4')

# # 获取音频
# audio_clip = AudioFileClip("original.mp4")
#
# # 视频里面添加声音
# final_video = video_clip.set_audio(audio_clip)

# 保存视频
video_clip.write_videofile("static/video/withsound.mp4")
