# Podloot

Podloot is a podcast downloader and manager using RSS feeds. It provides a command-line interface for downloading and managing podcast episodes from RSS feeds.

## Features

- Download episodes from a single RSS feed or a file containing multiple feeds.
- Get information about a specific podcast episode.
- Get the artwork URL for a podcast.
- Check for duplicate episodes in a podcast.

## Installation

You can install Podloot using pip:

```bash
pip install git+https://github.com/gusanmaz/podloot.git
```

Usage

### Download episodes from a file with multiple RSS feeds

`podloot download <feed_file> <destination>`

### Download episodes from a single RSS feed

`podloot download_single <feed_url> <destination>`

### Get information about a specific podcast episode

`podloot info <podcast_dir> <audio_file>`

### Get the artwork URL for a podcast

`podloot artwork <podcast_dir>`

### Check for duplicate episodes in a podcast

`podloot duplicates <podcast_dir>`

## Contributing

Pull requests and bug reports are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT License](https://choosealicense.com/licenses/mit/)

``As for improvements to features and code, here are a few suggestions: 1. Add functionality to download only the latest episode or a specific number of latest episodes. 2. Allow users to limit the download of episodes based on a date range or the age of the episodes. 3. Implement automatic episode cleanup based on user-defined criteria, such as age or total storage space used. 4. Add support for downloading episodes in parallel to speed up the download process. 5. Implement a more interactive CLI using a library like `click` to provide a more user-friendly experience. Remember to thoroughly test any new features or code changes before committing them to the repository.``