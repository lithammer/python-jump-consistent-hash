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
    TypeError: If `key` or `num_buckets` is not an integer.\n\
    OverflowError: If `num_buckets` is outside the signed 32-bit range.\n\
    ValueError: If `num_buckets` is not a positive number.\n");

PyDoc_STRVAR(jump__doc__, "Fast, minimal memory, consistent hash algorithm.");

static PyObject *jump_hash(PyObject *self, PyObject *const *args,
			   Py_ssize_t nargs)
{
	PyObject *key_obj, *num_buckets_obj;
	uint64_t key;
	long long num_buckets;
	int overflow;

	if (nargs != 2) {
		PyErr_Format(PyExc_TypeError,
			     "function takes exactly 2 arguments (%zd given)",
			     nargs);
		return NULL;
	}

	/* Convert through __index__ first. On 3.9 the converters below still
	 * fall back to __int__ and would silently truncate a float, where
	 * 3.10+ and py_hash raise TypeError. */
	key_obj = PyNumber_Index(args[0]);
	if (key_obj == NULL)
		return NULL;

	num_buckets_obj = PyNumber_Index(args[1]);
	if (num_buckets_obj == NULL) {
		Py_DECREF(key_obj);
		return NULL;
	}

	/* Both are exact integers now, so neither conversion can fail.
	 * PyLong_AsLongLongAndOverflow rather than PyLong_AsLong keeps the
	 * bound off the width of C long, which differs on Windows. */
	key = PyLong_AsUnsignedLongLongMask(key_obj);
	num_buckets = PyLong_AsLongLongAndOverflow(num_buckets_obj, &overflow);

	Py_DECREF(key_obj);
	Py_DECREF(num_buckets_obj);

	if (overflow > 0 || num_buckets > INT32_MAX) {
		PyErr_SetString(PyExc_OverflowError,
				"signed integer is greater than maximum");
		return NULL;
	}

	if (overflow < 0 || num_buckets < INT32_MIN) {
		PyErr_SetString(PyExc_OverflowError,
				"signed integer is less than minimum");
		return NULL;
	}

	if (num_buckets < 1) {
		PyErr_Format(
			PyExc_ValueError,
			"'num_buckets' must be a positive number, got %lld",
			num_buckets);
		return NULL;
	}

	return PyLong_FromLong(jump_consistent_hash(key, (int32_t)num_buckets));
}

static PyMethodDef jump_methods[] = { { "hash",
					(PyCFunction)(void (*)(void))jump_hash,
					METH_FASTCALL, hash__doc__ },
				      { NULL, NULL, 0, NULL } };

/* jump_consistent_hash() is pure and the module holds no state, so it needs
 * neither the GIL nor a per-interpreter copy. Declaring that requires
 * multi-phase init; single-phase init silently re-enables the GIL
 * process-wide on free-threaded builds. */
static PyModuleDef_Slot jump_slots[] = {
#if PY_VERSION_HEX >= 0x030C0000
	{ Py_mod_multiple_interpreters, Py_MOD_PER_INTERPRETER_GIL_SUPPORTED },
#endif
#if PY_VERSION_HEX >= 0x030D0000
	{ Py_mod_gil, Py_MOD_GIL_NOT_USED },
#endif
	{ 0, NULL }
};

static struct PyModuleDef jumpmodule = {
	.m_base = PyModuleDef_HEAD_INIT,
	.m_name = "jump._jump",
	.m_doc = jump__doc__,
	.m_size = 0,
	.m_methods = jump_methods,
	.m_slots = jump_slots,
};

PyMODINIT_FUNC PyInit__jump(void)
{
	return PyModuleDef_Init(&jumpmodule);
}
