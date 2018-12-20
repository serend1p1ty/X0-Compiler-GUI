from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QRect
import Interpret as Ipt

class StackDisplayer(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.parent = parent

    def paintEvent(self, QPaintEvent):
        opt = QStyleOption()
        opt.initFrom(self)
        # painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, QPainter(self), self)

        if self.parent.isDebug == 0:
            return

        colorTable = [0xFF0000, 0xFF7F00, 0xFFFF00, 0x0000FF,
                      0x8B00FF, 0x00FF00, 0x00FFFF]

        rec = self.contentsRect()
        height = rec.height() * 5 / 16
        width = rec.width() / 25
        topx = 0
        topy = rec.height() * 11 / 32
        painter = QPainter(self)

        font = QFont()
        font.setFamily("consolas")
        painter.setFont(font)
        painter.setPen(QColor(163, 163, 163))

        # Draw instruction text
        fctCodeString = ["lit", "opr", "lod", "sto", "cal", "ini", "jmp", "jpc", "add", "sub", "tad"]
        inst = Ipt.code[Ipt.p]
        if inst.fct == Ipt.FctCode.lit and inst.opr2 != 0:
            painter.drawText(QRect(0, 20, 300, 25), Qt.AlignVCenter,
                          "Next instruction:%s %s %s" % (fctCodeString[inst.fct],
                                                         inst.opr1, round(inst.opr2, 2)))
        else:
            painter.drawText(QRect(0, 20, 300, 25), Qt.AlignVCenter,
                          "Next instruction:%s %s %s" % (fctCodeString[inst.fct],
                                                         inst.opr1, int(inst.opr2)))


        typeString = ["", "int", "dbl", "chr", "bol"]
        for i in range(1, Ipt.t + 1):
            # Draw name and type
            painter.drawText(QRect(topx, topy + height, width, 25),
                             Qt.AlignHCenter | Qt.AlignVCenter, "%s" % typeString[Ipt.s[i].dataType])
            painter.drawText(QRect(topx, topy - 25, width, 25), Qt.AlignHCenter | Qt.AlignVCenter, Ipt.stype[i])


            # Draw rectangle
            if Ipt.stype[i] == "null":
                color =QColor(colorTable[0])
            elif Ipt.stype[i] == "DL":
                color =QColor(colorTable[1])
            elif Ipt.stype[i] == "RA":
                color =QColor(colorTable[2])
            else:
                color = QColor(colorTable[Ipt.s[i].dataType + 2])
            painter.fillRect(topx, topy, width, height, color)
            painter.setPen(color.darker())
            painter.drawLine(topx, topy, topx, topy + height)
            painter.setPen(QColor(163, 163, 163))
            painter.drawLine(topx, topy, topx + width, topy)
            painter.drawLine(topx + width, topy, topx + width, topy + height)
            painter.drawLine(topx, topy + height, topx + width, topy + height)


            # Draw specific data
            if Ipt.s[i].dataType == Ipt.DataType.Double:
                painter.drawText(QRect(topx, topy + height / 2 - 12.5, width, 25), Qt.AlignHCenter | Qt.AlignVCenter,
                              "%s" % round(Ipt.s[i].dblData, 2))
            else:
                painter.drawText(QRect(topx, topy + height / 2 - 12.5, width, 25), Qt.AlignHCenter | Qt.AlignVCenter,
                                  "%s" % Ipt.s[i].intData)
            topx = topx + width


