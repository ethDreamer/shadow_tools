
# Shadowing Practice Scripts

These scripts help you create audio and video samples for language shadowing practice. Shadowing is a technique where you listen to audio and repeat it immediately to improve your language skills.

## Requirements

- **Python**: [Download and install Python](https://www.python.org/downloads/).
- **FFmpeg** (optional, required only for video creation): [Download and install FFmpeg](https://ffmpeg.org/download.html).

## Setup

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Set up a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

Note: If you want to create videos, you need to install FFmpeg. Follow the [FFmpeg installation instructions](https://ffmpeg.org/download.html).

## Basic Usage

### Create Audio Samples

To create audio samples for shadowing practice, use the `audio_creation.py` script.

    ```sh
    python audio_creation.py <audio_file> <timestamps_file> <output_file> --repeat_count <count> --min_time <seconds> --mode <1|2>
    ```

- `audio_file`: Path to the input audio file.
- `timestamps_file`: Path to the file with timestamps.
- `output_file`: Path to save the output audio file.
- `--repeat_count <count>`: Number of repetitions for each chunk (optional, specify either this or `--min_time`).
- `--min_time <seconds>`: Minimum time (in seconds) for each chunk (optional, specify either this or `--repeat_count`).
- `--mode <1|2>`: Mode for repeating (1 for each sentence, 2 for sentence pairs).

### Create Video Samples

To create a video sample from an audio clip and a single image, use the `video_creation.py` script.

    ```sh
    python video_creation.py <image_path> <audio_path> <output_path> --resolution <resolution>
    ```

- `image_path`: Path to the input image file.
- `audio_path`: Path to the input audio file.
- `output_path`: Path to the output video file.
- `--resolution <resolution>`: Desired video resolution (e.g., `1920x1080`, `1280x720`, or `native`).

### Create Both Audio and Video Samples

To create both audio and video samples, use the `shadow.py` script.

    ```sh
    python shadow.py <audio_file> <timestamps_file> <image_path> --audio_output_file <audio_output_file> --video_output_file <video_output_file> --repeat_count <count> --min_time <seconds> --mode <1|2> --resolution <resolution>
    ```

- `audio_file`: Path to the input audio file (optional if output audio file already exists).
- `timestamps_file`: Path to the file with timestamps.
- `image_path`: Path to the input image file.
- `--audio_output_file <audio_output_file>`: Path to save the output audio file (default: `single.mp3` or `pairs.mp3`).
- `--video_output_file <video_output_file>`: Path to save the output video file (default: `single<resolution>.mp4` or `pairs<resolution>.mp4`).
- `--repeat_count <count>`: Number of repetitions for each chunk (optional, specify either this or `--min_time`).
- `--min_time <seconds>`: Minimum time (in seconds) for each chunk (optional, specify either this or `--repeat_count`).
- `--mode <1|2>`: Mode for repeating (1 for each sentence, 2 for sentence pairs).
- `--resolution <resolution>`: Desired video resolution (e.g., `1920x1080`, `1280x720`, or `native`).

## Notes

- **FFmpeg Installation**: If you want to create videos, you need to install FFmpeg. Follow the [FFmpeg installation instructions](https://ffmpeg.org/download.html).
- **Dependencies**: The scripts are designed to conditionally import FFmpeg only if video creation is required, so you don't need to install FFmpeg if you only want to use the `audio_creation.py` script.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
