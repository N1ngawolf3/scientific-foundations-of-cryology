from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog, QFileDialog
from topdf import topdf, funcs_list
import traceback
import sys





class Warning(QDialog):
    def __init__(self, warning_text):
        super().__init__()
        loadUi(f'UI/Warning.ui', self)
        self.error_text.setText(str(warning_text))


class SCCalcWindow(QDialog):
    def __init__(self, throttling_cycle: str, context: dict):
        super().__init__()
        self.context = context
        self.cycle_name = throttling_cycle
        loadUi(f'UI/{throttling_cycle}_calc.ui', self)
        self.label.setText(throttling_cycle)
        self.fluid_lineEdit.setText(context['fluid'])
        self.Tcon_lineEdit.setText(str(context['Tcon']))
        self.Tev_lineEdit.setText(str(context['Tev']))
        self.p1_lineEdit.setText(str(context['p'][0]))
        self.p2_lineEdit.setText(str(context['p'][1]))
        self.qx_lineEdit.setText(str(context['q_refr']))
        self.l_compr_lineEdit.setText(str(context['l_compr']))
        self.refr_coef_lineEdit.setText(str(context['refr_coef']))
        self.refr_coef_carno_lineEdit.setText(str(context['refr_coef_carno']))
        self.therm_degree_lineEdit.setText(str(context['therm_degree']))
        self.save_button.clicked.connect(self.save)

    def save(self):
        path = QFileDialog.getExistingDirectory()
        surname = str(self.surname_lineEdit.text())
        number = str(self.number_spinBox.text())
        topdf(self.cycle_name, surname, number, self.context, path)


class STLCalcWindow(QDialog):
    def __init__(self, throttling_cycle: str, context: dict):
        super().__init__()
        self.context = context
        self.cycle_name = throttling_cycle
        loadUi(f'UI/{throttling_cycle}_calc.ui', self)
        self.label.setText(throttling_cycle)
        self.fluid_lineEdit.setText(context['fluid'])
        self.p1_lineEdit.setText(str(context['p'][0]))
        self.p_in2_lineEdit.setText(str(context['p_in']))
        self.x_lineEdit.setText(str(context['x'][0]))
        self.Ne0_lineEdit.setText(str(context['Ne0'][0]))
        self.l_compr_lineEdit.setText(str(context['l_compr'][0]))
        self.l_min_lineEdit.setText(str(context['l_min'][0]))
        self.therm_degree_lineEdit.setText(str(context['therm_degree'][0]))

        self.fluid_lineEdit_2.setText(context['fluid'])
        self.p1_lineEdit_2.setText(str(context['p'][1]))
        self.p_in2_lineEdit_2.setText(str(context['p_in']))
        self.x_lineEdit_2.setText(str(context['x'][1]))
        self.Ne0_lineEdit_2.setText(str(context['Ne0'][1]))
        self.l_compr_lineEdit_2.setText(str(context['l_compr'][1]))
        self.l_min_lineEdit_2.setText(str(context['l_min'][1]))
        self.therm_degree_lineEdit_2.setText(str(context['therm_degree'][1]))
        self.save_button.clicked.connect(self.save)

    def save(self):
        path = QFileDialog.getExistingDirectory()
        surname = str(self.surname_lineEdit.text())
        number = str(self.number_spinBox.text())
        topdf(self.cycle_name, surname, number, self.context, path)


class STLDialog(QDialog):
    def __init__(self, title):
        super().__init__()
        try:
            self.title = title
            loadUi(f'UI/{self.title}.ui', self)
            self.setWindowTitle(self.title)
            self.pushButton.clicked.connect(self.calculate)
            self.fluid_comboBox.addItems(['Oxygen','Air','Argon','Nitrogen'])
        except Exception as ex:
            traceback.print_exception(ex)

    def calculate(self):
        try:
            fluid = str(self.fluid_comboBox.currentText())
            p1 = int(self.p1_lineEdit.text())
            p2 = int(self.p2_lineEdit.text())
            p_in = float(self.p_in2_lineEdit.text())
            context = funcs_list[self.title](fluid, p1, p2, p_in)
            calc_window = STLCalcWindow(self.title, context)
            calc_window.exec()
        except Exception as ex:
            traceback.print_exception(ex)
            warning = Warning(ex)
            warning.exec()

class STRDialog(QDialog):
    def __init__(self, title):
        super().__init__()
        try:
            self.title = title
            loadUi(f'UI/{self.title}.ui', self)
            self.setWindowTitle(self.title)
            # self.pushButton.clicked.connect(self.calculate)
            self.fluid_comboBox.addItems(['Oxygen','Air','Argon','Nitrogen'])
        except Exception as ex:
            traceback.print_exception(ex)

class TPRLDialog(QDialog):
    def __init__(self, title):
        super().__init__()
        try:
            self.title = title
            loadUi(f'UI/{self.title}.ui', self)
            self.setWindowTitle(self.title)
            self.fluid_comboBox.addItems(['Oxygen', 'Air', 'Argon', 'Nitrogen'])
            # self.pushButton.clicked.connect(self.calculate)
        except Exception as ex:
            traceback.print_exception(ex)

class TPRRDialog(QDialog):
    def __init__(self, title):
        super().__init__()
        try:
            self.title = title
            loadUi(f'UI/{self.title}.ui', self)
            self.setWindowTitle(self.title)
            self.fluid_comboBox.addItems(['Oxygen', 'Air', 'Argon', 'Nitrogen'])
            # self.pushButton.clicked.connect(self.calculate)
        except Exception as ex:
            traceback.print_exception(ex)


class DTLDialog(QDialog):
    def __init__(self, title):
        super().__init__()
        try:
            self.title = title
            loadUi(f'UI/{self.title}.ui', self)
            self.setWindowTitle(self.title)
            self.fluid_comboBox.addItems(['Oxygen', 'Air', 'Argon', 'Nitrogen'])
            # self.pushButton.clicked.connect(self.calculate)
        except Exception as ex:
            traceback.print_exception(ex)

class DTRDialog(QDialog):
    def __init__(self, title):
        super().__init__()
        try:
            self.title = title
            loadUi(f'UI/{self.title}.ui', self)
            self.setWindowTitle(self.title)
            self.fluid_comboBox.addItems(['Oxygen', 'Air', 'Argon', 'Nitrogen'])
            # self.pushButton.clicked.connect(self.calculate)
        except Exception as ex:
            traceback.print_exception(ex)


class SCDialog(QDialog):
    def __init__(self, title):
        super().__init__()
        try:
            self.title = title
            loadUi(f'UI/{self.title}.ui', self)
            self.setWindowTitle(self.title)
            self.fluid_comboBox.addItems(['R404a', 'R22', 'R134a'])
            self.pushButton.clicked.connect(self.calculate)
        except Exception as ex:
            traceback.print_exception(ex)

    def calculate(self):
        try:
            fluid = str(self.fluid_comboBox.currentText())
            tcon = int(self.Tcon_lineEdit.text()) + 273
            tev = int(self.Tev_lineEdit.text()) + 273
            context = funcs_list[self.title](fluid, tcon, tev)
            calc_window = SCCalcWindow(self.title, context)
            calc_window.exec()
        except Exception as ex:
            traceback.print_exception(ex)
            warning = Warning(ex)
            warning.exec()


dialogs = {'Цикл простого дросселирования Ожижительный режим': STLDialog,
           'Цикл простого дросселирования Рефрижераторный режим': STRDialog,
           'Дроссельный цикл с предварительный охлаждением Рефрижераторный режим': TPRRDialog,
           'Дроссельный цикл с предварительный охлаждением Ожижительный режим': TPRLDialog,
           'Цикл двойного дросселирования Рефрижераторный режим': DTRDialog,
           'Цикл двойного дросселирования Ожижительный режим': DTLDialog,
           'Парокомпрессионный цикл': SCDialog}


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Load the dialog's GUI
        loadUi("UI/main.ui", self)
        self.setWindowTitle('Дроссельные циклы')
        self.setFixedSize(800, 200)
        for number, func in enumerate(dialogs.keys()):
            self.listWidget.insertItem(number, func)
        self.pushButton.clicked.connect(self.item_chosen)
        self.listWidget.doubleClicked.connect(self.item_chosen)

    def item_chosen(self):
        item = self.listWidget.currentItem()
        dlg = dialogs[str(item.text())](str(item.text()))
        dlg.exec()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
