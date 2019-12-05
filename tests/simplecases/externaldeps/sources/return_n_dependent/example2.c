#include "example2.h"
#include <stdio.h>
#include <return_n.h>

int
print_and_return_n (int n)
{
  printf ("1 = %d", return_n(n));
  return return_n(n);
}
