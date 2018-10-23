#include "register.h"
#include "../DataSearch/datasearch.h"
#include "datas.hpp"
#include <QtWidgets/QApplication>
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	Register w;
	DataS k;
	w.show();
	while (true)
	{
		if (w.data_ui)
		{
			k.show();
			delete &w;
			break;
		}

	}
	return a.exec();
}
