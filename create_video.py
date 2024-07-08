#!/usr/bin/env python3
import argparse
import ffmpeg

def create_video(image_path, audio_path, output_path, resolution):
    # Probe the audio file to get its duration
    audio_info = ffmpeg.probe(audio_path)
    audio_duration = audio_info['format']['duration']
    
    # Create the FFmpeg input streams
    image_input = ffmpeg.input(image_path, loop=1, t=audio_duration)
    audio_input = ffmpeg.input(audio_path)
    
    # Define the scaling filter based on the resolution
    if resolution == 'native':
        video_stream = image_input
    else:
        width, height = resolution.split('x')
        video_stream = image_input.filter('scale', width, height)
    
    # Construct the FFmpeg command with scaling if needed
    (
        ffmpeg
        .output(video_stream, audio_input, output_path,
                vcodec='libx264',  # Use H.264 video codec
                tune='stillimage',  # Optimize for still images
                acodec='aac',  # Use AAC audio codec
                audio_bitrate='128k',  # Set audio bitrate to 128kbps
                pix_fmt='yuv420p',  # Set pixel format to YUV 4:2:0
                shortest=None)  # Ensure the video is as long as the shortest input (audio in this case)
        .run()
    )

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

