# uncrustify-objc

> This script tool is used for formatting code for Objective-C language project. Since the [BBUncrustifyPlugin-Xcode](https://github.com/benoitsan/BBUncrustifyPlugin-Xcode/issues/137) plugin doesn't work in Xcode 9 anymore. It seems there are not any Xcode plugin based on [*Source Editor Extension*](https://developer.apple.com/documentation/xcodekit/creating_a_source_editor_extension) like [ClangFormat-Xcode](https://github.com/travisjeffery/ClangFormat-Xcode), what a pity!
>
> See more in [pypi page](https://pypi.python.org/pypi/uncrustify-objc).



## Environment

* Python 2.7 or later.

* [uncrustify](https://github.com/uncrustify/uncrustify)

  * Highly recommend you compile the uncrustify executable binary file with the latest source code.

  * Run the command after downloading the source project.
    ```shell
     mkdir build && cd build/
     cmake -G Xcode .. -DCMAKE_BUILD_TYPE=Release
    ```
    Open the `uncrustify.xcodeproj` project and switch the `uncrustify` target, it'd better compile the release version via switching the `Edit scheme` -> `Run` -> `Info` -> `Build Configuration`.

  * `cp Release/uncrustify /usr/local/bin`, make it could be located in your `$PATH`.



## Installation

```shell
pip install uncrustify-objc
```


## Usage

```shell
➜ uncrustify-objc --help

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
```

Highly recommend you to track the `uncrustify.cfg` and `uncrustify_ignore` files in your SCM. :)


## Author

Will Han, xingheng.hax@qq.com


## License

MIT license.