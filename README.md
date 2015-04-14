# AutoCBuild
A small python build system I wrote to build my C++ projects. Should work on C and Obj-C.

## Why?
Because I got tired of makefiles, CMake, and whatever.

This is not nessecarily better, infact, its change detection is slower and it lacks the flashy features that other build systems can (such as conditional source includes).

However, it's simple. Really simple.

And it does incremental compilation. What is there to hate?

## Basic Usage
Create a build.json (I would suggest copying the one in the repo and editing it) in the acb-config and edit until it fits your program.

Once finished, go to the directory where the build.json is located and just type `acb`.

If you need to rebuild, type `acb clean` and then `acb`, or `acb rebuild`.

Compiling for any given build configuration is just `acb {configuration}`. Make sure you have configured `acb-config/{configuration}.json` first.

If you just want to validate the files, just use `acb validate`.

## JSON file structure.

### Output settings
`binname`: The name of the executable output.

`interbuild`: The directory where all the object files should be stored before linking.

`bindir`: The name of the directory that the executable will be dumped to, you can just use "." for the top level one.

### Build settings
`command`: The command that the compiler goes by.

`srcext`: The extensions your source files go by.

`incext`: The extensions your include/additional files go by.

`flags`: A list of all the flags that will be used during compilation.

`srcdir`: Where your source files are located. Will be tracked.

`includedir`: Where additional include files, such as library includes are kept. Will not be tracked.

### Link settings
`link`: A boolean, wether this setting should link or just stop at compilation.

`libs`: Libraries to hunt for, specifically, `-l{key}` style.

`extlibs`: Directory for libraries your compiler will not search for by default.

## TODO:
  - [x] Generate dependency information and finally implement efficient partial compilation.
  - [x] Thread the compilation for more speed.
  - [x] Make config file and execution much more platform agnostic.
  - [ ] Use timestamps before hashing for more performance.
