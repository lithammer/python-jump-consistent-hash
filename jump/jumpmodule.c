#include <Python.h>
#include "jump.h"

#if PY_MAJOR_VERSION >= 3
#define IS_PY3K
#endif

static PyObject *
jump_hash(PyObject *self, PyObject *args)
{
    uint64_t key;
    int32_t num_buckets;

    if (!PyArg_ParseTuple(args, "Li", &key, &num_buckets)) {
        return NULL;
    }

    if (num_buckets < 1) {
        PyErr_SetString(PyExc_ValueError, "num_buckets must be a positive number");
        return NULL;
    }

    int32_t h = JumpConsistentHash(key, num_buckets);
    return Py_BuildValue("i", h);
}

static PyMethodDef JumpMethods[] = {
    {"hash", jump_hash, METH_VARARGS, "Jump Consistent Hash"},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef jumpmodule = {
    PyModuleDef_HEAD_INIT,
    "jump",
    NULL,
    -1,
    JumpMethods
};

PyMODINIT_FUNC
PyInit__jump(void)
#else
void
init_jump(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
    return PyModule_Create(&jumpmodule);
#else
    (void) Py_InitModule("_jump", JumpMethods);
#endif
}
