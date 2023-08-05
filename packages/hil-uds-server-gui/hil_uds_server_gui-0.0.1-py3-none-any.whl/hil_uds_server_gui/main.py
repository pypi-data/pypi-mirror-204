import os
import yaml

from PyQt5 import QtCore, QtGui, QtWidgets
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import PushButton, PrimaryPushButton, InfoBar, InfoBarPosition

from .ui import window, home, card
from . import client

current_path = os.path.dirname(os.path.abspath(__file__))
default_qss = os.path.join(current_path, "default.qss")

class BaseWindow(QtWidgets.QMainWindow):
    qss = "app.qss"
    default_qss = default_qss

    def __init__(self):
        super().__init__()
        self.ui = window.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupWatcher()
        self.setupQss()

    def setupWatcher(self):
        self.watcher = QtCore.QFileSystemWatcher(self)
        self.watcher.addPath(self.qss)
        self.watcher.fileChanged.connect(self.setupQss)

    def setupQss(self):
        try:
            if os.path.exists(self.default_qss):
                with open(self.default_qss, "r", encoding="utf-8") as f:
                    stylesheet = f.read()
                    self.setStyleSheet(stylesheet)
            with open(self.qss, "r", encoding="utf-8") as f:
                stylesheet = f.read()
                self.setStyleSheet(stylesheet)
        except:
            pass


class CardView(QtWidgets.QWidget):
    def __init__(self, parent=None, title: str = ""):
        super().__init__(parent)
        self.ui = card.Ui_Card()
        self.ui.setupUi(self)
        self.ui.vBoxLayout.setAlignment(QtCore.Qt.AlignTop)
        self.ui.linkIcon.setIcon(FIF.LINK)
        self.ui.linkIcon.setFixedSize(16, 16)
        self.setTitle(title)

    def setTitle(self, title: str):
        self.ui.titleLabel.setText(title)

    def setDescrreption(self, desc: str):
        self.ui.sourcePathLabel.setText(desc)

    def setContentWidget(self, widget: QtWidgets.QWidget):
        self.ui.topLayout.addWidget(widget, 0, QtCore.Qt.AlignLeft)


class HomeView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = home.Ui_Home()
        self.ui.setupUi(self)
        self.ui.verticalLayout.setAlignment(QtCore.Qt.AlignTop)

    def addCard(self, title: str, description: str = None, widget: QtWidgets.QWidget = None):
        card = CardView(self, title)
        self.ui.verticalLayout.addWidget(card, 0, QtCore.Qt.AlignTop)
        if widget is not None:
            card.setContentWidget(widget)
        if description is not None:
            card.setDescrreption(description)
        return card


class MainWindow(BaseWindow):

    def __init__(self, config: str = "config.yaml"):
        super().__init__()
        self.ui = window.Ui_MainWindow()
        self.ui.setupUi(self)
        self.home = HomeView(self)
        self.config = config

        with open(self.config, "r", encoding="utf-8") as f:
            self.cards = yaml.safe_load(f)

        def createCard(card):
            title = card["title"]
            desc = card["description"]
            text = card["title"]
            icon = FIF(card["icon"])
            enabled = card["enabled"]

            if enabled:                
                button = PrimaryPushButton(text, self, icon)
                button.clicked.connect(
                    lambda: self.applyCard(card)
                )
            else:
                button = PushButton(text, self, icon)
                button.clicked.connect(
                    lambda: InfoBar.warning(
                        title, "功能未实现",
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
                )
            self.home.addCard(title, desc, button)

        for card in self.cards:
            createCard(card)

        self.navModel = [
            ("Home", FIF.HOME, self.home),
            ("Settings", FIF.SETTING, QtWidgets.QLabel("Settings"))
        ]

        def createNavItems(text, icon, widget):
            self.ui.navigationInterface.addItem(
                text, icon, text, lambda: self.switchTo(widget))
            self.ui.stackedWidget.addWidget(widget)

        # 不要再for循环里使用lambda表达式
        # https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture
        # https://github.com/python/cpython/issues/57861
        for text, icon, widget in self.navModel:
            createNavItems(text, icon, widget)

        self.switchTo(self.home)

    def switchTo(self, widget):
        self.ui.stackedWidget.setCurrentWidget(widget)

    def applyCard(self, card):
        try:
            self.ecu = client.get_ecu()
            if "echo" in card["ecu"]:
                for key, value in card["ecu"]["echo"].items():
                    value = bytearray.fromhex(value.replace(" ", ""))
                    self.ecu.echo[key] = list(value)
            client.set_ecu(self.ecu)
            InfoBar.success(
                card['title'], card['description'],
                orient=QtCore.Qt.Vertical,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
        except Exception as e:
            InfoBar.error(
                "异常", str(e),
                position=InfoBarPosition.TOP,
                duration=4000,
                parent=self
            )


