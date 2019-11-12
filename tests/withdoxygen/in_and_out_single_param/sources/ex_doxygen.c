#include "ex_doxygen.h"
#include "stdlib.h"
int reverse_array_order(int n, int* array){

    int j = n-1;
    int * array_tmp = (int*)malloc(n*sizeof(int));
    for(int i=0; i<n; i++){
		array_tmp[i] = array[j];
		j--;
	}
	for(int i=0; i<n; i++){
		array[i] = array_tmp[i];
	}
	return 0;
}