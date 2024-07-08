#!/usr/bin/env python3
import argparse
from src.utils import create_video

def main():
    parser = argparse.ArgumentParser(description="Create a video from an audio clip and a single image.")
    parser.add_argument('image_path', type=str, help='Path to the input image file')
    parser.add_argument('audio_path', type=str, help='Path to the input audio file')
    parser.add_argument('output_path', type=str, help='Path to the output video file')
    parser.add_argument('--resolution', type=str, default='1280x720', help='Desired video resolution in the format WIDTHxHEIGHT (e.g., 1920x1080 for 1080p) or "native" to use the native image resolution (default: 1280x720)')

    args = parser.parse_args()

    create_video(args.image_path, args.audio_path, args.output_path, args.resolution)

if __name__ == "__main__":
    main()
