import os
import logging
import re
from .path import Path
from bs4 import BeautifulSoup
from .errors import HTMLFormattingError, LogFileError
from .settings import LOGGER_FILE_PATH


class File:
    """Base class for every derived file class"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def read_file(self) -> str:
        pass

    def file_name(self) -> str:
        pass


class HtmlFile(File):
    """
    This class is created with the purpose to handle html file by refactoring refs, writing logs and others.
    """

    HTML_FILES_ITERATED = set()

    def __init__(self, file_path: str, translate_to_rel: bool = False, write_to_log: bool = False, write_to_log_script: bool = False):
        super().__init__(file_path)

        self.references = []
        self.translate_to_rel = translate_to_rel
        self.write_to_log = write_to_log
        self.write_to_log_script = write_to_log_script

        HtmlFile.HTML_FILES_ITERATED.add(self.file_path.path)

        if self.translate_to_rel:
            self.modify_local_references()
        if self.write_to_log:
            logger = LoggerHTML(LOGGER_FILE_PATH, self.file_path.path, self.map_all_references())
            logger.output_to_logger_file()

        if self.write_to_log_script:
            logger_scripts = LoggerScripts(LOGGER_FILE_PATH, self.file_path.path, self.map_all_scripts())
            logger_scripts.output_to_logger_file()

    def read_file(self) -> str:
        """Reads the content of the html file"""
        if os.path.exists(self.file_path.path):
            with open(self.file_path.path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            logging.warning(f"File {self.file_path} not found.")
            return ""

    def modify_local_references(self):
        """Translates local references from absolute to relative"""
        try:
            # Open and parse the HTML file
            with open(self.file_path.path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'lxml')

            # Modify all <a> tags with local href attributes and that absolute path
            for a_tag in soup.find_all('a', href=True):
                print(a_tag)
                if Path.is_local_reference(a_tag['href']) and os.path.isabs(a_tag['href']):
                    # Replace the old local part with the new one
                    a_tag['href'] = Path(a_tag['href']).relative_path(self.file_path.dirname())

            # Modify all <img> tags with local src attributes and have absolute path
            for img_tag in soup.find_all('img', src=True):
                if Path.is_local_reference(img_tag['src']) and os.path.isabs(img_tag['src']):
                    # Replace the old local part with the new one
                    img_tag['src'] = Path(img_tag['src']).relative_path(self.file_path.dirname())

            # Modify all <link> tags with local src attributes and have absolute path
            for link_tag in soup.find_all('link', href=True):
                if Path.is_local_reference(link_tag['href']) and os.path.isabs(link_tag['href']):
                    # Replace the old local part with the new one
                    link_tag['href'] = Path(link_tag['href']).relative_path(self.file_path.dirname())

            # Write the modified content back to the file
            with open(self.file_path.path, 'w', encoding='utf-8') as file:
                file.write(str(soup))

        except Exception as e:
            logging.info(f"Received: {e}", HTMLFormattingError)

    @property
    def file_name(self) -> str:
        """Returns the file name"""
        return self.file_path.path.split('\\')[-1]

    # Function to add the references to the list
    def add_reference(self, ref_type, ref_value, is_absolute):
        """Adds the given reference to the list"""
        self.references.append({
            "type": ref_type,
            "url": ref_value,
            "is_absolute": is_absolute
        })

    def map_all_scripts(self) -> str:
        """Get match for scripts and write them to logger"""
        html_content = self.read_file()
        if not html_content:
            return ""
        if self.write_to_log_script:
            script_tags = re.findall(r'<script[^>]*(type="([^"]+)"|src="([^"]+)")[^>]*>.*?</script>', html_content, re.DOTALL | re.IGNORECASE)

            output_content = ""
            for script_type in script_tags:
                output_content += f"\t\t{script_type}\n"
            return output_content
        return ""

    def map_all_references(self) -> list[dict[str, any]]:
        """Iterate over the content and get all the references from the file"""
        html_content = self.read_file()
        if not html_content:
            return [{'type': "Dead end", 'url': "None", 'is_absolute':"Unkown"}]
        soup = BeautifulSoup(html_content, "html.parser")

        # Iterate over all inline images
        for img in soup.find_all("img"):
            src = img.get("src")
            if src:
                is_absolute = bool(re.match(r"^https?://", src))
                self.add_reference("Inline Image", src, is_absolute)

        # Extract background css images which are inline
        for element in soup.find_all(style=True):
            style = element["style"]
            background_images = re.findall(r'url\((.*?)\)', style)
            for img_url in background_images:
                is_absolute = bool(re.match(r"^https?://", img_url))
                self.add_reference("CSS Background Image", img_url.strip('"').strip("'"), is_absolute)

        # Extract css files
        for link in soup.find_all("link", rel="stylesheet"):
            href = link.get("href")
            if href:
                is_absolute = bool(re.match(r"^https?://", href))
                self.add_reference("CSS File", href, is_absolute)

        # Extract anchors with (tag: <a name>)
        for anchor in soup.find_all("a"):
            name = anchor.get("name")
            if name:
                self.add_reference("Internal Anchor", f"#{name}", False)

        # Extract external links (tag: <a href>)
        for anchor in soup.find_all("a", href=True):
            href = anchor.get("href")
            if href:
                is_absolute = bool(re.match(r"^https?://", href))
                ref_type = "External Link" if is_absolute else "Internal Link"
                self.add_reference(ref_type, href, is_absolute)
                is_html = HtmlFile.is_html_file(href)

                reference_html_path = os.path.join(os.path.dirname(self.file_path.path), href)
                reference_html_path = reference_html_path.replace("\\", "/")  # from windows path to unix path

                if ref_type == "Internal Link" and is_html and reference_html_path not in HtmlFile.HTML_FILES_ITERATED:
                    HtmlFile.HTML_FILES_ITERATED.add(reference_html_path)
                    HtmlFile(reference_html_path, self.translate_to_rel, self.write_to_log, self.write_to_log_script)

        return self.references

    @classmethod
    def is_html_file(cls, url: str) -> bool:
        return bool(re.search(r"\.html?$|/$", url))


class LogFile(File):
    """
    This class is meant to create the log in which the information is stored
    """
    def __init__(self, file_path: str, parent_html_file: str):
        super().__init__(file_path)
        self.parent_html_file = parent_html_file

        if not self.file_path.exists():
            raise LogFileError(f"The file for path: {file_path} doesn't exist!")

    def read_file(self) -> str:
        """Reads the content of the html file"""
        try:
            with open(self.file_path.path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise LogFileError(f"{e}")

    @property
    def file_name(self) -> str:
        return self.file_path.path.split('\\')[-1]

    def write_to_file_refs(self, content: list[dict[str, any]]):
        """Method to write the given content to the current logger"""
        with open(self.file_path.path, "a", encoding="utf-8") as log_file:
            log_file.write(f"\nLog for {self.parent_html_file}:\n")
            try:
                for ref in content:
                    log_file.write(f"\t\tType: {ref['type']}, URL: {ref['url']}, Absolute: {ref['is_absolute']}\n")
            except Exception as e:
                raise LogFileError(e)
            log_file.close()

    def write_to_file_scripts(self, content: str):
        """Method to write the given content to the current logger"""
        with open(self.file_path.path, "a", encoding="utf-8") as log_file:
            log_file.write(f"\t\tInformation about scripts for html file {self.parent_html_file}:\n")
            try:
                log_file.write(content)
            except Exception as e:
                raise LogFileError(e)
            log_file.close()


class LoggerHTML:
    """Logger for HTML"""
    def __init__(self, file_path, parent_html_file: str, content_to_write: list[dict[str, any]]):
        self.log_file = LogFile(file_path, parent_html_file)
        self.content_to_write = content_to_write

    def output_to_logger_file(self):
        self.log_file.write_to_file_refs(self.content_to_write)


class LoggerScripts:
    """Logger for Scripts"""
    def __init__(self, file_path, parent_html_file: str, content_to_write: str):
        self.log_file = LogFile(file_path, parent_html_file)
        self.content_to_write = content_to_write

    def output_to_logger_file(self):
        self.log_file.write_to_file_scripts(self.content_to_write)


"""
Type: Inline Image, URL: images/logo.png, Absolute: False
Type: CSS File, URL: css/style.css, Absolute: False
Type: Internal Anchor, URL: #section1, Absolute: False
Type: External Link, URL: https://example.com, Absolute: True
Type: Internal Link, URL: /about, Absolute: False
Type: CSS Background Image, URL: https://example.com/background.jpg, Absolute: True
"""
