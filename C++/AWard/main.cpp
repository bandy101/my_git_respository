#include "award.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	AWard w;
	w.show();
	return a.exec();
}
