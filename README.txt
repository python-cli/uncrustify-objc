
uncrustify-objc --help

Usage: uncrustify-objc [OPTIONS] PROJECT_PATH

  uncrustify-obj is used to format the objective-c files under the specified
  project path.

  For the uncrustify.cfg config file, it will search it recursively from the
  project directory to its top parent directory. If none, the
  ~/uncrustify.cfg or ~/.uncrustify/uncrustify.cfg will be assumed to use.

  Configure the uncrustify_ignore in the project path to make a path
  blacklist which matched items will not be formatted. It uses the gitignore
  file template, more documentation could be found from 
  https://git-scm.com/docs/gitignore.

  By default, it will search the ignore file from the project path, if not
  specify with --ignore-file. Besides, there is a global ignore file located
  ~/.uncrustify/uncrustify_ignore_global which will be combined to the
  target ignore spec.

  If the project path is under the git version control, passing the --git-
  only option will make the changed source files to be used as source file
  list, the ignore files will be  omitted because the git-scm already used
  the gitignore spec.

  Highly recommend you to make a shell alias like `alias uncrustify-objc
  ='uncrustify-objc --git-only'`.

Options:
  -c, --cfg-file CFG_FILE        The CFG config file used to format.
  -i, --ignore-file IGNORE_FILE  The ignore file used to ignore the matching
                                 files for formatting.
  -g, --git-only                 Format the current git staged and unstaged
                                 files only.
  -n, --dry-run                  Do not format any files, but show a list of
                                 files to be formatted.
  -v, --verbose                  Enables verbose mode.
  --help                         Show this message and exit.
