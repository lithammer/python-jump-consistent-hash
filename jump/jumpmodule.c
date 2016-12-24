#include <Python.h>

#include "jump.h"

#if PY_MAJOR_VERSION >= 3
#define IS_PY3K
#endif

PyDoc_STRVAR(hash__doc__, "hash(key, num_buckets) -> int\n\
\n\
Generate a number in the range [0, num_buckets).\n\
\n\
This function uses C bindings for speed.\n\
\n\
Args:\n\
    key (int): The key to hash.\n\
    num_buckets (int): Number of buckets to use.\n\
\n\
Returns:\n\
    The bucket number `key` computes to.\n\
\n\
Raises:\n\
    ValueError: If `num_buckets` is not a positive number.\n");

PyDoc_STRVAR(jump__doc__, "Fast, minimal memory, consistent hash algorithm.");

static PyObject *jump_hash(PyObject *self, PyObject *args) {
  uint64_t key;
  int32_t num_buckets, h;

  if (!PyArg_ParseTuple(args, "Li", &key, &num_buckets)) {
    return NULL;
  }

  if (num_buckets < 1) {
    PyErr_SetString(PyExc_ValueError, "num_buckets must be a positive number");
    return NULL;
  }

  h = JumpConsistentHash(key, num_buckets);
  return Py_BuildValue("i", h);
}

static PyMethodDef JumpMethods[] = {
    {"hash", jump_hash, METH_VARARGS, hash__doc__}, {NULL, NULL, 0, NULL}};

#ifdef IS_PY3K
static struct PyModuleDef jumpmodule = {PyModuleDef_HEAD_INIT, "jump",
                                        jump__doc__, -1, JumpMethods};

PyMODINIT_FUNC PyInit__jump(void)
#else
void init_jump(void)
#endif
{
#ifdef IS_PY3K
  return PyModule_Create(&jumpmodule);
#else
  (void)Py_InitModule3("_jump", JumpMethods, jump__doc__);
#endif
}
