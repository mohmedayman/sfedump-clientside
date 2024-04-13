import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QLineEdit, QCheckBox, QListWidget, QFileDialog
from Widgets.InputBox import *
from Widgets.ResponseBox import *
from Widgets.ClearButton import *
from Widgets.SendButton import *
import urllib.parse
import html
import base64
# import base58
import codecs
import binascii
from PyQt5.QtCore import QRunnable, QThread, QMetaObject, Q_ARG, Qt, QProcess
from PyQt5.QtCore import pyqtSlot, QThreadPool, QObject

def url_encode(decoded_value):
    return urllib.parse.quote(decoded_value)

def url_decode(encoded_value):
    return urllib.parse.unquote(encoded_value)

def html_encode(decoded_value):
    return html.escape(decoded_value)

def html_decode(encoded_value):
    return html.unescape(encoded_value)

def base32_encode(decoded_value):
    return base64.b32encode(decoded_value.encode()).decode()

def base32_decode(encoded_value):
    return base64.b32decode(encoded_value).decode()

# def base58_encode(decoded_value):
#     return base58.b58encode(decoded_value.encode()).decode()
#
# def base58_decode(encoded_value):
#     return base58.b58decode(encoded_value).decode()

def base64_encode(decoded_value):
    return base64.b64encode(decoded_value.encode()).decode()

def base64_decode(encoded_value):
    return base64.b64decode(encoded_value).decode()

def rot13_encode(decoded_value):
    return codecs.encode(decoded_value, 'rot_13')

def rot13_decode(encoded_value):
    return codecs.encode(encoded_value, 'rot_13')

def binary_encode(decoded_value):
    return ''.join(format(ord(char), '08b') for char in decoded_value)

def binary_decode(encoded_value):
    try:
        binary_values = [encoded_value[i:i+8] for i in range(0, len(encoded_value), 8)]
        return ''.join(chr(int(b, 2)) for b in binary_values)
    except:
        decimal_result = ""
        current_binary = ""

        for char in encoded_value:
            if char in ('0', '1'):
                current_binary += char
            else:
                if current_binary:
                    decimal_result += str(int(current_binary, 2))
                    current_binary = ""
                decimal_result += char

        if current_binary:
            decimal_result += str(int(current_binary, 2))

        return decimal_result

def hex_encode(decoded_value):
    return binascii.hexlify(decoded_value.encode()).decode()

def hex_decode(encoded_value):
    try:
        return binascii.unhexlify(encoded_value).decode()
    except:
        decimal_result = ""
        current_hex = ""

        for char in encoded_value:
            if char.isdigit() or (char.lower() in ('a', 'b', 'c', 'd', 'e', 'f')):
                current_hex += char
            else:
                if current_hex:
                    decimal_result += str(int(current_hex, 16))
                    current_hex = ""
                decimal_result += char

        if current_hex:
            decimal_result += str(int(current_hex, 16))

        return decimal_result

def octal_encode(decoded_value):
    return ''.join(format(ord(char), 'o') for char in decoded_value)

def octal_decode(encoded_value):
    try:
        octal_values = encoded_value.split()
        return ''.join(chr(int(octal, 8)) for octal in octal_values)
    except:
        decimal_result = ""
        current_octal = ""

        for char in encoded_value:
            if char in ('0', '1', '2', '3', '4', '5', '6', '7'):
                current_octal += char
            else:
                if current_octal:
                    decimal_result += str(int(current_octal, 8))
                    current_octal = ""
                decimal_result += char

        if current_octal:
            decimal_result += str(int(current_octal, 8))

        return decimal_result
    
def perform_decode_encode(input_string,op,type,output):
    # URL encode & decode
    print(input_string)
    print(type)
    print(op)
#     print(type.lower())
    if type.lower() == "url":
        if op.lower() == "encode":
            url_encoded = url_encode(input_string)
            print(f"URL Encoded: {url_encoded}")
            output.setPlainText(url_encoded)

        elif op.lower() == "decode":
            try:
                url_decoded = url_decode(input_string)
                print(f"URL Decoded: {url_decoded}\n")
                output.setPlainText(url_decoded)
            except Exception as error:
                print(f"invalid input\n", error)
                output.setPlainText("invalid input\n")


    elif type.lower() == "html":
        # HTML encode & decode
        if op.lower() == "encode":
            html_encoded = html_encode(input_string)
            print(f"HTML Encoded: {html_encoded}")
            output.setPlainText(html_encoded)
        elif op.lower() == "decode":
            try:
                html_decoded = html_decode(input_string)
                print(f"HTML Decoded: {html_decoded}\n")
                output.setPlainText(html_decoded)
            except Exception as error:
                print(f"invalid input\n", error)
                output.setPlainText("invalid input\n")

    # Base32 encode & decode
    elif type.lower() == "base32":
        if op.lower() == "encode":
            base32_encoded = base32_encode(input_string)
            print(f"Base32 Encoded: {base32_encoded}")
            output.setPlainText(base32_encoded)
        elif op.lower() == "decode":
            try:
                base32_decoded = base32_decode(input_string)
                print(f"Base32 Decoded: {base32_decoded}\n")
                output.setPlainText(base32_decoded)
            except Exception as error:
                print(f"invalid input\n", error)
                output.setPlainText("invalid input\n")

    # Base58 encode & decode
    # elif type.lower() == "base58":
    #     if op.lower() == "encode":
    #         base58_encoded = base58_encode(input_string)
    #         print(f"Base58 Encoded: {base58_encoded}")
    #     elif op.lower() == "decode":
    #         try:
    #             base58_decoded = base58_decode(input_string)
    #             print(f"Base58 Decoded: {base58_decoded}\n")
    #         except Exception as error:
    #             print(f"invalid input!\n")
    #             self.show_error_message(e)


    # Base64 encode & decode
    elif type.lower() == "base64":
        if op.lower() == "encode":
            base64_encoded = base64_encode(input_string)
            print(f"Base64 Encoded: {base64_encoded}")
            output.setPlainText(base64_encoded)
        elif op.lower() == "decode":
            try:
                base64_decoded = base64_decode(input_string)
                print(f"Base64 Decoded: {base64_decoded}\n")
                output.setPlainText(base64_decoded)
            except Exception as error:
                print(f"invalid input\n", error)
                output.setPlainText("invalid input\n")

    # ROT13 encode & decode
    elif type.lower() == "rot13":
        if op.lower() == "encode":
            rot13_encoded = rot13_encode(input_string)
            print(f"ROT13 Encoded: {rot13_encoded}")
            output.setPlainText(rot13_encoded)
        elif op.lower() == "decode":
            try:
                rot13_decoded = rot13_decode(input_string)
                print(f"ROT13 Decoded: {rot13_decoded}\n")
                output.setPlainText(rot13_decoded)
            except Exception as error:
                print(f"invalid input\n", error)
                output.setPlainText("invalid input\n")

    # Binary encode & decode
    elif type.lower() == "binary":

        if op.lower() == "encode":
            binary_encoded = binary_encode(input_string)
            print(f"Binary Encoded: {binary_encoded}")
            output.setPlainText(binary_encoded)
        elif op.lower() == "decode":
            try:
                binary_decoded = binary_decode(input_string)
                print(f"Binary Decoded: {binary_decoded}\n")
                output.setPlainText(binary_decoded)
            except Exception as error:
                print(f"invalid input\n", error)
                output.setPlainText("invalid input\n")

    # Hexa encode & decode
    if type.lower() == "hexa":
        if op.lower() == "encode":
            hex_encoded = hex_encode(input_string)
            print(f"Hex Encoded: {hex_encoded}")
            output.setPlainText(hex_encoded)
        elif op.lower() == "decode":
            try:
                hex_decoded = hex_decode(input_string)
                print(f"Hex Decoded: {hex_decoded}\n")
                output.setPlainText(hex_decoded)
            except Exception as error:
                print(f"invalid input\n", error)
                output.setPlainText("invalid input\n")
    # Octal encode & decode
    if type.lower() == "octal":
        if op.lower() == "encode":
            octal_encoded = octal_encode(input_string)
            print(f"Octal Encoded: {octal_encoded}")
            output.setPlainText(octal_encoded)
        elif op.lower() == "decode":
            try:
                octal_decoded = octal_decode(input_string)
                print(f"Octal Decoded: {octal_decoded}\n")
                output.setPlainText(octal_decoded)
            except Exception as error:
                print(f"invalid input\n", error)
                output.setPlainText("invalid input\n")


def update_decode_button_text(operation, decode_button):
    decode_button.setText("Encode" if operation == "Encode" else "Decode")

def clear_text(input_text_edit, output_text_edit):
    input_text_edit.clear()
    output_text_edit.clear()

def setup_decoder_tab(parent):
    layout = QVBoxLayout()

    # Decoder label
    decoder_label = QLabel("Text:")
    layout.addWidget(decoder_label)

    Resonse_label = QLabel("Response:")

    # Input and output text areas
    input_text_edit = InputBox()
    output_text_edit = ResponseBox()
    input_text_edit.setPlaceholderText("Enter text to decode/encode")
    output_text_edit.setPlaceholderText("Decoded/encoded text will appear here")
    layout.addWidget(input_text_edit)
    layout.addWidget(Resonse_label)
    layout.addWidget(output_text_edit)

    # Decoder type selection
    decoder_type_label = QLabel("Operation:")
    decoder_type_combo = QComboBox()
    decoder_type_combo.addItem("Encode")
    decoder_type_combo.addItem("Decode")
    layout.addWidget(decoder_type_label)
    layout.addWidget(decoder_type_combo)

    # Encoder type selection
    encoder_type_label = QLabel("Type:")
    encoder_type_combo = QComboBox()
    encoder_type_combo.addItem("URL")
    encoder_type_combo.addItem("HTML")
    encoder_type_combo.addItem("Base32")
    encoder_type_combo.addItem("Base64")
    encoder_type_combo.addItem("ROT13")
    encoder_type_combo.addItem("Hexa")
    encoder_type_combo.addItem("Octal")
    encoder_type_combo.addItem("Binary")
    layout.addWidget(encoder_type_label)
    layout.addWidget(encoder_type_combo)

    # Buttons
    button_layout = QHBoxLayout()
    decode_button = SendButton()
    decode_button.setText("Encode")
    clear_button = ClearButton("Clear")
    button_layout.addWidget(decode_button)
    button_layout.addWidget(clear_button)
    layout.addLayout(button_layout)

    # Connect decode button click to perform decode/encode operation
    decode_button.clicked.connect(lambda: perform_decode_encode(input_text_edit.toPlainText(), decoder_type_combo.currentText(), encoder_type_combo.currentText(),output_text_edit))

    # Connect decoder type combo currentTextChanged to update decode button text
    decoder_type_combo.currentTextChanged.connect(lambda operation: update_decode_button_text(operation, decode_button))
    
    clear_button.clicked.connect(lambda: clear_text(input_text_edit, output_text_edit))

    parent.decoder_tab.setLayout(layout)

class Runnable(QRunnable):
    def __init__(self, main, callable,  *args, **kwargs):
        QRunnable.__init__(self)
        self.main = main
        self.args = args
        self.kwargs = kwargs
        self.callable = callable

    def run(self):

        r = self.callable(*self.args, **self.kwargs)

        QThread.msleep(1000)
        QMetaObject.invokeMethod(self.main, "perform_decode_encode",
                                 Qt.QueuedConnection,
                                 Q_ARG(requests.Response, r))
