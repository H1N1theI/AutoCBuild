# AutoCBuild
A small python build system I wrote to build my C++ projects. Should work on C and Obj-C.

## Why?
Because I got tired of makefiles, CMake, and whatever.

This is not nessecarily better, infact, is worse at incremental building due to the fact that I have not implemented parsing the -MM flag on GCC yet.

However, tt's simple. Really simple.

Hopefully one day, it will support proper incremental building.

## Basic Usage
Create a build.json (I would suggest copying the one in the repo and editing it) and edit until it fits your program.

Once finished, go to the directory where the build.json is located and just type `acb`.

If you need to rebuild, type `acb clean` and then `acb`, or `acb rebuild`.

Compiling for a release build is just `acb release`.

## JSON file structure.

### Output settings
`binname`: The name of the executable output.

`interbuild`: The directory where all the object files should be stored before linking.

`bindir`: The name of the directory that the executable will be dumped to, you can just use "." for the top level one.

### Generic build settings
`command`: The command that the compiler goes by.

`srcext`: The extensions your source files go by.

`incext`: The extensions your include/additional files go by.

`flags`: A list of all the flags that will be used during compilation.

`srcdir`: Where your source files are located. Will be tracked.

`includedir`: Where additional include files, such as library includes are kept. Will not be tracked.

`libs`: Libraries to hunt for, specifically, `-l{key}` style.

`extlibs`: Directory for libraries your compiler will not search for by default.

### Specific build settings
Any additional setting can be invoked via `acb {option}`

`flags`: List of flags to include for that specific setting.

`libs`: Libraries to use.

`extlibs`: External library directories, like above.

You can have as many extra configurations as you want, but keep in mind that the configuration file will be loaded at runtime.

## TODO:

- [ ]: Generate dependency information and finally implement efficient partial compilation.
- [ ]: Make config file and execution much more platform agnostic.
- [ ]: Use timestamps before hashing for more performance.