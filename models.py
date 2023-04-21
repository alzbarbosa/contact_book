from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QGridLayout, QTableWidgetItem
from connection import DatabaseConnection
list_of_types_of_contact = ["Friend", "Family", "Network", "Work", "Other"]


class AlertDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        # window setup
        self.setWindowTitle("About")
        content = "Please select a contact first"
        self.setText(content)


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = "This app was created by Andre Barbosa"
        self.setText(content)


class AddContactDialog(QDialog):
    def __init__(self):
        super().__init__()

        # window setup
        self.setWindowTitle("Insert Contact")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()
        self.setLayout(layout)

        # add contact name widget
        self.contact_name = QLineEdit()
        self.contact_name.setPlaceholderText("Name")
        layout.addWidget(self.contact_name)

        # add type of contact widget
        self.type_contact = QComboBox()
        types_of_contact = list_of_types_of_contact
        self.type_contact.addItems(types_of_contact)
        layout.addWidget(self.type_contact)

        # add contact phone widget
        self.contact_phone = QLineEdit()
        self.contact_phone.setPlaceholderText("Phone")
        layout.addWidget(self.contact_phone)

        # add contact phone widget
        self.contact_email = QLineEdit()
        self.contact_email.setPlaceholderText("Email")
        layout.addWidget(self.contact_email)

        # add a submit button
        add_btn = QPushButton("Add Contact")
        add_btn.clicked.connect(self.add_contact)
        layout.addWidget(add_btn)

    def add_contact(self):
        # collect data input by the user to insert into the table
        contact_name = self.contact_name.text()
        type_contact = self.type_contact.itemText(self.type_contact.currentIndex())
        contact_phone = self.contact_phone.text()
        contact_email = self.contact_email.text()

        # check if contact_name is empty
        if not contact_name.strip():
            QMessageBox.warning(self, "Warning", "Please enter a name.")
            return

        elif not contact_phone.isdigit():
            QMessageBox.warning(self, "Invalid phone number", "Phone number must contain only digits.")
            return

        # connect to the database and create a cursor object
        conn = DatabaseConnection().connect()
        cur = conn.cursor()

        # insert the data into the table
        cur.execute("INSERT INTO contacts (name, type, phone, email) VALUES (?, ?, ?, ?)",
                       (contact_name, type_contact, contact_phone, contact_email))

        # commit the changes to the database
        conn.commit()

        # close the cursor object and database connection
        cur.close()
        conn.close()

        # close the add contact window
        self.close()


class EditContactDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        # window setup
        self.setWindowTitle("Update Contact")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Get the index of the selected row
        index_cell_clicked = main_window.table.currentRow()

        # Get contact id from selected row
        self.contact_id = main_window.table.item(index_cell_clicked, 0).text()

        # Add contact name widget
        current_contact_name = main_window.table.item(index_cell_clicked, 1).text()
        self.contact_name = QLineEdit(current_contact_name)
        layout.addWidget(self.contact_name)

        # Add combo box of types of contacts
        current_type_contact = main_window.table.item(index_cell_clicked, 2).text()
        self.type_of_contacts_box = QComboBox()
        types_contacts = list_of_types_of_contact
        self.type_of_contacts_box.addItems(types_contacts)
        self.type_of_contacts_box.setCurrentText(current_type_contact)
        layout.addWidget(self.type_of_contacts_box)

        # Add phone widget
        current_contact_phone = main_window.table.item(index_cell_clicked, 3).text()
        self.contact_phone = QLineEdit(current_contact_phone)
        layout.addWidget(self.contact_phone)

        # Add email widget
        current_contact_email = main_window.table.item(index_cell_clicked, 4).text()
        self.contact_email = QLineEdit(current_contact_email)
        layout.addWidget(self.contact_email)

        # Add a submit button
        update_btn = QPushButton("Update Contact")
        update_btn.clicked.connect(self.update_contact)
        layout.addWidget(update_btn)

    def update_contact(self):
        # connect to the database and create a cursor object
        conn = DatabaseConnection().connect()
        cur = conn.cursor()

        # update the data
        cur.execute("UPDATE contacts SET name = ?, type = ?, phone = ?, email = ? WHERE id = ?",
                       (self.contact_name.text(), self.type_of_contacts_box.itemText(self.type_of_contacts_box.currentIndex()),
                        self.contact_phone.text(), self.contact_email.text(), self.contact_id))

        # commit the changes to the database
        conn.commit()

        # close the cursor object and database connection
        cur.close()
        conn.close()

        # close the add contact window
        self.close()


class DeleteDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()

        # window setup
        self.setWindowTitle("Delete Contact")
        layout = QGridLayout()
        self.setLayout(layout)

        # Get the index of the selected row
        self.index_cell_clicked = main_window.table.currentRow()

        # Get contact id from selected row
        self.contact_id = main_window.table.item(self.index_cell_clicked, 0).text()
        self.contact_name = main_window.table.item(self.index_cell_clicked, 1).text()

        # confirmation box text
        confirmation = QLabel("Are you sure you want to delete?")
        contact_info = QLabel(f"Contact: {self.contact_name}")
        y_btn = QPushButton("Yes")
        n_btn = QPushButton("No")

        # confirmation box layout
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(contact_info, 1, 0, 1, 2)
        layout.addWidget(y_btn, 2, 0)
        layout.addWidget(n_btn, 2, 1)

        # link delete_contact to button Yes
        y_btn.clicked.connect(self.delete_contact)

        # close the dialog if "No" button is clicked
        n_btn.clicked.connect(self.reject)

        self.main_window = main_window

    def delete_contact(self):
        conn = DatabaseConnection().connect()
        cur = conn.cursor()
        cur.execute("DELETE from contacts WHERE id = ?", (self.contact_id, ))

        # commit the changes to the database
        conn.commit()

        # close the cursor object and database connection
        cur.close()
        conn.close()

        # close the add contact window
        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()


class FilterContactDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()

        # save the instance of MainWindow
        self.main_window = main_window

        # Set window title and size
        self.setWindowTitle("Filter Contacts")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Create layout and input widget
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Create button
        button = QPushButton("Search")
        button.clicked.connect(self.filter_contacts)
        layout.addWidget(button)

        self.setLayout(layout)

    def filter_contacts(self):
        name = self.student_name.text()
        conn = DatabaseConnection().connect()
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM contacts WHERE name LIKE ?", ('%' + name + '%',))
        # Clean the table before loading new data
        self.main_window.table.setRowCount(0)
        list_result = list(result)
        # Loop to display the data in the table
        for row_number, row_data in enumerate(list_result):
            self.main_window.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.main_window.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        # Close the connection
        conn.close()

        # close the add contact window
        self.close()

        # Center the data in all columns
        self.table = self.main_window.table
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                item.setTextAlignment(Qt.AlignCenter)
