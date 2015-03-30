#include <Python.h>
#include "jump.h"

static PyObject *
jump_hash(PyObject *self, PyObject *args)
{
    uint64_t key;
    int32_t num_buckets;

    if (!PyArg_ParseTuple(args, "li", &key, &num_buckets)) {
        return NULL;
    }

    if (num_buckets < 1 ) {
        PyErr_SetString(PyExc_ValueError, "num_buckets must be greater than 0");
        return NULL;
    }

    int32_t h = JumpConsistentHash(key, num_buckets);
    return Py_BuildValue("i", h);
}

static PyMethodDef JumpMethods[] = {
    {"hash", jump_hash, METH_VARARGS, "Jump Consistent Hash"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef jumpmodule = {
    PyModuleDef_HEAD_INIT,
    "jump",
    NULL,
    -1,
    JumpMethods
};

PyMODINIT_FUNC
PyInit__jump(void)
{
    return PyModule_Create(&jumpmodule);
}
