ECHO ON
REM A batch script to execute a Python script
SET PATH=%PATH%;C:\Python27
python F:\DevArchive\Scripts\convertAllChildrenToJpeg.py "%cd%"
PAUSE