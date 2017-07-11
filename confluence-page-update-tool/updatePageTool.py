#!/usr/bin/env python
import sys
import requests
import argparse
import json
import re

url = "https://confluence.xxx.com/rpc/json-rpc/confluenceservice-v2"

def getArgument():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # optional arguments
    parser.add_argument('--url', action='store', dest='url',
                        default=url,
                        help='Confluence json rpc url')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    # authentication group
    authGroup = parser.add_argument_group('authentication')
    authGroup.add_argument('--user', '-u', action='store', dest='user',
                    default=None,
                    help='Confluence username')
    authGroup.add_argument('--password', '-p', action='store', dest='password',
                        default=None,
                        help='Confluence password')
    # page info group
    pageGroup = parser.add_argument_group('page info')
    pageGroup.add_argument('--pageId', action='store', dest='pageId',
                        default=None,
                        help='Page ID of the attachment')
    # regular expression group
    releaseGroup = parser.add_argument_group('regular expression')
    releaseGroup.add_argument('--regex', action='append', dest='regex',
                        default=[],
                        help='Regular expression statement')
    releaseGroup.add_argument('--sub', action='append', dest='sub',
                        default=[],
                        help='Substitution')

    return parser.parse_args()

def getPageResult(args):
    payload = "{\"jsonrpc\":\"2.0\",\"method\":\"getPage\",\"params\":[\"%s\"],\"id\": 1}" % (args.pageId)
    headers = {
        'content-type': "application/json"
    }
    response = requests.post(args.url, auth=(args.user, args.password), data=payload, headers=headers, verify=False)
    if response.status_code != 200:
        sys.exit("HTTP_REQUEST_ERROR")
    data = json.loads(response.text)
    if "result" in data:
        return data["result"]
    else:
        sys.exit("GET_PAGE_FAILURE")

def multipleReplace(regexDict, content):
  # Create a regular expression from the dictionary keys
  regex = re.compile(r'%s' % "|".join(regexDict.keys()))
  return regex.sub(lambda mo: regexDict[
      [ k for k in regexDict if
      re.search(k, mo.string[mo.start():mo.end()])
      ][0]], content)

def substituteContent(args, content):
    if len(args.regex) != len(args.sub):
        sys.exit("REGEX_NOT_PAIR")
    regexDict = dict(zip(args.regex, args.sub))
    if regexDict == {}:
        sys.exit("NO_REGEX")
    else:
        return multipleReplace(regexDict, content)

def storePage(args, pageResult):
    params = {
        'id': pageResult["id"],
        'space': pageResult["space"],
        'title': pageResult["title"],
        'content': substituteContent(args, pageResult["content"]),
        'version': pageResult["version"]
    }
    payload = "{\"jsonrpc\":\"2.0\",\"method\":\"storePage\",\"params\":%s,\"id\": 1}" % (json.dumps(params))
    headers = {
        'content-type': "application/json"
    }
    response = requests.post(args.url, auth=(args.user, args.password), data=payload, headers=headers, verify=False)
    if response.status_code != 200:
        sys.exit("HTTP_REQUEST_ERROR")
    data = json.loads(response.text)
    if "result" in data:
        print "SUCCESS"
    else:
        sys.exit("UPDATE_PAGE_FAILURE")

def main():
    args = getArgument()
    pageResult = getPageResult(args)
    storePage(args, pageResult)


if __name__ == '__main__':
    main()
