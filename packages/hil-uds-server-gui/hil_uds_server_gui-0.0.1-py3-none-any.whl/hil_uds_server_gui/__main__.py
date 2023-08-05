import os
import sys
import argparse

from .main import MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

def get_default_config():
    # 当前文件所在路径
    current_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_path, "config.yaml")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default=get_default_config(),
                        help="Path to config file")
    parser.add_argument("-f", "--factor", default="1.5", help="Scale factor")
    args = parser.parse_args()
    # QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(
    #     QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    # QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = args.factor
    # QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(args.config)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()