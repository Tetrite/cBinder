typedef enum
{
    A, B, C=123
} SomeEnum;

enum
{
    UNNAMED_0, UNNAMED_1
};

int some_enum_to_int(SomeEnum v);
void print_unnamed_enum_value(int v);

enum ProblemEnum{
    D, E, F=123
};
