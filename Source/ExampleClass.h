#ifndef EXAMPLE_CLASS_H
#define EXAMPLE_CLASS_H

#include "pandabase.h"

class ExampleClass {

    PUBLISHED:

        ExampleClass();
        ~ExampleClass();

        inline int multiply(int a, int b);
        void print_string(const string& str);

};


// Inline functions are defined in a seperate file
#include "ExampleClass.I"

#endif // EXAMPLE_CLASS_H
