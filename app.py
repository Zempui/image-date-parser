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

def check_metadata(img_path:str) -> bool:
    """
    Check wether an image's 'datetime' and 'datetime_original' are the same
    as the date in their name.
    """
    result = False
    filename = img_path[img_path.rfind("/")+1:]
    dst_date = datetime.datetime.strptime(f"{filename[4:12]}","%Y%m%d")
    with open(img_path, 'rb') as img_file:
        img = Image(img_file)
    if (img.has_exif and ("datetime" in img.list_all()) and ("datetime_original" in img.list_all())):
        if(img.get("datetime")[:10] == dst_date.strftime("%Y:%m:%d") and 
        img.get("datetime")[:10] == img.get("datetime_original")[:10]):
            result = True
    return result

def mod_metadata(img_path:str):
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
    folder_path:str = vars(parser.parse_args())["directory"][0]

    files:list = glob.glob(f'{folder_path}/IMG-????????-WA*.jpg', recursive=False)
    files_to_change:list = []
    print(f"Found {len(files)} images")

    print("Checking which images have to have their metadata changed...")
    
    for i in trange(len(files), desc="Progress"):
        try:
            if (not check_metadata(files[i])):
                files_to_change.append(files[i])
        except TypeError:
            print(f"{Fore.RED}TypeError in {files[i][files[i].rfind('/')+1:]} -> dst_date.strftime('%Y:%m:%d')={datetime.datetime.strptime(files[i][files[i].rfind('/')+1:][4:12],'%Y%m%d').strftime('%Y:%m:%d')}{Fore.RESET}")
    
    print(f"A total of {len(files_to_change)} files have to have their metadata changed\n"+
          "Changing images' metadata...")
    for i in trange(len(files_to_change), desc="Progress"):
        mod_metadata(files_to_change[i])
    print(f"{Fore.GREEN}Done!{Fore.RESET}")
