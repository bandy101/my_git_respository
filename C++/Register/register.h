#ifndef REGISTER_H
#define REGISTER_H

#include <QtWidgets/QMainWindow>
#include "ui_register.h"
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
public slots:
	void ClickButton();

private:
	string disk_id;
	Ui::RegisterClass ui;
	bool flag,is_limit;
	QString Lisence,Award;
	//DataSearch w;
	
};

#endif // REGISTER_H
