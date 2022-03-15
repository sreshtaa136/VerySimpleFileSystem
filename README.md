# VSFS ( A Very Simple FileSystem)
VSFS creates a simple file system that can be manipulated in various ways. The file system is basically inside the text file named "VSFS.notes". 

## Format of the file system:

The notes file format is described as follows:
1. It is a text file with variable length records.   
2. All records  starting with “#” are ignored. 
3. The first record in the VSFS file starts with “NOTES V1.0”. A valid notes file must contain this text in the first line. 
4. A file name record starts with “@” as the first character followed by a “path/.../file”  entry. If path is omitted, path = “”. That is, there is no leading “/” in the name. So a plain file “abc” is encoded as “@abc”.
5. A directory record is a file record starting with “=” and ending with a path ending in “/”. 
6. A content record contains a “ ” (space) in the first character and must succeed a file record. All subsequent content records go in the same file entry, until a non-content record is encountered. 
7. A file may be deleted. In that case, the file record and any following content records will have the first character set to “#”. 
8. A new file using copyin is always appended to the VSFS. 
9. If copyin is used to replace a file, that file is first deleted, and the new file appended. 
10. When using copyin to insert a file, always prepend the content records with a “ ” (space).
11. Only records starting with one of the first characters described above are allowed in the VSFS file. Any other character will result in an error.
12. No two notes should have identical names at the same directory level. 

## How to run the program:

1) In your command prompt/terminal, cd into the 'VSFS' folder present inside the project directory
2) To make the file an executable, enter this command in the terminal: **chmod 700 VSFS.py**
3) You are now ready to use the file system. Enter a command from the following set of commands:

    - **./VSFS.py copyin VSFS.notes EF IF:** Copy the external file, EF, into the file system(VSFS.notes) as internal file named IF 

    - **./VSFS.py copyout VSFS.notes IF EF:** Copy the internal file IF within the file system(VSFS.notes) to external file EF

    - **./VSFS.py mkdir VSFS.notes ID:** Creates empty internal directory ID in the file system(VSFS.notes)

    - **./VSFS.py rm VSFS.notes IF:** Remove internal file IF from the file system(VSFS.notes)

    - **./VSFS.py rmdir VSFS.notes ID:** Remove internal directory ID from the file system(VSFS.notes)

    - **./VSFS.py defrag VSFS.notes:** Defragment the file system(VSFS.notes), removing all deleted entries 

4) To check if the changes were applied, open the notes file using your favourite editor eg.nano.