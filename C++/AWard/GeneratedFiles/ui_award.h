/********************************************************************************
** Form generated from reading UI file 'award.ui'
**
** Created by: Qt User Interface Compiler version 5.9.6
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_AWARD_H
#define UI_AWARD_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_AWardClass
{
public:
    QWidget *centralWidget;
    QTabWidget *tabWidget;
    QWidget *tab;
    QGroupBox *groupBox;
    QLineEdit *regst_code;
    QLabel *label;
    QGroupBox *groupBox_2;
    QLineEdit *award_code;
    QPushButton *generate;
    QWidget *tab_2;

    void setupUi(QMainWindow *AWardClass)
    {
        if (AWardClass->objectName().isEmpty())
            AWardClass->setObjectName(QStringLiteral("AWardClass"));
        AWardClass->resize(715, 628);
        QIcon icon;
        icon.addFile(QStringLiteral("C:/Users/NHT/Desktop/test_pre/images/watermark.png"), QSize(), QIcon::Normal, QIcon::Off);
        AWardClass->setWindowIcon(icon);
        AWardClass->setStyleSheet(QStringLiteral("background-color:qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(41, 10, 114, 255), stop:1 rgba(255, 255, 255, 255))"));
        AWardClass->setAnimated(true);
        centralWidget = new QWidget(AWardClass);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        centralWidget->setAutoFillBackground(false);
        tabWidget = new QTabWidget(centralWidget);
        tabWidget->setObjectName(QStringLiteral("tabWidget"));
        tabWidget->setEnabled(true);
        tabWidget->setGeometry(QRect(60, 30, 581, 561));
        tabWidget->setStyleSheet(QLatin1String("color:rgb(0, 170, 255);font-size:20px;font-weight:20px;\n"
"selection-color:rgb(0, 255, 0); "));
        tab = new QWidget();
        tab->setObjectName(QStringLiteral("tab"));
        tab->setEnabled(true);
        groupBox = new QGroupBox(tab);
        groupBox->setObjectName(QStringLiteral("groupBox"));
        groupBox->setEnabled(true);
        groupBox->setGeometry(QRect(70, 50, 441, 131));
        regst_code = new QLineEdit(groupBox);
        regst_code->setObjectName(QStringLiteral("regst_code"));
        regst_code->setEnabled(true);
        regst_code->setGeometry(QRect(60, 40, 331, 61));
        QFont font;
        regst_code->setFont(font);
        regst_code->setAcceptDrops(true);
        regst_code->setStyleSheet(QLatin1String("background-color:qconicalgradient(cx:0.5, cy:0.5, angle:0, stop:0 rgba(78, 80, 242, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color:rgb(0, 0, 0);"));
        regst_code->setDragEnabled(false);
        regst_code->setReadOnly(false);
        label = new QLabel(groupBox);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(20, 30, 21, 81));
        label->setTextFormat(Qt::PlainText);
        label->setWordWrap(true);
        groupBox_2 = new QGroupBox(tab);
        groupBox_2->setObjectName(QStringLiteral("groupBox_2"));
        groupBox_2->setEnabled(true);
        groupBox_2->setGeometry(QRect(70, 280, 441, 121));
        award_code = new QLineEdit(groupBox_2);
        award_code->setObjectName(QStringLiteral("award_code"));
        award_code->setEnabled(true);
        award_code->setGeometry(QRect(60, 30, 331, 61));
        award_code->setFont(font);
        award_code->setStyleSheet(QLatin1String("background-color:qconicalgradient(cx:0.5, cy:0.5, angle:0, stop:0 rgba(78, 80, 242, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color:rgb(0,0,0);"));
        award_code->setReadOnly(true);
        generate = new QPushButton(groupBox_2);
        generate->setObjectName(QStringLiteral("generate"));
        generate->setEnabled(true);
        generate->setGeometry(QRect(20, 30, 31, 61));
        tabWidget->addTab(tab, QString());
        tab_2 = new QWidget();
        tab_2->setObjectName(QStringLiteral("tab_2"));
        tab_2->setEnabled(true);
        tab_2->setFont(font);
        tab_2->setStyleSheet(QStringLiteral("color:rgb(0, 170, 255)"));
        tabWidget->addTab(tab_2, QString());
        AWardClass->setCentralWidget(centralWidget);

        retranslateUi(AWardClass);

        tabWidget->setCurrentIndex(0);


        QMetaObject::connectSlotsByName(AWardClass);
    } // setupUi

    void retranslateUi(QMainWindow *AWardClass)
    {
        AWardClass->setWindowTitle(QApplication::translate("AWardClass", "\351\201\245\346\265\213\346\237\245\350\257\242\346\216\210\346\235\203", Q_NULLPTR));
        groupBox->setTitle(QApplication::translate("AWardClass", "\346\263\250\345\206\214\344\277\241\346\201\257", Q_NULLPTR));
        regst_code->setText(QString());
        label->setText(QApplication::translate("AWardClass", "\346\263\250\345\206\214\347\240\201", Q_NULLPTR));
        groupBox_2->setTitle(QApplication::translate("AWardClass", "\347\224\237\346\210\220\346\216\210\346\235\203\347\240\201", Q_NULLPTR));
        award_code->setText(QString());
        generate->setText(QApplication::translate("AWardClass", "\347\224\237\n"
"\346\210\220", Q_NULLPTR));
        tabWidget->setTabText(tabWidget->indexOf(tab), QApplication::translate("AWardClass", "\351\201\245\346\265\213\350\275\257\344\273\266\346\216\210\346\235\203", Q_NULLPTR));
        tabWidget->setTabText(tabWidget->indexOf(tab_2), QApplication::translate("AWardClass", "\345\212\240\345\257\206\350\247\243\345\257\206", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class AWardClass: public Ui_AWardClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_AWARD_H
