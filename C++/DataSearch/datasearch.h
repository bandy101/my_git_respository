#pragma once
#ifndef DATASEARCH_H
#define DATASEARCH_H

#include <QtWidgets/QMainWindow>
//#include "GeneratedFiles/ui_datasearch.h".
#include "ui_datasearch.h"
class DataSearch : public QMainWindow
{
	Q_OBJECT

public:
	DataSearch(QWidget *parent = 0);
	~DataSearch();

private:
	Ui::DataSearchClass ui;
};

#endif // DATASEARCH_H
