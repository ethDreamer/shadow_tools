#!/usr/bin/env python3
import argparse
from src.utils import load_timestamps, split_audio, repeat_chunks, repeat_chunks_to_min_time, generate_transition_chunks, generate_transition_chunks_to_min_time, save_audio, validate_args

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

    save_audio(processed_chunks, args.output_file)

def main():
    parser = argparse.ArgumentParser(description='Generate shadowing practice tracks.')
    parser.add_argument('audio_file', type=str, help='Path to the input audio file')
    parser.add_argument('timestamps_file', type=str, help='Path to the file with timestamps')
    parser.add_argument('output_file', type=str, help='Path to save the output audio file')
    parser.add_argument('--repeat_count', type=int, help='Number of repetitions for each chunk')
    parser.add_argument('--min_time', type=int, help='Minimum time (in seconds) for each chunk')
    parser.add_argument('--mode', type=int, choices=[1, 2], default=1, help='1: Repeat each sentence, 2: Repeat sentence pairs')

    args = parser.parse_args()
    validate_args(args)
    process_audio(args)

if __name__ == '__main__':
    main()
