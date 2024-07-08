#!/usr/bin/env python3
import argparse
import os
from pydub import AudioSegment
from src.utils import load_timestamps, split_audio, repeat_chunks, repeat_chunks_to_min_time, generate_transition_chunks, generate_transition_chunks_to_min_time, save_audio, create_video, validate_args

def process_audio(args):
    timestamps = load_timestamps(args.timestamps_file)
    audio = AudioSegment.from_file(args.audio_file)
    
    # Add start and end time to timestamps
    timestamps = [0] + timestamps + [len(audio) / 1000]
    chunks = split_audio(args.audio_file, timestamps)
    
    if args.mode == 1:
        if args.repeat_count is not None:
            processed_chunks = repeat_chunks(chunks, args.repeat_count)
        else:
            processed_chunks = repeat_chunks_to_min_time(chunks, args.min_time)
    elif args.mode == 2:
        if args.repeat_count is not None:
            processed_chunks = generate_transition_chunks(chunks, args.repeat_count)
        else:
            processed_chunks = generate_transition_chunks_to_min_time(chunks, args.min_time)

    save_audio(processed_chunks, args.audio_output_file)

def get_resolution_short_hand(resolution):
    if resolution == 'native':
        return '_native'
    if resolution == '1920x1080':
        return '1080p'
    if resolution == '1280x720':
        return '720p'
    if resolution == '3840x2160':
        return '4k'
    return resolution.replace('x', 'x')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate shadowing practice tracks and create a video.')
    
    # Audio creation arguments
    parser.add_argument('audio_file', type=str, nargs='?', help='Path to the input audio file')
    parser.add_argument('timestamps_file', type=str, help='Path to the file with timestamps')
    parser.add_argument('--audio_output_file', type=str, help='Path to save the output audio file')
    parser.add_argument('--repeat_count', type=int, help='Number of repetitions for each chunk')
    parser.add_argument('--min_time', type=int, help='Minimum time (in seconds) for each chunk')
    parser.add_argument('--mode', type=int, choices=[1, 2], default=1, help='1: Repeat each split, 2: Repeat split pairs')

    # Video creation arguments
    parser.add_argument('image_path', type=str, help='Path to the input image file')
    parser.add_argument('--video_output_file', type=str, help='Path to the output video file')
    parser.add_argument('--resolution', type=str, default='1280x720', help='Desired video resolution in the format WIDTHxHEIGHT (e.g., 1920x1080 for 1080p) or "native" to use the native image resolution (default: 1280x720)')

    return parser.parse_args()

def set_default_output_files(args):
    # Determine default audio output file name
    if args.audio_output_file is None:
        if args.mode == 1:
            args.audio_output_file = 'single.mp3'
        else:
            args.audio_output_file = 'pairs.mp3'

    # Determine default video output file name
    resolution_short_hand = get_resolution_short_hand(args.resolution)
    if args.video_output_file is None:
        if args.mode == 1:
            args.video_output_file = f'single{resolution_short_hand}.mp4'
        else:
            args.video_output_file = f'pairs{resolution_short_hand}.mp4'

def main():
    args = parse_arguments()
    validate_args(args)
    set_default_output_files(args)
    
    # Process audio if input audio file is provided or default audio file does not exist
    if not os.path.exists(args.audio_output_file):
        if args.audio_file is None:
            raise ValueError("Input audio file must be provided or output audio file must exist.")
        process_audio(args)
    else:
        print(f"Skipping audio processing because {args.audio_output_file} already exists.")

    # Create video
    create_video(args.image_path, args.audio_output_file, args.video_output_file, args.resolution)

if __name__ == '__main__':
    main()
