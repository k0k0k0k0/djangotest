import time
from datetime import datetime
import os

from os.path import getsize

# для обработки файловых типов
import openpyxl
import docx
from PIL import Image
#from PIL.ExifTags import TAGS
from pypdf import PdfReader
import cv2
from pydub.utils import mediainfo
from tinytag import TinyTag
import sys, pycdlib
import csv
import pytz
#import ffmpeg

def format_datetime(dt):
    """
    Format a datetime object into a string in the format 'YYYY-MM-DD HH:MM:SS'.

    Args:
        dt (datetime): The datetime object to format.

    Returns:
        str: A formatted datetime string. If `dt` is None, returns None.
    """
    if dt:
        # Assuming the timestamp is in UTC, if needed you can localize it to a timezone
        dt = dt.astimezone(pytz.UTC)  # Adjust this line if you want to use a different timezone
        #return dt.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return None

class GeneralResearcher:
    """
    General researcher class for extracting basic metadata about files.

    Attributes:
        keyList (list): List of keys for metadata fields.
        infoDict (dict): Template dictionary for file metadata.
    """
    def __init__(self):
        # создаем пустой словарь с заранее определенным списком ключей-параметров файлов
        self.keyList = ['path', 'extension', 'is_folder', "size", "last_modified", "created_time",
                         'is_container', 'contents', 
                         'within_container', 'parent_object',
                    "Office_last_mod_time", "Office_last_mod_by",
                    'XLS_num_sheets',
                    'PDF_num_pages', 'PDF_layout',
                    "MP3_track_title", "MP3_artist", "MP3_duration", 'AUD_bitrate',
                    'IMG_size', 'IMG_dpi', "IMG_device"]
        self.infoDict = {key: None for key in self.keyList}
    
    def get_info(self, file):
        """
        Get metadata information about a general file.

        Args:
            file (str): Path to the file.

        Returns:
            dict: Metadata information about the file.

        """
        file_info = self.infoDict.copy() # получаем пустой словарь с ключами-параметрами
        
        dt_object = datetime.fromtimestamp(os.path.getmtime(file)) # Convert the timestamp to a datetime object
        file_info['last_modified'] = dt_object.strftime("%Y-%m-%d %H:%M:%S.%f%z") # сразу отдаем в нужном формате
        #file_info['last_modified'] = format_datetime(os.path.getmtime(file))

        file_info['size'] = round(getsize(file)/1024) # в кб
        return file_info
    

# далее ряд "специализированных" рисерчеров: для XLS, DOC и графических файлов
class ExcelResearcher(GeneralResearcher):
    """
    Researcher class for extracting metadata from Excel files.
    """
    def get_info(self, file):
        """
        Get metadata information about an Excel file.

        Args:
            file (str): Path to the Excel file.

        Returns:
            dict: Metadata information about the file.

        """
        file_info = super(ExcelResearcher, self).get_info(file)

        wb = openpyxl.load_workbook(file)
        file_info['XLS_num_sheets'] = len(wb.sheetnames)

        file_info['created_time'] =  datetime.ctime(wb.properties.created)
        file_info['Office_last_mod_time'] =  datetime.ctime(wb.properties.modified)
        file_info['Office_last_mod_by'] = wb.properties.lastModifiedBy

        return file_info
    

class WordResearcher(GeneralResearcher):
    """
    Researcher class for extracting metadata from Word documents.
    """
    def get_info(self, file):
        """
        Get metadata information about a Word document.

        Args:
            file (str): Path to the Word document.

        Returns:
            dict: Metadata information about the file.
            
        """
        file_info = super(WordResearcher, self).get_info(file)

        doc = docx.Document(file)
        prop = doc.core_properties
        ### todo: количество страниц и формат
        file_info['created_time'] = datetime.ctime(prop.created)
        file_info['Office_last_mod_time'] = datetime.ctime(prop.modified)
        file_info['Office_last_mod_by'] = prop.last_modified_by

        return file_info
    

class ImageResearcher(GeneralResearcher):
    """
    Researcher class for extracting metadata from image files.
    """
    def get_info(self, file):
        """
        Get metadata information about an image file.

        Args:
            file (str): Path to the image file.

        Returns:
            dict: Metadata information about the file.
        """
        file_info = super(ImageResearcher, self).get_info(file)

        image = Image.open(file)
        exifdata = image.getexif()
        # тут отдается что-то вроде словаря
        #for tag_id in exifdata:
            # в экзифе ключи — числа, но можно достать названия
            #tag = TAGS.get(tag_id, tag_id)
            #print(f"{tag:25}: {exifdata.get(tag_id)}")  
        if exifdata.get(306):
            try:
                dt_object = datetime.strptime(exifdata.get(306), "%Y:%m:%d %H:%M:%S")  # отдается строка в странном формате, нужен unix time
                file_info['created_time'] = int(dt_object.timestamp())
            except Exception as e:
                pass
        file_info['IMG_size'] = round(image.size[0]*image.size[1], None)
        file_info['IMG_dpi'] = image.info.get('dpi', 'No data')
        file_info['IMG_device'] = exifdata.get(271, "No data")  # это модель устройства, с которого снимали
    
        return file_info
    
class VideoResearcher(GeneralResearcher):
    """
    Researcher class for extracting metadata from video files.
    """
    def get_info(self, file):
        """
        Get metadata information about a video file.

        Args:
            file (str): Path to the video file.

        Returns:
            dict: Metadata information about the file.
        """
        file_info = super(VideoResearcher, self).get_info(file)

        vid = cv2.VideoCapture(file)
        file_info['VID_height'] = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        file_info['VID_width'] = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    
        return file_info
    

class PDFDocResearcher(GeneralResearcher):
    """
    Researcher class for extracting metadata from PDF documents.
    """
    def get_info(self, file):
        """
        Get metadata information about a PDF file.

        Args:
            file (str): Path to the PDF file.

        Returns:
            dict: Metadata information about the file.
        """
        file_info = super(PDFDocResearcher, self).get_info(file)

        reader = PdfReader(file)
        file_info['PDF_num_pages'] = reader.get_num_pages()
        file_info['PDF_layout'] = reader.page_layout

        meta = reader.metadata
        file_info['Office_last_mod_by'] = meta.author

        return file_info
    

class MusicResearcher(GeneralResearcher):
    """
    Researcher class for extracting metadata from music/audio files.
    """
    def get_info(self, file):
        """
        Get metadata information about an audio file.

        Args:
            file (str): Path to the audio file.

        Returns:
            dict: Metadata information about the file.
        """
        file_info = super(MusicResearcher, self).get_info(file)

        mediainfo(file)
        file_info['AUD_bitrate'] = mediainfo['bit_rate']
        
        tag = TinyTag.get(file)
        file_info['MP3_track_title'] = tag.title 
        file_info['MP3_artist'] = tag.albumartist
        file_info['MP3_duration'] = tag.duration
        
        return file_info
    

class ISOResearcher(GeneralResearcher):
    """
    Researcher class for extracting metadata from ISO (disk image) files.
    """
    def get_info(self, file):
        """
        Get metadata information about an ISO file and its contents.

        Args:
            file (str): Path to the ISO file.

        Returns:
            dict: Metadata information about the ISO file, including its contents.
        """
        file_info = super(ISOResearcher, self).get_info(file)
        file_info['is_container'] = True

        # Create a new PyCdlib object.
        iso = pycdlib.PyCdlib()

        # Open the ISO file and parse its metadata.
        iso.open(file)
        objects_list = []
        
        for root, dirs, files in iso.walk(iso_path='/'):    # на каждый уровень вложенности
            for d in dirs:
                dir_researcher = GeneralResearcher()
                iso_dir_info = dir_researcher.infoDict
                iso_dir_info['path'] = file + root + '/' + d
                iso_dir_info['is_folder'] = True
                iso_dir_info['size'] = 0  # не сумеем определить размер вложенных файлов
                iso_dir_info['within_container'] = True
                iso_dir_info['parent_object'] = file
                objects_list.append(iso_dir_info)
            for f in files:
                nested_file_researcher = GeneralResearcher()
                iso_nested_file_info = nested_file_researcher.infoDict
                iso_nested_file_info['path'] = file + root + '/' + f[:-2]
                iso_nested_file_info['size'] = 0  # не сумеем определить размер вложенных файлов
                iso_nested_file_info['is_folder'] = False
                iso_nested_file_info['within_container'] = True
                iso_nested_file_info['parent_object'] = file
                iso_nested_file_info['extension'] = f[:-2].split(".")[1].lower()  # FILENAME.FIL;1 -> extract extension
                objects_list.append(iso_nested_file_info)

        # Close the ISO object after processing.
        iso.close()

        file_info['contents'] = objects_list
        return file_info
