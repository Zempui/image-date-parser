# image-date-parser
Software that changes metadata contained in the images of a specified folder depending on their names. The naming format must be `IMG-YYYYMMDD-WAXXXX.jpg`, which is the standart in some mobile phones.
## Usage
Simply clone the repository and execute the following sentence while located inside of the folder:
```bash
python3 -m pip install -r requirements.txt
```
After that, you are good to go! Execute the `app.py` file with `python3 app.py <Folder_where_your_images_are>` and the script should do its work and change their `datetime` and `datetime_original` metadata to that of their names.
