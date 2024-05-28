from PyQt5.QtWidgets import QTextEdit,QMessageBox,QInputDialog,QWidget
from PyQt5.QtGui import QTextCursor, QTextCharFormat
from PyQt5.QtCore import Qt
class ResponseBox(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet(
            "QTextEdit {"
            "   background-color: #f0f0f0;"  # Black background color
            "   color: green;"              # White text color
            "   border: none;"              # No border
            "   padding: 8px;"              # Padding for better appearance
            "}"
        )
    def clear_text(self):
        #print("here")
        self.clear()

    def search_response(self,parent_tab):
        text_to_find, ok = QInputDialog.getText(parent_tab, "Search", "Enter text to find in the response:")
        if ok:
            text_to_find = str(text_to_find)
            if text_to_find:
                response_text = self.toPlainText()
                if text_to_find in response_text:
                    cursor = QTextCursor(self.document())
                    found = cursor.document().find(text_to_find)
                    if found:
                        cursor.setPosition(found.position())
                        cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, len(text_to_find))
                        self.setTextCursor(cursor)
                        self.ensureCursorVisible()
                        self.setFocus(Qt.OtherFocusReason)
                        QMessageBox.information(self, "Search", f"Text found: {text_to_find}")
                    else:
                        QMessageBox.information(self, "Search", f"Text not found: {text_to_find}")
                else:
                    QMessageBox.information(self, "Search", f"Text not found: {text_to_find}")
