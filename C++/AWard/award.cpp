#include "award.h"
#include "LiMit.hpp"

using namespace std;
AWard::AWard(QWidget *parent)
	: QMainWindow(parent)
{
	ui.setupUi(this);
	ui.regst_code->setFocus();
	connect(ui.generate, SIGNAL(clicked()), this, SLOT(ClickButton()));
}

AWard::~AWard()
{

}

void AWard::ClickButton()
{
	regst = ui.regst_code->text();
	string  r = regst.toStdString();
	privateConvert(const_cast<char*>(r.c_str()));
	ui.award_code->setText(QString::fromStdString(r));
}