#include <stdio.h>

#include "struct.h"

double get_b(simple_struct* s)
{
    return s->b;
}

void increment_b(simple_struct* s)
{
    s->b += 1.0;
}

double get_b_value(simple_struct s)
{
    return s.b;
}

double get_b_sum(simple_struct s[])
{
    double sum = 0.0;
    for (int i = 0; i < 2; ++i) sum += s[i].b;
    return sum;
}


void print(simple_struct* s)
{
    printf("%d %g %c\n", s->a, s->b, s->c);
}
