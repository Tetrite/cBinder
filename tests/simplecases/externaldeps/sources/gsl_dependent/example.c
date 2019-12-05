#include "example.h"
#include <stdio.h>
#include <gsl/gsl_sf_bessel.h>

int
print_gsl_sf_bessel_J0 (double x)
{
  double y = gsl_sf_bessel_J0 (x);
  printf ("J0(%g) = %.18e\n", x, y);
  return 0;
}
