# Confluence page update tool
Help to do update page info automatically.

## Project need
- Python 2.7+

## Installation
```
pip install requests
```

## Using guide

```
$ git clone git@github.com:ColaCheng/regex-replace-tool.git
$ cd regex-replace-tool/confluence-page-update-tool
$ python updatePageTool.py -h
usage: updatePageTool.py [-h] [--url URL] [--version] [--user USER]
                         [--password PASSWORD] [--pageId PAGEID]
                         [--regex REGEX] [--sub SUB]

optional arguments:
  -h, --help            show this help message and exit
  --url URL             Confluence json rpc url (default:
                        https://confluence.fuhu.org/rpc/json-rpc/confluenceservice-v2)
  --version, -v         show program's version number and exit

authentication:
  --user USER, -u USER  Confluence username (default: None)
  --password PASSWORD, -p PASSWORD
                        Confluence password (default: None)

page info:
  --pageId PAGEID       Page ID of the attachment (default: None)

regular expression:
  --regex REGEX         Regular expression statement (default: [])
  --sub SUB             Substitution (default: [])
```

## Example

```
$ python updatePageTool.py -u {USER} -p {PASSWORD} --pageId {PAGEID} --regex "<strong>Latest Version:<\/strong> \d\.\d*\.\d" --sub "<strong>Latest Version:</strong> 0.86.0" --regex "<td colspan=\"1\">0.84.0" --sub "<td colspan=\"1\">0.88.0"
```

## Result message

### success
| message | description         |
|---------|---------------------|
| SUCCESS | Update page success |

### failure
| message             | description                                         |
|---------------------|-----------------------------------------------------|
| HTTP_REQUEST_ERROR  | Http request failure                                |
| GET_PAGE_FAILURE    | Get page failure (e.g., wrong pageId)               |
| UPDATE_PAGE_FAILURE | Update page failure                                 |
| REGEX_NOT_PAIR      | Regular expression and substitution need as pairing |
| NO_REGEX            | No regular expression                               |
