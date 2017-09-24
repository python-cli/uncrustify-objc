#!/usr/bin/python

import argparse
import os
import os.path
import plistlib
import subprocess
# import pdb
# pdb.set_trace()

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
    output = None

    try:
        if showVerbose:
            print 'Formatting ' + path
        with open(os.devnull, 'w') as devnull:
            subprocess.check_output('uncrustify -c ' + cfg_config_file + ' -l oc --no-backup ' + path + ' > /dev/null', shell=True, stderr=devnull)
    except subprocess.CalledProcessError, e:
        print "uncrustify exception:\n", e

    if showVerbose and output is not None:
        # print output
        pass

def formatcode(root_dir, plist_path):
    items = get_resursive_subdirectories(root_dir)

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
                    if showVerbose:
                        print y + ' ignored!'

        for x in whitelist:
            if not x in items:
                items.append(x)
                if showVebose:
                    print x + ' added!'

    except:
        print "Read file paths from plist failed!"
        return

    for item in items:
        if os.path.exists(item):
            path = item

            if os.path.isdir(path):
                if path[-1] != '/':
                    path = path + '/'

                run_uncrustify(path + '*.h')
                run_uncrustify(path + '*.m')
                #run_uncrustify(path + '*.mm') fnmatch
            else:
                run_uncrustify(path)
        else:
            print '\'%s\' not found, skipped!' % item


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
        return

    if not os.path.exists(plist_config_file):
        print plist_config_file + ' does\'t exist!'
        return

    if not os.path.exists(cfg_config_file):
        print cfg_config_file + ' does\'t exist!'
        return

    if showVerbose:
        print 'Working on ' + root_dir + ' with config file ' + plist_config_file

    formatcode(root_dir, plist_config_file)


if __name__ == "__main__":
    main()

