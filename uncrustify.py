#!/usr/bin/python

import argparse
import sys
import os
import os.path
import plistlib
import subprocess
import glob
import click

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


@click.command()
@click.argument('project_path', default='.', metavar='PROJECT_PATH',
                            type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.option('--cfg-file', '-c', type=click.Path(exists=True, dir_okay=False, file_okay=True),
                            envvar='CFG_FILE', metavar='CFG_FILE',
                            help='The CFG config file used to format.')
@click.option('--path-file', '-p', type=click.Path(exists=True, dir_okay=False, file_okay=True),
                            envvar='PATH_FILE', metavar='PATH_FILE',
                            help='The path config file used to maintain the file lists.')
@click.option('--git-only', '-g', is_flag=True, default=False,
                            help='Format the current git staged and unstaged files only.')
@click.option('--dry-run', '-n', is_flag=True, default=False,
                            help='Do not format any files, but show a list of files to be formatted.')
@click.option('--verbose', '-v', is_flag=True, default=False,
                            help='Enables verbose mode.')
def cli(project_path, cfg_file, path_file, git_only, dry_run, verbose):
    """
    uncrustify-obj is used to format the objective-c files under the specified project path.
    
    For the uncrustify.cfg config file, it will search it recrussivly from the project directory
    to its top parent directory. If none, the ~/uncrustify.cfg or ~/.uncrustify/uncrustify.cfg
    will be assumed to use.
    """
    
    project_path = os.path.abspath(project_path)

    def get_cfg_file(cfg_dir):
        cfg_path = os.path.join(cfg_dir, cfg_config_file)

        if os.path.exists(cfg_path):
            return cfg_path

        if cfg_dir == '/':
            return None

        cfg_dir = os.path.dirname(cfg_dir)

        return get_cfg_file(cfg_dir)

    global cfg_config_file
    
    if cfg_file is None:
        cfg_file = get_cfg_file(project_path)
        
        if cfg_file is None:
            cfg_file = os.path.join(os.path.expanduser('~'), cfg_config_file)
            
            if not os.path.exists(cfg_file):
                cfg_file = os.path.join(os.path.expanduser('~/.uncrustify'), cfg_config_file)

                if not os.path.exists(cfg_file):
                    raise click.ClickException('Not found the %s file!' % cfg_config_file)

        cfg_config_file = cfg_file
    else:
        cfg_config_file = os.path.abspath(cfg_file)

    click.echo(project_path)
    click.echo(cfg_config_file)
    click.echo(path_file)
    click.echo(verbose)
    
    
