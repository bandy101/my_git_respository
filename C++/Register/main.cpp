#include "register.h"
#include "datas.hpp"
#include <QtWidgets/QApplication>
#include <QGuiApplication>
#include <QtQml/QQmlApplicationEngine>
#include <QtQml/qqmlcontext.h>

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	Register w;
	DataS k;
	//w.show();
	k.show();
	//QQuickView view;                                                                       //QQuickView����
	//view.setSource(QUrl(QStringLiteral("qrc:///timeControl.qml")));       //����QML
	//view.show();                                                                                //QQuickView������ʾ���ӻ�QML����
	//QQuickItem* item = view.rootObject();                                   //���ص�ǰQQuickView�ĸ��ڵ�
	//tiem->setWidth(500);                                                                //QQuickItem* ��ֵ����
	//QQmlApplicationEngine  engine;
	//engine.load(QUrl(QLatin1String("timeControl.qml")));
	//QQmlComponent *component;//QML����
	//component(&engine, QUrl(QStringLiteral("qrc:///timeControl.qml")));       //����QML
	//��QQmlComponent����һ�������ʵ�������Ҹ�ֵ��object*���ⲽ�����ǳ��ؼ���Object���Ϳ���ת�������������ͣ�����QQuickItem
	//QObject* object = component.create();
	//object->setProperty("width", 500);                                                           //Ԫ����ϵͳ��ֵ����
	//QQmlProperty(object, "width").write(500);                                              //Ԫ����ϵͳ��ֵ����
	//QQuickItem* item = qobject_cast<QQuickItem*>(object);                    //�� QObject* ת���� QQuickItem* ����
	//tiem->setWidth(500);

	//QQmlEngine engine;															                         //QML����
	//engine.load(QUrl(QStringLiteral("qrc:/main.qml")));
	//while (true)
	//{
	//	if (w.data_ui)
	//	{
	//		k.show();
	//		delete &w;
	//		break;
	//	}

	//}
	return a.exec();
}
