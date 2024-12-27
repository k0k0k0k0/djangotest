import csv
import time
import os

from os.path import join, splitext
from collections import Counter
from datetime import datetime
#import researchers
from . import researchers

# A general-purpose decorator to measure and print the execution time of a function
def timeit(fun):
    """
    Decorator to measure the execution time of a function.

    Parameters:
        fun (function): The function to measure.

    Returns:
        function: A wrapper function that times the input function.
    """
    def newf(*arg, **kw):
        tic = time.perf_counter()
        res = fun(*arg, **kw)
        toc = time.perf_counter()
        print(f"Completed in {toc - tic:0.4f} seconds")
        return res
    return newf

def get_extension(file):
    """
    Extract the file extension from the given file path.

    Parameters:
        file (str): Path to the file.

    Returns:
        str: File extension (lowercased), or "None" if no extension exists.
    """
    extension = splitext(file)[1].lower()
    return extension if extension else "None"

class ExplorationTool:
    """
    A tool for exploring files and directories within a given path.

    Attributes:
        path (str): The base path to explore.
    """
    def __init__(self, path):
        """
        Initialize the ExplorationTool with a base path.

        Parameters:
            path (str): The base directory path.
        """
        self.path = path

    def files(self):
        """
        Generator that yields all files and directories in the path recursively.

        Yields:
            str: Full path to a file or directory.
        """
        for root, dirs, files in os.walk(self.path):
            for d in dirs:
                yield join(root, d)
            for f in files:
                yield join(root, f)

class ResearchVessel:
    """
    A vessel for conducting research on various file types within a directory.

    Attributes:
        path (str): The base path for research.
        ExplorationTool (ExplorationTool): Tool for file exploration.
        Researcher (GeneralResearcher): General-purpose researcher.
        XLSResearcher (ExcelResearcher): Researcher for Excel files.
        DOCResearcher (WordResearcher): Researcher for Word documents.
        ImgResearcher (ImageResearcher): Researcher for image files.
        PDFResearcher (PDFDocResearcher): Researcher for PDF documents.
        VidResearcher (VideoResearcher): Researcher for video files.
        IsoFileResearcher (ISOResearcher): Researcher for ISO files.
        extension_counter (Counter): Counter for file extensions.
    """
    def __init__(self, path):
        """
        Initialize the ResearchVessel with the given path and associated researchers.

        Parameters:
            path (str): The base directory path for research.
        """
        self.ExplorationTool = ExplorationTool(path)
        self.Researcher = researchers.GeneralResearcher()
        self.XLSResearcher = researchers.ExcelResearcher()
        self.DOCResearcher = researchers.WordResearcher()
        self.ImgResearcher = researchers.ImageResearcher()
        self.PDFResearcher = researchers.PDFDocResearcher()
        self.VidResearcher = researchers.VideoResearcher()
        self.IsoFileResearcher = researchers.ISOResearcher()
        self.path = path 
        self.extension_counter = Counter()

    def fetch_file_objects(self):
        """
        Generator that yields file information for all files in the directory.

        Yields:
            dict: A dictionary containing file information such as extension, size, and metadata.
        """
        for f in self.ExplorationTool.files():

            all_extensions = []

            if not os.path.isdir(f):  # If it's a file
                file_extension = get_extension(f).lower()
                all_extensions.append(file_extension)
                match file_extension:
                    case ".xlsx":
                        info = self.XLSResearcher.get_info(f)
                    case '.docx':
                        info = self.DOCResearcher.get_info(f)
                    case '.pdf':
                        info = self.PDFResearcher.get_info(f)
                    case '.jpg' | '.jpeg' | '.gif' | '.png':
                        info = self.ImgResearcher.get_info(f)
                    case '.avi':
                        info = self.VidResearcher.get_info(f)
                    case ".iso":
                        info = self.IsoFileResearcher.get_info(f)
                    case _:
                        info = self.Researcher.get_info(f)
                
                info['extension'] = file_extension
                info['is_folder'] = False
            else:
                info = self.Researcher.get_info(f)
                info['is_folder'] = True
            
            info['path'] = f

            if info['is_container'] == True:  # It's an ISO file
                objects_list = info['contents']
                yield info
                for nested_obj in objects_list:
                    all_extensions.append(nested_obj['extension'])
                    self.extension_counter.update(all_extensions)
                    info['is_container'] = False
                    yield nested_obj
            else:
                self.extension_counter.update(all_extensions)
                info['is_container'] = False
                yield info

    def fetch_file_objects_django(self):
        """
        Generator that yields file information formatted for Django compatibility.

        Yields:
            dict: A dictionary with file information excluding unsupported fields like 'contents'.
        """
        def format_date(date_string):
            dt_object = datetime.strptime(date_string, "%a %b %d %H:%M:%S %Y")
            return dt_object.strftime("%Y-%m-%d %H:%M:%S")

        for info in self.fetch_file_objects():
            info_copy = info.copy()
            del info_copy['contents']
            yield info_copy

    @timeit
    def display_folder_overview(self):
        """
        Display an overview of the folder content, including file details.

        Yields:
            dict: A dictionary containing file information for display.
        """
        for info in self.fetch_file_objects():
            yield info

    def print_file_info(self, f, info):
        """
        Print file information in a human-readable format.

        Parameters:
            f (str): File path.
            info (dict): File metadata.
        """
        display_extension = info['extension'] if not info['is_folder'] else "FOLDER"
        print(f"{f:65} {display_extension:6}    {info['size']:10}    {info['last_modified']}")

    @timeit
    def save_as_csv(self, path_to_csv='file_listing.csv'):
        """
        Save file information to a CSV file.

        Parameters:
            path_to_csv (str): Path to the output CSV file. Defaults to 'file_listing.csv'.
        """
        field_names = self.Researcher.infoDict.keys()

        with open(path_to_csv, 'w', encoding='utf8', newline='') as f:
            writer = csv.DictWriter(f, field_names, extrasaction='raise')
            writer.writeheader()
            for file_info in self.fetch_file_objects():
                writer.writerow(file_info)

    @timeit
    def extension_stats(self):
        """
        Print statistics on the count of different file extensions in the directory.

        Prints:
            str: File extension and its count.
        """
        all_extensions = []
        for f in self.ExplorationTool.files():
            file_extension = get_extension(f)
            all_extensions.append(file_extension)
        c = Counter(all_extensions)
        for item, cnt in c.items():
            print(f"{item:10} :", cnt)

if __name__ == "__main__":
    santa_maria = ResearchVessel('P:/Work')

    for i in santa_maria.save_as_csv():
        print(i)
