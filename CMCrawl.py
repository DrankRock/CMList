import sys, re, csv, pyperclip

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

from graphics import QtWidgets, Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QSpinBox, QComboBox, QFileDialog
from functionalCore import urlScrape

DEBUG = False

dict_language = {
    "none": None,
    "English": 1,
    "French": 2,
    "German": 3,
    "Spanish": 4,
    "Italian": 5,
    "S-Chinese": 6,
    "Japanese": 7,
    "Portuguese": 8,
    "Russian": 9,
    "Korean": 10,
    "T-Chinese": 11,
    "Dutch": 12,
    "Polish": 13,
    "Czech": 14,
    "Hungarian": 15
}

dict_cond = {
    "none": 0,
    "MT": 1,
    "NM": 2,
    "EX": 3,
    "GD": 4,
    "LP": 5,
    "PL": 6,
    "PO": 0
}

def errorDialog(error_message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Error")
    msg.setInformativeText(error_message)
    msg.setWindowTitle("Error")
    msg.exec_()


def debug_print(text):
    if DEBUG:
        print(text)


# =############################################################=#
# ----------------------- WORKER SIGNAL ---------------------- ####
# The worker part is necessary to launch the GUI without stopping #
# the functional core. Freezes are to expect without this      ####
class WorkerSignals(QtCore.QObject):
    progress = pyqtSignal(int)
    end = pyqtSignal(bool)


# =############################################################=#
# ------------------------ WORKER CLASS ---------------------- #
# I followed https://www.pythonguis.com/tutorials/multithreading-pyqt-applications-qthreadpool/
# This tutorial. To avoid pyqt5 freezes.
class Worker(QtCore.QRunnable):
    def __init__(self, url):
        super(Worker, self).__init__()
        # run's variables
        self.output_list = None
        self.url = url
        self.signals = WorkerSignals()

    def run(self):
        self.output_list = urlScrape(self.url, self.signals)

    def output(self):
        return self.output_list


def condition_combo_box():
    combo = QComboBox()
    combo.addItems(["none", "MT", "NM", "EX", "GD", "LP", "PL", "PO"])
    return combo


def condition_to_value(condition):
    return dict_cond.get(condition)


def language_to_value(language):
    return dict_language.get(language)


def language_combo_box():
    combo = QComboBox()
    combo.addItems(["none", "English", "French", "German", "Spanish", "Italian", "S-Chinese", "Japanese", "Portuguese",
                    "Russian", "Korean", "T-Chinese", "Dutch", "Polish", "Czech", "Hungarian"])
    return combo


def fill_table(filler_list, table):
    debug_print("-- fill table : {}".format(table.objectName()))
    debug_print(filler_list)
    number_of_results = len(filler_list)
    debug_print(number_of_results)
    table.setRowCount(number_of_results)
    for row, line in enumerate(filler_list):
        debug_print(row)
        for col, elem in enumerate(line):
            debug_print(elem)
            if col == 4:
                spinbox = QSpinBox()
                spinbox.setValue(int(elem))
                table.setCellWidget(row, col, spinbox)
            elif col == 5:
                combobox = condition_combo_box()
                if elem != 0:
                    combobox.setCurrentText(elem)
                table.setCellWidget(row, col, combobox)
            elif col == 6:
                combobox = language_combo_box()
                if elem != 0:
                    combobox.setCurrentText(elem)
                table.setCellWidget(row, col, combobox)
            else:
                table.setItem(row, col, QTableWidgetItem(elem))


def url_add_condition_language(url, condition, language):
    if '?' in url :
        url = url.split('?')[0]
    separator = '?'
    new_url = url
    if condition != "none":
        new_url += separator + "minCondition=" + str(condition_to_value(condition))
        separator = '&'
    if language != "none":
        new_url += separator + "language=" + str(language_to_value(language))
    return new_url


def list_to_string(chosen_list):
    to_copy = ""
    condition = ""
    language = ""
    for line in chosen_list:
        for col, elem in enumerate(line):
            if col == 2:
                to_copy += "\"{}\", ".format(elem)
            if col == 5:
                condition = elem
            if col == 6:
                language = elem
            if col == 7:
                elem = url_add_condition_language(elem, condition, language)
                to_copy += "{}".format(elem)
            else:
                to_copy += "{}, ".format(elem)

        to_copy += "\n"
    return to_copy


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.worker = None
        self.setupUi(self)
        self.run_url_btn.clicked.connect(self.runURL)
        self.cancel_url_btn.clicked.connect(self.cancel_action)
        self.current_found_list = []
        self.init_table(self.current_list_table)
        self.init_table(self.found_items_table)
        self.bottom_list = []
        self.quantity = {}
        self.condition = {}
        self.language = {}
        self.by_name.clicked.connect(self.sort_by_name)
        self.by_rarity.clicked.connect(self.sort_by_rarity)
        self.by_number.clicked.connect(self.sort_by_number)
        self.by_expansion.clicked.connect(self.sort_by_expansion)

        self.pushButton.clicked.connect(self.add_to_list)
        self.export_btn.clicked.connect(self.export)
        self.import_btn.clicked.connect(self.import_file)
        self.copy_btn.clicked.connect(self.copyToClipboard)

        self.increasing.setChecked(True)

        # Used by the Worker
        self.threadpool = QtCore.QThreadPool()

    def init_table(self, table):
        table.setColumnCount(8)
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)

    def sort_by_name(self):
        self.sort_found_list(self.current_found_list, self.found_items_table, type_of_sort=2)

    def sort_by_rarity(self):
        self.sort_found_list(self.current_found_list, self.found_items_table, type_of_sort=3)

    def sort_by_number(self):
        self.sort_found_list(self.current_found_list, self.found_items_table, type_of_sort=1)

    def sort_by_expansion(self):
        self.sort_found_list(self.current_found_list, self.found_items_table, type_of_sort=0)

    def generic_button_action(self):
        debug_print("Oh hi there ! - {}".format(self.increasing.isChecked()))

    def runURL(self):
        self.found_items_table.clear()
        pattern = re.compile("^https:\/\/www\.cardmarket\.com\/.*")
        url = self.url_input_line_edit.text()
        if not pattern.match(url):
            errorDialog("Error : url is incorrect")
            return
        else:
            self.run_url_btn.setDisabled(True)
            # ## # # # # # #
            self.worker = Worker(url)
            self.threadpool.start(self.worker)
            self.worker.signals.progress.connect(self.update_progress)
            self.worker.signals.end.connect(self.end_worker)
            #  # # # # ## # #

    # sort the top table
    # This deletes the values of the spinBox / combobox. Avoiding this is possible but troublesome
    def sort_found_list(self, current_lis, current_table, type_of_sort=1):
        # type_of_sort 0 = Expansion, 1 = Number, 2 = Name, 3 = Rarity

        # There is a way to keep values, with a dict, conteianing "exp|num|name" : <int>
        # And updating this dict before sorting, then updating the table after filling
        # same should be done for the combobox

        for row in range(len(current_lis)):
            key = "" + current_table.item(row, 0).text() + "|" + current_table.item(row,
                                                                                    1).text() + "|" + current_table.item(
                row, 2).text()
            self.quantity[key] = current_table.cellWidget(row, 4).value()
            self.condition[key] = current_table.cellWidget(row, 5).currentText()
            self.language[key] = current_table.cellWidget(row, 6).currentText()
        debug_print(self.condition)
        debug_print(self.quantity)

        debug_print("Sorting list : {}".format(current_lis))
        current_lis = sorted(current_lis, key=lambda x: x[type_of_sort],
                             reverse=(not self.increasing.isChecked()))
        for line in current_lis:
            key = "" + line[0] + "|" + line[1] + "|" + line[2]
            line[4] = int(self.quantity[key])
            line[5] = self.condition[key]
            line[6] = self.language[key]
        fill_table(current_lis, current_table)

    def add_to_list(self):
        self.bottom_list += self.table_to_list(self.found_items_table)
        fill_table(self.bottom_list, self.current_list_table)

    def table_to_list(self, table):
        output = []
        for i in range(0, table.rowCount()):
            number_of_item = table.cellWidget(i, 4).value()
            if number_of_item > 0:
                output.append([
                    table.item(i, 0).text(),
                    table.item(i, 1).text(),
                    table.item(i, 2).text(),
                    table.item(i, 3).text(),
                    number_of_item,
                    table.cellWidget(i, 5).currentText(),
                    table.cellWidget(i, 6).currentText(),
                    url_add_condition_language(
                        table.item(i, 7).text(),
                        table.cellWidget(i, 5).currentText(),
                        table.cellWidget(i, 6).currentText()
                    )
                ])
        return output

    def update_progress(self, n):
        self.progressBar.setValue(n)

    def end_worker(self, true):
        self.progressBar.setValue(100)
        self.current_found_list = self.worker.output()
        fill_table(self.current_found_list, self.found_items_table)
        self.run_url_btn.setEnabled(True)

    def cancel_action(self):
        errorDialog("I have not yet found a way to stop an operation, sorry :c")

    def export(self):
        file_name = self.file_dialog()
        fields = ['Expansion', 'Number', 'Name', 'Rarity', 'Quantity', 'Condition', 'Langage', 'URL']
        new_list = self.table_to_list(self.current_list_table)
        if file_name:
            with open(file_name, 'w') as f:
                write = csv.writer(f)
                write.writerow(fields)
                write.writerows(new_list)

    def import_file(self):
        file_name = self.file_dialog(1)
        if file_name:
            with open(file_name, 'r') as f:
                data = list(csv.reader(f, delimiter=","))
                if data[0][0] == "Expansion" and data[0][1] == "Number":
                    data = data[1:]
                debug_print("data to import : {}".format(data))
                self.bottom_list += data
                fill_table(self.bottom_list, self.current_list_table)

    def file_dialog(self, type=0):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if type == 0:
            filename, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                      "All Files (*);;Python Files (*.py)", options=options)
        else:
            filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.geOpenFileName()", "",
                                                      "All Files (*);;Python Files (*.py)", options=options)
        if filename:
            return filename

    def copyToClipboard(self):
        to_copy = list_to_string(self.bottom_list)
        pyperclip.copy(to_copy)


def graphic():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


graphic()
