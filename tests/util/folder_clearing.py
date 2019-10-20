import os
import shutil


def clear_folder_contents(path_to_folder):
    for the_file in os.listdir(path_to_folder):
        file_path = os.path.join(path_to_folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)
