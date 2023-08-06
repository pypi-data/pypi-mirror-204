from entx.storage import JSONClient
from .errors import *
import os

class FileClient:
    def __init__(self, password: str, file_path: str):
        if os.path.exists(file_path):
            self.client = JSONClient(password)
            self.file_path = file_path
        else:
            raise InvalidPath("File does not exist.")
        
    def pack(self):
        if self.file_path.endswith(".py"):
            with open(self.file_path, "r", encoding = "utf-8") as input_file:
                contents = input_file.read()
                contents_obj = {
                    "python": contents
                }
                new_path = self.file_path[:-3] + ".entxpy"
                with open(new_path, "w", encoding = "utf-8") as output_file:
                    self.client.dump(contents_obj, output_file)
                    os.remove(self.file_path)
                    self.file_path = new_path
        else:
            raise InvalidOperation("The file to be packed must be a .py file.")
             
    def unpack(self):
        if self.file_path.endswith(".entxpy"):
            with open(self.file_path, "r", encoding = "utf-8") as input_file:
                decrypted_contents = self.client.load(input_file)
                new_path = self.file_path[:-7] + ".py"
                with open(new_path, "w", encoding = "utf-8") as output_file:
                    output_file.write(decrypted_contents["python"])
                    os.remove(self.file_path)
                    self.file_path = new_path
        else:
            raise InvalidOperation("The file to be unpacked must be a .entxpy file.")
    
    def run(self):
        if self.file_path.endswith(".py"):
            with open(self.file_path, "r", encoding = "utf-8") as to_run:
                exec(to_run)
        elif self.file_path.endswith(".entxpy"):
            with open(self.file_path, "r", encoding = "utf-8") as to_run:
                exec(self.client.load(to_run)["python"])
        else:
            raise InvalidOperation("File must be either a .py file or a .entxpy file.")