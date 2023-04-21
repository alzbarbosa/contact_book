def style_button(button, primary_color='#4CAF50', secondary_color='#3e8e41'):
    button.setStyleSheet(f'''
        QPushButton {{
            background-color: {primary_color};
            color: white;
            font-size: 14px;
            padding: 6px 12px;
            border-radius: 4px;
        }}
        QPushButton:hover {{
            background-color: {secondary_color};
        }}
    ''')


def style_menu(menu_bar):
     menu_bar.setStyleSheet("""
        QMenuBar {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #424242, 
                            stop: 0.6 #303030, stop:1 #303030);
            color: white;
            padding: 2px;
        }
        QMenuBar::item {
            spacing: 3px;
            padding: 2px 10px;
            background-color: transparent;
            border-radius: 4px;
        }
        QMenuBar::item:selected {
            background-color: #b7b7b7;
        }
    """)


def style_header(header):
    header.setStyleSheet("""
                        QHeaderView::section {
                            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #424242, 
                            stop: 0.6 #303030, stop:1 #303030);
                            color: white;
                            padding-left: 4px;
                            border: 1px solid #6c6c6c;
                        }""")
