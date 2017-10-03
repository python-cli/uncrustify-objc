#!/usr/bin/python

import argparse
import sys
import os
import os.path
import plistlib
import subprocess
import glob

showVerbose = False
cfg_config_file = 'uncrustify.cfg'


def get_immediate_subdirectories(a_dir):
    return [os.path.join(a_dir, name) for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def get_resursive_subdirectories(dir):
    items = get_immediate_subdirectories(dir)

    for item in items:
        sub_items = get_immediate_subdirectories(str(item))
        items.extend(sub_items)

    return items

def run_uncrustify(path):
    matched_path = glob.glob(path)

    if len(matched_path) <= 0:
        return True

    output = None

    try:
        if showVerbose:
            print 'Formatting ' + path

        with open(os.devnull, 'w') as devnull:
            subprocess.check_output('uncrustify -c ' + cfg_config_file + ' -l OC --no-backup ' + path + ('' if showVerbose else ' -q'), shell=True, stderr=devnull)
    except subprocess.CalledProcessError, e:
        if e.returncode == 1:
            return True # Suppress the warning message from uncrustify. https://github.com/uncrustify/uncrustify/issues/857

        print "exception:\n", e.cmd, '\ncode:', e.returncode, 'output:', e.output if len(e.output) > 0 else 'None'
        return True
    else:
        return True

def formatcode(root_dir, plist_path):
    result = True
    items = get_resursive_subdirectories(root_dir)
    items.append(root_dir)

    try:
        plroot = plistlib.readPlist(plist_path)
        blacklist = plroot["Blacklist"]
        whitelist = plroot["Whitelist"]

        blacklist = map(os.path.abspath, blacklist)
        whitelist = map(os.path.abspath, whitelist)

        for x in blacklist:
            for y in items[:]:
                if y.find(x) >= 0:
                    items.remove(y)

        for x in whitelist:
            if not x in items:
                items.append(x)
                if showVebose:
                    print x + ' added!'

    except:
        print "Read file paths from plist failed!"
        return False

    for item in items:
        if os.path.exists(item):
            path = item

            if os.path.isdir(path):
                if path[-1] != '/':
                    path = path + '/'

                result &= run_uncrustify(path + '*.h')
                result &= run_uncrustify(path + '*.m')
                result &= run_uncrustify(path + '*.mm')
            else:
                result &= run_uncrustify(path)
        else:
            print '\'%s\' not found, skipped!' % item

    return result


def main():

    parser = argparse.ArgumentParser(description='Format code with uncrustify for Objective-C project.')
    parser.add_argument('-v', action='store_true', dest='showVerbose', default=False,
                        help='output the verbose log')

    parser.add_argument('-d', action='store', dest='root_dir',
                         help='a valid directory path points to source code project.')

    parser.add_argument('-c', action='store', dest='cfg_config_file',
                         help='a config file path point to uncrustify.cfg file for formatting.')

    parser.add_argument('-p', action='store', dest='plist_config_file',
                         help='a plist config file used for path management.')

    args = parser.parse_args()

    global showVerbose

    showVerbose = args.showVerbose
    root_dir = args.root_dir
    plist_config_file = args.plist_config_file

    if root_dir is None or len(root_dir) < 1:
        root_dir = '.'

    if plist_config_file is None or len(plist_config_file) < 1:
        plist_config_file = 'uncrustify_path.plist'

    if args.cfg_config_file is not None and len(args.cfg_config_file) > 1:
        global cfg_config_file
        cfg_config_file = args.cfg_config_file

    root_dir = os.path.abspath(root_dir)
    plist_config_file = os.path.abspath(plist_config_file)

    if not os.path.exists(root_dir):
        print root_dir + ' doesn\'t exist!'
        return False

    if not os.path.exists(plist_config_file):
        print plist_config_file + ' does\'t exist!'
        return False

    if not os.path.exists(cfg_config_file):
        print cfg_config_file + ' does\'t exist!'
        return False

    if showVerbose:
        print 'Working on ' + root_dir + ' with config file ' + plist_config_file

    if formatcode(root_dir, plist_config_file):
        print '''|-------------------------------|
|                               |
|\x1b[5;32m \033[1m           Awesome!          \033[0m \x1b[0m|
|                               |
|-------------------------------|'''
        return True
    else:
        print '\x1b[5;31m' + 'Oops! Something went wrong.' + '\x1b[0m'
        return False


if __name__ == "__main__":
    if not main():
        sys.exit(1)

