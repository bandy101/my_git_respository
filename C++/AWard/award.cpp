#include "award.h"

AWard::AWard(QWidget *parent)
	: QMainWindow(parent)
{
	ui.setupUi(this);
	ui.regst_code->setFocus();
}

AWard::~AWard()
{

}
