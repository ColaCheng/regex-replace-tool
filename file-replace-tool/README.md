# File content replace tool
Help to do update file content automatically.

## Project need
- Python 2.7+

## Using guide

```
$ git clone git@github.com:ColaCheng/regex-replace-tool.git
$ cd regex-replace-tool/file-replace-tool
$ python fileReplaceTool.py -h
usage: fileReplaceTool.py [-h] [--version] [--path PATH] [--file FILE]
                          [--regex REGEX] [--sub SUB]

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit

File description:
  --path PATH, -p PATH  Path for this file (default: None)
  --file FILE, -f FILE  File full name (default: None)

regular expression:
  --regex REGEX         Regular expression statement (default: [])
  --sub SUB             Substitution (default: [])
```
