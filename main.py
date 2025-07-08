import pygame
import os

class MusicPlayer:
    def __init__(self):
        try:
            pygame.mixer.init()
            print("Audio mixer initialized successfully.")
        except pygame.error as e:
            print(f"Warning: Could not initialize audio mixer: {e}")
            print("Playback will not work, but playlist management is available.")
        self.playlist = []
        self.current_song_index = -1
        self.playing = False

    def add_song(self, song_path):
        """Adds a song to the playlist."""
        if os.path.exists(song_path) and song_path.lower().endswith((".mp3", ".ogg", ".wav")): # Added ogg and wav
            self.playlist.append(song_path)
            # print(f"Added: {os.path.basename(song_path)}") # Quieter adding
        else:
            print(f"Invalid song path or format, or file does not exist: {song_path}")

    def load_songs_from_directory(self, directory="songs/"):
        """Loads all supported audio files from a directory into the playlist."""
        if not os.path.isdir(directory):
            print(f"Directory not found: {directory}")
            return
        count = 0
        for filename in os.listdir(directory):
            if filename.lower().endswith((".mp3", ".ogg", ".wav")):
                self.add_song(os.path.join(directory, filename))
                count += 1
        if count > 0:
            print(f"Loaded {count} songs from '{directory}'.")
        else:
            print(f"No supported audio files found in '{directory}'.")


    def load_song(self, song_path):
        """Loads a song into the music player."""
        try:
            pygame.mixer.music.load(song_path)
            print(f"Loaded: {os.path.basename(song_path)}")
        except pygame.error as e:
            print(f"Error loading song {os.path.basename(song_path)}: {e}")

    def play_song(self):
        """Plays the currently loaded song."""
        if not self.playlist:
            print("Playlist is empty. Add songs first.")
            return

        if self.current_song_index == -1 and self.playlist:
            self.current_song_index = 0 # Start with the first song if nothing was selected

        if 0 <= self.current_song_index < len(self.playlist):
            song_to_play = self.playlist[self.current_song_index]
            self.load_song(song_to_play)
            if pygame.mixer.music.get_busy(): # Stop previous before loading new if needed
                pygame.mixer.music.stop()
            pygame.mixer.music.play()
            self.playing = True
            print(f"Playing: {os.path.basename(song_to_play)} ({self.current_song_index + 1}/{len(self.playlist)})")
        elif not self.playlist:
            print("Playlist is empty. Cannot play.")
        else:
            print("Invalid song index or playlist issue.")

    def play_next(self):
        """Plays the next song in the playlist."""
        if not self.playlist:
            print("Playlist is empty.")
            return
        if self.current_song_index < len(self.playlist) - 1:
            self.current_song_index += 1
        else:
            self.current_song_index = 0 # Loop back to the first song
        self.play_song()

    def play_previous(self):
        """Plays the previous song in the playlist."""
        if not self.playlist:
            print("Playlist is empty.")
            return
        if self.current_song_index > 0:
            self.current_song_index -= 1
        else:
            self.current_song_index = len(self.playlist) - 1 # Loop back to the last song
        self.play_song()

    def pause_song(self):
        """Pauses the currently playing song."""
        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False
            print("Song paused.")

    def unpause_song(self):
        """Unpauses the song."""
        if not self.playing and pygame.mixer.music.get_busy(): # Check if music was playing before pause
             # This logic is a bit tricky, get_busy might not be enough
             # For now, we assume if not self.playing and mixer is busy, it was paused.
            pygame.mixer.music.unpause()
            self.playing = True
            print("Song unpaused.")
        elif not pygame.mixer.music.get_busy():
            print("No song is currently loaded or playing (to unpause).")


    def stop_song(self):
        """Stops the currently playing song."""
        pygame.mixer.music.stop()
        self.playing = False
        # Do not reset current_song_index here, so play can resume from the same spot or next
        print("Song stopped.")

    def get_current_song_name(self):
        """Returns the name of the currently loaded or playing song."""
        if 0 <= self.current_song_index < len(self.playlist):
            return os.path.basename(self.playlist[self.current_song_index])
        return "None"

# Main application file for the MP3 player
if __name__ == "__main__":
    player = MusicPlayer()
    player.load_songs_from_directory() # Load songs automatically

    if not player.playlist:
        print("No songs found in the 'songs' directory. Please add some MP3, OGG, or WAV files.")
    else:
        # Basic command-line interface
        print("\n--- Music Player Controls ---")
        print("p: Play/Resume | s: Stop | pause: Pause | n: Next | prev: Previous | q: Quit")
        print("---------------------------")

        player.play_song() # Start playing the first song

        while True:
            if player.playlist and not pygame.mixer.music.get_busy() and player.playing:
                # Auto-play next song if the current one finishes
                print(f"Song '{player.get_current_song_name()}' finished.")
                player.play_next()

            command = input(f"Current: {player.get_current_song_name()} > ").strip().lower()

            if command == 'p':
                if not player.playing and player.playlist:
                    if pygame.mixer.music.get_pos() > 0 : # Paused state
                        player.unpause_song()
                    else: # Stopped or new song
                        player.play_song()
                elif not player.playlist:
                    print("Playlist is empty. Load songs first.")
            elif command == 's':
                player.stop_song()
            elif command == 'pause':
                player.pause_song()
            elif command == 'n':
                player.play_next()
            elif command == 'prev':
                player.play_previous()
            elif command == 'q':
                player.stop_song()
                pygame.quit()
                print("Exiting player.")
                break
            else:
                print("Invalid command.")
