#ifndef AWARD_H
#define AWARD_H

#include <QtWidgets/QMainWindow>
#include "ui_award.h"

class AWard : public QMainWindow
{
	Q_OBJECT

public:
	AWard(QWidget *parent = 0);
	~AWard();
	public slots:
	void ClickButton();
private:
	QString regst;
	Ui::AWardClass ui;
};

#endif // AWARD_H
