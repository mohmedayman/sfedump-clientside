import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QTextEdit,QTableWidget, QTableWidgetItem, QComboBox,QMessageBox,QLineEdit,QCheckBox,QListWidget,QFileDialog
from PyQt5.QtGui import QIcon


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Burp Suite Application")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("icon.jpeg"))
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create a tab widget
        self.tabs = QTabWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_widget.setLayout(main_layout)

        # Create tabs
        self.proxy_tab = QWidget()
        self.target_tab = QWidget()
        self.intruder_tab = QWidget()
        self.repeater_tab = QWidget()
        self.sequencer_tab = QWidget()
        self.decoder_tab = QWidget()
        self.comparer_tab = QWidget()
        self.extender_tab = QWidget()

        # Add tabs to tab widget
        self.tabs.addTab(self.proxy_tab, "Proxy")
        self.tabs.addTab(self.target_tab, "Target")
        self.tabs.addTab(self.intruder_tab, "Intruder")
        self.tabs.addTab(self.repeater_tab, "Repeater")
        self.tabs.addTab(self.sequencer_tab, "Sequencer")
        self.tabs.addTab(self.decoder_tab, "Decoder")
        self.tabs.addTab(self.comparer_tab, "Comparer")
        self.tabs.addTab(self.extender_tab, "Extender")

        # Add content to tabs
        self.setup_proxy_tab()
        self.setup_target_tab()
        self.setup_sequencer_tab()
        self.setup_decoder_tab()
        self.setup_intruder_tab()
        self.setup_repeater_tab()
        self.setup_comparer_tab()
        self.setup_extender_tab()
        # Add content to proxy tab
    def setup_proxy_tab(self):
        layout = QVBoxLayout()

        # Proxy status label
        self.proxy_status_label = QLabel("Proxy Status: Running")
        layout.addWidget(self.proxy_status_label)

        # Request section
        request_label = QLabel("Request:")
        self.request_text_edit = QTextEdit()
        layout.addWidget(request_label)
        layout.addWidget(self.request_text_edit)

        # Response section
        response_label = QLabel("Response:")
        self.response_text_edit = QTextEdit()
        layout.addWidget(response_label)
        layout.addWidget(self.response_text_edit)

        # Buttons
        button_layout = QHBoxLayout()
        clear_button = QPushButton("Clear")
        forward_button = QPushButton("Forward")
        drop_button = QPushButton("Drop")

        button_layout.addWidget(clear_button)
        button_layout.addWidget(forward_button)
        button_layout.addWidget(drop_button)

        layout.addLayout(button_layout)

        self.proxy_tab.setLayout(layout)

        # Connect buttons to functions
        clear_button.clicked.connect(self.clear_content)
        forward_button.clicked.connect(self.forward_request)
        drop_button.clicked.connect(self.drop_request)

    def clear_content(self):
        self.request_text_edit.clear()
        self.response_text_edit.clear()

    def forward_request(self):
        # Logic to forward the request
        pass

    def drop_request(self):
        # Logic to drop the request
        pass

        # Add content to target tab
        

    def setup_target_tab(self):
        layout = QVBoxLayout()

        # Target label
        target_label = QLabel("Target")
        layout.addWidget(target_label)

        # Host and port input fields
        host_label = QLabel("Host:")
        self.host_input = QTextEdit()
        layout.addWidget(host_label)
        layout.addWidget(self.host_input)

        port_label = QLabel("Port:")
        self.port_input = QTextEdit()
        layout.addWidget(port_label)
        layout.addWidget(self.port_input)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        clear_button = QPushButton("Clear")

        save_button.clicked.connect(self.save_target)
        clear_button.clicked.connect(self.clear_target)

        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        layout.addLayout(button_layout)

        # Display table button
        display_button = QPushButton("Display Hosts Table")
        display_button.clicked.connect(self.display_table)
        layout.addWidget(display_button)

        self.target_tab.setLayout(layout)

    # Table widget for displaying hosts and ports
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Host", "Port"])

    def save_target(self):
        host = self.host_input.toPlainText()
        port = self.port_input.toPlainText()
        if host and port:
            # Add data to the table
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(host))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(port))

            print(f"Saved target: Host - {host}, Port - {port}")
            # You can add logic here to save the target to a file or database
        else:
            print("Please provide both host and port.")

    def clear_target(self):
        self.host_input.clear()
        self.port_input.clear()

    def display_table(self):
        self.table_widget.setWindowIcon(QIcon('icon.jpeg'))
        self.table_widget.show()

    def setup_intruder_tab(self):
        layout = QVBoxLayout()

        # Intruder label
        intruder_label = QLabel("Intruder")
        layout.addWidget(intruder_label)

        # Request section
        request_label = QLabel("Request:")
        self.request_text_edit = QTextEdit()
        layout.addWidget(request_label)
        layout.addWidget(self.request_text_edit)

        # Payload section
        payload_label = QLabel("Payload:")
        self.payload_text_edit = QTextEdit()
        layout.addWidget(payload_label)
        layout.addWidget(self.payload_text_edit)

        # Payload type selection
        payload_type_label = QLabel("Payload Type:")
        self.payload_type_combo = QComboBox()
        self.payload_type_combo.addItem("Simple List")
        self.payload_type_combo.addItem("Numbers")
        self.payload_type_combo.addItem("Characters")
        layout.addWidget(payload_type_label)
        layout.addWidget(self.payload_type_combo)

        # Buttons
        button_layout = QHBoxLayout()
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start_intruder)
        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self.stop_intruder)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_intruder)

        button_layout.addWidget(start_button)
        button_layout.addWidget(stop_button)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

        self.intruder_tab.setLayout(layout)

    def start_intruder(self):
        # Get the request and payload from text areas
        request = self.request_text_edit.toPlainText()
        payload = self.payload_text_edit.toPlainText()

        if not request:
            QMessageBox.warning(self, "Warning", "Please provide a request to intrude.")
            return

        if not payload:
            QMessageBox.warning(self, "Warning", "Please provide a payload for the intruder.")
            return

        # Parse the payload based on the selected payload type
        selected_payload_type = self.payload_type_combo.currentText()
        payloads = []
        if selected_payload_type == "Simple List":
            payloads = payload.split("\n")  # Assuming each line contains a separate payload
        elif selected_payload_type == "Numbers":
            try:
                start, end = map(int, payload.split("-"))
                payloads = list(range(start, end + 1))
            except ValueError:
                QMessageBox.warning(self, "Warning", "Invalid number range format. Please provide start and end separated by '-'")
                return
        elif selected_payload_type == "Characters":
            payloads = [char for char in payload]

        # Placeholder for processing responses and displaying results
        results = []
        for payload in payloads:
            # Send the request with the payload
            # Receive and process the response
            # Here, we simply generate placeholder results
            result = f"Payload: {payload} - Response: Placeholder Response"
            results.append(result)

        # Display results in a user-friendly manner
        QMessageBox.information(self, "Intruder Results", "\n".join(results))


    def stop_intruder(self):
        # Placeholder logic for stopping intruder
        QMessageBox.information(self, "Information", "Intruder Stopped")

    def clear_intruder(self):
        # Clear request and payload text areas
        self.request_text_edit.clear()
        self.payload_text_edit.clear()

        self.repeater_layout = QVBoxLayout()
        self.repeater_layout.addWidget(QLabel("Repeater Content"))
        self.repeater_tab.setLayout(self.repeater_layout)

    def setup_repeater_tab(self):
        layout = QVBoxLayout()

        # Repeater label
        repeater_label = QLabel("Repeater")
        layout.addWidget(repeater_label)

        # Request and response text areas
        self.request_text_edit = QTextEdit()
        self.response_text_edit = QTextEdit()
        layout.addWidget(QLabel("Request:"))
        layout.addWidget(self.request_text_edit)
        layout.addWidget(QLabel("Response:"))
        layout.addWidget(self.response_text_edit)

        # HTTP methods combo box
        self.http_methods_combo = QComboBox()
        self.http_methods_combo.addItems(["GET", "POST", "PUT", "DELETE"])
        layout.addWidget(self.http_methods_combo)

        # Headers input
        self.headers_label = QLabel("Headers:")
        self.headers_text_edit = QTextEdit()
        layout.addWidget(self.headers_label)
        layout.addWidget(self.headers_text_edit)

        # Content type combo box
        self.content_type_combo = QComboBox()
        self.content_type_combo.addItems(["application/json", "application/xml", "text/plain"])
        layout.addWidget(QLabel("Content Type:"))
        layout.addWidget(self.content_type_combo)

        # Authentication input
        self.auth_label = QLabel("Authentication:")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.auth_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)

        # Send, Save, and Clear buttons
        button_layout = QHBoxLayout()
        send_button = QPushButton("Send")
        save_button = QPushButton("Save")
        clear_button = QPushButton("Clear")

        send_button.clicked.connect(self.send_request)
        save_button.clicked.connect(self.save_request)
        clear_button.clicked.connect(self.clear_fields)

        button_layout.addWidget(send_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        layout.addLayout(button_layout)

        self.repeater_tab.setLayout(layout)

    def send_request(self):
        method = self.http_methods_combo.currentText()
        url = "http://localhost:8000"  # Example URL, change it to your server's URL
        request = self.request_text_edit.toPlainText()

        headers = {}
        headers_text = self.headers_text_edit.toPlainText()
        if headers_text:
            for line in headers_text.split('\n'):
                key, value = line.split(': ')
                headers[key] = value

        content_type = self.content_type_combo.currentText()
        headers['Content-Type'] = content_type

        auth = None
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            auth = (username, password)

        try:
            response = requests.request(method, url, data=request, headers=headers, auth=auth)
            response_text = f"Status Code: {response.status_code}\n\n{response.text}"
            self.response_text_edit.setPlainText(response_text)
        except requests.RequestException as e:
            QMessageBox.warning(self, "Request Error", str(e))

    def save_request(self):
        # Placeholder for saving the request to a file
        request = self.request_text_edit.toPlainText()
        if request:
            with open("saved_request.txt", "w") as file:
                file.write(request)
            QMessageBox.information(self, "Save Request", "Request saved successfully.")
        else:
            QMessageBox.warning(self, "Save Request", "No request to save.")

    def clear_fields(self):
        # Clearing the request and response text areas
        self.request_text_edit.clear()
        self.response_text_edit.clear()
        self.headers_text_edit.clear()
        self.username_input.clear()
        self.password_input.clear()
    def setup_sequencer_tab(self):
        layout = QVBoxLayout()

        # Sequencer label
        sequencer_label = QLabel("Sequencer")
        layout.addWidget(sequencer_label)

        # Input and output text areas
        self.input_text_edit = QTextEdit()
        self.output_text_edit = QTextEdit()
        self.input_text_edit.setPlaceholderText("Enter text to sequence")
        self.output_text_edit.setPlaceholderText("Sequence results will appear here")
        layout.addWidget(self.input_text_edit)
        layout.addWidget(self.output_text_edit)

        # Start and stop buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.start_button.clicked.connect(self.start_sequence)
        self.stop_button.clicked.connect(self.stop_sequence)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        self.sequencer_tab.setLayout(layout)

    def start_sequence(self):
        input_text = self.input_text_edit.toPlainText()
        if not input_text:
            self.output_text_edit.setPlainText("Please enter text to sequence.")
            return

        # Perform sequence generation and calculation here
        sequence_result = self.generate_sequence(input_text)

        # Display the result
        self.output_text_edit.setPlainText(sequence_result)

    def stop_sequence(self):
        # Placeholder for stopping sequence
        pass

    def generate_sequence(self, input_text):
        # Placeholder for generating sequence
        # For now, simply return the input text as is
        return input_text


    def setup_decoder_tab(self):
        layout = QVBoxLayout()

        # Decoder label
        decoder_label = QLabel("Decoder")
        layout.addWidget(decoder_label)

        # Input and output text areas
        input_text_edit = QTextEdit()
        output_text_edit = QTextEdit()
        input_text_edit.setPlaceholderText("Enter text to decode/encode")
        output_text_edit.setPlaceholderText("Decoded/encoded text will appear here")
        layout.addWidget(input_text_edit)
        layout.addWidget(output_text_edit)

        # Decoder type selection
        decoder_type_label = QLabel("Decoder Type:")
        decoder_type_combo = QComboBox()
        decoder_type_combo.addItem("URL")
        decoder_type_combo.addItem("Base64")
        decoder_type_combo.addItem("HTML")
        decoder_type_combo.addItem("Hex")
        decoder_type_combo.addItem("Octal")
        decoder_type_combo.addItem("Binary")
        layout.addWidget(decoder_type_label)
        layout.addWidget(decoder_type_combo)
        # Decoder type selection
        encoder_type_label = QLabel("Encoder Type:")
        encoder_type_combo = QComboBox()
        encoder_type_combo.addItem("URL")
        encoder_type_combo.addItem("Base64")
        encoder_type_combo.addItem("HTML")
        encoder_type_combo.addItem("Hex")
        encoder_type_combo.addItem("Octal")
        encoder_type_combo.addItem("Binary")
        layout.addWidget(encoder_type_label)
        layout.addWidget(encoder_type_combo)

        # Buttons
        button_layout = QHBoxLayout()
        decode_button = QPushButton("Decode")
        clear_button = QPushButton("Clear")
        decode_button.clicked.connect(self.Decode)
        button_layout.addWidget(decode_button)
        button_layout.addWidget(clear_button)
        layout.addLayout(button_layout)
        
        self.decoder_tab.setLayout(layout)
    def Decode(self):
        #logic to decode here
        pass
    
    def setup_comparer_tab(self):
        layout = QVBoxLayout()

        # Comparer label
        comparer_label = QLabel("Comparer")
        layout.addWidget(comparer_label)

        # Text areas for comparison
        self.text_area_1 = QTextEdit()
        self.text_area_2 = QTextEdit()

        layout.addWidget(QLabel("Text 1:"))
        layout.addWidget(self.text_area_1)
        layout.addWidget(QLabel("Text 2:"))
        layout.addWidget(self.text_area_2)

        # Options for comparison
        options_layout = QHBoxLayout()
        self.case_sensitive_checkbox = QCheckBox("Case Sensitive")
        self.line_by_line_checkbox = QCheckBox("Line by Line")

        options_layout.addWidget(self.case_sensitive_checkbox)
        options_layout.addWidget(self.line_by_line_checkbox)
        layout.addLayout(options_layout)

        # Compare button
        compare_button = QPushButton("Compare")
        compare_button.clicked.connect(self.compare_texts)
        layout.addWidget(compare_button)

        self.comparer_tab.setLayout(layout)

    def compare_texts(self):
        text1 = self.text_area_1.toPlainText()
        text2 = self.text_area_2.toPlainText()

        if self.case_sensitive_checkbox.isChecked():
            case_sensitive = True
        else:
            case_sensitive = False

        if self.line_by_line_checkbox.isChecked():
            line_by_line = True
        else:
            line_by_line = False

        if line_by_line:
            text1_lines = text1.splitlines()
            text2_lines = text2.splitlines()
            if len(text1_lines) != len(text2_lines):
                QMessageBox.information(self, "Comparison Result", "Texts have different line counts.")
                return

            for line1, line2 in zip(text1_lines, text2_lines):
                if not self.compare_line(line1, line2, case_sensitive):
                    QMessageBox.information(self, "Comparison Result", "Texts are different.")
                    return

            QMessageBox.information(self, "Comparison Result", "Texts are identical.")

        else:
            if self.compare_line(text1, text2, case_sensitive):
                QMessageBox.information(self, "Comparison Result", "Texts are identical.")
            else:
                QMessageBox.information(self, "Comparison Result", "Texts are different.")

    def compare_line(self, line1, line2, case_sensitive):
        if case_sensitive:
            return line1 == line2
        else:
            return line1.lower() == line2.lower()

    def setup_extender_tab(self):
        layout = QVBoxLayout()

        # Extender label
        extender_label = QLabel("Extender")
        layout.addWidget(extender_label)

        # List widget to display loaded extensions
        self.extension_list = QListWidget()
        layout.addWidget(self.extension_list)

        # Load and Unload buttons
        button_layout = QHBoxLayout()
        load_button = QPushButton("Load Extension")
        unload_button = QPushButton("Unload Extension")
        configure_button = QPushButton("Configure Extension")
        run_button = QPushButton("Run Extension")

        load_button.clicked.connect(self.load_extension)
        unload_button.clicked.connect(self.unload_extension)
        configure_button.clicked.connect(self.configure_extension)
        run_button.clicked.connect(self.run_extension)

        button_layout.addWidget(load_button)
        button_layout.addWidget(unload_button)
        button_layout.addWidget(configure_button)
        button_layout.addWidget(run_button)
        layout.addLayout(button_layout)

        self.extender_tab.setLayout(layout)

    def load_extension(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Extension", "", "Python Files (*.py)")
        if file_path:
            self.extension_list.addItem(file_path)
            QMessageBox.information(self, "Extension Loaded", "Extension loaded successfully.")

    def unload_extension(self):
        selected_item = self.extension_list.currentItem()
        if selected_item:
            self.extension_list.takeItem(self.extension_list.row(selected_item))
            QMessageBox.information(self, "Extension Unloaded", "Extension unloaded successfully.")
        else:
            QMessageBox.warning(self, "No Extension Selected", "Please select an extension to unload.")
    
    def configure_extension(self):
        pass

    def run_extension(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())