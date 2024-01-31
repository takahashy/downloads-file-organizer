# Downloads File Organizer
Program to organize files in my downloads directory. Have this file and a log
file in the downloads directory to run it on the downloads directory. Look through 
each file. If it has a pdf extension look at its content and if it is a cover 
letter or job related move it into the jobs_related folder, else move it to 
other pdfs. If its a picture, video, or audio move it to that folder. Move any 
other files to the maybe_trash folder. Run this program automatically once every
two weeks using crontab in linux. Writes a log to the log file every time the program is run.

# How to Run
The program runs automatically by the crontab command in linux, by running crontab -e.
In the editor type the following to schedule 18:30 on Monday every week
    
    30 18 * * 1 /usr/bin/python3 /path/to/file_organizer.py >> /path/to/log_file 2>&1

But can be also run manually with the following

    python3 file_organizer.py

