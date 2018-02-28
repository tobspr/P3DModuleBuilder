[![Build Status](https://travis-ci.org/tobspr/P3DModuleBuilder.svg?branch=master)](https://travis-ci.org/tobspr/P3DModuleBuilder)

# Panda3D Module Builder

This tool allows you to seamlessly mix your C++ and Python code for the 
<a href="http://github.com/panda3d/panda3d">Panda3D Game Engine</a>.

It makes compiling your C++ code the matter of a single mouse-click.


## Features

 - Automatic Python bindings using `interrogate`
 - Works on Windows, Linux and Mac

## Getting started


#### 1. Clone this repository

You can use the download-zip button, or clone this repository. Copy it to a
suitable path in your project.

#### 2. Write your source code

You can now start to write your C++ code and store it in the `source/` directory.
Here's a simple example you can start with (save it as `source/example.h` for example):

```cpp
#ifndef EXAMPLE_H
#define EXAMPLE_H

#include "pandabase.h"


BEGIN_PUBLISH // This exposes all functions in this block to python

inline int multiply(int a, int b) {
    return a * b;
}

END_PUBLISH


class ExampleClass {
    PUBLISHED: // Exposes all functions in this scope, use instead of "public:"
        inline int get_answer() {
            return 42;
        };
};


#endif EXAMPLE_H
```

#### 3. Compile the module

After you wrote your C++ code, run `python build.py`. It will ask you for
a module name, for this example we will choose "TestModule".

When the compilation finished, there should now be a `TestModule.pyd` / `TestModule.so` (depending on your platform) generated.

#### 4. Use your module

Using your compiled module is straightforward:

```python
import panda3d.core  # Make sure you import this first before importing your module

import TestModule

print(TestModule.multiply(3, 4)) # prints 12

example = TestModule.ExampleClass()
print(example.get_answer()) # prints 42

```



#### 

## Requirements

- The Panda3D SDK (get it <a href="http://www.panda3d.org/download.php?sdk">here</a>)
- CMake 2.6 or higher (get it <a href="https://cmake.org/download/">here</a>)
- windows only: The thirdparty folder installed in the Panda3D sdk folder (See <a href="https://www.panda3d.org/forums/viewtopic.php?f=9&t=18775">here</a>)


**For compiling on Windows 32 bit:**

- Visual Studio 2010/2015

**For compiling on Windows 64 bit:**

- Visual Studio 2010/2015
- Windows SDK 7.1 (be sure to tick the VC++ 64 bit compilers option)


## Advanced configuration

**Please clean up your built directories after changing the configuration! You can
do so with passing `--clean` in the command line.**


### Command Line
Command line options are:

- `--optimize=N` to override the optimize option. This overrides the option set in the `config.ini`
- `--clean` to force a clean rebuild

### config.ini
Further adjustments can be made in the `config.ini` file:

- You can set `generate_pdb` to `0` or `1` to control whether a `.pdb` file is generated.
- You can set `optimize` to change the optimization. This has to match the `--optimize=` option of your Panda3D Build.
- You can set `require_lib_eigen` to `1` to require the Eigen 3 library
- You can set `require_lib_bullet` to `1` to require the Bullet library
- You can set `require_lib_freetype` to `1` to require the Freetype library
- You can set `verbose_igate` to `1` or `2` to get detailed interrogate output (1 = verbose, 2 = very verbose)

### Additional libaries

If you want to include additional (external) libraries, you can create a
cmake file named `additional_libs.cmake` in the folder of the module builder,
which will then get included during the build.

If you would like to include the protobuf library for example, your cmake file could look like this:

```cmake
find_package(Protobuf REQUIRED)
include_directories(${PROTOBUF_INCLUDE_DIRS})
set(LIBRARIES "${LIBRARIES};${PROTOBUF_LIBRARIES}")

```

