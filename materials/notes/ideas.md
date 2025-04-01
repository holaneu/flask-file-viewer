# File storage manager
I need to implement some kind of simple file storage system.
First I will start with just file viewer.
- function returning json map of all files and folders located in the the base folder - currently the base folder is "files"
  - The structure of files and folders might be multi-level, so in there might be more nested folders containing files.
  - each folder or file is treated as a single item having filels like
    - id
    - type - file, folder
    - title
    - file_path - relative path within the  base folder. Example: if file has the full path files/subf1/subf2/file.txt then the file_path shoudl be "subf1/subf2/file.txt"
    - parent - id of the parent
    - hidden - True/False