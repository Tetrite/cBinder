#include <stdio.h>

#include "struct.h"

double get_b(simple_struct* s)
{
    return s->b;
}

void print(simple_struct* s)
{
    printf("%d %g %c\n", s->a, s->b, s->c);
}
