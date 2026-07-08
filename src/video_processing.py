import cv2
import os


def extract_video_frames(video_path, max_frames=5):
    """
    Opens a video file, extracts metadata, and saves a reference frame
    to disk for vision analysis.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found at {video_path}")

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps > 0 else 0

    # Choose a target frame right in the middle of the video to use as our visual summary
    middle_frame_target = total_frames // 2
    saved_frame_path = os.path.join(os.path.dirname(video_path), "frame.jpg")

    interval = max(1, total_frames // max_frames)
    frames_data = []

    frame_idx = 0
    success = True
    while success:
        success, frame = cap.read()
        if not success:
            break

        # Save the physical frame when we hit the midpoint of the video
        if frame_idx == middle_frame_target:
            cv2.imwrite(saved_frame_path, frame)

        if frame_idx % interval == 0 and len(frames_data) < max_frames:
            timestamp = frame_idx / fps
            frames_data.append({
                "frame_index": frame_idx,
                "timestamp_seconds": round(timestamp, 2)
            })
        frame_idx += 1

    cap.release()
    return {
        "duration_seconds": round(duration, 2),
        "total_frames": total_frames,
        "extracted_frames": frames_data
    }


if __name__ == "__main__":
    print("Video processing module ready.")