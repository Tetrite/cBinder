/**
  * Case 1: there are three arrays: two IN, and one OUT, same size
  * The function multiply array adds a to b and result is in c
  * @param[in]   n   size of an array
  * @param[in]   a   sample array (array of size n)
  * @param[in]   b    sample array (array of size n)
  * @param[out]  c    sample array (array of size n)
  * @return                status
  */

int array_adding_result_in_separate(int n, int* a, int* b, int* c);

/**
  * Case 2: there are four arrays: two IN, and two OUT, different sizes
  * The function takes two arrays of size n_1: array_1 and array_2
  * and returns in:
  *   - array_result_1 accordingly, n_2 first elements of array_1, 0s for indexes beyond n_1 -1
  *   - array_result_2 accordingly, n_2 first elements of array_2, 0s for indexes beyond n_2 -1
  * @param[in]   n_1   size of an array
  * @param[in]   n_2   size of an array
  * @param[in]   array_1   sample array (array of size n_1)
  * @param[in]   array_2    sample array (array of size n_1)
  * @param[out]  array_result_1    sample array (array of size n_2)
  * @param[out]  array_result_2    sample array (array of size n_2)
  * @return                status
  */

int get_first_n_elems(int n_1, int n_2,
                int* array_1, int* array_2,
                int* array_result_1, int* array_result_2);

/**
  * Case 3: there are three arrays:
  *      - two arrays of the same size, one IN and one OUT (array_in_1, and array_out)
  *      - one array of a different size, IN (array_in_2)
  * The function adds to every element of array_in_1, sum of elements in array_in_2,
  * and rewrites these sums into OUT array: array_out
  * @param[in]   n_1   size of an array
  * @param[in]   n_2   size of an array
  * @param[in]   array_in_1   sample array (array of size n_1)
  * @param[out]   array_out    sample array (array of size n_1)
  * @param[int]  array_in_2    sample array (array of size n_2)
  * @return                status
  */

int combine_arrays(int n_1, int n_2,
                int* array_1, int* array_2,
                int* array_result_1, int* array_result_2);