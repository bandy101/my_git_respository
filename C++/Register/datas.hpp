#pragma once
#include <QWidget>
#include "ui_datas.h"

class DataS : public QWidget {
	Q_OBJECT

public:
	DataS(QWidget * parent = Q_NULLPTR);
	~DataS();

private:
	Ui::DataS ui;
};
