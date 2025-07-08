import os
import googleapiclient.discovery
import googleapiclient.errors
import yt_dlp # Added import for yt-dlp
import shutil # For checking ffmpeg

# --- Configuration ---
YOUTUBE_API_KEY = "AIzaSyBClNYx_xNw9EHVEQQO029T-DUgR2dZ00g" # HARDCODED API KEY
OUTPUT_DIR = "downloaded_songs/" # Make sure this directory exists or is created

def check_ffmpeg():
    """Checks if ffmpeg is installed and in PATH."""
    return shutil.which("ffmpeg") is not None

def download_audio_as_mp3(video_id, output_path):
    """
    Downloads audio from a YouTube video ID as an MP3 file.

    Args:
        video_id: The YouTube video ID.
        output_path: The path (directory + filename) to save the MP3.

    Returns:
        True if download and conversion were successful, False otherwise.
    """
    if not check_ffmpeg(): # Restoring the ffmpeg check
        print("Error: ffmpeg not found. ffmpeg is required to convert audio to MP3.")
        print("Please install ffmpeg and ensure it's in your system's PATH.")
        return False

    video_url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path.replace('.mp3', '.%(ext)s'), # Let yt-dlp determine temp extension
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', # Standard MP3 quality
        }],
        'noplaylist': True, # Ensure only single video is downloaded
        'quiet': False, # Set to True for less output
        'progress': True,
    }

    try:
        print(f"\nDownloading and converting audio for video ID: {video_id}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([video_url])
            if error_code == 0:
                # Ensure the file is named correctly as .mp3 if yt-dlp didn't rename it perfectly
                # (e.g. if original was .webm, postprocessor should make it .mp3)
                # yt-dlp usually handles this with outtmpl and postprocessor.
                # We just need to ensure the final path ends with .mp3 for consistency.
                base_output_path = output_path.rsplit('.', 1)[0]
                final_mp3_path = base_output_path + ".mp3"
                if not os.path.exists(final_mp3_path) and os.path.exists(output_path.replace('.mp3', '.temp')): # Example if temp existed
                     # This part might need refinement based on how yt-dlp names intermediate files
                     pass # Assuming yt-dlp handles the final rename to .mp3 correctly with the options above.
                print(f"Successfully downloaded and converted to: {final_mp3_path}")
                return True
            else:
                print(f"yt-dlp encountered an error (code: {error_code}).")
                return False
    except Exception as e:
        print(f"An error occurred during download/conversion: {e}")
        return False

def search_youtube_videos(api_key, query, max_results=5):
    """
    Searches YouTube for videos based on a query.

    Args:
        api_key: Your YouTube Data API v3 key.
        query: The search term.
        max_results: The maximum number of results to return.

    Returns:
        A list of dictionaries, where each dictionary contains
        'title' and 'videoId' of a search result, or None if an error occurs.
    """
    if not api_key:
        print("Error: YouTube API key is not set. Please set the YOUTUBE_API_KEY environment variable.")
        return None

    try:
        youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=api_key)

        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=max_results
        )
        response = request.execute()

        videos = []
        for item in response.get("items", []):
            videos.append({
                "title": item["snippet"]["title"],
                "videoId": item["id"]["videoId"]
            })
        return videos

    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        if e.resp.status == 403:
            print("This might be due to an invalid API key or exceeded quota.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    # Check for ffmpeg presence early
    ffmpeg_present = check_ffmpeg()
    print(f"DEBUG: ffmpeg found during this run? {ffmpeg_present}") # Re-add debug for this test

    if not YOUTUBE_API_KEY:
        print("\nError: YOUTUBE_API_KEY environment variable not set.")
        print("Please set it to your YouTube Data API v3 key to use this script.")
        print("You can get an API key from the Google Cloud Console: https://console.cloud.google.com/apis/credentials")
        if not ffmpeg_present:
            print("Additionally, ffmpeg was not found. Please install it and ensure it's in your PATH for MP3 conversion.")
    else:
        print("YouTube Downloader Initialized.")
        if not ffmpeg_present:
            print("Warning: ffmpeg not found. MP3 conversion will fail. Please install ffmpeg.")

        # Example Search:
        search_term = input("Enter song name or search query: ") # Restored interactive input
        if search_term:
            results = search_youtube_videos(YOUTUBE_API_KEY, search_term)
            if results:
                print("\n--- Search Results ---")
                for i, video in enumerate(results):
                    print(f"{i+1}. {video['title']}")
                print("----------------------")

                while True: # Restored interactive selection loop
                    try:
                        choice = input("Enter the number of the video to download (or 0 to cancel): ")
                        choice_num = int(choice)
                        if 0 <= choice_num <= len(results):
                            break
                        else:
                            print(f"Invalid choice. Please enter a number between 0 and {len(results)}.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")

                if choice_num > 0: # Ensure results exist before indexing (already handled by loop condition)
                    selected_video = results[choice_num - 1]
                    video_title = selected_video['title']
                    video_id = selected_video['videoId']
                    print(f"\nYou selected: {video_title} (ID: {video_id})")

                    # Sanitize filename
                    safe_filename = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in video_title).rstrip()
                    safe_filename = safe_filename.replace(' ', '_') # Replace spaces with underscores
                    if not safe_filename: # Handle cases where title had no valid chars
                        safe_filename = video_id
                    mp3_filename = f"{safe_filename}.mp3"

                    # Create output directory if it doesn't exist
                    if not os.path.exists(OUTPUT_DIR):
                        os.makedirs(OUTPUT_DIR)
                        print(f"Created output directory: {OUTPUT_DIR}")

                    output_file_path = os.path.join(OUTPUT_DIR, mp3_filename)

                    download_audio_as_mp3(video_id, output_file_path)
                else:
                    print("Download cancelled.")

            elif results == []:
                print("No videos found for your query.")
            # If results is None, an error message was already printed by search_youtube_videos
        # Next steps: download using yt-dlp
        pass
