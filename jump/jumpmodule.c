#include <Python.h>
#include "jump.h"

#if PY_MAJOR_VERSION >= 3
#define IS_PY3K
#endif

PyDoc_STRVAR(doc_hash, "Generate a number in the range [0, num_buckets).\n\n\
This function uses C bindings for speed.\n\n\
Args:\n\
    key (int): The key to hash.\n\
    num_buckets (int): Number of buckets to use.\n\n\
Returns:\n\
    The bucket number `key` computes to.\n\n\
Raises:\n\
    ValueError: If `num_buckets` is not a positive number.\n");

PyDoc_STRVAR(doc_jump, "Fast, minimal memory, consistent hash algorithm.");

static PyObject *jump_hash(PyObject *self, PyObject *args) {
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

static PyMethodDef JumpMethods[] = {{"hash", jump_hash, METH_VARARGS, doc_hash},
                                    {NULL, NULL, 0, NULL}};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef jumpmodule = {PyModuleDef_HEAD_INIT, "jump", doc_jump,
                                        -1, JumpMethods};

PyMODINIT_FUNC PyInit__jump(void)
#else
void init_jump(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
  return PyModule_Create(&jumpmodule);
#else
  (void)Py_InitModule3("_jump", JumpMethods, doc_jump);
#endif
}
