import magic
import os

LIST_OF_IMAGE_MIME = ['image/bmp','image/jpeg','image/x-png','image/png','image/gif']


class ImageValidator:
    def __init__(self,file_path, file_size):
        self.file_path = file_path
        self.file_size = file_size


    def check_file_size(self,file_path,file_size):
        # get the current working directory
        current_dir = os.getcwd()
        # create a file path by joining the current directory and the file name
        file_dir = os.path.join(current_dir, file_path)
        file_size_ = os.path.getsize(file_dir)
        if file_size_ != file_size:
            return "The image size is not valid."
        return file_size

    def check_file_mime_type(self,file_path):
        """
        Checks the MIME type of a file using the python-magic library.

        :param file_path: The path to the file.
        :type file_path: str
        :param expected_mime_type: The expected MIME type of the file.
        :type expected_mime_type: str
        :return: True if the MIME type matches the expected type, False otherwise.
        :rtype: bool
        """
        mime = magic.Magic(mime=True)
        file_mime_type = mime.from_file(file_path)
        file_type_checked = file_mime_type not in  LIST_OF_IMAGE_MIME
        if file_type_checked:
            return "The image file is not valid."
        return True
  
            



# imagecheck = ImageValidator("./hello.txt",2014)
# rr1 = imagecheck.check_file_size("./hello.txt",2014)
# rr2 = imagecheck.check_file_mime_type("./hello.txt")
# print(rr1)
# print(rr2)
        