#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class X0Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlightingRules = []

        # the first kind of keyword
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(0x00C5CD))
        keywordFormat.setFontWeight(QFont.Bold)
        keywords = ["bool", "char", "double", "int", "const", "void"]
        keywordPatterns = [("\\b" + keyword + "\\b") for keyword in keywords]
        self.highlightingRules += [(QRegExp(pattern), keywordFormat)
                                   for pattern in keywordPatterns]

        # the second kind of keyword
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(0x8968CD))
        keywordFormat.setFontWeight(QFont.Bold)
        keywords = ["break", "case", "continue", "default", "do", "else",
                    "exit", "for", "if", "repeat", "return", "switch",
                    "until", "while"]
        keywordPatterns = [("\\b" + keyword + "\\b") for keyword in keywords]
        self.highlightingRules += [(QRegExp(pattern), keywordFormat)
                                   for pattern in keywordPatterns]

        # the third kind of keyword
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(0x8B7355))
        keywordFormat.setFontWeight(QFont.Bold)
        keywords = ["write", "read"]
        keywordPatterns = [("\\b" + keyword + "\\b") for keyword in keywords]
        self.highlightingRules += [(QRegExp(pattern), keywordFormat)
                                   for pattern in keywordPatterns]

        # the fourth kind of keyword
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(0xCD4F39))
        keywordFormat.setFontWeight(QFont.Bold)
        keywords = ["true", "false"]
        keywordPatterns = [("\\b" + keyword + "\\b") for keyword in keywords]
        self.highlightingRules += [(QRegExp(pattern), keywordFormat)
                                   for pattern in keywordPatterns]



    def highlightBlock(self, text):
        for pattern, Format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, Format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)


class QLineNumberArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.codeEditor = parent

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class QCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth()
        self.highlight = X0Highlighter(self.document())

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(50, 50, 50).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(50, 50, 50))
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(block_number + 1)

                # Let line number for the selected line to be highlight
                if block_number == self.textCursor().blockNumber():
                    painter.setPen(QColor(163, 163, 163))
                else:
                    painter.setPen(QColor(100, 100, 100))

                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    editor = QCodeEditor()
    editor.show()
    sys.exit(app.exec_())