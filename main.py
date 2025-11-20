import PySide6
from PySide6.QtWidgets import (QApplication,
                               QLabel,          # ラベルを使うのに必要
                               QWidget)
import os
import sys
# PySide6のアプリ本体（ユーザがコーディングしていく部分）
class MainWindow(QWidget):
    def __init__(self, parent=None):
        # 親クラスの初期化
        super().__init__(parent)
        
        # ウィンドウタイトル
        self.setWindowTitle("PySide6で作ったアプリです。")
        
        # ラベルを表示するメソッド
        self.SetLabel()
        
    # ラベルは別のメソッドに分けました
    def SetLabel(self):
        # ラベルを使うことを宣言（引数のselfはウィンドウのことで、ウィンドウにラベルが表示されます）
        label = QLabel(self)
        
        # ラベルに文字を指定
        label.setText("こんにちは。ラベルです。")


if __name__ == "__main__":
    # 環境変数にPySide6を登録
    dirname = os.path.dirname(PySide6.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    
    app = QApplication(sys.argv)    # PySide6の実行
    window = MainWindow()           # ユーザがコーディングしたクラス
    window.show()                   # PySide6のウィンドウを表示
    sys.exit(app.exec())            # PySide6の終了