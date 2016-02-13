
#include "dtoolbase.h"
#include "interrogate_request.h"

#include "py_panda.h"

extern LibraryDef asd_moddef;
extern void Dtool_asd_RegisterTypes();
extern void Dtool_asd_ResolveExternals();
extern void Dtool_asd_BuildInstants(PyObject *module);

#if PY_MAJOR_VERSION >= 3 || !defined(NDEBUG)
#ifdef _WIN32
extern "C" __declspec(dllexport) PyObject *PyInit_asd();
#elif __GNUC__ >= 4
extern "C" __attribute__((visibility("default"))) PyObject *PyInit_asd();
#else
extern "C" PyObject *PyInit_asd();
#endif
#endif
#if PY_MAJOR_VERSION < 3 || !defined(NDEBUG)
#ifdef _WIN32
extern "C" __declspec(dllexport) void initasd();
#elif __GNUC__ >= 4
extern "C" __attribute__((visibility("default"))) void initasd();
#else
extern "C" void initasd();
#endif
#endif

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef py_asd_module = {
  PyModuleDef_HEAD_INIT,
  "asd",
  NULL,
  -1,
  NULL,
  NULL, NULL, NULL, NULL
};

PyObject *PyInit_asd() {
  PyImport_Import(PyUnicode_FromString("panda3d.core"));
  Dtool_asd_RegisterTypes();
  Dtool_asd_ResolveExternals();

  LibraryDef *defs[] = {&asd_moddef, NULL};

  PyObject *module = Dtool_PyModuleInitHelper(defs, &py_asd_module);
  if (module != NULL) {
    Dtool_asd_BuildInstants(module);
  }
  return module;
}

#ifndef NDEBUG
void initasd() {
  PyErr_SetString(PyExc_ImportError, "asd was compiled for Python " PY_VERSION ", which is incompatible with Python 2");
}
#endif
#else  // Python 2 case

void initasd() {
  PyImport_Import(PyUnicode_FromString("panda3d.core"));
  Dtool_asd_RegisterTypes();
  Dtool_asd_ResolveExternals();

  LibraryDef *defs[] = {&asd_moddef, NULL};

  PyObject *module = Dtool_PyModuleInitHelper(defs, "asd");
  if (module != NULL) {
    Dtool_asd_BuildInstants(module);
  }
}

#ifndef NDEBUG
PyObject *PyInit_asd() {
  PyErr_SetString(PyExc_ImportError, "asd was compiled for Python " PY_VERSION ", which is incompatible with Python 3");
  return (PyObject *)NULL;
}
#endif
#endif

