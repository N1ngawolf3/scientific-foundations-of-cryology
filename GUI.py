from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog
from topdf import topdf, funcs_list
import traceback
import sys


class CalcWindow(QDialog):
    def __init__(self, throttling_cycle: str, context: dict):
        super().__init__()
        self.context = context
        self.cycle_name = throttling_cycle
        loadUi(f'UI/{throttling_cycle}_calc.ui', self)
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
        topdf(self.cycle_name, '123', 123, self.context)


class Warning(QDialog):
    def __init__(self, warning_text):
        super().__init__()
        loadUi(f'UI/Warning.ui', self)
        self.error_text.setText(str(warning_text))


class Dialog(QDialog):
    def __init__(self, title):
        super().__init__()
        try:
            self.title = title
            loadUi(f'UI/{self.title}.ui', self)
            self.setWindowTitle(self.title)
            self.pushButton.clicked.connect(self.calculate)
        except Exception as ex:
            traceback.print_exception(ex)

    def calculate(self):
        try:
            fluid = str(self.fluid_lineEdit.text())
            tcon = int(self.Tcon_lineEdit.text()) + 273
            tev = int(self.Tev_lineEdit.text()) + 273
            context = funcs_list[self.title](fluid, tcon, tev)
            calc_window = CalcWindow(self.title, context)
            calc_window.exec()
        except Exception as ex:
            traceback.print_exception(ex)
            warning = Warning(ex)
            warning.exec()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Load the dialog's GUI
        loadUi("UI/main.ui", self)
        self.setWindowTitle('Дроссельные циклы')
        self.setFixedSize(800, 200)
        for number, func in enumerate(funcs_list.keys()):
            self.listWidget.insertItem(number, func)
        self.pushButton.clicked.connect(self.item_chosen)
        self.listWidget.doubleClicked.connect(self.item_chosen)

    def item_chosen(self):
        item = self.listWidget.currentItem()
        dlg = Dialog(str(item.text()))
        dlg.exec()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
