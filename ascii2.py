import cv2
import tkinter as tk
from tkinter import filedialog
import time
import os
import sys
import shutil


if os.name == 'nt':
    os.system('')


ASCII_CHARS = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

def select_file():
    root = tk.Tk()
    root.withdraw() 
    file_path = filedialog.askopenfilename(
        title="Select an image or video",
        filetypes=[
            ("Медиа файлы", "*.mp4 *.avi *.mov *.mkv *.jpg *.jpeg *.png *.bmp"),
            ("Видео", "*.mp4 *.avi *.mov *.mkv"),
            ("Изображения", "*.jpg *.jpeg *.png *.bmp"),
            ("Все файлы", "*.*")
        ]
    )
    return file_path

def resize_frame_to_terminal(frame):
    """Automatically adjusts the frame size to the terminal size"""
    term_size = shutil.get_terminal_size(fallback=(120, 30))
    term_width = term_size.columns
    term_height = term_size.lines - 1 

    img_height, img_width = frame.shape[:2]
    char_aspect_ratio = 0.45 

    new_width = term_width
    new_height = int(new_width * (img_height / img_width) * char_aspect_ratio)

    if new_height > term_height:
        new_height = term_height
        new_width = int(new_height * (img_width / img_height) / char_aspect_ratio)

    new_width = max(1, new_width)
    new_height = max(1, new_height)

    resized_frame = cv2.resize(frame, (new_width, new_height))
    return resized_frame

def frame_to_ascii_color(frame):
    """Converts an OpenCV frame into a string of colored ASCII characters"""
    frame = resize_frame_to_terminal(frame)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    ascii_buffer = []
    chars_len = len(ASCII_CHARS) - 1
    
    height, width = frame.shape[:2]
    
    for y in range(height):
        for x in range(width):
            b, g, r = frame[y, x]
            brightness = gray_frame[y, x]
            
            char_index = int(brightness / 255 * chars_len)
            char = ASCII_CHARS[char_index]
            
            ascii_buffer.append(f"\033[38;2;{r};{g};{b}m{char}")
            
        ascii_buffer.append("\033[0m\n")
    
    return "".join(ascii_buffer)

def play_media(file_path):
    if not file_path:
        print("The file is not selected. Exit.")
        return

    is_video = file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))

    os.system('cls' if os.name == 'nt' else 'clear')

    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        print("Error: The file could not be opened.")
        return

    if is_video:
        print("Play the video (loop). Press Ctrl+C to exit.")
        time.sleep(1) 

    try:
        while True:
            ret, frame = cap.read()
            
           
            if not ret:
                if is_video:
                    
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue 
                else:
                    break 

            ascii_image = frame_to_ascii_color(frame)

            if is_video:
                sys.stdout.write('\033[H') 
                sys.stdout.write(ascii_image)
                sys.stdout.flush()
                time.sleep(0.015) 
            else:
                sys.stdout.write('\033[H')
                sys.stdout.write(ascii_image)
                sys.stdout.flush()
                break 

    except KeyboardInterrupt:
        pass 
    finally:
        cap.release()
       
        print("\033[0m\n\n Decided by the user.")

if __name__ == "__main__":
    file = select_file()
    play_media(file)