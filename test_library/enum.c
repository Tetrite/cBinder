#include "enum.h"

#include <stdio.h>

int some_enum_to_int(SomeEnum v)
{
    return (int)v;
}

void print_unnamed_enum_value(int v)
{
    printf("%d", v);
}
