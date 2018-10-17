/********************************************************************************
** Form generated from reading UI file 'register.ui'
**
** Created by: Qt User Interface Compiler version 5.9.6
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_REGISTER_H
#define UI_REGISTER_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSplitter>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_RegisterClass
{
public:
    QWidget *centralWidget;
    QGroupBox *reg;
    QLineEdit *reg_code;
    QGroupBox *award;
    QLineEdit *awd_code;
    QPushButton *active;
    QSplitter *splitter;

    void setupUi(QMainWindow *RegisterClass)
    {
        if (RegisterClass->objectName().isEmpty())
            RegisterClass->setObjectName(QStringLiteral("RegisterClass"));
        RegisterClass->resize(572, 331);
        QIcon icon;
        icon.addFile(QStringLiteral("C:/Users/NHT/Desktop/test_pre/images/watermark.png"), QSize(), QIcon::Normal, QIcon::Off);
        RegisterClass->setWindowIcon(icon);
        RegisterClass->setStyleSheet(QStringLiteral("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 178, 102, 255), stop:0.55 rgba(235, 148, 61, 255), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0))"));
        centralWidget = new QWidget(RegisterClass);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        reg = new QGroupBox(centralWidget);
        reg->setObjectName(QStringLiteral("reg"));
        reg->setGeometry(QRect(120, 50, 301, 81));
        reg_code = new QLineEdit(reg);
        reg_code->setObjectName(QStringLiteral("reg_code"));
        reg_code->setEnabled(true);
        reg_code->setGeometry(QRect(10, 20, 281, 51));
        QFont font;
        font.setFamily(QStringLiteral("Adobe Arabic"));
        font.setPointSize(18);
        font.setBold(false);
        font.setWeight(50);
        reg_code->setFont(font);
        reg_code->setReadOnly(true);
        award = new QGroupBox(centralWidget);
        award->setObjectName(QStringLiteral("award"));
        award->setGeometry(QRect(120, 150, 301, 81));
        awd_code = new QLineEdit(award);
        awd_code->setObjectName(QStringLiteral("awd_code"));
        awd_code->setEnabled(true);
        awd_code->setGeometry(QRect(10, 20, 281, 51));
        awd_code->setFont(font);
        awd_code->setFocusPolicy(Qt::ClickFocus);
        active = new QPushButton(centralWidget);
        active->setObjectName(QStringLiteral("active"));
        active->setEnabled(true);
        active->setGeometry(QRect(450, 280, 81, 31));
        QFont font1;
        font1.setBold(true);
        font1.setWeight(75);
        font1.setKerning(true);
        active->setFont(font1);
        active->setMouseTracking(false);
        active->setTabletTracking(false);
        active->setAcceptDrops(false);
        active->setAutoFillBackground(false);
        active->setStyleSheet(QLatin1String("color:rgb(255, 0, 0);boder-radius:25px;\n"
"button{border-style: solid;boder-radius:25px;color:red;border-width: 5px;border-color: blue;}"));
        active->setInputMethodHints(Qt::ImhNone);
        QIcon icon1;
        icon1.addFile(QStringLiteral("C:/Users/NHT/Desktop/test_pre/images/home-logo.png"), QSize(), QIcon::Normal, QIcon::Off);
        active->setIcon(icon1);
        active->setIconSize(QSize(299, 20));
        active->setCheckable(false);
        active->setChecked(false);
        active->setAutoRepeat(false);
        active->setAutoExclusive(false);
        active->setAutoDefault(false);
        active->setFlat(false);
        splitter = new QSplitter(centralWidget);
        splitter->setObjectName(QStringLiteral("splitter"));
        splitter->setGeometry(QRect(0, 0, 0, 0));
        splitter->setOrientation(Qt::Horizontal);
        RegisterClass->setCentralWidget(centralWidget);

        retranslateUi(RegisterClass);

        active->setDefault(false);


        QMetaObject::connectSlotsByName(RegisterClass);
    } // setupUi

    void retranslateUi(QMainWindow *RegisterClass)
    {
        RegisterClass->setWindowTitle(QApplication::translate("RegisterClass", "\346\263\250\345\206\214", Q_NULLPTR));
        reg->setTitle(QApplication::translate("RegisterClass", "\346\263\250\345\206\214\347\240\201", Q_NULLPTR));
        reg_code->setText(QString());
        award->setTitle(QApplication::translate("RegisterClass", "\346\216\210\346\235\203\347\240\201", Q_NULLPTR));
        awd_code->setText(QString());
        active->setText(QApplication::translate("RegisterClass", "\346\277\200\346\264\273", Q_NULLPTR));
#ifndef QT_NO_SHORTCUT
        active->setShortcut(QString());
#endif // QT_NO_SHORTCUT
    } // retranslateUi

};

namespace Ui {
    class RegisterClass: public Ui_RegisterClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_REGISTER_H
