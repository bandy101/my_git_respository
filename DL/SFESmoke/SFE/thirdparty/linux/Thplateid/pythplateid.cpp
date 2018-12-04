#include <Python.h>
#include <opencv2/opencv.hpp>
#include <vector>
#include <TH_PlateID.h>

static unsigned char mem1[1024 * 1024];		 //1M
static unsigned char mem2[50 * 1024 * 1024]; //50M

static TH_PlateIDCfg cfg;

static bool InitDll(TH_PlateIDCfg &cfg)
{
	cfg.nMinPlateWidth = 60;
	cfg.nMaxPlateWidth = 400;
	cfg.nMaxImageWidth = 4000;
	cfg.nMaxImageHeight = 3000;
	cfg.bVertCompress = 0;		// 垂直方向压缩
	cfg.bIsFieldImage = 0;		// 是否是场图片
	cfg.bOutputSingleFrame = 1; //0、相同的车牌输出多次    1 、相同的车牌只输出一次 ，这个参数视频模式才起作用  也就是 configure.bMovingImage = 1
	cfg.bMovingImage = 0;		//  0  、图片模式   1、视频模式
	cfg.bIsNight = 0;
	cfg.nImageFormat = 1;

	cfg.pFastMemory = mem1;
	cfg.nFastMemorySize = 1024 * 1024; //1M
	cfg.pMemory = mem2;
	cfg.nMemorySize = 50 * 1024 * 1024; //50M

	cfg.bLeanCorrection = 1; //倾斜矫正  0  、不矫正  1、矫正
	cfg.bShadow = 1;		 // 阴影牌识别
	cfg.nImproveSpeed = 0;
	cfg.bUTF8 = 1; // 字符编码为UTF8
	int n = TH_InitPlateIDSDK(&cfg);
	switch (n)
	{
	case TH_ERR_NONE:
		printf("车牌识别库初始化成功\n");
		break;
	case TH_ERR_INVALIDCALL:
		printf("非法调用\n");
		return false;
	case TH_ERR_INVALIDMOUDLE:
		printf("不合法授权\n");
		return false;
	case TH_ERR_INITVEHDETECT:
		printf("VehFeature.bin 不存在");
		return false;
	default:
		printf("未知错误, %d\n", n);
		return false;
	}
	n = TH_SetImageFormat(1, 0, 0, &cfg);
	if (n != TH_ERR_NONE)
	{
		printf("设置图片格式出错, %d\n", n);
		return false;
	}
	n = TH_SetRecogThreshold(0, 0, &cfg);
	if (n != TH_ERR_NONE)
	{
		printf("设置识别阈值出错, %d\n", n);
		return false;
	}
	TH_SetContrast(0, &cfg);
	int plate[] = {2, 4, 6, 8, 12, 16, 22, 24};
	int i;
	for (i = 0; i < 8; i += 1)
	{
		TH_SetEnabledPlateFormat(plate[i], &cfg);
	}
	printf("use thplateid\n");
	return true;
}

static PyObject *plateRecognize(PyObject *self, PyObject *args)
{

	int rows = 0,
		cols = 0,
		channel = 0;
	void *data = NULL;
	int size = 0;
	if (!PyArg_ParseTuple(args, "iiis#", &rows, &cols, &channel, &data, &size))
	{
		return PyTuple_New(0);
	}

	cv::Mat mat = cv::Mat(rows, cols, CV_MAKETYPE(CV_8U, channel), data);

	TH_PlateIDResult result;
	memset(&result, 0, sizeof(result));
	int count = 1;
	TH_RECT rect;
	rect.top = 0;
	rect.left = 0;
	rect.right = cols;
	rect.bottom = rows;

	TH_RecogImage((unsigned char *)data, cols, rows, &result, &count, &rect, &cfg);

	PyObject *tuple = PyTuple_New(count);
	for (int i = 0; i < count; i++)
	{
		char buff[100];
		sprintf(buff, "%s:%s:%d", result.license, result.color, result.nType);
		std::string plate = buff;
		PyTuple_SetItem(tuple, i, PyUnicode_Decode(plate.c_str(), plate.size(), "UTF8", NULL));
	}
	return tuple;
}

static PyMethodDef methods[] = {
	{"plateRecognize", (PyCFunction)plateRecognize, METH_VARARGS, "plateRecognize(rows, cols, channel, data) -> plates"},
	{NULL, NULL, 0, NULL}};

static struct PyModuleDef module = {
	PyModuleDef_HEAD_INIT,
	"pythplateid",
	NULL,
	-1,
	methods};

PyMODINIT_FUNC PyInit_pythplateid()
{
	if (!InitDll(cfg))
	{
		PyErr_SetString(PyExc_Exception, "车牌识别库初始化失败");
		return NULL;
	}

	return PyModule_Create(&module);
}