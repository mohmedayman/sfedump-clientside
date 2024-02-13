import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QTextEdit,QTableWidget, QTableWidgetItem, QComboBox,QMessageBox,QLineEdit,QCheckBox,QListWidget,QFileDialog

def setup_comparer_tab(parent):
        layout = QVBoxLayout()

        # Comparer label
        comparer_label = QLabel("Comparer")
        layout.addWidget(comparer_label)

        # Text areas for comparison
        parent.text_area_1 = QTextEdit()
        parent.text_area_2 = QTextEdit()

        layout.addWidget(QLabel("Text 1:"))
        layout.addWidget(parent.text_area_1)
        layout.addWidget(QLabel("Text 2:"))
        layout.addWidget(parent.text_area_2)

        # Options for comparison
        options_layout = QHBoxLayout()
        parent.case_sensitive_checkbox = QCheckBox("Case Sensitive")
        parent.line_by_line_checkbox = QCheckBox("Line by Line")

        options_layout.addWidget(parent.case_sensitive_checkbox)
        options_layout.addWidget(parent.line_by_line_checkbox)
        layout.addLayout(options_layout)

        # Compare button
        compare_button = QPushButton("Compare")
        compare_button.clicked.connect(lambda:compare_texts(parent))
        layout.addWidget(compare_button)

        parent.comparer_tab.setLayout(layout)

def compare_texts(parent):
        text1 = parent.text_area_1.toPlainText()
        text2 = parent.text_area_2.toPlainText()

        if parent.case_sensitive_checkbox.isChecked():
            case_sensitive = True
        else:
            case_sensitive = False

        if parent.line_by_line_checkbox.isChecked():
            line_by_line = True
        else:
            line_by_line = False

        if line_by_line:
            text1_lines = text1.splitlines()
            text2_lines = text2.splitlines()
            if len(text1_lines) != len(text2_lines):
                QMessageBox.information(parent, "Comparison Result", "Texts have different line counts.")
                return

            for line1, line2 in zip(text1_lines, text2_lines):
                if not compare_line(parent,line1, line2, case_sensitive):
                    QMessageBox.information(parent, "Comparison Result", "Texts are different.")
                    return

            QMessageBox.information(parent, "Comparison Result", "Texts are identical.")

        else:
            if compare_line(parent,text1, text2, case_sensitive):
                QMessageBox.information(parent, "Comparison Result", "Texts are identical.")
            else:
                QMessageBox.information(parent, "Comparison Result", "Texts are different.")

def compare_line(parent, line1, line2, case_sensitive):
        if case_sensitive:
            return line1 == line2
        else:
            return line1.lower() == line2.lower()
