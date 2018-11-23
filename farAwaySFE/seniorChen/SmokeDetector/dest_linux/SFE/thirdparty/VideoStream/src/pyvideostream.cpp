#include <Python.h>
#include "video_stream.h"

static PyObject *init(PyObject *self, PyObject *args)
{

	char *ip, *user, *pwd;
	int ip_size, user_size, pwd_size;
	int port, channel;

	if (!PyArg_ParseTuple(args, "s#is#s#i", &ip, &ip_size, &port, &user, &user_size, &pwd, &pwd_size, &channel))
	{
		Py_RETURN_FALSE;
	}

	if (sfe::init(ip, port, user, pwd, channel))
		Py_RETURN_TRUE;
	else
		Py_RETURN_FALSE;
}

static PyObject *destroy(PyObject *self, PyObject *args)
{
	sfe::destroy();
	Py_RETURN_NONE;
}

static PyObject *getFrameSize(PyObject *self, PyObject *args)
{
	return Py_BuildValue("(i, i)", sfe::frame_width, sfe::frame_height);
}

static PyObject *nextFrame(PyObject *self, PyObject *args)
{
	shared_ptr<Mat> img = sfe::next_frame();
	if (img == NULL)
	{
		Py_RETURN_NONE;
	}
	PyObject *ret = PyBytes_FromStringAndSize((char *)img->data, sfe::frame_width * sfe::frame_height * 3);
	return ret;
}

static PyMethodDef methods[] = {
	{"init", (PyCFunction)init, METH_VARARGS, "init(ip, prot, user, pwd, channel) -> bool"},
	{"destroy", (PyCFunction)destroy, METH_NOARGS, NULL},
	{"getFrameSize", (PyCFunction)getFrameSize, METH_NOARGS, "getFrameSize() -> (width, height)"},
	{"nextFrame", (PyCFunction)nextFrame, METH_NOARGS, "nextFrame() -> bytes/None"},
	{NULL, NULL, 0, NULL}};

static struct PyModuleDef module = {
	PyModuleDef_HEAD_INIT,
	"pyvideostream",
	NULL,
	-1,
	methods};

PyMODINIT_FUNC PyInit_pyvideostream()
{
	return PyModule_Create(&module);
}