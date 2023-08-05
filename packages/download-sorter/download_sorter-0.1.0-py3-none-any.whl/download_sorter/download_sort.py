import os
import json
import shutil
import time

class DownloadSorter:
    """
    A class to sort files in a directory based on their file extensions.
    """

    def __init__(self, downloads_path, destination_base="~", config_file="sort.json"):
        """
        Initialize the DownloadSorter object.

        :param downloads_path: The path to the directory containing the files to be sorted.
        :param config_file: The path to the JSON file containing the folder-to-extension mappings.
        """
        self.destination_base = os.path.expanduser(destination_base)
        self.downloads_path = downloads_path
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        """
        Load the configuration from the JSON file, reverse the folder-to-extension mappings, and store it in the config attribute.
        """
        with open(self.config_file, "r") as f:
            folder_to_ext = json.load(f)
            self.config = {ext: folder for folder, exts in folder_to_ext.items() for ext in exts}

    def move_file(self, file, _destination_folder):
        """
        Move a file to the specified destination folder.
        If a file with the same name exists in the destination folder, append the current Unix timestamp to the file name to avoid conflicts.

        :param file: The path to the file to be moved.
        :param destination_folder: The path to the destination folder.
        """
        destination_folder = os.path.join(self.destination_base, destination_folder)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        file_name, file_ext = os.path.splitext(os.path.basename(file))
        destination_base = os.path.join(destination_folder, file_name + file_ext)

        if os.path.exists(destination_base):
            timestamp = int(time.time())
            new_file_name = f"{file_name}_{timestamp}{file_ext}"
            destination_base = os.path.join(destination_folder, new_file_name)

        shutil.move(file, destination_base)

    def sort_downloads(self):
        """
        Sort the files in the downloads_path directory based on the extension-to-folder mappings in the config attribute.
        This method only processes files directly in the downloads_path and does not search subdirectories.
        """
        # Iterate through the contents of the downloads_path directory
        for file in os.listdir(self.downloads_path):
            # Construct the full path of the item
            file_path = os.path.join(self.downloads_path, file)

            # Check if the item is a file (skip directories)
            if os.path.isfile(file_path):
                # Extract the file extension, converting it to lowercase for consistency
                file_ext = os.path.splitext(file)[-1].lower()

                # If the file extension is in the config, move the file to the corresponding folder
                if file_ext in self.config:
                    # Determine the destination folder based on the config
                    destination_folder = os.path.join(self.downloads_path, self.config[file_ext])

                    # Move the file to the destination folder, avoiding naming conflicts
                    self.move_file(file_path, destination_folder)


if __name__ == "__main__":
    downloads_path = os.path.expanduser("~/Downloads" if os.name == 'nt' else "~/downloads")
    destination_base = "~" # Destinations will be relative to this directory
    sorter = DownloadSorter(downloads_path, destination_base=destination_base)
    sorter.sort_downloads()
