
#include "ExampleClass.h"

#include <iostream>

ExampleClass::ExampleClass() {
    // Empty constructor
}


ExampleClass::~ExampleClass() {
    // Empty destructor
}


void ExampleClass::print_string(const string& str) const {
    cout << "String from python: " << str << endl;
}