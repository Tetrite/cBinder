# cBinder [<img src="https://travis-ci.org/Tetrite/cBinder.svg?branch=master">](https://travis-ci.org/Tetrite/cBinder)

C bindings and wrapper generator for Python using CFFI library

# Examples

## Simple C functions

- Create new directory ```my_lib``` in cBinder directory

- Create files ```test.c``` and ```test.h``` in above directory:

    ```C
    //test.h
    
    int add(int a, int b);
    
    float addF(float a, float b);
    ```
    
    ```C
    //test.c
    
    #include "add.h"
    
    int add(int a, int b){
        return a + b;
    }
    
    float addF(float a, float b){
        return a + b;
    }
    ```

- Open terminal/command prompt in cBinder directory and run following command:

    ```python main.py my_lib -f./my_lib -d./my_lib/out compile```

- Now go to ```my_lib/out``` directory. In ```dist``` directory you will find distribution packages ready to be pushed to PyPi. \
Wrapper for test functions lies in ```my_lib``` directory so open up Python terminal in there

- Test generated wrapper

    ```
    >>>import test
    >>>test.add(1,2)
    3
    >>>test.addF(1.0,2.0)
    3.0
    ```
