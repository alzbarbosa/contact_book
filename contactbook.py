from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QToolBar, \
    QHBoxLayout, QAbstractItemView
from PyQt6.QtGui import QAction, QIcon
import qtawesome

from connection import DatabaseConnection
from models import AlertDialog, AboutDialog, AddContactDialog, EditContactDialog, DeleteDialog, FilterContactDialog
from styles import style_button, style_menu, style_header


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contact Book")
        self.setMinimumSize(800, 600)

        # Create widget and set central
        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        # Create horizontal layout
        self.main_layout = QHBoxLayout()
        self.widget.setLayout(self.main_layout)

        # create icons to be used by menu elements and toolbar elements
        icon_plus = qtawesome.icon('fa.plus', color='green')
        icon_filter = qtawesome.icon('fa.filter', color='green')
        show_all_icon = qtawesome.icon('fa5s.list', color='green')
        edit_icon = qtawesome.icon('fa.edit', color='green')
        delete_icon = qtawesome.icon('fa.trash', color='red')
        about_icon = qtawesome.icon('fa.info-circle', color='green')

        # Set stylesheet for menu bar
        menu_bar = self.menuBar()
        style_menu(menu_bar)

        # Create Menu
        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        about_menu_item = self.menuBar().addMenu("&About")

        # create the actions for menu and toolbar
        add_contact_action = QAction(QIcon(icon_plus), "Add Contact", self)
        add_contact_action.triggered.connect(self.add_contact)

        show_all_contacts_action = QAction(QIcon(show_all_icon), "Show All Contacts", self)
        show_all_contacts_action.triggered.connect(self.load_data)

        filter_action = QAction(QIcon(icon_filter), "Filter", self)
        filter_action.triggered.connect(self.filter_contact)

        edit_action = QAction(QIcon(edit_icon), "Edit", self)
        edit_action.triggered.connect(self.edit_contact)

        delete_action = QAction(QIcon(delete_icon), "Delete", self)
        delete_action.triggered.connect(self.delete_contact)

        about_action = QAction(QIcon(about_icon), "About", self)
        about_action.triggered.connect(self.about)

        # add menu elements
        file_menu_item.addAction(add_contact_action)
        file_menu_item.addAction(show_all_contacts_action)
        edit_menu_item.addAction(edit_action)
        edit_menu_item.addAction(filter_action)
        about_menu_item.addAction(about_action)
        edit_menu_item.addAction(delete_action)

        # Create toolbar and add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_contact_action)
        toolbar.addAction(filter_action)
        toolbar.addAction(edit_action)
        toolbar.addAction(show_all_contacts_action)
        toolbar.addAction(delete_action)

        # Create the table view widget
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Type", "Phone", "Email"))
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Set column widths
        self.table.setColumnWidth(0, 20)  # First column width set to 20 pixels
        self.table.setColumnWidth(1, 220)  # Second column width set to 100 pixels
        self.table.setColumnWidth(2, 70)  # Third column width set to 10 pixels
        self.table.setColumnWidth(3, 115)  # Fourth column width set to 100 pixels
        self.table.setColumnWidth(4, 220)  # Fifth column width set to 100 pixels

        # Set the header style
        header = self.table.horizontalHeader()
        style_header(header)

        # Create buttons
        filter_btn = QPushButton("Filter Contacts", self)
        filter_btn.clicked.connect(self.filter_contact)

        add_btn = QPushButton("Add Contact", self)
        add_btn.clicked.connect(self.add_contact)

        show_btn = QPushButton("Show All", self)
        show_btn.clicked.connect(self.load_data)

        edit_btn = QPushButton("Edit Contact")
        edit_btn.clicked.connect(self.edit_contact)

        delete_btn = QPushButton("Delete Contact")
        delete_btn.clicked.connect(self.delete_contact)

        # Set the button style
        style_button(filter_btn)
        style_button(add_btn)
        style_button(show_btn)
        style_button(edit_btn)
        style_button(delete_btn, '#DC143C', '#B93338')

        # Lay out the GUI
        layout = QVBoxLayout()  #
        layout.addWidget(add_btn)
        layout.addWidget(filter_btn)
        layout.addWidget(edit_btn)
        layout.addWidget(show_btn)
        layout.addStretch()
        layout.addWidget(delete_btn)
        self.main_layout.addWidget(self.table)

        self.main_layout.addLayout(layout)

        # Load initial data
        self.load_data()

    def load_data(self):
        """Loads the data from the table"""
        # Connect to the database and create a cursor object
        conn = DatabaseConnection().connect()
        cur = conn.cursor()

        # Select all rows from the table and fetch the results
        cur.execute("SELECT * FROM contacts")
        result = cur.fetchall()

        # Clean the table before loading new data
        self.table.setRowCount(0)

        # Loop to display the data in the table
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        # Close the connection
        conn.close()

        # Center the data in all columns
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                item.setTextAlignment(Qt.AlignCenter)

    def add_contact(self):
        """Calls a new window to add contact"""
        dialog = AddContactDialog()
        dialog.exec()
        # refresh the data displayed in the main window
        self.load_data()

    def filter_contact(self):
        dialog = FilterContactDialog(self)
        dialog.exec()

    def edit_contact(self):
        # Get the index of the selected row
        index_cell_clicked = self.table.currentRow()

        if index_cell_clicked == -1:
            dialog = AlertDialog()
            dialog.exec()
        else:
            dialog = EditContactDialog(self)
            dialog.exec()
            # refresh the data displayed in the main window
            self.load_data()

    def delete_contact(self):
        # Get the index of the selected row
        index_cell_clicked = self.table.currentRow()

        if index_cell_clicked == -1:
            dialog = AlertDialog()
            dialog.exec()
        else:
            dialog = DeleteDialog(self)
            dialog.exec()
            # refresh the data displayed in the main window
            self.load_data()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()
