import sys
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt5.QtWidgets import QApplication, QTextEdit, QMainWindow

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlight_rules = []

        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("blue"))
        keywords = ["def", "class", "return", "if", "else", "import", "from", "for", "while"]
        self.highlight_rules += [(QRegExp(r"\b" + kw + r"\b"), keyword_format) for kw in keywords]

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(Qt.darkGreen)
        self.highlight_rules.append((QRegExp(r"#.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlight_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)

class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setFontFamily("Courier")
        self.setFontPointSize(11)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            self.insertPlainText(" " * 4)  # Insert 4 spaces for indentation
        else:
            super().keyPressEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.editor = CodeEditor()
        self.highlighter = PythonHighlighter(self.editor.document())
        self.setCentralWidget(self.editor)
        self.setWindowTitle("Python Code Editor")
        self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
