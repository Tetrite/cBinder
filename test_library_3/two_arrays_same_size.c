#include "two_arrays_same_size.h"
#include "single_array.h"
#include <stdlib.h>

int sum_of_two_arrays(int n, int* in_arr1, int* in_arr2) {

    int sum = 0;
    sum += sum_of_array(n, in_arr1);
    sum += sum_of_array(n, in_arr2);
    return sum;
}

int sum_of_two_arrays_constant_size(int* in_arr1, int* in_arr2){
    int sum = 0;
    sum += sum_of_array_constant(in_arr1);
    sum += sum_of_array_constant(in_arr2);
    return sum;
}

int double_the_values_inside_two_arrays(int n, int* in_out_arr1, int* in_out_arr2){
    double_the_values_inside_array(n, in_out_arr1);
    double_the_values_inside_array(n, in_out_arr2);
    return 0;
}

int fill_two_arrays_with_twos(int n, int* out_arr1, int* out_arr2){
    fill_array_with_twos(n, out_arr1);
    fill_array_with_twos(n, out_arr2);
    return 0;
}

int reverse_array_order(int n, int* in_order, int* reverse_order ){

    int j = n-1;
	for(int i=0; i<n; i++){
		reverse_order[i] = in_order[j];
		j--;
	}
	return 0;
}

int reverse_both_arrays_order(int n, int* in_order, int* reverse_order ){

    int * copy = (int*) malloc(n*sizeof(int));
    for(int i=0; i<n; i++){
        copy[i] = in_order[i];
    }
    reverse_array_order(n, copy, in_order);
    reverse_array_order(n, copy, reverse_order);
    return 0;
}

int array_adding(int n, int* array_1, int* array_2 ) {

    for(int i=0; i<n; i++){
        array_2[i] = array_1[i] + array_2[i];
    }
    return 0;
}