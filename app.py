"""
Software that changes metadata contained in the images of a specified folder
depending on their names. The naming format must be 'IMG-YYYYMMDD-WAXXXX.jpg',
which is the standart in some mobile phones.
"""
from exif import Image
import datetime
import glob
import argparse
from colorama import Fore
from tqdm import trange

def mod_metadata(img_path:str):
    ok = True
    filename = img_path[img_path.rfind("/")+1:]
    dst_date = datetime.datetime.strptime(f"{filename[4:12]}","%Y%m%d")
    with open(img_path, 'rb') as img_file:
        img = Image(img_file)

    img.datetime = f"{dst_date.strftime('%Y:%m:%d %H:%M:%S')}"
    img.datetime_original = img.datetime
    

    with open(f'{img_path}','wb') as img_mod_file:
        img_mod_file.write(img.get_file())

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="A tool to set the 'datetime' and 'datetime_original' metadatas of mobile phone images to the date indicated by their name.")
    parser.add_argument("directory",nargs=1, help="the directory where the images are stored.")
    folder_path = vars(parser.parse_args())["directory"][0]
    files = glob.glob(f'{folder_path}/IMG-????????-WA*.jpg', recursive=False)
    

    for i in trange(len(files), desc="Progress"):
        mod_metadata(files[i])
    print(f"{Fore.GREEN}Done!{Fore.RESET}")
