#include "ex_doxygen.h"
int reverse_array_order(int* in_order, int* reverse_order){

    int n = ARRAY_SIZE;
    int j = n-1;
	for(int i=0; i<n; i++){
		reverse_order[i] = in_order[j];
		j--;
	}
	return 0;
}