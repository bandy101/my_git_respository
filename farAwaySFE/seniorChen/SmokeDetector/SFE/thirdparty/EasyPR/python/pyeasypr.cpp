#include <Python.h>
#include <easypr.h>
#include <vector>
#include <TH_PlateID.h>

static unsigned char mem1[1024 * 1024];		 //16K
static unsigned char mem2[50 * 1024 * 1024]; //40M

static easypr::CPlateRecognize recognize;
static TH_PlateIDCfg cfg;
static int USED_EASYPR = 0;
#if defined(WIN32)
static const char *coding = "GBK";
#else
static const char *coding = "UTF8";
#endif

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
	cfg.nFastMemorySize = 1024 * 1024; //32K
	cfg.pMemory = mem2;
	cfg.nMemorySize = 50 * 1024 * 1024; //40M

	cfg.bLeanCorrection = 1; //倾斜矫正  0  、不矫正  1、矫正
	cfg.bShadow = 1;		 // 阴影牌识别
	cfg.nImproveSpeed = 0;
	int n = TH_InitPlateIDSDK(&cfg);
	int k = TH_SetImageFormat(1, 0, 0, &cfg);
	int l = TH_SetRecogThreshold(0, 0, &cfg);
	if (n != 0 || k != 0 || l != 0)
	{
		return false;
	}
	TH_SetContrast(0, &cfg);
	int plate[] = {2, 4, 6, 8, 12, 16, 22, 24};
	int i;
	for (i = 0; i < 8; i += 1)
	{
		TH_SetEnabledPlateFormat(plate[i], &cfg);
	}

	return true;
}

static PyObject *plateRecognize(PyObject *self, PyObject *args)
{

	int rows = 100,
		cols = 100,
		channel = 3;
	void *data = NULL;
	int size = 0;
	if (!PyArg_ParseTuple(args, "iiis#", &rows, &cols, &channel, &data, &size))
	{
		return PyTuple_New(0);
	}

	Mat mat = Mat(rows, cols, CV_MAKETYPE(CV_8U, channel), data);

	if (USED_EASYPR)
	{
		// 使用Easy PR
		vector<easypr::CPlate> plates;
		recognize.plateRecognize(mat, plates);
		PyObject *tuple = PyTuple_New(plates.size());
		for (int i = 0; i < plates.size(); i++)
		{
			string plate = plates[i].getPlateStr();
			PyTuple_SetItem(tuple, i, PyUnicode_Decode(plate.c_str(), plate.size(), coding, NULL));
		}
		return tuple;
	}
	else
	{
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
			sprintf(buff, "%s:%s", result.color, result.license);
			string plate = buff;
			PyTuple_SetItem(tuple, i, PyUnicode_Decode(plate.c_str(), plate.size(), "GBK", NULL));
		}
		return tuple;
	}
}

static PyMethodDef methods[] = {
	{"plateRecognize", (PyCFunction)plateRecognize, METH_VARARGS, "plateRecognize(rows, cols, channel, data) -> plates"},
	{NULL, NULL, 0, NULL}};

static struct PyModuleDef module = {
	PyModuleDef_HEAD_INIT,
	"pyeasypr",
	NULL,
	-1,
	methods};

PyMODINIT_FUNC PyInit_pyeasypr()
{
	if (!InitDll(cfg))
	{
		printf("use easypr\n");
		recognize.setDetectType(easypr::PR_DETECT_CMSER | easypr::PR_DETECT_COLOR | easypr::PR_DETECT_SOBEL);
		recognize.setLifemode(true);
		USED_EASYPR = 1;
	}

	return PyModule_Create(&module);
}