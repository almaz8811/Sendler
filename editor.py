# Form implementation generated from reading ui file 'editor.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        MainWindow.resize(1094, 795)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1091, 641))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.textEdit.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(840, 760, 241, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_save_template = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_save_template.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.btn_save_template.setObjectName("btn_save_template")
        self.horizontalLayout.addWidget(self.btn_save_template)
        self.btn_cancel_template = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_cancel_template.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.btn_cancel_template.setObjectName("btn_cancel_template")
        self.horizontalLayout.addWidget(self.btn_cancel_template)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 640, 831, 151))
        self.groupBox.setObjectName("groupBox")
        self.textEdit_2 = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_2.setGeometry(QtCore.QRect(10, 20, 811, 121))
        self.textEdit_2.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(840, 640, 241, 61))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_view_browser = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_view_browser.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.btn_view_browser.setObjectName("btn_view_browser")
        self.verticalLayout_2.addWidget(self.btn_view_browser)
        self.btn_view_jinja = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_view_jinja.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.btn_view_jinja.setObjectName("btn_view_jinja")
        self.verticalLayout_2.addWidget(self.btn_view_jinja)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Редактор шаблона"))
        self.btn_save_template.setText(_translate("MainWindow", "Сохранить"))
        self.btn_cancel_template.setText(_translate("MainWindow", "Отмена"))
        self.groupBox.setTitle(_translate("MainWindow", "Справка"))
        self.textEdit_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Из строки CSV файла контактов, например:    ИП </span><span style=\" font-size:8pt; color:#e29700;\">(или ООО Рога и Копыта)</span><span style=\" font-size:8pt;\"> Кучеров Обисмал Святославович,obis@yandex.ru</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">{{company}}</span><span style=\" font-size:8pt;\">    -    Название компании    -    </span><span style=\" font-size:8pt; font-style:italic;\">ИП </span><span style=\" font-size:8pt; font-style:italic; color:#e29700;\">(или ООО Рога и Копыта)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">{{name}}</span><span style=\" font-size:8pt;\">    -    Имя получателя    -    </span><span style=\" font-size:8pt; font-style:italic;\">Обисмал</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">{{patronymic}}</span><span style=\" font-size:8pt;\">    -    Отчество получателя    -    </span><span style=\" font-size:8pt; font-style:italic;\">Святославович</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">{{surname}}</span><span style=\" font-size:8pt;\">    -    Фамилия получателя    -    </span><span style=\" font-size:8pt; font-style:italic;\">Кучеров</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">{{email}}</span><span style=\" font-size:8pt;\">    -    E-mail    -    </span><span style=\" font-size:8pt; font-style:italic;\">obis@yandex.ru</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">{{full_name}}</span><span style=\" font-size:8pt;\">    -    Полное ФИО    -    </span><span style=\" font-size:8pt; font-style:italic;\">Кучеров Обисмал Святославович</span></p></body></html>"))
        self.btn_view_browser.setText(_translate("MainWindow", "Просмотр"))
        self.btn_view_jinja.setText(_translate("MainWindow", "Просмотр с автозаменой"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
