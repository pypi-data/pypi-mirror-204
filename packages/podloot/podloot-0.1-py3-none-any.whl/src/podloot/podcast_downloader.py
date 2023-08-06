import hashlib
import os
import json
import ssl
import string
import urllib.request
from datetime import datetime
import time

import requests
import podcastparser
from tqdm import tqdm

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def make_fs_safe(input_string):
    safe_characters = set(string.ascii_letters + string.digits + "._-")
    fs_safe_string = "".join(c if c in safe_characters else "_" for c in input_string)
    return fs_safe_string.strip()


class PodcastDownloader:
    def __init__(self, feed_url, destination_path):
        self.feed_url = feed_url
        self.destination_path = destination_path

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        response = requests.get(feed_url, verify=False)
        self.feed_data = podcastparser.parse(feed_url, urllib.request.urlopen(feed_url, context=context))

        self.podcast_title = self.feed_data["title"]
        self.podcast_title_safe = make_fs_safe(self.podcast_title)

        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        self.podcast_directory = os.path.join(destination_path, self.podcast_title_safe)

        if not os.path.exists(self.podcast_directory):
            os.makedirs(self.podcast_directory)

        self.podcast_data_file = os.path.join(self.podcast_directory, "podcast_data.json")

    def _download_audio_file(self, audio_url, episode_title_safe):
        max_retries = 3
        retry_count = 0
        success = False

        while not success and retry_count < max_retries:
            try:
                with requests.get(audio_url, stream=True, verify=False) as response:
                    if response.status_code != 200:
                        print(f"Error downloading {episode_title_safe}: Status code {response.status_code}")
                        break

                    audio_file = os.path.join(self.podcast_directory, f"{episode_title_safe}.mp3")
                    total_size = int(response.headers.get('content-length', 0))
                    block_size = 8192
                    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
                    with open(audio_file, "wb") as f:
                        for chunk in response.iter_content(chunk_size=block_size):
                            if chunk:
                                f.write(chunk)
                                progress_bar.update(len(chunk))

                    progress_bar.close()
                    success = True

                    # Calculate and update the hash info for the downloaded file
                    file_hash = self.calculate_file_hash(audio_file)
                    self._update_hash_info(episode_title_safe, file_hash)

            except Exception as e:
                print(f"Error downloading {episode_title_safe}: {e}")
                retry_count += 1
                time.sleep(5)

        return success

    def _initialize_podcast_data(self):
        podcast_data = {}
        for episode in self.feed_data["episodes"]:
            episode_title = episode["title"]
            episode_title_safe = make_fs_safe(episode_title)

            episode_data = {
                "episode_info": episode,
                "downloaded": False,
                "download_date": None,
                "download_problem": False
            }

            podcast_data[episode_title_safe] = episode_data

        return podcast_data

    # def _initialize_podcast_data(self):
    #     general_info = {
    #         "title": self.title,
    #         "description": self.description,
    #         "category": self.category,
    #     }
    #
    #     podcast_data = {}
    #     for episode in self.feed_data["episodes"]:
    #         episode_title = episode["title"]
    #         episode_title_safe = make_fs_safe(episode_title)
    #
    #         episode_data = {
    #             "episode_info": episode,
    #             "downloaded": False,
    #             "download_date": None,
    #             "download_problem": False
    #         }
    #
    #         podcast_data[episode_title_safe] = episode_data
    #
    #     return {"general": general_info, "episodes": podcast_data}

    # def _initialize_podcast_data(self):
    #     general_info = {
    #         "title": self.podcast.title,
    #         "description": self.podcast.description,
    #         "category": self.podcast.category,
    #     }
    #
    #     podcast_data = {}
    #     for episode in self.podcast.episodes:
    #         episode_title = episode.title
    #         episode_title_safe = make_fs_safe(episode_title)
    #
    #         episode_data = {
    #             "episode_info": episode.to_dict(),
    #             "downloaded": False,
    #             "download_date": None,
    #             "download_problem": False
    #         }
    #
    #         podcast_data[episode_title_safe] = episode_data
    #
    #     return {"general": general_info, "episodes": podcast_data}

    def _load_podcast_data(self):
        if os.path.exists(self.podcast_data_file):
            with open(self.podcast_data_file, "r") as f:
                podcast_data = json.load(f)
        else:
            podcast_data = self._initialize_podcast_data()
            with open(self.podcast_data_file, "w") as f:
                json.dump(podcast_data, f, indent=4)

        return podcast_data

    def _update_podcast_data(self, podcast_data):
        with open(self.podcast_data_file, "w") as f:
            json.dump(podcast_data, f, indent=4)

    def download_all_episodes(self):
        podcast_data = self._load_podcast_data()

        # Download episodes with a "downloaded" status of False
        for episode_title_safe, episode_data in podcast_data.items():
            if not episode_data["downloaded"]:
                print(f"Downloading {episode_title_safe}")

                audio_url = episode_data["episode_info"]["enclosures"][0]["url"]
                success = self._download_audio_file(audio_url, episode_title_safe)

                if success:
                    episode_data["downloaded"] = True
                    episode_data["download_date"] = datetime.now().isoformat()
                else:
                    episode_data["download_problem"] = True

                self._update_podcast_data(podcast_data)

        # Retry failed downloads
        for episode_title_safe, episode_data in podcast_data.items():
            if episode_data["download_problem"]:
                print(f"Retrying download of {episode_title_safe}")

                audio_url = episode_data["episode_info"]["enclosures"][0]["url"]
                success = self._download_audio_file(audio_url, episode_title_safe)

                if success:
                    episode_data["downloaded"] = True
                    episode_data["download_date"] = datetime.now().isoformat()
                    episode_data["download_problem"] = False

                self._update_podcast_data(podcast_data)

    def stats(self):
        podcast_data = self._load_podcast_data()
        downloaded_count = 0
        failed_count = 0
        total_duration = 0
        min_duration = float('inf')
        max_duration = 0
        first_episode_date = None
        last_episode_date = None

        for episode_title_safe, episode_data in podcast_data.items():
            if episode_data["downloaded"]:
                downloaded_count += 1
            else:
                failed_count += 1

            duration = int(episode_data["episode_info"]["duration"])
            total_duration += duration
            min_duration = min(min_duration, duration)
            max_duration = max(max_duration, duration)

            episode_date = datetime.strptime(episode_data["episode_info"]["published"], '%Y-%m-%dT%H:%M:%S%z')
            if first_episode_date is None or episode_date < first_episode_date:
                first_episode_date = episode_date
            if last_episode_date is None or episode_date > last_episode_date:
                last_episode_date = episode_date

        print(f"Total episodes: {downloaded_count + failed_count}")
        print(f"Downloaded episodes: {downloaded_count}")
        print(f"Failed downloads: {failed_count}")
        print(f"Total duration: {total_duration} seconds")
        print(f"Shortest episode: {min_duration} seconds")
        print(f"Longest episode: {max_duration} seconds")
        print(f"First episode date: {first_episode_date}")
        print(f"Last episode date: {last_episode_date}")

    def sort_episodes(self, sort_by="title", order="asc", only_downloaded=False):
        podcast_data = self._load_podcast_data()
        episodes = []

        for episode_title_safe, episode_data in podcast_data.items():
            if not only_downloaded or episode_data["downloaded"]:
                episodes.append((episode_title_safe, episode_data))

        if sort_by == "title":
            episodes.sort(key=lambda x: x[1]["episode_info"]["title"], reverse=(order == "desc"))
        elif sort_by == "date":
            episodes.sort(key=lambda x: x[1]["episode_info"]["published"], reverse=(order == "desc"))
        elif sort_by == "duration":
            episodes.sort(key=lambda x: int(x[1]["episode_info"]["duration"]), reverse=(order == "desc"))

        return episodes

    def get_audio_url_by_filename(self, filename):
        podcast_data = self._load_podcast_data()
        filename_without_extension = os.path.splitext(filename)[0]

        for episode_title_safe, episode_data in podcast_data.items():
            if episode_title_safe == filename_without_extension:
                return episode_data["episode_info"]["enclosures"][0]["url"]

        return None

    def get_podcast_artwork_url(self):
        podcast_data = self._load_podcast_data()
        episodes = self.sort_episodes(sort_by="date", order="desc")

        for episode_title_safe, episode_data in episodes:
            if "image" in episode_data["episode_info"]:
                return episode_data["episode_info"]["image"]["url"]

        return None

    def get_episode_info_by_filename(self, filename):
        podcast_data = self._load_podcast_data()
        filename_without_extension = os.path.splitext(filename)[0]

        for episode_title_safe, episode_data in podcast_data.items():
            if episode_title_safe == filename_without_extension:
                episode_info = episode_data["episode_info"]
                human_readable_duration = self._convert_duration_to_human_readable(int(episode_info["duration"]))
                human_readable_date = self._convert_timestamp_to_human_readable(episode_info["published"])

                return {
                    "title": episode_info["title"],
                    "duration": {
                        "human_readable": human_readable_duration,
                        "machine_readable": int(episode_info["duration"]),
                    },
                    "published": {
                        "human_readable": human_readable_date,
                        "machine_readable": episode_info["published"],
                    },
                    "description": episode_info["description"],
                    "artwork_url": episode_info["image"]["url"] if "image" in episode_info else None,
                    "audio_url": episode_info["enclosures"][0]["url"],
                    "authors": episode_info["authors"],
                    "link": episode_info["link"],
                }

        return None

    def calculate_file_hash(self, file_path):
        hash_algorithm = hashlib.sha256()
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_algorithm.update(chunk)
        return hash_algorithm.hexdigest()

    def _update_hash_info(self, episode_title_safe, file_hash):
        podcast_data = self._load_podcast_data()
        episode_data = podcast_data[episode_title_safe]
        episode_data["file_hash"] = file_hash
        self._save_podcast_data(podcast_data)

    def find_duplicate_hashes(self):
        podcast_data = self._load_podcast_data()
        hash_groups = {}

        for episode_title_safe, episode_data in podcast_data.items():
            if "file_hash" in episode_data:
                file_hash = episode_data["file_hash"]

                if file_hash not in hash_groups:
                    hash_groups[file_hash] = []

                hash_groups[file_hash].append({
                    "episode_name": episode_data["episode_info"]["title"],
                    "audio_url": episode_data["episode_info"]["enclosures"][0]["url"],
                    "file_name": episode_title_safe + ".mp3",
                })

        duplicates = {k: v for k, v in hash_groups.items() if len(v) > 1}

        for file_hash, episodes in duplicates.items():
            print(f"Duplicate hash: {file_hash}")
            for episode in episodes:
                print(f"{episode['episode_name']} - {episode['audio_url']} - {episode['file_name']}")
            print()

        return duplicates

    @staticmethod
    def _convert_duration_to_human_readable(duration_in_seconds):
        minutes, seconds = divmod(duration_in_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        duration_str = ""

        if hours > 0:
            duration_str += f"{hours} hour{'s' if hours > 1 else ''} "
            if minutes > 0:
                duration_str += f"{minutes} minute{'s' if minutes > 1 else ''} "
            if seconds > 0:
                duration_str += f"{seconds} second{'s' if seconds > 1 else ''}"

    @staticmethod
    def _convert_timestamp_to_human_readable(timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
