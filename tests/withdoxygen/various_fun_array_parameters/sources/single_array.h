/* -------------------------  SINGLE ARRAYS TEST CASES ------------------------- */
#define ARR_SIZE 5
/**
  * Case 1: there is only one IN array
  * The function returns sum of one array
  * @param[in]   n         number of elements in array
  * @param[in]   in_arr   sample array (array of size n)
  * @return                sum of elements
  */

int sum_of_array(int n, int* in_arr);

/**
  * Case 2: there is only one IN array - size defined as constant
  * The function returns sum of one array
  * @param[in]   in_arr   sample array (array of size ARR_SIZE)
  * @return                sum of elements
  */

int sum_of_array_constant(int* in_arr);

/**
  * Case 3: there is only one IN/OUT array
  * The function doubles the values of an array
  * @param[in]   n         number of elements in array
  * @param[in,out]   in_out_arr   sample array (array of size n)
  * @return                sum of elements
  */

int double_the_values_inside_array(int n, int* in_out_arr);

/**
  * Case 4: there is only one OUT array
  * The function fills the array with integer=2 constant value
  * @param[in]   n         number of elements in array
  * @param[out]   out_arr   sample array (array of size n)
  * @return                sum of elements
  */

int fill_array_with_twos(int n, int* out_arr);