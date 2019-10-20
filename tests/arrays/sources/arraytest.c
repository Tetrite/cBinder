#include "arraytest.h"

void func(double out[]){
    for(int i=0;i<5;i++){
        out[i] = i;
    }
}

double sum(double a, double out[]){
    double s = a;
	for(int i=0;i<5;i++){
        s += out[i];
    }
	return s;
}