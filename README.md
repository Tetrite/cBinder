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
Wrapper for test functions lies in ```my_lib``` directory

- Open up Python terminal in ```my_lib/out``` directory

- Test generated wrapper

    ```
    >>>import my_lib.test
    >>>my_lib.test.add(1,2)
    3
    >>>my_lib.test.addF(1.0,2.0)
    3.0
    ```

# To use cBinder to compile libamtrack project on Unix:

libamtrack with corrected doxygen comments:
https://github.com/certaindividual/library

Copy these external dependencies:  
libgsl  
libgslcblas  

Use this call:  
libamtrack                                {name of output folder}   
-f    
/some-path..../libamtrack/library/src     {.c files}   
-f   
/some-path..../libamtrack/library/include  {.h files}   
-d   
some-results-path                           {path to folder with results}   
-es   
path-to-export symbols                      {path to export symbols list}   
-mono                                       {create one file}  
libAT                                       {name of final library}  
compile                                     {compiling mode}  
-i  
path-to-external-dependencies-headers    (libgsl, libgslcblas)  
-i  
path-to-libamtrack-headers  
-b  
path-to-external-dependencies-libraries (libgsl, libgslcblas)  
-l  
gsl  
-l  
gslcblas  
-l  
m  
