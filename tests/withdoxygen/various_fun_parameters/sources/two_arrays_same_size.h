/* -------------------------  TWO ARRAYS OF THE SAME TYPE, SAME SIZE  ------------------------- */
#define ARR_SIZE 5
/**
  * Case 1: there are two IN arrays of the same size - parameter
  * The function sums the values of two separate arrays and returns it
  * @param[in]   n         number of elements in array
  * @param[i]   in_arr1   sample array (array of size n)
  * @param[i]   in_arr2   sample array (array of size n)
  * @return                sum of elements
  */

int sum_of_two_arrays(int n, int* in_arr1, int* in_arr2);

/**
  * Case 2: there are two IN arrays of the same size - constant
  * The function sums the values of two separate arrays and returns it
  * @param[i]   in_arr1   sample array (array of size ARR_SIZE)
  * @param[i]   in_arr2   sample array (array of size ARR_SIZE)
  * @return                sum of elements
  */

int sum_of_two_arrays_constant_size(int* in_arr1, int* in_arr2);

/**
  * Case 3: there are two IN,OUT arrays of the same size
  * The function doubles the values of two separate arrays
  * @param[in]   n         number of elements in array
  * @param[in,out]   in_out_arr1   sample array (array of size n)
  * @param[in,out]   in_out_arr2   sample array (array of size n)
  * @return                sum of elements
  */

int double_the_values_inside_two_arrays(int n, int* in_out_arr1, int* in_out_arr2);

/**
  * Case 4: there are two OUT arrays of the same size
  * The function fills the arrays with integer==2 constant value
  * @param[in]   n         number of elements in array
  * @param[out]   in_out_arr   sample array (array of size n)
  * @return                sum of elements
  */

int fill_two_arrays_with_twos(int n, int* out_arr1, int* out_arr2);

/* -------------------------  TWO ARRAYS OF THE SAME TYPE, SAME SIZE END  ------------------------- */

/* -------------------------  TWO ARRAYS OF DIFFERENT TYPES, SAME SIZE  ------------------------- */

/**
  * Case 1: there are two arrays: one IN and one OUT
  * The function takes values from IN array and writes it into OUT array in reversed order
  * @param[in]   n   size of an array
  * @param[in]   in_order   sample array (array of size n)
  * @param[out]  reverse_order    sample reversed array (array of size n)
  * @return                status
  */

int reverse_array_order(int n, int* in_order, int* reverse_order );

/**
  * Case 2: there are two arrays: one IN,OUT and one OUT
  * The function takes values from IN array and writes it into OUT array in reversed order
  * it also reverses an order of IN,OUT array
  * @param[in]   n   size of an array
  * @param[in]   in_order   sample array (array of size n)
  * @param[out]  reverse_order    sample reversed array (array of size n)
  * @return                status
  */

int reverse_both_arrays_order(int n, int* in_order, int* reverse_order );

/**
  * Case 3: there are two arrays: one IN and one IN,OUT
  * The function performs for every i: arrayIN,OUT[i] = arrayIN[i] + arrayIN,OUT[i]
  * it also reverses an order of IN,OUT array
  * @param[in]   n   size of an array
  * @param[in]   array_1   sample array (array of size n)
  * @param[in,out]  array_2    sample array (array of size n)
  * @return                status
  */

int array_adding(int n, int* array_1, int* array_2);

/* -------------------------  TWO ARRAYS OF DIFFERENT TYPES, SAME SIZE END  ------------------------- */