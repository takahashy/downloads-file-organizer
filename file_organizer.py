from pathlib import Path
from datetime import datetime
import PyPDF2

DOWNLOADS   = Path("")
PICS_VIDS   = ""
OTHER_PDFS  = ""
JOB_RELATED = ""
MAYBE_TRASH = ""
COVER_LETTER = ""
THIS_FILE = "file_organizer.py"
CRON_LOG  = ""
FAILED = False

'''
Purpose: Appends todays date and time to the log file
Parameters: None
Returns: None
'''
def addDateToLog():
    log = str(DOWNLOADS) + '/' + CRON_LOG
    with open(log, 'a') as log_file:
        time = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_file.write(f"\033[94m{time}\033[0m\n")

'''
Purpose: Determines whether the pdf file passed in is job related or not by
         reading in the pdf and detecting for a specific string
Parameters: 
    . file_path - Path object to the pdf file
Returns:
    . boolean - true if pdf is job related, false otherwise
'''
def isJobRelated(file_path:Path) -> bool:
    file = str(file_path)
    with open(file, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        page = pdf_reader.pages[0]
        text = page.extract_text()
        
        if COVER_LETTER in text:
            return True
        
    return False

'''
Purpose: Move the file in the downloads to the corresponding subdirectory
Parameters: 
    . source - Path object to the file to move
    . destination - name of the destination subdirectory
Returns: None
'''
def move_file(source:Path, destination:str):
    global FAILED
    print(f"\033[1m--------\033[0m")
    try:
        source.rename(destination + '/' + source.name)
        print(f"\033[92mMOVED {source.name} to {destination.split('/')[-1]}\033[0m\n")
    except Exception as err:
        FAILED = True
        print(f"\033[91mCould NOT Move {source.name} to {destination.split('/')[-1]}\033[0m\n")
        print(err)

'''
Purpose: main function, go through all the files in the downloads directory and 
         call the corresponding function for each extension.
Parameters: None
Returns: None
'''
def main():
    addDateToLog()
    for file in DOWNLOADS.iterdir():
        if (file.name == THIS_FILE) or (file.name == CRON_LOG):
            continue
        
        if file.is_file():
            ext = file.suffix
            if ext == ".pdf":
                if isJobRelated(file):
                    move_file(file, JOB_RELATED)
                else:
                    move_file(file, OTHER_PDFS)
            elif (ext == ".png") or (ext == ".jpg") or (ext == ".mp4") or (ext == ".mp3"):
                move_file(file, PICS_VIDS)
            else:
                move_file(file, MAYBE_TRASH)
                
    if FAILED:
        print(f"\033[91mSome of the tests failed. Check Above\033[0m\n")
    

if __name__ == "__main__":
    main()