import os
from pathlib import Path
import shutil
import re
from sys import argv
path = Path(input())
main_path = path
path_of_files = []
know_list = []
unknown_list = []
# key names will be folder names!
extensions = {

    'video': ['mp4', 'mov', 'avi', 'mkv', 'wmv', '3gp', '3g2', 'mpg', 'mpeg', 'm4v', 
              'h264', 'flv', 'rm', 'swf', 'vob'],

    'data': ['sql', 'sqlite', 'sqlite3', 'csv', 'dat', 'db', 'log', 'mdb', 'sav', 
             'tar', 'xml'],

    'audio': ['mp3', 'wav', 'ogg', 'flac', 'aif', 'mid', 'midi', 'mpa', 'wma', 'wpl',
              'cda'],

    'image': ['jpg', 'png', 'bmp', 'ai', 'psd', 'ico', 'jpeg', 'ps', 'svg', 'tif', 
              'tiff'],

    'archive': ['zip', 'rar', '7z', 'z', 'gz', 'rpm', 'arj', 'pkg', 'deb'],

    'text': ['pdf', 'txt', 'doc', 'docx', 'rtf', 'tex', 'wpd', 'odt'],

    '3d': ['stl', 'obj', 'fbx', 'dae', '3ds', 'iges', 'step'],

    'presentation': ['pptx', 'ppt', 'pps', 'key', 'odp'],

    'spreadsheet': ['xlsx', 'xls', 'xlsm', 'ods'],

    'font': ['otf', 'ttf', 'fon', 'fnt'],

    'gif': ['gif'],

    'exe': ['exe'],

    'bat': ['bat'],

    'apk': ['apk']
    
}
# cоздание папок
def create_folders_from_list(folder_path, folder_names):
    for folder in folder_names:
        if not os.path.exists(f'{folder_path}\\{folder}'):
            os.mkdir(f'{folder_path}\\{folder}')
create_folders_from_list(main_path, extensions)
# пути подпапок и файлов
def get_subfolder_paths(folder_path) -> list:
    subfolder_paths = [f.path for f in os.scandir(folder_path) if f.is_dir()]

    return subfolder_paths
# пути файлов 
def get_file_paths(folder_path) -> list:
    file_paths = [f.path for f in os.scandir(folder_path) if not f.is_dir()]

    return file_paths
# имена фалйов
def get_file_names(folder_path) -> list:
    file_paths = [f.path for f in os.scandir(folder_path) if not f.is_dir()]
    file_names = [f.split('\\')[-1] for f in file_paths]

    return file_names
# удаление пустых
def remove_empty_folders(folder_path):
    subfolder_paths = get_subfolder_paths(folder_path)

    for p in subfolder_paths:
        if not os.listdir(p):
            print('Deleting empty folder:', p.split('\\')[-1], '\n')
            os.rmdir(p)
# сортировка файлов
def sort_files(folder_path):
    file_paths = get_file_paths(folder_path)
    ext_list = list(extensions.items())

    for file_path in file_paths:
        extension = file_path.split('.')[-1]
        file_name = file_path.split('\\')[-1]

        for dict_key_int in range(len(ext_list)):
            if extension in ext_list[dict_key_int][1]:
                print(f'Moving {file_name} in {ext_list[dict_key_int][0]} folder\n')
                try:
        
                    os.rename(file_path, f'{main_path}\\{ext_list[dict_key_int][0]}\\{file_name}')
                except FileExistsError:
                    os.remove(file_path)
# распаковка 
def unpack_archive(main_path: Path):
    archive_directory = main_path / 'archive'
    for archive in archive_directory.glob('*.*'):
        path_archive_folder = archive_directory / archive.stem.upper()
        try:
            shutil.unpack_archive(archive, path_archive_folder)
        except:
            continue
# нормализация
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ ʼ'\"@"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g",
               "_", "_", "_", "_", "_")
def translate(name):
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION ):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    imya = name.translate(TRANS)
    return imya
def normalize(file):
    ch = f"{file}"
    ck = translate(ch)
    os.rename(file, f"{ck}")
def norm_list(path):
    for i in path.glob('**/*'):
        normalize(i)
# список всіх шляхів
def folder_list(path):
    sort_files(path)
    for i in path.glob('**/*'):
        if i.is_dir() == True: 
            print(i)
            sort_files(i)
def all_in(path):        
    folder_list(path)
    remove_empty_folders(path)
    norm_list(path)
    unpack_archive(path)
    remove_empty_folders(path)
if __name__ == "__main__"
all_in(path)