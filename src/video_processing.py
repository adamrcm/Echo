import cv2
import os


def extract_video_frames(video_path, max_frames=5):
    """
    Opens a video file and extracts a fixed number of frames uniformly
    distributed across the video duration.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found at {video_path}")

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps > 0 else 0

    # Calculate intervals to get evenly spaced frames
    interval = max(1, total_frames // max_frames)
    frames_data = []

    frame_idx = 0
    success = True
    while success:
        success, frame = cap.read()
        if not success:
            break

        if frame_idx % interval == 0 and len(frames_data) < max_frames:
            timestamp = frame_idx / fps
            # In a full vision-pipeline, you might save the image or convert to base64.
            # For our initial scaffolding, we track the metadata.
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


# Quick local test
if __name__ == "__main__":
    # replace with a path to a test video later
    print("Video processing module ready.")