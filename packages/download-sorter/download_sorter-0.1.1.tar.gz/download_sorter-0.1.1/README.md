# DownloadSorter

DownloadSorter is a Python module that organizes the files in your Downloads folder based on their file extensions. The module moves files into predefined folders according to a configuration file, making it easier to find and manage your downloaded files.

## Features

- Organizes files directly in the Downloads folder (non-recursive)
- Customizable folder organization using a JSON configuration file
- Automatically appends Unix timestamps to filenames to avoid conflicts
- Cross-platform compatibility

## Getting Started

### Prerequisites

- Python 3.x
- JSON configuration file (default: `sort.json`)

### Installation

1. Clone the repository or download the `sort_downloads.py` file.
2. Create a JSON configuration file, if not using the provided `sort.json`.

### Configuration

The `sort.json` file defines the folder organization for different file extensions. The structure of the JSON file is as follows:

```json
{
    "DestinationFolder1": ["ext1", "ext2"],
    "DestinationFolder2": ["ext3", "ext4"]
}
```

For example, to organize music into the "Music" folder and image files into the "Pictures" folder, the `sort.json` file should look like this:

```json
{
    "Music": [
        ".mp3",
        ".wma",
        ".ogg",
        ".wav"
    ],
    "Pictures": [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webm",
        ".bmp"
    ]
}
```

### Usage

To use the DownloadSorter, simply run the `sort_downloads.py` script:

```sh
python sort_downloads.py
```

By default, the script will organize files in the `~/Downloads` directory if you're using Windows, or `~/downloads` for non-Windows users. You can modify the `downloads_path` variable in the script to point to a different directory if needed, or pass the directory path as a command line argument when running `sort_downloads.py`.

## Customization

If you want to customize DownloadSorter, you can modify the `sort_downloads.py` script:

- Change the `config_file` parameter in the `DownloadSorter` constructor to use a different JSON configuration file.
- Update the `downloads_path` variable in the `__main__` block to use a different directory for sorting files, or pass the directory path as a command line argument when running `sort_downloads.py`.

## Contributing

Contributions are welcome! If you have any ideas, feature requests, or bug reports, feel free to submit an issue or create a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.