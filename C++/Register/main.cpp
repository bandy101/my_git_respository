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
	//QQuickView view;                                                                       //QQuickView对象
	//view.setSource(QUrl(QStringLiteral("qrc:///timeControl.qml")));       //加载QML
	//view.show();                                                                                //QQuickView可以显示可视化QML对象
	//QQuickItem* item = view.rootObject();                                   //返回当前QQuickView的根节点
	//tiem->setWidth(500);                                                                //QQuickItem* 赋值操作
	//QQmlApplicationEngine  engine;
	//engine.load(QUrl(QLatin1String("timeControl.qml")));
	//QQmlComponent *component;//QML引擎
	//component(&engine, QUrl(QStringLiteral("qrc:///timeControl.qml")));       //加载QML
	//用QQmlComponent创建一个组件的实例，并且赋值给object*，这步操作非常关键，Object类型可以转换其他任意类型，比如QQuickItem
	//QObject* object = component.create();
	//object->setProperty("width", 500);                                                           //元对象系统赋值操作
	//QQmlProperty(object, "width").write(500);                                              //元对象系统赋值操作
	//QQuickItem* item = qobject_cast<QQuickItem*>(object);                    //把 QObject* 转换成 QQuickItem* 类型
	//tiem->setWidth(500);

	//QQmlEngine engine;															                         //QML引擎
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
