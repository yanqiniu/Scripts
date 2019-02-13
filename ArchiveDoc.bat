ECHO OFF
REM Move file to archive bin folder
SET PATH=%PATH%; C:\Python36
python F:\DevArchive\Scripts\MoveSingleFile.py "I:\GDrive\Archive\Bin" "%~1"