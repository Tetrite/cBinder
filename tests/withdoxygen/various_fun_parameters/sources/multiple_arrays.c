#include "complex_example.h"
#include <stdlib.h>


int array_adding_result_in_separate(int n, int* a, int* b, int* c);

    for(int i=0; i<n; i++){
        c[i] = a[i] + b[i];
    }
    return 0;
}


int get_first_n_elems(int n_1, int n_2,
                int* array_1, int* array_2,
                int* array_result_1, int* array_result_2) {

    // Get array_1 and rewrite its first n_2 elements into array_result_1, 0s beyond index n_1 -1
    // Also, get array_2 and rewrite its first n_2 elements into array_result_2, 0s beyond index n_1 -1
    for(int i=0; i<n_2;i++){
        if(i<n_1){
            array_result_1[i] = array_1[i];
            array_result_2[i] = array_2[i];
        }
        else {
            array_result_1[i] = 0;
            array_result_2[i] = 0;
        }
    }
    return 0;
}

int combine_arrays(int n_1, int n_2, int* array_in_1, int* array_out, int* array_in_2) {

    //Calculate the sum of array_in_2 elements:
    int sum = 0;
    for (int i=0; i<n_2; i++){
        sum += array_in_2[i];
    }
    //Fill the array_out
    for (int i=0; i<n_1; i++){
        array_out[i] = array_in_1[i] + sum;
    }
    return 0;
}