#include <Python.h>
#include <opencv2/opencv.hpp>
#include "segment-image.h"



static PyObject *segment(PyObject *self, PyObject *args)
{

	int rows = 100,
		cols = 100,
		channel = 1;
	void *data = NULL;
    int size = 0;
    float sigma = 0.5;
    int c = 1000;
    int min_size = 50;
	if (!PyArg_ParseTuple(args, "s#(ii)|fii", &data, &size, &rows, &cols, &sigma, &c, &min_size))
	{
		Py_RETURN_NONE; 
    }

	Mat mat = Mat(rows, cols, CV_MAKETYPE(CV_8U, channel), data);
    Mat ret;
    segment_image(mat, sigma, c, min_size, ret);

	return PyBytes_FromStringAndSize((char*)ret.data, ret.cols * ret.rows * ret.channels());
}


static PyMethodDef methods[] = {
	{"segment", (PyCFunction)segment, METH_VARARGS, "segment(image: bytes, shape: tuple, sigma: float=0.5, c: int=1000, min_size: int=50) -> bytes"},
	{NULL, NULL, 0, NULL}};


static struct PyModuleDef module = {
	PyModuleDef_HEAD_INIT,
	"ESegment",
	NULL,
	-1,
	methods};

PyMODINIT_FUNC PyInit_PyEsegment()
{
	return PyModule_Create(&module);
}