'''
file organizer
2024 Jan 30

Organizes files in the downloads folder into different folders.
'''
from pathlib import Path
from datetime import datetime
import PyPDF2

CURR_DIR  = Path.cwd()
CURR_FILE = Path(__file__)
WORK_RELATED = ["career", "employee", "salary"]
WORK         = CURR_DIR / "work"
PDFS         = CURR_DIR / "pdfs"
PICS_VIDS    = CURR_DIR / "pics_vids"
MAYBE_TRASH  = CURR_DIR / "maybe_trash"
LOG_FILE     = "logfile.log"
FAILED       = False

'''
Purpose: Appends todays date and time to the log file
Parameters: None
Returns: None
'''
def addDateToLog():
    with open(LOG_FILE, 'a') as log:
        time = datetime.now().strftime("%Y/%m/%d %H:%M")
        log.write(f"\n\033[94m{time}\033[0m\n")

'''
Purpose: Create the subdirectories if not existent
Parameters: None
Returns: None
'''
def makeDirs():
    if not WORK.exists(): WORK.mkdir()
    if not PDFS.exists(): PDFS.mkdir()
    if not PICS_VIDS.exists(): PICS_VIDS.mkdir()
    if not MAYBE_TRASH.exists(): MAYBE_TRASH.mkdir()

'''
Purpose: Determines whether the pdf file passed in is job related or not by
         reading in the pdf and detecting for a specific string
Parameters: 
    . file_path - Path object to the pdf file
Returns:
    . boolean - true if pdf is job related, false otherwise
'''
def isJobRelated(file:Path) -> bool:
    global FAILED
    try:
        with open(file, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            page = pdf_reader.pages[0]
            text = page.extract_text()

            for words in WORK_RELATED:
                if words in text:
                    return True
            return False
        
    except PyPDF2.errors.EmptyFileError as emptyErr:
        print(f"\033[91m{emptyErr}: \033[0m{file.name}")
        FAILED = True

'''
Purpose: check if the extension is a picture, video, or audio
Parameters: ext - string extension
Returns: boolean
'''
def isPicVid(ext:str) -> bool :
    return (ext == ".png") or (ext == ".jpeg") or (ext == ".jpg") or (ext == ".mp3") or (ext == ".mp4")

'''
Purpose: Move the file in the downloads to the corresponding subdirectory
Parameters: 
    . source - Path object of the file to move
    . destination - Path object of destination directory
Returns: None
'''
def move_file(source:Path, destination:Path):
    global FAILED
    print(f"\033[1m--------\033[0m")
    try:
        new_path = destination / source.name
        source.rename(new_path)
        print(f"\033[92mMOVED {source.name} to {destination.name}\033[0m")
    except Exception as err:
        print(f"\033[91mCould NOT Move {source.name} to {destination.name}\033[0m\n")
        print(err)
        FAILED = True

'''
Purpose: main function, go through all the files in the downloads directory and 
         call the corresponding function for each extension.
Parameters: None
Returns: None
'''
def main():
    addDateToLog()
    makeDirs()
    for item in CURR_DIR.iterdir():
        if item.is_file():
            if item != CURR_FILE and item.name != LOG_FILE:
                ext = item.suffix
                if (ext == ".pdf") and isJobRelated(item):
                    move_file(item, WORK)
                elif ext == ".pdf":
                    move_file(item, PDFS)
                elif isPicVid(ext):
                    move_file(item, PICS_VIDS)
                else:
                    move_file(item, MAYBE_TRASH)
    
    if FAILED:
        print(f"\n\033[91mSomething failed. Check Above\033[0m")
    else:
        print(f"\n\033[92mAll moved!\033[0m")

if __name__ == "__main__":
    main()