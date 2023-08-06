import os
import shutil
import re


def move_folder_contents(folder_path):


    for name in os.listdir(folder_path):
        path = os.path.join(folder_path, name)
        
        if os.path.isdir(path):
            move_folder_contents(path)
        elif os.path.isfile(path):
            pass
        else:
            pass

        if os.path.isdir(path):
            for subname in os.listdir(path):
                subpath = os.path.join(path, subname)
                shutil.move(subpath, folder_path)
            os.rmdir(path)


def normalize(folder_path):


    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', 
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            filename, ext = os.path.splitext(file)
            new_filename = ''
            for char in filename:
                if char.isalpha() and char not in translit_dict:
                    new_filename += char
                elif char.isdigit() or char.isalpha() and char in translit_dict:
                    new_filename += translit_dict.get(char, ' ')
                else:
                    new_filename += ' '
            new_file = new_filename + ext
            os.rename(os.path.join(root, file), os.path.join(root, new_file))


def make_new_folders(folder_path):
    # Create the six target directories
    os.makedirs(os.path.join(folder_path, 'images'), exist_ok=True)
    os.makedirs(os.path.join(folder_path, 'video'), exist_ok=True)
    os.makedirs(os.path.join(folder_path, 'documents'), exist_ok=True)
    os.makedirs(os.path.join(folder_path, 'music'), exist_ok=True)
    os.makedirs(os.path.join(folder_path, 'archives'), exist_ok=True)
    os.makedirs(os.path.join(folder_path, 'unknown extensions'), exist_ok=True)

    extensions = {
        '.jpg': 'images',
        '.jpeg': 'images',
        '.png': 'images',
        '.gif': 'images',
        '.bmp': 'images',
        '.svg': 'images',
        '.mp4': 'video',
        '.avi': 'video',
        '.mov': 'video',
        '.mkv': 'video',
        '.doc': 'documents',
        '.docx': 'documents',
        '.pdf': 'documents',
        '.xls': 'documents',
        '.xlsx': 'documents',
        '.ppt': 'documents',
        '.pptx': 'documents',
        '.txt': 'documents',
        '.mp3': 'music',
        '.wav': 'music',
        '.flac': 'music',
        '.zip': 'archives',
        '.rar': 'archives',
        '.7z': 'archives',
    }

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in extensions:
                source_path = os.path.join(root, file)
                target_path = os.path.join(folder_path, extensions[ext], file)
                shutil.move(source_path, target_path)
            else:
                source_path = os.path.join(root, file)
                target_path = os.path.join(folder_path, 'unknown extensions', file)
                shutil.move(source_path, target_path)

 
def main():
    folder_path = input('Введите путь к папке, которую хотите очистить используя два обратных слеша:   ')
    move_folder_contents(folder_path)
    normalize(folder_path)
    make_new_folders(folder_path)

    
if __name__ == '__main__':
    main()
