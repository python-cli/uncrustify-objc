#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import subprocess
import click
import pathspec
import distutils.spawn

showVerbose = False
dry_run_option = False
git_changed_only = False
cfg_config_file = 'uncrustify.cfg'
current_ignore_file = 'uncrustify_ignore'


def run_uncrustify(path):
    try:
        executable = distutils.spawn.find_executable('uncrustify')

        if executable is None:
            click.secho('uncrustify is required!\n\n'
                        'Go to install it first and make sure it could be found in your $PATH.\n'
                        'https://github.com/uncrustify/uncrustify', fg='red')
            return False

        cmd = executable + ' -c ' + cfg_config_file + ' -l OC --no-backup ' + path
        p = subprocess.Popen(['/bin/sh', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        ret_code = p.wait()

        if showVerbose:
            str_output = p.stdout.read()
            if len(str_output) > 0:
                click.echo(click.style('\Output:\n%s' % str_output, fg='green'))

        if ret_code == 0:
            pass  # Succeed!
        elif ret_code == 1:
            pass  # Suppress this warning message from uncrustify. https://github.com/uncrustify/uncrustify/issues/857
        elif ret_code > 0:
            str_error = p.stderr.read()

            if len(str_error) > 0:
                click.echo(click.style('\nError:\n%s' % str_error, fg='red'))
        else:
            pass # siglal, suppressed by click

    except Exception, e:
        click.echo(click.style('\nException:\n%s' % e, fg='red'))
        return False
    else:
        return True


def get_changed_files(root_dir):
    try:
        executable = distutils.spawn.find_executable('git')

        if executable is None:
            click.secho('git is missing in the envionment paths!', fg='red')
            return []

        cmd = executable + ' -C "' + os.path.abspath(root_dir) + '" status --short'
        p = subprocess.Popen(['/bin/sh', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ret_code = p.wait()

        if ret_code == 0:
            str_output = p.stdout.read()

            if str_output:
                # https://git-scm.com/docs/git-status
                file_list = []

                for line in str_output.splitlines():
                    # Get the relative file path
                    path = line[3:]
                    # Use the the new file path if rename/copy mode exist
                    idx = path.find('->')
                    if idx != -1:
                        path = path[idx + 2:]
                    # Strip the quoted string literal if whitespace or other nonprintable characters exist
                    path = path.strip(' "\'')
                    # Convert to the full file path
                    path = os.path.abspath(os.path.join(root_dir, path))

                    assert os.path.exists(path)
                    file_list.append(path)

                return file_list

        elif ret_code > 0:
            str_error = p.stderr.read()

            if len(str_error) > 0:
                click.echo(click.style('\nError:\n%s' % str_error, fg='red'))
        else:
            pass # siglal, suppressed by click

    except Exception, e:
        click.echo(click.style('\nException:\n%s' % e, fg='red'))

    return []


def formatcode(root_dir):
    target_files = None

    if git_changed_only:
        allfiles = get_changed_files(root_dir)
        target_files = filter((lambda x: os.path.splitext(x)[1] in ['.h', '.m', '.mm']), allfiles)
    else:
        all_spec = pathspec.PathSpec.from_lines('gitwildmatch', ['*.h', '*.m', '*.mm'])
        allfiles = list(all_spec.match_tree(root_dir))
        allfiles = map((lambda x: os.path.join(root_dir, x)), allfiles)

        if showVerbose:
            click.echo("Found total items: %d" % len(allfiles))

        ignore_spec_list = []
        ignore_global_file = os.path.expanduser('~/.uncrustify/uncrustify_ignore_global')

        if os.path.exists(ignore_global_file):
            with open(ignore_global_file, 'r') as file:
                ignore_spec_list.extend(file.read().splitlines())

        if current_ignore_file is not None and os.path.exists(current_ignore_file):
            with open(current_ignore_file, 'r') as file:
                ignore_spec_list.extend(file.read().splitlines())

        ignore_spec = pathspec.PathSpec.from_lines(pathspec.GitIgnorePattern, ignore_spec_list)
        blacklist = set(ignore_spec.match_files(allfiles))

        if showVerbose:
            click.echo("Found items to be ignored: %d" % len(blacklist))

        def check_in_blacklist(item):
            for i in blacklist:
                if item.find(i) >= 0:
                    return False
            return True

        target_files = filter(check_in_blacklist, allfiles)

    if len(target_files) <= 0:
        return False

    if showVerbose:
        click.echo("Formatting on %d items..." % len(target_files))

    if dry_run_option:
        cur_dir = os.getcwd()

        for item in target_files:
            click.echo("Formatting on %s" % os.path.relpath(item, cur_dir))
        return True

    concate_files = reduce((lambda x, y: x + ' ' + y), target_files)
    return run_uncrustify(concate_files)


@click.command()
@click.argument('project_path', default='.', metavar='PROJECT_PATH',
                type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.option('--cfg-file', '-c', type=click.Path(exists=True, dir_okay=False, file_okay=True),
                            envvar='CFG_FILE', metavar='CFG_FILE',
                            help='The CFG config file used to format.')
@click.option('--ignore-file', '-i', type=click.Path(exists=True, dir_okay=False, file_okay=True),
              envvar='IGNORE_FILE', metavar='IGNORE_FILE',
              help='The ignore file used to ignore the matching files for formatting.')
@click.option('--git-only', '-g', is_flag=True, default=False,
              help='Format the current git staged and unstaged files only.')
@click.option('--dry-run', '-n', is_flag=True, default=False,
              help='Do not format any files, but show a list of files to be formatted.')
@click.option('--verbose', '-v', is_flag=True, default=False,
              help='Enables verbose mode.')
def cli(project_path, cfg_file, ignore_file, git_only, dry_run, verbose):
    """
    uncrustify-obj is used to format the objective-c files under the specified project path.

    For the uncrustify.cfg config file, it will search it recursively from the project directory
    to its top parent directory. If none, the ~/uncrustify.cfg or ~/.uncrustify/uncrustify.cfg
    will be assumed to use.

    Configure the uncrustify_ignore in the project path to make a path blacklist which matched
    items will not be formatted. It uses the gitignore file template, more documentation could
    be found from https://git-scm.com/docs/gitignore.

    By default, it will search the ignore file from the project path, if not specify with
    --ignore-file. Besides, there is a global ignore file located
    ~/.uncrustify/uncrustify_ignore_global which will be combined to the target ignore spec.

    If the project path is under the git version control, passing the --git-only option will
    make the changed source files to be used as source file list, the ignore files will be
    omitted because the git-scm already used the gitignore spec.

    Highly recommend you to make a shell alias like
    `alias uncrustify-objc='uncrustify-objc --git-only'`.
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
                cfg_file = os.path.join(os.path.expanduser(
                    '~/.uncrustify'), cfg_config_file)

                if not os.path.exists(cfg_file):
                    raise click.ClickException(
                        'Not found the %s file!' % cfg_config_file)

        cfg_config_file = cfg_file
    else:
        cfg_config_file = os.path.abspath(cfg_file)

    global current_ignore_file

    if ignore_file is None:
        ignore_file = os.path.join(project_path, current_ignore_file)

        if not os.path.exists(ignore_file):
            ignore_file = None

        current_ignore_file = ignore_file
    else:
        current_ignore_file = os.path.abspath(ignore_file)

    global showVerbose, dry_run_option, git_changed_only
    showVerbose = verbose
    dry_run_option = dry_run
    git_changed_only = git_only

    if showVerbose:
        click.echo('Working on project: %s\nCFG file: %s\nIgnore spec: %s\n' %
            (project_path, cfg_config_file, current_ignore_file))

    if formatcode(project_path):
        click.echo('\x1b[5;32m\033[1mAwesome!\033[0m\x1b[0m')
