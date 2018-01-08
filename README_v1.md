# uncrustify_ocproject

> This script tool is used for formatting code for Objective-C language project. Since the [BBUncrustifyPlugin-Xcode](https://github.com/benoitsan/BBUncrustifyPlugin-Xcode/issues/137) plugin doesn't work in Xcode 9 anymore. It seems there are not any Xcode plugin based on [*Source Editor Extension*](https://developer.apple.com/documentation/xcodekit/creating_a_source_editor_extension) like [ClangFormat-Xcode](https://github.com/travisjeffery/ClangFormat-Xcode), what a pity!



## Environment

* macOS 10.12.6 or later

* Python 2.7.x

* [uncrustify](https://github.com/uncrustify/uncrustify)

  * Highly recommend you compile the uncrustify executable binary file with the latest source code.

  * Run the command after downloading the source project.
    ```shell
     mkdir build && cd build/
     cmake -G Xcode .. -DCMAKE_BUILD_TYPE=Release
    ```
    Open the `uncrustify.xcodeproj` project and switch the `uncrustify` target, it'd better compile the release version via switching the `Edit scheme` -> `Run` -> `Info` -> `Build Configuration`.
  * `cp Release/uncrustify /usr/local/bin`


## Usage

```shell
./uncrustify.py -h
usage: uncrustify.py [-h] [-v] [-d ROOT_DIR] [-c CFG_CONFIG_FILE]
                     [-p PLIST_CONFIG_FILE]

Format code with uncrustify for Objective-C project.

optional arguments:
  -h, --help            show this help message and exit
  -v                    output the verbose log
  -d ROOT_DIR           a valid directory path points to source code project.
  -c CFG_CONFIG_FILE    a config file path point to uncrustify.cfg file for
                        formatting.
  -p PLIST_CONFIG_FILE  a plist config file used for path management.
```

> ROOT_DIR: All the subdirectories including itself will be counted in.
>
> CFG_CONFIG_FILE: Point to uncrustify configuration file.
>
> PLIST_CONFIG_FILE: The plist file maintains the working directories for formatting. Ignore the 3rd party code file directories, add the files or directories under the blacklist directories to the whitelist node if needed, it depends on your project requirement.

By default, the command `./uncrustify.py` assumes that the file `uncrustify.cfg` and `uncrustify_path.plist` under the *current working directory*.

Highly recommend you to track this files in your version control. :)



## Author

Will Han, xingheng.hax@qq.com



## License

MIT license.