
# Panda3D Module Builder

This is a prefab to create modules and extensions for the <a href="http://github.com/panda3d/panda3d">Panda3D</a> engine. It provides a cmake script to make building
and distributing your modules the matter of a single command / mouseclick.

## Requirements

- The Panda3D SDK (get it <a href="http://www.panda3d.org/download.php?sdk">here</a>)
- CMake 2.6 or higher (get it <a href="https://cmake.org/download/">here</a>)


**For compiling on Windows 32 bit:**

- Visual Studio 2010 (any version)

**For compiling on Windows 64 bit:**

- Visual Studio 2010 (any version)
- Windows SDK 7.1 (be sure to tick the VC++ 64 bit compilers)



## Usage


1. Copy the contents of this repository to a suitable path in your project
2. Move your C++ Code to the `Source/` directory.
3. To compile your module, use:

    ```
    python build.py
    ```

This will ask you for a module name the first time you run it. After that, it will generate a binary with the name `<module-name>.pyd` or `<module-name>.so` (depending on your platform) in the directory of the build script.

You can then simply import the module in python, like this:

```python
from insert_module_name_here import ExampleClass
test_class = ExampleClass()
```

There is also a small example class contained in the source directory, which shows the
basics of using interrogate.

