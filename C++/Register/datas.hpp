#pragma once
#include <QWidget>
#include "ui_datas.h"

class DataS : public QWidget {
	Q_OBJECT

public:
	DataS(QWidget * parent = Q_NULLPTR);
	~DataS();
	public slots:
	void showPup();
public:
	void init();
private:
	Ui::DataS ui;
};
