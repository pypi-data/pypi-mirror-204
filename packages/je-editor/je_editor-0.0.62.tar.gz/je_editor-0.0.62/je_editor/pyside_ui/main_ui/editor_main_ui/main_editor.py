import os

from PySide6.QtGui import QFontDatabase, QAction
from PySide6.QtWidgets import QMainWindow

from je_editor.pyside_ui.main_ui_setting.ui_setting import set_ui
from je_editor.pyside_ui.menu.menu_bar.set_menu_bar import set_menu_bar
from je_editor.pyside_ui.treeview.project_treeview.set_project_treeview import set_project_treeview
from je_editor.utils.file.save.save_file import SaveThread


class EditorMain(QMainWindow):

    def __init__(self):
        super(EditorMain, self).__init__()
        # set python buffered
        os.environ["PYTHONUNBUFFERED"] = "1"
        # Auto save thread
        self.auto_save_thread = None
        # current file
        self.current_file = None
        # Font
        self.font_database = QFontDatabase()
        set_ui(self)
        set_project_treeview(self)
        set_menu_bar(self)
        self.add_font_menu()
        self.add_font_size_menu()
        self.showMaximized()
        self.focusWidget()
        if self.current_file is not None and self.auto_save_thread is None:
            self.auto_save_thread = SaveThread(
                self.current_file,
                self.code_edit.code_edit.toPlainText()
            )

    def add_font_menu(self):
        self.font_menu = self.text_menu.addMenu("Font")
        for family in self.font_database.families():
            font_action = QAction(family, parent=self)
            font_action.triggered.connect(self.set_font)
            self.font_menu.addAction(font_action)

    def add_font_size_menu(self):
        self.font_size_menu = self.text_menu.addMenu("Font Size")
        for size in range(12, 38, 2):
            font_action = QAction(str(size), parent=self)
            font_action.triggered.connect(self.set_font_size)
            self.font_size_menu.addAction(font_action)

    def set_font(self):
        self.code_edit.setFont(self.font_database.font(self.sender().text(), "", 12))
        self.code_result.setFont(self.font_database.font(self.sender().text(), "", 12))

    def set_font_size(self):
        self.code_edit.setFont(
            self.font_database.font(
                self.font().family(),
                "",
                int(self.sender().text())
            )
        )
        self.code_result.setFont(
            self.font_database.font(
                self.font().family(),
                "",
                int(self.sender().text())
            )
        )
