#!/usr/bin/env python
import os
import sys
import re
import argparse
import fileinput

def getArgument():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # optional arguments
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    # file description group
    authGroup = parser.add_argument_group('File description')
    authGroup.add_argument('--path', '-p', action='store', dest='path',
                    default=None,
                    help='Path for this file')
    authGroup.add_argument('--file', '-f', action='store', dest='file',
                    default=None,
                    help='File full name')
    # regular expression group
    releaseGroup = parser.add_argument_group('regular expression')
    releaseGroup.add_argument('--regex', action='append', dest='regex',
                        default=[],
                        help='Regular expression statement')
    releaseGroup.add_argument('--sub', action='append', dest='sub',
                        default=[],
                        help='Substitution')

    return parser.parse_args()

def multipleReplace(regexDict, content):
    # Create a regular expression from the dictionary keys
    regex = re.compile(r'%s' % "|".join(regexDict.keys()))
    return regex.sub(lambda mo: regexDict[
        [
            k for k in regexDict if re.search(k, mo.string[mo.start():mo.end()])
        ][0]],
        content
    )

def substituteContent(args, content):
    if len(args.regex) != len(args.sub):
        sys.exit("REGEX_NOT_PAIR")
    regexDict = dict(zip(args.regex, args.sub))
    if regexDict == {}:
        sys.exit("NO_REGEX")
    else:
        return multipleReplace(regexDict, content)

def main():
    args = getArgument()
    fileName = ("%s/%s") % (args.path, args.file)
    fileNameTemp = ("%s/%sTemp") % (args.path, args.file)
    fileInput = open(fileName, "r")
    fileOuput = open(fileNameTemp, "wb+")
    result = substituteContent(args, fileInput.read())
    fileOuput.write(result)
    os.remove(fileName)
    os.rename(fileNameTemp, fileName)
    fileInput.close()
    fileOuput.close()


if __name__ == '__main__':
    main()
