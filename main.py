import sys
import os
import shutil
import smtplib
import csv
import window
import editor
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTreeWidgetItem
from PyQt6 import QtCore
from PyQt6.QtCore import QTimer, QEventLoop, QRegularExpression
from config_core import get_config, update_config, path_settings
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QIcon
from jinja2 import Template
import ctypes


class MyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.regexp_by_format = dict()
        char_format = QTextCharFormat()
        char_format.setFontWeight(800)
        char_format.setForeground(QColor(86, 156, 214))
        self.regexp_by_format[r'<html|<head|<title|<xml|<xml>|<style|<u|<body|<div|<tbody|<table|<tr|<td|<br|<h1|<h2|<h3|<h4|<span|<strong|<p|<font|<b|<pre|<a|<img|<meta|>|/>|<!|<!--'] = char_format

        char_format = QTextCharFormat()
        char_format.setFontWeight(800)
        char_format.setForeground(QColor(86, 156, 214))
        self.regexp_by_format[r'</html>|</head>|</title>|</xml>|</style>|</u>|</body>|</div>|</tbody>|</table>|</tr>|</td>|</br>|</h1>|</h2>|</h3>|</h4>|</span>|</strong>|</p>|</font>|</b>|</pre>|</a>|</img>'] = char_format

        char_format = QTextCharFormat()
        char_format.setFontWeight(800)
        char_format.setForeground(QColor(86, 156, 214))
        self.regexp_by_format[
            r'<o:|</o:|<w:|</w:|<m:|</m:'] = char_format

        char_format = QTextCharFormat()
        char_format.setFontWeight(800)
        char_format.setForeground(QColor(206, 145, 120))
        self.regexp_by_format[r'class=|size=|lang=|border=|moz-do-not-send=|alt=|name=|width=|cellspacing=|cellpadding=|bgcolor=|align=|colspan=|style=|color=|valign=|height=|src=|href=|target=|http-equiv=|content=|charset='] = char_format

        char_format = QTextCharFormat()
        char_format.setFontWeight(800)
        char_format.setForeground(QColor(143, 55, 255))
        self.regexp_by_format[r'{{name}}|{{surname}}|{{patronymic}}|{{email}}|{{company}}|{{full_name}}'] = char_format

    def highlightBlock(self, text: str):
        for regexp, char_format in self.regexp_by_format.items():
            expression = QRegularExpression(regexp)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), char_format)


class EditorWindow(QMainWindow, editor.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon('metroui.ico'))
        self.textEdit.setFontFamily('Courier New')
        self.textEdit.setFontPointSize(11)


class MainWindow(QMainWindow, window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.editor_window = EditorWindow()
        self.setWindowIcon(QIcon('metroui.ico'))
        self.editor_window.btn_cancel_template.clicked.connect(self.close_editor)
        self.editor_window.btn_save_template.clicked.connect(self.save_editor)
        self.editor_window.btn_view_browser.clicked.connect(self.view_browser)
        self.editor_window.btn_view_jinja.clicked.connect(self.view_browser_jinja)
        self.read_settings()
        self.setFixedSize(self.size())
        self.treeWidget.resizeColumnToContents(0)
        self.treeWidget.resizeColumnToContents(1)
        self.treeWidget.resizeColumnToContents(2)
        self.treeWidget.resizeColumnToContents(3)
        self.treeWidget.resizeColumnToContents(4)
        self.lineEdit_login.textEdited.connect(self.edit_value)
        self.lineEdit_password.textEdited.connect(self.edit_value)
        self.lineEdit_smtp_server.textEdited.connect(self.edit_value)
        self.lineEdit_smtp_port.textEdited.connect(self.edit_value)
        self.spinBox_interval.valueChanged.connect(self.edit_value)
        self.lineEdit_file_csv.textEdited.connect(self.edit_value)
        self.lineEdit_subject_mail.textEdited.connect(self.edit_value)
        self.lineEdit_template_mail.textEdited.connect(self.edit_value)
        self.btn_save_settings.clicked.connect(self.write_settings)
        self.toolButton_openfile_csv.clicked.connect(self.btn_open_csv)
        self.toolButton_openfile_template.clicked.connect(self.btn_open_template)
        self.btn_reset_template.clicked.connect(self.reset_template)
        self.btn_edit_template.clicked.connect(self.open_editor)
        self.btn_send_mail.clicked.connect(self.start_send)
        self.btn_stop_mail.clicked.connect(self.stop_send)
        self.sending = True
        self.csv_type = 2

    def read_settings(self):
        self.read_csv()
        self.read_template()
        self.lineEdit_login.setText(settings.get('Server', 'login'))
        self.lineEdit_password.setText(settings.get('Server', 'password'))
        self.lineEdit_smtp_server.setText(settings.get('Server', 'smtp_server'))
        self.lineEdit_smtp_port.setText(settings.get('Server', 'smtp_port'))
        self.spinBox_interval.setValue(int(settings.get('Global', 'interval')))
        self.lineEdit_file_csv.setText(settings.get('Global', 'file_csv'))
        self.lineEdit_subject_mail.setText(settings.get('Global', 'subject_mail'))
        self.lineEdit_template_mail.setText(settings.get('Global', 'template_mail'))
        self.btn_save_settings.setEnabled(False)
        self.btn_send_mail.setEnabled(True)
        self.btn_stop_mail.setEnabled(False)

    def write_settings(self):
        settings.set('Server', 'login', self.lineEdit_login.text())
        settings.set('Server', 'password', self.lineEdit_password.text())
        settings.set('Server', 'smtp_server', self.lineEdit_smtp_server.text())
        settings.set('Server', 'smtp_port', self.lineEdit_smtp_port.text())
        settings.set('Global', 'interval', str(self.spinBox_interval.value()))
        settings.set('Global', 'file_csv', self.lineEdit_file_csv.text())
        settings.set('Global', 'subject_mail', self.lineEdit_subject_mail.text())
        settings.set('Global', 'template_mail', self.lineEdit_template_mail.text())
        update_config(settings)
        self.btn_save_settings.setEnabled(False)
        self.btn_send_mail.setEnabled(True)
        self.btn_stop_mail.setEnabled(False)
        self.read_settings()

    def edit_value(self):
        self.btn_save_settings.setEnabled(True)
        self.btn_send_mail.setEnabled(False)
        self.btn_stop_mail.setEnabled(False)
        self.btn_stop_mail.setEnabled(False)
        self.btn_edit_template.setEnabled(False)

    def read_csv(self):
        self.treeWidget.clear()
        try:
            with open(settings.get('Global', 'file_csv'), encoding='cp1251', newline='') as file_test:
                test_reader = csv.reader(file_test)
                for row in test_reader:
                    self.csv_type = len(row)
                    break
            with open(settings.get('Global', 'file_csv'), encoding='cp1251', newline='') as file:
                reader = csv.reader(file)
                self.add_items(reader, self.csv_type)
        except:
            error = QMessageBox()
            error.setWindowTitle('Ошибка')
            error.setWindowIcon(QIcon('metroui.ico'))
            error.setText(f'Файл с контактами CSV не найден.\nИсправьте путь к файлу.')
            error.setIcon(QMessageBox.Icon.Warning)
            error.exec()
            self.row_count = 0
            settings.set('Global', 'file_csv', '')
            self.lineEdit_file_csv.clear()

    def read_template(self):
        try:
            with open(settings.get('Global', 'template_mail'), 'r', encoding='utf-8') as file_temp:
                self.template = file_temp.read()
                self.btn_edit_template.setEnabled(True)
        except FileNotFoundError:
            error = QMessageBox()
            error.setWindowTitle('Ошибка')
            error.setWindowIcon(QIcon('metroui.ico'))
            error.setText(f'Файл шаблона письма не найден.\nИсправьте путь к файлу.')
            error.setIcon(QMessageBox.Icon.Warning)
            error.exec()
            settings.set('Global', 'template_mail', '')
            self.lineEdit_template_mail.clear()
            self.btn_edit_template.setEnabled(False)

    def write_template(self):
        try:
            with open(settings.get('Global', 'template_mail'), 'w', encoding='utf-8') as file_temp:
                file_temp.write(self.template)
                self.btn_edit_template.setEnabled(True)
        except FileNotFoundError:
            error = QMessageBox()
            error.setWindowTitle('Ошибка')
            error.setWindowIcon(QIcon('metroui.ico'))
            error.setText('fФайл шаблона письма не найден.\nИсправьте путь к файлу.')
            error.setIcon(QMessageBox.Icon.Warning)
            error.exec()
            settings.set('Global', 'template_mail', '')
            self.lineEdit_template_mail.clear()
            self.btn_edit_template.setEnabled(False)

    def btn_open_csv(self):
        self.lineEdit_file_csv.setText(QFileDialog.getOpenFileName(self, filter='Контакты CSV (*.csv);;Текст (*.txt)')[0])
        self.btn_save_settings.setEnabled(True)
        self.btn_send_mail.setEnabled(False)
        self.btn_stop_mail.setEnabled(False)

    def btn_open_template(self):
        self.lineEdit_template_mail.setText(QFileDialog.getOpenFileName(self, filter='HTML файл (*.htm *.html);;Текст (*.txt)')[0])
        self.btn_save_settings.setEnabled(True)
        self.btn_send_mail.setEnabled(False)
        self.btn_stop_mail.setEnabled(False)

    def reset_template(self):
        shutil.copy2('template.bak', '../template.html')
        self.lineEdit_template_mail.setText('../template.html')
        self.write_settings()
        self.read_settings()
        self.btn_save_settings.setEnabled(True)
        self.btn_send_mail.setEnabled(False)
        self.btn_stop_mail.setEnabled(False)
        self.btn_edit_template.setEnabled(False)

    def open_editor(self):
        self.editor_window.show()
        self.editor_window.textEdit.setPlainText(self.template)
        self.highlighter = MyHighlighter(self.editor_window.textEdit.document())

    def close_editor(self):
        self.editor_window.close()

    def save_editor(self):
        self.template = self.editor_window.textEdit.toPlainText()
        self.write_template()
        self.close_editor()

    def add_items(self, reader, csv_type: int):
        self.treeWidget.clear()
        if csv_type == 2:
            for name, email in reader:
                name = name.replace('  ', ' ').split(' ')
                if len(name) != 4:
                    company = name[0]
                    director = f'{name[1]} {name[2]}'
                else:
                    company = name[0]
                    director = f'{name[1]} {name[2]} {name[3]}'
                item = QTreeWidgetItem()
                item.setText(0, str(self.treeWidget.topLevelItemCount() + 1))
                item.setText(1, str(company))
                item.setText(2, str(director))
                item.setText(3, str(email))
                self.treeWidget.addTopLevelItem(item)
            self.treeWidget.resizeColumnToContents(0)
            self.treeWidget.resizeColumnToContents(1)
            self.treeWidget.resizeColumnToContents(2)
            self.treeWidget.resizeColumnToContents(3)
            self.treeWidget.resizeColumnToContents(4)
        elif csv_type == 3:
            for company, email, director in reader:
                item = QTreeWidgetItem()
                item.setText(0, str(self.treeWidget.topLevelItemCount() + 1))
                item.setText(1, str(company))
                item.setText(2, str(director))
                item.setText(3, str(email))
                self.treeWidget.addTopLevelItem(item)
            self.treeWidget.resizeColumnToContents(0)
            self.treeWidget.resizeColumnToContents(1)
            self.treeWidget.resizeColumnToContents(2)
            self.treeWidget.resizeColumnToContents(3)
            self.treeWidget.resizeColumnToContents(4)
        self.progressBar.setMaximum(self.treeWidget.topLevelItemCount())
        self.total = self.treeWidget.topLevelItemCount()

    def send_mail(self, pos, company: str, full_name: str, name: str, surname: str, patronymic: str, email: str):
        smtp_server = smtplib.SMTP(settings.get('Server', 'smtp_server'), settings.get('Server', 'smtp_port'))
        smtp_server.starttls()
        # Создаем объект SMTP
        server: SMTP = smtplib.SMTP(settings.get('Server', 'smtp_server'), settings.get('Server', 'smtp_port'))
        server.set_debuglevel(False)   # Включаем режим отладки - если отчет не нужен, пишем False
        server.starttls()  # Начинаем шифрованный обмен по TLS
        server.login(settings.get('Server', 'login'), settings.get('Server', 'password'))  # Получаем доступ
        exception: email.errors.MessageError
        email_getter = str(email)
        msg = MIMEMultipart()
        msg['From'] = settings.get('Server', 'login')
        msg['To'] = email_getter
        temp_subject = Template(settings.get('Global', 'subject_mail'))
        render_subject = temp_subject.render(name=name, surname=surname, patronymic=patronymic,
                                             email=email, company=company, full_name=full_name)
        msg['Subject'] = render_subject
        temp_msg = Template(self.template)
        render_page = temp_msg.render(name=name, surname=surname, patronymic=patronymic,
                                      email=email, company=company, full_name=full_name)
        msg.attach(MIMEText(render_page, 'html'))
        try:
            server.send_message(msg)  # Отправляем сообщение
        except Exception as e:
            self.treeWidget.topLevelItem(pos).setForeground(4, QtCore.Qt.GlobalColor.red)
            self.treeWidget.topLevelItem(pos).setText(4, 'Ошибка отправки')
            self.bad += 1
            with open("end.txt", "a") as file:
                # file.writelines(name + ';' + email + ';' + 'Ошибка отправки' + '\n')
                file.writelines(f'{full_name}; {email}; Ошибка отправки\n{e}\n')
        else:
            self.treeWidget.topLevelItem(pos).setForeground(4, QtCore.Qt.GlobalColor.darkGreen)
            self.treeWidget.topLevelItem(pos).setText(4, 'Отправлено')
            self.good += 1
            with open("end.txt", "a") as file:
                file.writelines(f'{full_name}; {email}; Отправлено\n')
        server.quit()

    def start_send(self):
        self.lineEdit_login.setEnabled(False)
        self.lineEdit_password.setEnabled(False)
        self.lineEdit_smtp_server.setEnabled(False)
        self.label_smtp_port.setEnabled(False)
        self.lineEdit_smtp_port.setEnabled(False)
        self.spinBox_interval.setEnabled(False)
        self.label_second.setEnabled(False)
        self.lineEdit_file_csv.setEnabled(False)
        self.toolButton_openfile_csv.setEnabled(False)
        self.lineEdit_subject_mail.setEnabled(False)
        self.lineEdit_template_mail.setEnabled(False)
        self.toolButton_openfile_template.setEnabled(False)
        self.btn_edit_template.setEnabled(False)
        self.btn_reset_template.setEnabled(False)
        self.btn_save_settings.setEnabled(False)
        self.btn_send_mail.setEnabled(False)
        self.btn_stop_mail.setEnabled(True)
        self.sending = True
        self.good = 0
        self.bad = 0
        for i in range(self.treeWidget.topLevelItemCount()):
            self.treeWidget.topLevelItem(i).setText(4, '')
        for i in range(self.treeWidget.topLevelItemCount()):
            company = self.treeWidget.topLevelItem(i).text(1)
            parse_full_name = self.treeWidget.topLevelItem(i).text(2).split(' ')
            surname = parse_full_name[0]
            name = parse_full_name[1]
            if len(parse_full_name) == 3:
                patronymic = parse_full_name[2]
            else:
                patronymic = ''
            full_name = self.treeWidget.topLevelItem(i).text(2)
            email = self.treeWidget.topLevelItem(i).text(3)
            if self.sending == True:
                self.send_mail(i, company, full_name, name, surname, patronymic, email)
                self.progressBar.setValue(i + 1)
            else:
                self.stop_send()
                break
            self.delay(int(settings.get('Global', 'interval')) * 1000)
        self.stop_send()
        self.show_info()

    def show_info(self):
        info = QMessageBox()
        info.setWindowIcon(QIcon('metroui.ico'))
        info.setIcon(QMessageBox.Icon.Information)
        info.setWindowTitle('Отчет')
        info.setText('Рассылка завершена')
        info.setInformativeText(f'Всего писем: {str(self.total)}\nОтправлено: {str(self.good)}\nОшибки: {str(self.bad)}')
        info.exec()

    def stop_send(self):
        if self.loop.isRunning():
            self.loop.quit()
        self.sending = False
        self.lineEdit_login.setEnabled(True)
        self.lineEdit_password.setEnabled(True)
        self.lineEdit_smtp_server.setEnabled(True)
        self.label_smtp_port.setEnabled(True)
        self.lineEdit_smtp_port.setEnabled(True)
        self.spinBox_interval.setEnabled(True)
        self.label_second.setEnabled(True)
        self.lineEdit_file_csv.setEnabled(True)
        self.toolButton_openfile_csv.setEnabled(True)
        self.lineEdit_subject_mail.setEnabled(True)
        self.lineEdit_template_mail.setEnabled(True)
        self.toolButton_openfile_template.setEnabled(True)
        self.btn_edit_template.setEnabled(True)
        self.btn_reset_template.setEnabled(True)
        self.btn_save_settings.setEnabled(False)
        self.btn_send_mail.setEnabled(True)
        self.btn_stop_mail.setEnabled(False)
        self.progressBar.setValue(0)

    def delay(self, msec: int):
        self.loop = QEventLoop()
        QTimer().singleShot(msec, lambda: self.loop.quit())
        self.loop.exec()

    def view_browser(self):
        temp_html = self.editor_window.textEdit.toPlainText()
        with open('temp_html.html', 'w', encoding='utf-8') as file_temp_html:
            file_temp_html.write(temp_html)
        os.system(f"start temp_html.html")

    def view_browser_jinja(self):
        temp_html = self.editor_window.textEdit.toPlainText()
        temp_jinja = Template(temp_html)
        render_jinja = temp_jinja.render(name='Обисмал', surname='Кучеров',
                                         patronymic='Святославович', email='obis@yandex.ru',
                                         company='ИП', full_name='Кучеров Обисмал Святославович')
        with open('temp_html.html', 'w', encoding='utf-8') as file_temp_html:
            file_temp_html.write(render_jinja)
        os.system(f"start temp_html.html")

def run():
    myappid = 'AlMaz.Sendler.v1.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('metroui.ico'))
    main_window = MainWindow()
    main_window.setWindowIcon(QIcon('metroui.ico'))
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    settings = get_config(path_settings)
    run()







