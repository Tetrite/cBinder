#include "single_array.h"

int sum_of_array(int n, int* in_arr){
    int sum = 0;
    for(int i=0; i<n; i++){
        sum += in_arr[i];
    }
    return sum;
}

int sum_of_array_constant(int* in_arr){
    int sum = 0;
    for(int i=0; i<ARR_SIZE; i++){
        sum += in_arr[i];
    }
    return sum;
}


int double_the_values_inside_array(int n, int* in_out_arr){

    for(int i=0; i<n; i++){
        in_out_arr[i] = in_out_arr[i] * 2;
    }
    return 0;
}


int fill_array_with_twos(int n, int* out_arr){

    for (int i=0; i<n; i++){
        out_arr[i] = 2;
    }
    return 0;
}