#!/usr/bin/env python3

def load_timestamps(file_path):
    with open(file_path, 'r') as file:
        timestamps = [float(line.split()[0]) for line in file]
    return timestamps

def split_audio(audio_file, timestamps):
    from pydub import AudioSegment
    audio = AudioSegment.from_file(audio_file)
    chunks = [audio[timestamps[i]*1000:timestamps[i+1]*1000] for i in range(len(timestamps) - 1)]
    return chunks

def repeat_chunks(chunks, repeat_count):
    return [chunk * repeat_count for chunk in chunks]

def repeat_chunks_to_min_time(chunks, min_time):
    min_time_ms = min_time * 1000
    repeated_chunks = []
    for chunk in chunks:
        repeat_count = (min_time_ms // len(chunk)) + 1
        repeated_chunks.append(chunk * repeat_count)
    return repeated_chunks

def generate_transition_chunks(chunks, repeat_count):
    transition_chunks = [chunks[i] + chunks[i+1] for i in range(len(chunks) - 1)]
    return [chunk * repeat_count for chunk in transition_chunks]

def generate_transition_chunks_to_min_time(chunks, min_time):
    min_time_ms = min_time * 1000
    transition_chunks = [chunks[i] + chunks[i+1] for i in range(len(chunks) - 1)]
    repeated_transitions = []
    for chunk in transition_chunks:
        repeat_count = (min_time_ms // len(chunk)) + 1
        repeated_transitions.append(chunk * repeat_count)
    return repeated_transitions

def save_audio(chunks, output_file):
    combined = sum(chunks)
    combined.export(output_file, format='mp3')

def validate_args(args):
    if args.repeat_count is not None and args.min_time is not None:
        raise ValueError("You must specify either repeat_count or min_time, not both.")
    if args.repeat_count is None and args.min_time is None:
        raise ValueError("You must specify one of repeat_count or min_time.")

# Video-related functions
def create_video(image_path, audio_path, output_path, resolution):
    import ffmpeg  # Conditional import
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
