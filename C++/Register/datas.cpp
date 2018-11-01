#include "datas.hpp"

DataS::DataS(QWidget * parent) : QWidget(parent) {
	ui.setupUi(this);
	init();
}

DataS::~DataS() {
	
}

void DataS::init()
{
	ui.calendar_0->hide();
	//ui.calendar_1->hide();
	ui.calendar_1->setVisible(false);
	connect(ui.date_0, SIGNAL(hidePopup()), this, SLOT(showPup()));
	//ui.calendar_1->setVisible(true);
	ui.date_0
}

void DataS::showPup()
{
	ui.calendar_1->setVisible(true);
}