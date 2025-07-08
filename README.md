# YouTube Audio Downloader

This script allows you to search for videos on YouTube and download their audio as MP3 files.

## Features

- Search YouTube for videos by title or keywords.
- Select a video from the search results.
- Download the audio of the selected video and convert it to MP3 format.
- Saves downloaded files to a `downloaded_songs/` directory.

## Setup and Dependencies

1.  **Python 3:** Ensure you have Python 3 installed.
2.  **API Key (Currently Hardcoded - Security Warning!):**
    *   The script currently has a YouTube Data API v3 key hardcoded directly into `youtube_downloader.py`.
    *   **IMPORTANT:** This is a significant security risk. It is strongly recommended to remove the hardcoded key and use an environment variable instead.
    *   To get your own key:
        *   Go to the [Google Cloud Console](https://console.cloud.google.com/).
        *   Create a new project or select an existing one.
        *   Enable the "YouTube Data API v3" for your project.
        *   Go to "Credentials" and create an "API key".
    *   **Recommended Secure Usage (modify the script):**
        *   Remove the line `YOUTUBE_API_KEY = "YOUR_HARDCODED_KEY"`
        *   Uncomment/restore the line `YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")`
        *   Then, before running the script, set the environment variable:
            ```bash
            export YOUTUBE_API_KEY="YOUR_ACTUAL_API_KEY"
            ```
            (For Windows PowerShell: `$env:YOUTUBE_API_KEY="YOUR_ACTUAL_API_KEY"`)

3.  **Python Libraries:** Install the required Python libraries using pip:
    ```bash
    pip install yt-dlp google-api-python-client
    ```
4.  **ffmpeg:** `ffmpeg` is required for converting the downloaded audio to MP3.
    *   You need to install `ffmpeg` on your system and ensure it is available in your system's PATH.
    *   **Linux (Debian/Ubuntu):** `sudo apt-get update && sudo apt-get install ffmpeg`
    *   **macOS (using Homebrew):** `brew install ffmpeg`
    *   **Windows:** Download `ffmpeg` from the [official website](https://ffmpeg.org/download.html), extract it, and add the `bin` directory (containing `ffmpeg.exe`) to your system's PATH environment variable.

## Running the Script

1.  **Navigate to the script's directory:**
    ```bash
    cd path/to/script_directory
    ```
2.  **Run the script:**
    ```bash
    python youtube_downloader.py
    ```
3.  **Follow the prompts:**
    *   Enter your search query (e.g., song name).
    *   A list of search results will be displayed.
    *   Enter the number corresponding to the video you want to download.
    *   The script will then attempt to download and convert the audio to MP3 in the `downloaded_songs/` directory.

## Output

Downloaded MP3 files will be saved in a directory named `downloaded_songs/` created in the same location as the script. Filenames are generated based on the video title, with special characters sanitized.

## Important Considerations

*   **YouTube's Terms of Service:** Be mindful of YouTube's terms of service regarding downloading content. Only download content for which you have permission or which is explicitly offered for download.
*   **API Key Security:** As mentioned, hardcoding API keys is risky. Protect your API key. If exposed, regenerate it immediately.
*   **Download Reliability:** `yt-dlp`'s ability to download from YouTube can sometimes be affected by changes YouTube makes to its platform or by network restrictions. If you encounter consistent "403 Forbidden" errors, it might be due to YouTube blocking requests from your IP address or network environment.
*   **ffmpeg Path:** If the script reports `ffmpeg not found` even after installation, ensure its installation directory is correctly added to your system's PATH.
