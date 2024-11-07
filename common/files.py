import os
import logging
from .path import Path
from bs4 import BeautifulSoup
from .errors import HTMLFormattingError, LogFileExistsError


class File:
    """Base class for every derived file class"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def read_file(self) -> str:
        pass

    def file_name(self) -> str:
        pass


class HtmlFile(File):

    def __init__(self, file_path: str, translate_to_relative=False):
        super().__init__(file_path)
        self.translate_to_relative = translate_to_relative

    def read_file(self) -> str:
        """Reads the content of the html file"""
        if os.path.exists(self.file_path.path):
            with open(self.file_path.path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise FileNotFoundError(f"File {self.file_path} not found.")

    def modify_local_references(self):
        """Translates local references from absolute to relative"""
        try:
            # Open and parse the HTML file
            with open(self.file_path.path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'lxml')

            # Modify all <a> tags with local href attributes and that absolute path
            for a_tag in soup.find_all('a', href=True):
                if Path.is_local_reference(a_tag['href']) and os.path.isabs(a_tag['href']):
                    # Replace the old local part with the new one
                    a_tag['href'] = Path(a_tag['href']).relative_path(self.file_path.dirname())

            # Modify all <img> tags with local src attributes and have absolute path
            for img_tag in soup.find_all('img', src=True):
                if Path.is_local_reference(img_tag['src']) and os.path.isabs(img_tag['src']):
                    # Replace the old local part with the new one
                    img_tag['src'] = Path(img_tag['src']).relative_path(self.file_path.dirname())

            # Write the modified content back to the file
            with open(self.file_path.path, 'w', encoding='utf-8') as file:
                file.write(str(soup))

        except Exception as e:
            logging.error(f"Received: {e}")
            raise HTMLFormattingError

    @property
    def file_name(self) -> str:
        return self.file_path.path.split('\\')[-1]


class LogFile(File):

    def __init__(self, file_path: str):
        super().__init__(file_path)

    def read_file(self) -> str:
        """Reads the content of the html file"""
        if os.path.exists(self.file_path.path):
            with open(self.file_path.path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise LogFileExistsError(f"File {self.file_path} not found.")

    def file_name(self) -> str:
        return self.file_path.path.split('\\')[-1]





