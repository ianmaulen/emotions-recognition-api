# -*- coding: utf-8 -*-

import cv2
import os

def extract_frames(video_path, output_folder, desired_frames=30):
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = total_frames // desired_frames

    frames_captured = 0
    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        if frame_count % frame_interval == 0:
            output_file = os.path.join(output_folder, f"frame_{frames_captured + 1}.jpg")
            is_success, im_buf_arr = cv2.imencode(".jpg", frame)
            im_buf_arr.tofile(output_file)
            # cv2.imencode('.jpg', frame)[1].toFile(output_file)
            frames_captured += 1

        if frames_captured == desired_frames:
            break

    cap.release()
    print(f'Se han capturado {desired_frames} fotogramas en la carpeta "{output_folder}".')