import os


class Path:
    """Path class to manage the given strings as system paths"""

    def __init__(self, path: str):
        self.path = path

    def relative_path(self, base_path: str) -> str:
        return os.path.relpath(self.path, base_path)

    def is_absolute(self) -> bool:
        return os.path.isabs(self.path)

    def __repr__(self) -> str:
        return f"Path({self.path})"

    def join(self, path):
        """Joins the current path with the provided path"""
        return Path(os.path.join(self.path, path))

    def dirname(self) -> str:
        return os.path.dirname(self.path)

    def exists(self) -> bool:
        return os.path.exists(self.path)

    def is_file(self) -> bool:
        """Checks if the path is a file"""
        return os.path.isfile(self.path)

    def is_dir(self) -> bool:
        """Checks if the path is a directory"""
        return os.path.isdir(self.path)

    @property
    def absolute_path(self) -> str:
        """Returns the absolute path of a file"""
        return os.path.abspath(self.path)

    @classmethod
    def is_local_reference(cls, url) -> bool:
        # Check if the URL is local (i.e., does not start with http:// or https://)
        return not (url.startswith('http://') or url.startswith('https://'))






