import json
import os

from podloot import PodcastDownloader
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Download and manage podcast episodes from RSS feeds.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Download episodes from a file with multiple RSS feeds
    download_parser = subparsers.add_parser("download", help="Download podcast episodes from RSS feeds in a file.")
    download_parser.add_argument("feed_file", help="Path to the file containing RSS feeds, one per line.")
    download_parser.add_argument("destination", help="Destination directory for the downloaded podcasts.")

    # Download episodes from a single RSS feed
    single_download_parser = subparsers.add_parser("download_single", help="Download podcast episodes from a single RSS feed.")
    single_download_parser.add_argument("feed_url", help="URL of the RSS feed.")
    single_download_parser.add_argument("destination", help="Destination directory for the downloaded podcasts.")

    # Get information about a specific podcast
    info_parser = subparsers.add_parser("info", help="Get information about a specific podcast.")
    info_parser.add_argument("podcast_dir", help="Path to the directory containing the podcast JSON file.")
    info_parser.add_argument("audio_file", help="Audio file name, with or without extension, to get information about.")

    # Get the artwork URL for a podcast
    artwork_parser = subparsers.add_parser("artwork", help="Get the artwork URL for a podcast.")
    artwork_parser.add_argument("podcast_dir", help="Path to the directory containing the podcast JSON file.")

    # Check for duplicate episodes
    duplicates_parser = subparsers.add_parser("duplicates", help="Check for duplicate episodes in a podcast.")
    duplicates_parser.add_argument("podcast_dir", help="Path to the directory containing the podcast JSON file.")

    args = parser.parse_args()
    return args

def main():
    # Default Values if DEBUG env var is set
    args = argparse.Namespace()

    args.feed_file = "/Users/guvenc/podcast_downloads/feeds.txt"
    args.destination = "/Users/guvenc/podcast_downloads/"
    args.command = "download"

    if not os.environ.get('DEBUG'):
        args = {}
        args = parse_arguments()

    if args.command == "download":
        with open(args.feed_file, "r") as f:
            for line in f:
                feed_url = line.strip()
                downloader = PodcastDownloader(feed_url, args.destination)
                downloader.download_all_episodes()
                downloader.print_stats()
    elif args.command == "download_single":
        downloader = PodcastDownloader(args.feed_url, args.destination)
        downloader.download_all_episodes()
        downloader.print_stats()
    elif args.command == "info":
        downloader = PodcastDownloader.from_directory(args.podcast_dir)
        info = downloader.get_episode_info_by_audio_file(args.audio_file)
        print(json.dumps(info, indent=4))
    elif args.command == "artwork":
        downloader = PodcastDownloader.from_directory(args.podcast_dir)
        artwork_url = downloader.get_podcast_artwork_url()
        print(artwork_url)
    elif args.command == "duplicates":
        downloader = PodcastDownloader.from_directory(args.podcast_dir)
        duplicates = downloader.check_for_duplicates()
        for duplicate_hash, episodes in duplicates.items():
            print(f"Duplicate hash: {duplicate_hash}")
            for episode in episodes:
                print(f"  {episode['title']} ({episode['audio_file']}) - {episode['audio_url']}")

if __name__ == "__main__":
    main()

