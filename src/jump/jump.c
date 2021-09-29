#include <stddef.h>
#include <stdint.h>

#include <Python.h>

static int32_t jump_consistent_hash(uint64_t key, int32_t num_buckets)
{
	int64_t b = -1, j = 0;

	while (j < num_buckets) {
		b = j;
		key = key * 2862933555777941757ULL + 1;
		j = (b + 1) * ((double)(1LL << 31) / (double)((key >> 33) + 1));
	}

	return (int32_t)b;
}

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

static PyObject *jump_hash(PyObject *self, PyObject *args)
{
	uint64_t key;
	int32_t num_buckets;

	if (!PyArg_ParseTuple(args, "Ki", &key, &num_buckets))
		return NULL;

	if (num_buckets < 1) {
		PyErr_Format(PyExc_ValueError,
			     "'num_buckets' must be a positive number, got %d",
			     num_buckets);
		return NULL;
	}

	return Py_BuildValue("i", jump_consistent_hash(key, num_buckets));
}

static PyMethodDef jump_methods[] = { { "hash", jump_hash, METH_VARARGS,
					hash__doc__ },
				      { NULL, NULL, 0, NULL } };

static struct PyModuleDef jumpmodule = { PyModuleDef_HEAD_INIT, "jump",
					 jump__doc__, -1, jump_methods };

PyMODINIT_FUNC PyInit__jump(void)
{
	return PyModule_Create(&jumpmodule);
}
