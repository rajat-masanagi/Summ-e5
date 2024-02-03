from pytube import YouTube
import cv2
import os

def extract_frames_from_video(url, output_folder, interval):
    try:
        # Download video and get its path
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        video_path = stream.download()

        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Open video file
        cap = cv2.VideoCapture(video_path)

        frame_count = 0
        img_count = 0

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            frame_count += 1

            # Save frame every 'interval' frames
            if frame_count % interval == 0:
                img_path = os.path.join(output_folder, f"frame_{img_count}.jpg")
                cv2.imwrite(img_path, frame)
                img_count += 1

        cap.release()
        cv2.destroyAllWindows()

        print(f"Frames extracted successfully and saved in '{output_folder}' folder!")

        # Delete the video file after extracting frames
        os.remove(video_path)

    except Exception as e:
        print(f"Error extracting frames: {e}")

if __name__ == "__main__":
    # video_url = input("Enter the URL of the YouTube video: ")
    video_url='https://www.youtube.com/watch?v=qWdyhFiyH0Ya'
    output_folder = "img"  # Folder to save the extracted frames
    # interval = int(input("Enter the interval to extract frames (e.g., every 10 frames): "))
    interval=100

    extract_frames_from_video(video_url, output_folder, interval)
