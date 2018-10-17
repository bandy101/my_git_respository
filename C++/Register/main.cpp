#include "register.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	Register w;
	w.show();
	return a.exec();
}
