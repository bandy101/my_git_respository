#pragma once
#ifndef REGISTER_H
#define REGISTER_H

#include <QtWidgets/QMainWindow>
#include "ui_register.h"
#include "datas.hpp"

//#include "datasearch.cpp"
//#include "../DataSearch/datasearch.cpp"
using namespace std;

class Register : public QMainWindow
{
	Q_OBJECT

public:
	Register(QWidget *parent = 0);
	~Register();
	bool Is_limit(QString str);
	void init();
	//Register *w;
public slots:
	void ClickButton();

private:
	DataS *k;
	Ui::RegisterClass ui;
	string disk_id;
	bool flag,is_limit;
	QString Lisence,Award;
	
};

#endif // REGISTER_H
