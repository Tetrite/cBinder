#include "chararray.h"
#include <string.h>

int get_string_length_pointer(char *the_string){
    return strlen(the_string);
}

int get_string_length_braces(char the_string[]){
    return strlen(the_string);
}

int get_sum_of_string_lengths_pointers(char **the_string, int n){
    int sum=0;
    int i = 0;
    while (i < n){
        sum += strlen(the_string[i]);
        i++;
    }
    return sum;
}

int get_sum_of_string_lengths_mix(char *the_string[], int n){
    int sum=0;
    int i = 0;
    while (i < n){
        sum += strlen(the_string[i]);
        i++;
    }
    return sum;
}