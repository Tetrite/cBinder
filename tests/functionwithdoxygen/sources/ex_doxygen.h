#include "returntype.h"
/**
  * Returns Z for given elemental symbols
  * @param[in]   n         number of elements in arrays
  * @param[in]   in_order   sample array (array of size n)
  * @param[out]  reverse_order    sample reversed array (array of size n)
  * @return                status
  */

int reverse_array_order( const int n,
		int* in_order,
		int reverse_order[] );