ECHO ON
REM A batch script to execute a Python script
SET PATH=%PATH%;C:\Python36
python F:\DevArchive\Scripts\moveToAuthorFolder.py "%~1" "K:\NewHCache\Manga" "author_list.txt"
PAUSE