import sys, re, csv, pyperclip

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

from graphics import QtWidgets, Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QSpinBox, QComboBox, QFileDialog, QDialog, QVBoxLayout, \
    QDesktopWidget, QDialogButtonBox
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


def extra_combo_box(game="YuGiOh"):
    if game == "YuGiOh":
        combo = QComboBox()
        combo.addItems(["none", "unlimited", "LIMITED", "1st"])
        return combo
    elif game == "Magic The Gathering":
        combo = QComboBox()
        combo.addItems(["Choose", "none", "Foil", "Not Foil"])
        return combo
    elif game == "Pokémon":
        combo = QComboBox()
        combo.addItems(["Choose", "none", "Foil", "Not Foil"])
        return combo

    return None


# # Class Generated by ChatGPT when asked :
'''
make me a pyqt5 snippet to make a function called "set_all_condition()" that opens a dialog containing a combobox to 
chose from "a", "b" and "c", and puts the chosen value in a variable "result"  if user clicks on accept button, 
and nothing if user exits or clicks on cancel button
'''
class set_dialog(QDialog):
    def __init__(self, items, parent=None):
        super().__init__()
        self.result = None
        self.combo = QComboBox(self)
        self.combo.addItems(items)
        self.combo.currentIndexChanged.connect(self.set_result)
        layout = QVBoxLayout(self)
        layout.addWidget(self.combo)
        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        layout.addWidget(buttonbox)
        self.setLayout(layout)

        self.parent = parent
        positions= self.parent.pos()

    def set_result(self):
        self.result = self.combo.currentText()

    def show(self):
        super().show()
        print("show")
        size = self.size()
        desktop_size = self.parent.size()
        print(self.parent.pos())
        top = (desktop_size.height() - size.height()) // 2
        left = (desktop_size.width() - size.width()) // 2
        self.move(left, top)


def fill_table(filler_list, table, expansion=None):
    debug_print("-- fill table : {}".format(table.objectName()))
    debug_print(filler_list)
    number_of_results = len(filler_list)
    debug_print(number_of_results)
    table.setRowCount(number_of_results)
    for row, line in enumerate(filler_list):
        debug_print(row)
        for col, elem in enumerate(line):
            debug_print(elem)
            if expansion is not None and col == 0:
                table.setItem(row, col, QTableWidgetItem(expansion))
            elif col == 4:
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
            elif col == 7:
                combobox = extra_combo_box()
                if elem != 0:
                    combobox.setCurrentText(elem)
                table.setCellWidget(row, col, combobox)
            else:
                table.setItem(row, col, QTableWidgetItem(elem))


def url_add_condition_language(url, condition, language):
    if '?' in url:
        url = url.split('?')[0]
    separator = '?'
    new_url = url
    if condition != "none":
        new_url += separator + "minCondition=" + str(condition_to_value(condition))
        separator = '&'
    if language != "none":
        new_url += separator + "language=" + str(language_to_value(language))
    return new_url


def list_to_string(chosen_list, urlMode=0, game="YuGiOh"):
    to_copy = ""
    condition = ""
    language = ""
    for line in chosen_list:
        number_of_lines = 0;
        for col, elem in enumerate(line):
            if urlMode == 1:
                if col == 4:
                    number_of_lines = int(elem)
                if col == 5:
                    condition = elem
                if col == 6:
                    language = elem
                if col == 8:
                    elem = url_add_condition_language(elem, condition, language)
                    for i in range(number_of_lines):
                        to_copy += "{}\n".format(elem)
            else:
                if col == 2:
                    to_copy += "\"{}\", ".format(elem)
                elif col == 5:
                    condition = elem
                    to_copy += "{}, ".format(elem)
                elif col == 6:
                    language = elem
                    to_copy += "{}, ".format(elem)
                elif col == 8:
                    elem = url_add_condition_language(elem, condition, language)
                    to_copy += "{}\n".format(elem)
                else:
                    to_copy += "{}, ".format(elem)
    return to_copy


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.pkmn_link_to_id = None
        self.pkmn_id_to_link = None
        self.pkmn_sets = None
        self.pkmn_data = None
        self.mtg_link_to_set = None
        self.current_expansion = None
        self.current_tcg = None
        self.mtg_id_to_link = None
        self.mtg_sets = None
        self.mtg_data = None
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
        self.extra = {}
        self.by_name.clicked.connect(self.sort_by_name)
        self.by_rarity.clicked.connect(self.sort_by_rarity)
        self.by_number.clicked.connect(self.sort_by_number)
        self.by_expansion.clicked.connect(self.sort_by_expansion)

        self.pushButton.clicked.connect(self.add_to_list)
        self.export_btn.clicked.connect(self.export)
        self.import_btn.clicked.connect(self.import_file)
        self.copy_btn.clicked.connect(self.copyToClipboard)

        self.increasing.setChecked(True)

        self.set_language.clicked.connect(self.set_all_languages)
        self.language_set_to = ""
        self.set_extra.clicked.connect(self.set_all_extra)
        self.extra_set_to = ""
        self.set_condition.clicked.connect(self.set_all_conditions)
        self.condition_set_to = ""

        self.duplicate_line.clicked.connect(self.duplicate_selected_line)

        self.game_combobox.addItems(["TCG", "Magic The Gathering", "Yu-Gi-Oh", "Pokémon"])
        self.game_combobox.currentIndexChanged.connect(self.game_choice_combobox)
        self.expansion_combobox.currentIndexChanged.connect(self.expansion_choice_combobox)

        self.expansion_combobox.addItems(["Choose a TCG first"])

        self.load_mtg_file()
        self.load_pokemon_file()


        # Used by the Worker
        self.threadpool = QtCore.QThreadPool()

    def init_table(self, table):
        table.setColumnCount(9)
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # Expansion
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)  # Number
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)  # Name
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)  # Rarity
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)  # Quantity
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)  # Condition
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)  # Language
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)  # Extra
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)  # Link

    def load_mtg_file(self):
        self.mtg_data = {}
        self.mtg_sets = []
        self.mtg_id_to_link = {}
        self.mtg_link_to_set = {}
        with open(".mtg_expansions", "r") as file:
            lines = sorted(file.read().splitlines())
            for line in lines :
                current = line.split(", ")
                cm_url = str(current[-1])
                cm_id = int(current[-2])
                mtg_set = str(current[-3])
                mtg_name = str(current[-4])
                current_name = mtg_set+", "+mtg_name.replace("\"", "")
                self.mtg_id_to_link[cm_id] = cm_url
                self.mtg_link_to_set[cm_url] = mtg_set
                self.mtg_data[current_name] = cm_id
                self.mtg_sets.append(current_name)
        self.mtg_sets = sorted(self.mtg_sets)

    def load_pokemon_file(self):
        self.pkmn_data = {}
        self.pkmn_sets = []
        self.pkmn_id_to_link = {}
        self.pkmn_link_to_set = {}
        with open(".pokemon_expansions", "r") as file :
            lines = sorted(file.read().splitlines())
            for line in lines:
                current = line.split(", ")
                pkmn_set = current[0]
                pkmn_id = current[1]
                pkmn_url = current[2]
                pkmn_name = ''.join(current[3:])
                data = pkmn_set + ", " + pkmn_name.replace("\"", "")
                self.pkmn_data[data] = pkmn_id
                self.pkmn_id_to_link[pkmn_id] = pkmn_url
                self.pkmn_link_to_set[pkmn_url] = pkmn_set
                self.pkmn_sets.append(data)




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
            base_url_2 = url.split('?')[0]
            base_url = re.findall(r'https:\/\/www.cardmarket.com(.*)', base_url_2)[0]
            print("'{}'".format(base_url))
            if "/Magic/" in url:
                self.current_tcg = "Magic The Gathering"
                self.current_expansion = self.mtg_link_to_set.get(base_url)
                print(self.current_expansion)
            if "/YuGiOh/" in url:
                self.current_tcg = "Yu-Gi-Oh"
            if "/Pokemon/" in url:
                self.current_tcg = "Pokémon"
                self.current_expansion = self.pkmn_link_to_set.get(base_url)
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
            self.extra[key] = current_table.cellWidget(row, 7).currentText()
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
            line[7] = self.extra[key]
        fill_table(current_lis, current_table)

    def add_to_list(self):
        self.bottom_list += self.table_to_list(self.found_items_table)
        fill_table(self.bottom_list, self.current_list_table)

    def table_to_list(self, table, type="AddToList"):
        output = []
        for i in range(0, table.rowCount()):
            number_of_item = table.cellWidget(i, 4).value()
            if number_of_item > 0:
                if self.export_combobox.currentText() == "links" and type == "Export":
                    for j in range(number_of_item):
                        output.append([
                            url_add_condition_language(
                                table.item(i, 8).text(),
                                table.cellWidget(i, 5).currentText(),
                                table.cellWidget(i, 6).currentText()
                            )
                        ])
                else:
                    output.append([
                        table.item(i, 0).text(),
                        table.item(i, 1).text(),
                        table.item(i, 2).text(),
                        table.item(i, 3).text(),
                        number_of_item,
                        table.cellWidget(i, 5).currentText(),
                        table.cellWidget(i, 6).currentText(),
                        table.cellWidget(i, 7).currentText(),
                        url_add_condition_language(
                            table.item(i, 8).text(),
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
        if self.current_tcg != "YuGiOh":
            for i in range(len(self.current_found_list)):
                self.current_found_list[i][0] = self.current_expansion

        fill_table(self.current_found_list, self.found_items_table, expansion=self.current_expansion)
        self.run_url_btn.setEnabled(True)

    def cancel_action(self):
        errorDialog("I have not yet found a way to stop an operation, sorry :c")

    def export(self):
        file_name = self.file_dialog()
        if self.export_combobox.currentText() != "links":
            fields = ['Expansion', 'Number', 'Name', 'Rarity', 'Quantity', 'Condition', 'Langage', 'Extra', 'Link']
        else:
            fields = ['Link']
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
        if self.export_combobox.currentText() == "everything":
            to_copy = list_to_string(self.bottom_list)
            pyperclip.copy(to_copy)
        else:
            to_copy = list_to_string(self.bottom_list, 1)
            pyperclip.copy(to_copy)

    def set_all_languages(self):
        dialog = set_dialog(["Choose", "none", "English", "French", "German", "Spanish", "Italian", "S-Chinese", "Japanese",
                             "Portuguese", "Russian", "Korean", "T-Chinese", "Dutch", "Polish", "Czech", "Hungarian"],
                            self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            for i in range(self.found_items_table.rowCount()):
                self.found_items_table.cellWidget(i, 6).setCurrentText(dialog.result)
    def set_all_conditions(self):
        dialog = set_dialog(["Choose", "none", "MT", "NM", "EX", "GD", "LP", "PL", "PO"], self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            for i in range(self.found_items_table.rowCount()):
                self.found_items_table.cellWidget(i, 5).setCurrentText(dialog.result)

    def set_all_extra(self):
        if self.current_tcg == "YuGiOh":
            dialog = set_dialog(["Choose", "none", "unlimited", "LIMITED", "1st"], self)
        elif self.current_tcg == "Pokémon":
            dialog = set_dialog(["Choose", "none", "Foil", "Not Foil"], self)
        elif self.current_tcg == "Magic The Gathering":
            dialog = set_dialog(["Choose", "none", "Foil", "Not Foil"], self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            for i in range(self.found_items_table.rowCount()):
                self.found_items_table.cellWidget(i, 7).setCurrentText(dialog.result)

    def duplicate_selected_line(self):
        row = self.found_items_table.currentRow()
        self.found_items_table.insertRow(row)
        self.found_items_table.setItem(row, 0, QTableWidgetItem(self.found_items_table.item(row+1, 0).text()))
        self.found_items_table.setItem(row, 1, QTableWidgetItem(self.found_items_table.item(row + 1, 1).text()))
        self.found_items_table.setItem(row, 2, QTableWidgetItem(self.found_items_table.item(row + 1, 2).text()))
        self.found_items_table.setItem(row, 3, QTableWidgetItem(self.found_items_table.item(row + 1, 3).text()))
        spinbox = QSpinBox()
        spinbox.setValue(0)
        self.found_items_table.setCellWidget(row, 4, spinbox)
        self.found_items_table.setCellWidget(row, 5, condition_combo_box())
        self.found_items_table.setCellWidget(row, 6, language_combo_box())
        self.found_items_table.setCellWidget(row, 7, extra_combo_box())
        self.found_items_table.setItem(row, 8, QTableWidgetItem(self.found_items_table.item(row + 1, 8).text()))

    def game_choice_combobox(self):
        self.expansion_combobox.clear()
        tcg = self.game_combobox.currentText()
        self.current_tcg = tcg
        print(tcg)
        if tcg == "Magic The Gathering":
            self.expansion_combobox.addItems(self.mtg_sets)
        elif tcg == "Pokémon":
            self.expansion_combobox.addItems(self.pkmn_sets)

    def expansion_choice_combobox(self):
        print("exp")
        print(self.expansion_combobox.currentText(), self.current_tcg)
        if len(self.expansion_combobox.currentText()) < 4:
            return
        if self.current_tcg == "Magic The Gathering":
            crt = self.expansion_combobox.currentText()
            print(crt)
            set = self.mtg_data[crt]
            print(set)
            url = "https://www.cardmarket.com"+self.mtg_id_to_link[set]
            self.url_input_line_edit.setText(url)
        elif self.current_tcg == "Pokémon":
            crt = self.expansion_combobox.currentText()
            set = self.pkmn_data[crt]
            url = "https://www.cardmarket.com" + self.pkmn_id_to_link[set]
            self.url_input_line_edit.setText(url)

    def link_to_base_url(self, url):
        base = url.split("?")[0]
        return base.split(".com")[1]


def graphic():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


graphic()
