#!/usr/bin/env python3
# coding:utf-8
import sys
import os
import sqlite3

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QFont

from library import bd_connect
from library import Constants as cnst
from forms.Главное_окошко import Ui_MainWindow
from forms.Спиcок_каталогов import Ui_CatListWindow
from forms.Редактирование_каталога import Ui_ItemCatEdit
from forms.Новый_каталог import Ui_NewCat
from forms.Редактирование_читателя import Ui_EditChitWindow
from forms.Редактирование_книги import Ui_BookWindow


class BBMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.search_button_clicked)
        self.listWidget.clicked.connect(self.show_books_for_directory)
        self.pushButton_6.clicked.connect(self.reset_filter)
        self.pushButton_cat.clicked.connect(self.open_katalogi)
        self.pushButton_read.clicked.connect(self.open_chitateli)
        self.pushButton_books.clicked.connect(self.open_knigi)
        self.reset_filter()

    def reset_filter(self):
        # Подключение к существующей базе данных
        with bd_connect() as conn:
            cursor = conn.cursor()
            query = "SELECT `Название_каталога` FROM `Каталоги`"
            cursor.execute(query)
            data_from_database = cursor.fetchall()

        self.listWidget.clear()
        for item_data in data_from_database:
            item = QtWidgets.QListWidgetItem(item_data[0])
            self.listWidget.addItem(item)
            item.setSizeHint(QtCore.QSize(200, 50))

        # Подключение к существующей базе данных
        with bd_connect() as conn:
            cursor = conn.cursor()
            # Выполнение запроса SELECT для получения данных из таблицы книги
            cursor.execute("SELECT * FROM Книги")
            books = cursor.fetchall()
        self.fill_table_view(books)

    def fill_table_view(self, books):
        # Заполнение таблицы данными
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Код", "Название книги", "Аннотация", "Автор", "Каталог", "Издательство",
             "Возрастное \n ограничение"])  # Заголовки столбцов
        for row_number, row_data in enumerate(books):
            self.tableWidget.insertRow(row_number)
            # font = QFont("Arial", 12)
            # self.tableWidget.setFont(font)
            for column_number, data in enumerate(row_data):

                if column_number == 2:
                    text_edit = QtWidgets.QTextEdit(str(data))
                    text_edit.setReadOnly(True)
                    text_edit.setFrameStyle(QtWidgets.QFrame.NoFrame)
                    text_edit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                    self.tableWidget.setCellWidget(row_number, column_number, text_edit)
                else:
                    item = QtWidgets.QTableWidgetItem(str(data))
                    item.setTextAlignment(QtCore.Qt.AlignHCenter)
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # Disable editing for other columns
                    self.tableWidget.setItem(row_number, column_number, item)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # Prevent column resizing
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # Prevent column resizing
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)  # Prevent column resizing
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # self.tableWidget.setShowGrid(True)
        # self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.resizeRowsToContents()

    def show_books_for_directory(self):
        selected_directory = self.listWidget.currentItem().text()
        # Список выбранных книг в выбранном каталоге
        selected_dir_books = []
        # Подключение к базе данных
        with bd_connect() as conn:
            cursor = conn.cursor()
            # Выполнение запроса SELECT для получения списка книг в выбранном каталоге
            query = """SELECT * FROM `Книги` WHERE `Каталог` = ?
                    """
            cursor.execute(query, (selected_directory,))
            selected_dir_books = cursor.fetchall()
        self.fill_table_view(selected_dir_books)

    def search_button_clicked(self):
        # Получение текста из строки поиска
        query = self.lineEdit.text()

        # Подключение к существующей базе данных
        with bd_connect() as conn:
            cursor = conn.cursor()
            # Выполнение запроса SELECT для поиска по тексту
            search_query = f"SELECT * FROM Книги WHERE Код_книги LIKE '%{query}%' " \
                           f"OR Название_книги LIKE '%{query}%' " \
                           f"OR Аннотация LIKE '%{query}%' " \
                           f"OR Автор LIKE '%{query}%' " \
                           f"OR Издательство LIKE '%{query}%'"
            cursor.execute(search_query)
            search_results = cursor.fetchall()
        if len(search_results) == 0:
            QtWidgets.QMessageBox.information(
                self.centralwidget, "Результаты поиска", "По данному запросу ничего не найдено.")
        else:
            self.fill_table_view(search_results)

    def open_katalogi(self):
        self.ui = Spisok_katalogov(self.reset_filter)
        if cnst.MAX:
            self.ui.showMaximized()
        else:
            self.ui.show()

    def open_chitateli(self):
        self.ui = Spisok_chitateley(self.reset_filter)
        if cnst.MAX:
            self.ui.showMaximized()
        else:
            self.ui.show()

    def open_knigi(self):
        self.ui = Spisok_knig(self.reset_filter)
        if cnst.MAX:
            self.ui.showMaximized()
        else:
            self.ui.show()

    def open_uchet(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Uchet()
        if cnst.MAX:
            self.ui.showMaximized()
        else:
            self.ui.show()


class Spisok_katalogov(QtWidgets.QWidget, Ui_CatListWindow):
    def __init__(self, refresh_parrent):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(2)
        self.pushButton_back.clicked.connect(self.close)
        self.pushButton_edit.clicked.connect(self.open_red_kataloga)
        self.pushButton_app.clicked.connect(self.open_dobavit_katalog)
        self.pushButton_del.clicked.connect(self.delete_selected_row)
        self.refresh_parrent = refresh_parrent
        self.refresh_table()

    def refresh_table(self):
        try:
            # Подключитесь к базе данных
            with bd_connect() as conn:
                cursor = conn.cursor()
                # Выполните запрос на получение данных из таблицы Каталоги
                select_query = "SELECT * FROM Каталоги"
                cursor.execute(select_query)
                # Получите все строки результатов запроса
                rows = cursor.fetchall()

            # Очистите таблицу tablewidget
            self.tableWidget.clear()

            # Установите количество строк и столбцов в таблице tablewidget
            self.tableWidget.setRowCount(len(rows))
            self.tableWidget.setColumnCount(2)  # Предполагается, что в таблице есть 2 столбца
            self.tableWidget.setHorizontalHeaderLabels(
                ["Каталоги", "Описание каталога"])  # Заголовки столбцов
            # font = QFont("Arial", 12)
            # self.tableWidget.setFont(font)

            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    # Создайте элемент таблицы QTableWidgetItem с соответствующим значением
                    item = QtWidgets.QTableWidgetItem(str(value))
                    # Установите элемент в соответствующую ячейку таблицы
                    self.tableWidget.setItem(i, j, item)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # Prevent column resizing
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.tableWidget.resizeRowsToContents()
        except sqlite3.Error as error:
            # Обработайте возможную ошибку при выполнении операций с базой данных
            print("Ошибка при выполнении операций с базой данных:", error)
            # rows = []

    def closeEvent(self, a0) -> None:
        self.refresh_parrent()


    def open_red_kataloga(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            katalog = self.tableWidget.item(selected_row, 0).text()
            opisanie = self.tableWidget.item(selected_row, 1).text()
            self.ui = red_kataloga(katalog, opisanie, self.refresh_table)
            self.ui.show()

    def open_dobavit_katalog(self):
        self.ui = okno_dobavit_katalog(self.refresh_table)
        self.ui.show()

    def delete_selected_row(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            # Получение значения первой ячейки выбранной строки
            catalog_name = self.tableWidget.item(selected_row, 0).text()

            userResponse = QtWidgets.QMessageBox.question(self, "",
                                                          f"{catalog_name}\n\nУдаляем безвозвратно?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.No)

            if userResponse == QtWidgets.QMessageBox.Yes:
                # Удаление строки из таблицы каталогов в базе данных
                with bd_connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Каталоги WHERE Название_каталога = ?", (catalog_name,))
                    conn.commit()
                self.tableWidget.removeRow(selected_row)


class red_kataloga(QtWidgets.QWidget, Ui_ItemCatEdit):
    def __init__(self, katalog, opisanie, refresh_table):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(2)
        self.katalog_key = katalog
        self.katalog.setText(katalog)
        self.opisanie.setText(opisanie)
        self.refresh_table = refresh_table
        # elf.Dialog = Dialog
        self.pushButton.clicked.connect(self.save_iz_kataloga)

    def save_iz_kataloga(self):
        # Получите данные из полей для ввода
        katalog = self.katalog.text()
        opisanie = self.opisanie.text()
        # Сохраните данные в базу данных
        try:
            # Подключитесь к базе данных
            with bd_connect()as conn:
                cursor = conn.cursor()
                update_query = """UPDATE Каталоги SET Название_каталога=?, 
                    Описание_каталога=? WHERE Название_каталога=?"""
                cursor.execute(update_query, (katalog, opisanie, self.katalog_key,))
                # Сохраните изменения в базе данных
                conn.commit()
            try:
                self.refresh_table()  # Здесь необходимо определить метод refresh_table() для обновления таблицы
                # self.Dialog.accept()
                self.close()
                # Обновите таблицу tablewidget
            except Exception as e:
                print("Ошибка при закрытии окна или обновлении таблицы:", e)
        except sqlite3.Error as error:
            # Обработайте возможную ошибку при выполнении операций с базой данных
            print("Ошибка при выполнении операций с базой данных:", error)


class okno_dobavit_katalog(QtWidgets.QWidget, Ui_NewCat):
    def __init__(self, refresh_table):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(2)
        self.refresh_table = refresh_table
        self.pushButton.clicked.connect(self.save_iz_kataloga)

    def save_iz_kataloga(self):
        # Получите данные из полей для ввода
        naz_kataloga = self.katalog.text()
        opisanie = self.opisanie.text()
        # Сохраните данные в базу данных
        try:
            # Подключитесь к базе данных
            with bd_connect() as conn:
                cursor = conn.cursor()
                # Выполните запрос на вставку новой записи
                insert_query = "INSERT INTO Каталоги (Название_каталога, Описание_каталога) VALUES (?, ?)"
                cursor.execute(insert_query, (naz_kataloga, opisanie,))
                conn.commit()
            try:
                self.refresh_table()  # Здесь необходимо определить метод refresh_table() для обновления таблицы
                print("Обновлено")
                # self.Dialog.accept()
                self.close()
                print("ЗАкрыто")
                # Обновите таблицу tablewidget
            except Exception as e:
                print("Ошибка при закрытии окна или обновлении таблицы:", e)
        except sqlite3.Error as error:
            if "UNIQUE constraint failed" in str(error):
                QtWidgets.QMessageBox.about(self, f"{naz_kataloga}",
                                            f"Уже существует")
            else:
                # Обработайте возможную ошибку при выполнении операций с базой данных
                print("Ошибка при выполнении операций с базой данных:", error)


class Spisok_chitateley(QtWidgets.QWidget, Ui_CatListWindow):
    def __init__(self, refresh_parrent):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(2)
        self.label.setText("Читатели")
        self.pushButton_back.clicked.connect(self.close)
        self.pushButton_edit.clicked.connect(self.open_red_chitatela)
        self.pushButton_app.clicked.connect(self.open_dobavit_chitatela)
        self.pushButton_del.clicked.connect(self.delete_selected_row)
        self.refresh_parrent = refresh_parrent
        self.refresh_table()

    def refresh_table(self):
        try:
            # Подключитесь к базе данных
            with bd_connect() as conn:
                cursor = conn.cursor()
                # Выполните запрос на получение данных из таблицы Каталоги
                select_query = "SELECT * FROM Читатели"
                cursor.execute(select_query)
                # Получите все строки результатов запроса
                rows = cursor.fetchall()

            # Очистите таблицу tablewidget
            self.tableWidget.clear()
            # Установите количество строк и столбцов в таблице tablewidget
            self.tableWidget.setRowCount(len(rows))
            self.tableWidget.setColumnCount(4)  # Предполагается, что в таблице есть 4 столбца
            self.tableWidget.setHorizontalHeaderLabels(
                ["№читательского \n билета", "ФИО", "Дата рождения", "Номер телефона"])  # Заголовки столбцов
            # font = QFont("Arial", 12)
            # self.tableWidget.setFont(font)

            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    # Создайте элемент таблицы QTableWidgetItem с соответствующим значением
                    item = QtWidgets.QTableWidgetItem(str(value))
                    # Установите элемент в соответствующую ячейку таблицы
                    self.tableWidget.setItem(i, j, item)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # Prevent column resizing
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.tableWidget.resizeRowsToContents()

        except sqlite3.Error as error:
            # Обработайте возможную ошибку при выполнении операций с базой данных
            print("Ошибка при выполнении операций с базой данных:", error)

    def open_red_chitatela(self, MainWindow):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            fio = self.tableWidget.item(selected_row, 1).text()
            data_rojdenia = self.tableWidget.item(selected_row, 2).text()
            chit_bilet = self.tableWidget.item(selected_row, 0).text()
            nomer_telefona = self.tableWidget.item(selected_row, 3).text()
            self.ui = red_chitatela(fio, data_rojdenia, chit_bilet,
                                   nomer_telefona, self.refresh_table)
            self.ui.show()

    def open_dobavit_chitatela(self, MainWindow):
        self.ui = dobavit_chitatela(self.refresh_table)
        self.ui.show()

    def delete_selected_row(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            # Получение значения первой ячейки выбранной строки
            chitatel = self.tableWidget.item(selected_row, 0).text()
            fio = self.tableWidget.item(selected_row, 1).text()
            userResponse = QtWidgets.QMessageBox.question(self, "",
                                                          f"{fio}\n\nУдаляем безвозвратно?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.No)
            if userResponse == QtWidgets.QMessageBox.Yes:
                # Удаление строки из таблицы читателей в базе данных
                with bd_connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Читатели WHERE №читательского_билета = ?", (chitatel,))
                    conn.commit()
                    self.tableWidget.removeRow(selected_row)


class red_chitatela(QtWidgets.QWidget, Ui_EditChitWindow):
    def __init__(self, fio, data_rojdenia, chit_bilet, nomer_telefona, refresh_table):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(2)
        self.chit_bilet = chit_bilet
        self.lineEdit_number.setText(chit_bilet)
        self.lineEdit_fio.setText(fio)
        self.lineEdit_born.setText(data_rojdenia)
        self.lineEdit_phone.setText(nomer_telefona)
        self.refresh_table = refresh_table
        self.pushButton.clicked.connect(self.save_iz_chitatela)

    def save_iz_chitatela(self):
        # Получите данные из полей для ввода
        fio = self.lineEdit_fio.text()
        data_rojdenia = self.lineEdit_born.text()
        chit_bilet = self.lineEdit_number.text()
        nomer_telefona = self.lineEdit_phone.text()
        # Сохраните данные в базу данных
        try:
            # Подключитесь к базе данных
            with bd_connect() as conn:
                cursor = conn.cursor()
                # Выполните запрос на измененние записи
                update_query = """UPDATE Читатели SET №читательского_билета=?, ФИО=?, Дата_рождения=?, 
                    Номер_телефона=? WHERE №читательского_билета=?"""
                cursor.execute(update_query, (chit_bilet, fio, data_rojdenia,
                                              nomer_telefona, self.chit_bilet,))
                # Сохраните изменения в базе данных
                conn.commit()
            try:
                self.refresh_table()  # Здесь необходимо определить метод refresh_table() для обновления таблицы
            except Exception as e:
                print("Ошибка при закрытии окна или обновлении таблицы:", e)

        except sqlite3.Error as error:
            # Обработайте возможную ошибку при выполнении операций с базой данных
            print("Ошибка при выполнении операций с базой данных:", error)
        self.close()


class dobavit_chitatela(QtWidgets.QWidget, Ui_EditChitWindow):
    def __init__(self, refresh_table):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(2)
        self.refresh_table = refresh_table
        self.pushButton.clicked.connect(self.save_chitatela)

    def save_chitatela(self):
        # Получите данные из полей для ввода
        chitatel_fio = self.lineEdit_fio.text()
        chitatel_data_rojdenia = self.lineEdit_born.text()
        chitatel_chit_bilet = self.lineEdit_number.text()
        chitatel_phone = self.lineEdit_phone.text()

        # Сохраните данные в базу данных
        try:
            # Подключитесь к базе данных
            if chitatel_chit_bilet.isdigit():
                with bd_connect() as conn:
                    cursor = conn.cursor()
                    # Выполните запрос на вставку новой записи
                    insert_query = """INSERT INTO Читатели (ФИО, Дата_рождения, №читательского_билета, 
                        Номер_телефона) VALUES (?, ?, ?, ?)"""
                    cursor.execute(insert_query,
                                   (chitatel_fio, chitatel_data_rojdenia, chitatel_chit_bilet, chitatel_phone))
                    # Сохраните изменения в базе данных
                    conn.commit()
                self.refresh_table()
            else:
                QtWidgets.QMessageBox.about(self, "",
                                            f"{chitatel_chit_bilet}\n\nНеправильный формат!")
        except sqlite3.Error as error:
            if "UNIQUE constraint failed" in str(error):
                QtWidgets.QMessageBox.about(self, "",
                                            f"{chitatel_chit_bilet}\n\nБилет уже существует")
            # Обработайте возможную ошибку при выполнении операций с базой данных
            print("Ошибка при выполнении операций с базой данных:", error)
        self.close()


class Spisok_knig(QtWidgets.QWidget, Ui_CatListWindow):
    def __init__(self, refresh_parrent):
        super().__init__()
        self.setupUi(self)
        self.label.setText("Каталог книг")
        self.setWindowModality(2)
        self.pushButton_back.clicked.connect(self.close)
        self.pushButton_edit.clicked.connect(self.open_red_knigi)
        # self.pushButton_app.clicked.connect(self.open_dobavit_chitatela)
        # self.pushButton_del.clicked.connect(self.delete_selected_row)
        self.refresh_parrent = refresh_parrent
        self.refresh_table()

    def refresh_table(self):
        with bd_connect() as conn:
            cursor = conn.cursor()
            # Выполнение запроса SELECT для получения данных из таблицы книги
            cursor.execute("SELECT * FROM Книги")
            books = cursor.fetchall()
        # Заполнение таблицы данными
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Код", "Название книги", "Аннотация", "Автор", "Каталог", "Издательство",
             "Возрастное \n ограничение"])  # Заголовки столбцов
        for row_number, row_data in enumerate(books):
            self.tableWidget.insertRow(row_number)
            # font = QFont("Arial", 12)
            # self.tableWidget.setFont(font)
            for column_number, data in enumerate(row_data):

                if column_number == 2:
                    text_edit = QtWidgets.QTextEdit(str(data))
                    text_edit.setReadOnly(True)
                    text_edit.setFrameStyle(QtWidgets.QFrame.NoFrame)
                    text_edit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                    self.tableWidget.setCellWidget(row_number, column_number, text_edit)
                else:
                    item = QtWidgets.QTableWidgetItem(str(data))
                    item.setTextAlignment(QtCore.Qt.AlignHCenter)
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # Disable editing for other columns
                    self.tableWidget.setItem(row_number, column_number, item)

        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)  # Prevent column resizing
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2,QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.resizeRowsToContents()

    def open_red_knigi(self):
        # Получение выбранной строки
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            # Получение данных из выбранной строки
            kod_knigi = self.tableWidget.item(selected_row, 0).text()
            nazvanie = self.tableWidget.item(selected_row, 1).text()
            annotaciya = self.tableWidget.cellWidget(selected_row, 2).toPlainText()
            avtor = self.tableWidget.item(selected_row, 3).text()
            katalog = self.tableWidget.item(selected_row, 4).text()
            izdatelstvo = self.tableWidget.item(selected_row, 5).text()
            vozrastnoe_ogranichenie = self.tableWidget.item(selected_row, 6).text()
            self.ui = red_knigi(self.refresh_table)
            # Заполнение полей окна редактирования данными из выбранной строки
            self.ui.lineEdit_code.setText(kod_knigi)
            self.ui.lineEdit_name.setText(nazvanie)
            self.ui.lineEdit_autor.setText(avtor)
            self.ui.lineEdit_source.setText(izdatelstvo)
            self.ui.lineEdit_limit.setText(vozrastnoe_ogranichenie)
            self.ui.lineEdit_cat.setText(katalog)
            self.ui.lineEdit_comment.setText(annotaciya)
            self.ui.show()

    def open_dobavit_knigy(self, MainWindow):
        self.window = QtWidgets.QDialog()
        self.ui = dobavit_knigy()
        self.ui.setupUi(self.window)
        self.window.show()

    def delete_selected_row(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            # Получение значения первой ячейки выбранной строки
            kniga = self.tableWidget.item(selected_row, 0).text()

            # Удаление строки из таблицы каталогов в базе данных
            conn = bd_connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Книги WHERE Код_книги = ?", (kniga,))
            conn.commit()
            conn.close()

            self.tableWidget.removeRow(selected_row)


class red_knigi(QtWidgets.QWidget, Ui_BookWindow):
    def __init__(self, refresh_table):
        super().__init__()
        self.setupUi(self)
        self.label.setText("Редактирование")
        self.setWindowModality(2)
        self.refresh_table = refresh_table
        self.pushButton.clicked.connect(self.save_iz_kigi)

    def save_iz_kigi(self):
        # Получите данные из полей для ввода
        kod_knigi = self.lineEdit.text()
        naz = self.lineEdit_2.text()
        avtor = self.lineEdit_3.text()
        izdatelstvo = self.lineEdit_4.text()
        vozras_ogran = self.lineEdit_5.text()
        katalog = self.lineEdit_6.text()
        annotasia = self.lineEdit_7.text()

        # Сохраните данные в базу данных
        try:
            # Подключитесь к базе данных
            conn = bd_connect()
            cursor = conn.cursor()

            # Удалите старую запись, если она существует
            delete_query = "DELETE FROM Книги WHERE Код_книги = ?"
            cursor.execute(delete_query, (kod_knigi,))

            # Выполните запрос на вставку новой записи
            insert_query = "INSERT INTO Книги (Код_книги, Название_книги, Автор, Издательство, Возрастное_ограничение, Каталог, Аннотация) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(insert_query,
                           (kod_knigi, naz, avtor, izdatelstvo, vozras_ogran,
                            katalog, annotasia))

            # Сохраните изменения в базе данных
            conn.commit()

            # Закройте соединение с базой данных
            conn.close()

        except sqlite3.Error as error:
            # Обработайте возможную ошибку при выполнении операций с базой данных
            print("Ошибка при выполнении операций с базой данных:", error)


class dobavit_knigy(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(530, 377)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(10, 10, 511, 361))
        self.frame.setStyleSheet("background-color:rgb(170, 255, 127)")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(190, 10, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(10, 70, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(270, 70, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_3.setGeometry(QtCore.QRect(10, 120, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_4.setGeometry(QtCore.QRect(270, 120, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_5.setGeometry(QtCore.QRect(10, 170, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_6.setGeometry(QtCore.QRect(270, 170, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_7.setGeometry(QtCore.QRect(40, 220, 431, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(190, 300, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Новая книга"))
        self.label.setText(_translate("Dialog", "Новая книги"))
        self.lineEdit.setText(_translate("Dialog", "Код книги"))
        self.lineEdit_2.setText(_translate("Dialog", "Название книги"))
        self.lineEdit_3.setText(_translate("Dialog", "Автор"))
        self.lineEdit_4.setText(_translate("Dialog", "Издательство"))
        self.lineEdit_5.setText(_translate("Dialog", "Возрастное ограничение"))
        self.lineEdit_6.setText(_translate("Dialog", "Каталог"))
        self.lineEdit_7.setText(_translate("Dialog", "Аннотация"))
        self.pushButton.setText(_translate("Dialog", "Создать"))


class Uchet(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1367, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1371, 81))
        self.frame.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.frame.setStyleSheet("background-color:rgb(170, 255, 127)")
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(600, 20, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 20, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.pushButton_3.setObjectName("pushButton_3")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(159, 109, 1081, 561))
        self.frame_2.setStyleSheet("background-color:rgb(170, 255, 127)")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.tableWidget = QtWidgets.QTableWidget(self.frame_2)
        self.tableWidget.setGeometry(QtCore.QRect(105, 61, 871, 461))
        self.tableWidget.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setColumnWidth(0, 350)
        self.tableWidget.setColumnWidth(1, 350)
        self.tableWidget.setColumnWidth(2, 185)

        self.tableWidget.setHorizontalHeaderLabels(
            ["Читатель", "Книга", "Дата сдачи"])  # Заголовки столбцов

        # Подключение к существующей базе данных
        conn = bd_connect()
        cursor = conn.cursor()

        # Выполнение запроса SELECT для получения данных из таблицы книги
        cursor.execute(
            "SELECT Читатели.ФИО AS Читатель, Книги.Название_книги AS Название_книги, Оформление_книги.Дата_сдачи AS Дата_сдачи "
            "FROM Оформление_книги "
            "JOIN Книги ON Оформление_книги.Название_книги = Книги.Код_книги "
            "JOIN Читатели ON Оформление_книги.№читательского_билета = Читатели.№читательского_билета")
        books = cursor.fetchall()

        # Заполнение таблицы данными
        for row_number, row_data in enumerate(books):
            self.tableWidget.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setTextAlignment(QtCore.Qt.AlignVCenter)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                item_font = QtGui.QFont()
                item_font.setPointSize(12)
                item.setFont(item_font)
                item.setSizeHint(QtCore.QSize(100, 100))
                self.tableWidget.setItem(row_number, column_number, item)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.tableWidget.resizeRowsToContents()

        # Закрытие подключения
        conn.close()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Учет выдачи"))
        self.label.setText(_translate("MainWindow", "Учет выдачи"))
        self.pushButton_3.setText(_translate("MainWindow", "Назад"))
        self.pushButton_3.clicked.connect(lambda: self.nazad4(MainWindow))

    def nazad4(self, MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        MainWindow.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = BBMainWindow()
    ui.showMaximized()
    if cnst.MAX:
        ui.showMaximized()
    else:
        ui.show()
    sys.exit(app.exec_())
