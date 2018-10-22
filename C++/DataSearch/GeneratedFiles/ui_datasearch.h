/********************************************************************************
** Form generated from reading UI file 'datasearch.ui'
**
** Created by: Qt User Interface Compiler version 5.9.6
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_DATASEARCH_H
#define UI_DATASEARCH_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QDateTimeEdit>
#include <QtWidgets/QDial>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_DataSearchClass
{
public:
    QWidget *centralWidget;
    QDateTimeEdit *dateTimeEdit;
    QDial *dial;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *DataSearchClass)
    {
        if (DataSearchClass->objectName().isEmpty())
            DataSearchClass->setObjectName(QStringLiteral("DataSearchClass"));
        DataSearchClass->resize(600, 400);
        centralWidget = new QWidget(DataSearchClass);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        dateTimeEdit = new QDateTimeEdit(centralWidget);
        dateTimeEdit->setObjectName(QStringLiteral("dateTimeEdit"));
        dateTimeEdit->setGeometry(QRect(130, 100, 194, 22));
        dial = new QDial(centralWidget);
        dial->setObjectName(QStringLiteral("dial"));
        dial->setGeometry(QRect(170, 180, 50, 64));
        DataSearchClass->setCentralWidget(centralWidget);
        mainToolBar = new QToolBar(DataSearchClass);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        DataSearchClass->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(DataSearchClass);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        DataSearchClass->setStatusBar(statusBar);

        retranslateUi(DataSearchClass);

        QMetaObject::connectSlotsByName(DataSearchClass);
    } // setupUi

    void retranslateUi(QMainWindow *DataSearchClass)
    {
        DataSearchClass->setWindowTitle(QApplication::translate("DataSearchClass", "DataSearch", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class DataSearchClass: public Ui_DataSearchClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_DATASEARCH_H
