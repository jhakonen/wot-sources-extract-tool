
import zipfile
import os

def iterfiles(dirpath):
    for root, dirs, files in os.walk(dirpath):
        for name in files:
            if not name.endswith('.pkg'):
                continue
            with zipfile.ZipFile(os.path.join(root, name), "r") as pkg_file:
                for member_path in pkg_file.namelist():
                    yield ContentFile(pkg_file, os.path.normpath(member_path))

class ContentFile(object):

    def __init__(self, pkg_file, filepath):
        self.__pkg_file = pkg_file
        self.__filepath = filepath

    @property
    def filename(self):
        return self.__filepath

    def extract(self, prefix):
        self.__pkg_file.extract(self.__filepath, prefix)
