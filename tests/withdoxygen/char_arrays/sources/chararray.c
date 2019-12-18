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


int fill_with_agh_2D(char *the_string[], int n){
    for(int i=0; i<n; i++){
        the_string[i] = "agh";
    }
    return 0;
}


int fill_with_agh_pointer(char *the_string){
    char * tmp = "agh";
    strcpy(the_string, tmp);
    return 0;
}


int fill_with_agh_brackets(char the_string[]){
    char * tmp = "agh";
    strcpy(the_string, tmp);
    return 0;
}