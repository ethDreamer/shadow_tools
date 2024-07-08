#!/usr/bin/env python3
import argparse
from pydub import AudioSegment

def load_timestamps(file_path):
    with open(file_path, 'r') as file:
        timestamps = [float(line.split()[0]) for line in file]
    return timestamps

def split_audio(audio_file, timestamps):
    audio = AudioSegment.from_file(audio_file)
    chunks = [audio[timestamps[i]*1000:timestamps[i+1]*1000] for i in range(len(timestamps) - 1)]
    return chunks

def repeat_chunks(chunks, repeat_count):
    repeated_chunks = [chunk * repeat_count for chunk in chunks]
    return repeated_chunks

def repeat_chunks_to_min_time(chunks, min_time):
    repeated_chunks = []
    min_time_ms = min_time * 1000
    for chunk in chunks:
        repeat_count = (min_time_ms // len(chunk)) + 1
        repeated_chunks.append(chunk * repeat_count)
    return repeated_chunks

def generate_transition_chunks(chunks, repeat_count):
    transition_chunks = [chunks[i] + chunks[i+1] for i in range(len(chunks) - 1)]
    repeated_transitions = [chunk * repeat_count for chunk in transition_chunks]
    return repeated_transitions

def generate_transition_chunks_to_min_time(chunks, min_time):
    transition_chunks = [chunks[i] + chunks[i+1] for i in range(len(chunks) - 1)]
    repeated_transitions = []
    min_time_ms = min_time * 1000
    for chunk in transition_chunks:
        repeat_count = (min_time_ms // len(chunk)) + 1
        repeated_transitions.append(chunk * repeat_count)
    return repeated_transitions

def save_audio(chunks, output_file):
    combined = sum(chunks)
    combined.export(output_file, format='mp3')

def main():
    parser = argparse.ArgumentParser(description='Generate shadowing practice tracks.')
    parser.add_argument('audio_file', type=str, help='Path to the input audio file')
    parser.add_argument('timestamps_file', type=str, help='Path to the file with timestamps')
    parser.add_argument('output_file', type=str, help='Path to save the output audio file')
    parser.add_argument('--repeat_count', type=int, help='Number of repetitions for each chunk')
    parser.add_argument('--min_time', type=int, help='Minimum time (in seconds) for each chunk')
    parser.add_argument('--mode', type=int, choices=[1, 2], default=1, help='1: Repeat each sentence, 2: Repeat sentence pairs')
    
    args = parser.parse_args()

    if args.repeat_count is not None and args.min_time is not None:
        raise ValueError("You must specify either repeat_count or min_time, not both.")
    
    timestamps = load_timestamps(args.timestamps_file)
    audio = AudioSegment.from_file(args.audio_file)
    
    # Add start and end time to timestamps
    timestamps = [0] + timestamps + [len(audio) / 1000]

    chunks = split_audio(args.audio_file, timestamps)
    
    if args.mode == 1:
        if args.repeat_count is not None:
            repeated_chunks = repeat_chunks(chunks, args.repeat_count)
        elif args.min_time is not None:
            repeated_chunks = repeat_chunks_to_min_time(chunks, args.min_time)
        save_audio(repeated_chunks, args.output_file)
    elif args.mode == 2:
        if args.repeat_count is not None:
            transition_chunks = generate_transition_chunks(chunks, args.repeat_count)
        elif args.min_time is not None:
            transition_chunks = generate_transition_chunks_to_min_time(chunks, args.min_time)
        save_audio(transition_chunks, args.output_file)

if __name__ == '__main__':
    main()

