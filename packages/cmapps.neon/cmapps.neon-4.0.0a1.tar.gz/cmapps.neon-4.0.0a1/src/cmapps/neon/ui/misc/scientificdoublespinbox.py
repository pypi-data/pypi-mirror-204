"""
Slightly modified code from:

    https://gist.githubusercontent.com/jdreaver/0be2e44981159d0854f5/raw/3170b5e6be28aa179c321b16650086f096ba06b9/scientificspin.py
"""
# Regular expression to find floats. Match groups are the whole string, the
# whole coefficient, the decimal part of the coefficient, and the exponent
# part.
import re

from PySide6 import QtGui, QtWidgets


_float_re = re.compile(r'(([+-]?\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)')


def valid_float_string(string):
    match = _float_re.search(string)
    return match.groups()[0] == string if match else False


class FloatValidator(QtGui.QValidator):

    def validate(self, string, position):
        if valid_float_string(string):
            return self.State.Acceptable
        if string == "" or string[position - 1] in 'e.-+':
            return self.State.Intermediate
        return self.State.Invalid

    def fixup(self, text):
        match = _float_re.search(text)
        return match.groups()[0] if match else ""


class ScientificDoubleSpinBox(QtWidgets.QDoubleSpinBox):

    def __init__(self, *args, **kwargs):
        super(ScientificDoubleSpinBox, self).__init__(*args, **kwargs)
        self.setMinimum(float('-inf'))
        self.setMaximum(float('inf'))
        self.validator = FloatValidator()
        self.setDecimals(1000)
        self.editingFinished.connect(self.adjustSize)
#         self.setSizePolicy()

    def validate(self, text, position):
        return self.validator.validate(text, position)

    def fixup(self, text):
        return self.validator.fixup(text)

    def valueFromText(self, text):
        return float(text)

    def textFromValue(self, value):
        return format_float(value)

    def stepBy(self, steps):
        text = self.cleanText()
        groups = _float_re.search(text).groups()
        decimal = float(groups[1])
        decimal += steps
        new_string = "{:g}".format(decimal) + (groups[3] if groups[3] else "")
        self.lineEdit().setText(new_string)

    def sizeHint(self):
        sh = super(ScientificDoubleSpinBox, self).sizeHint()
        fm = QtGui.QFontMetrics(QtGui.QFont())
        text_width = fm.width(self.text()) + 30  # Hard size for double spin box controls
        sh.setWidth(text_width)
        return sh

    def minimumSizeHint(self):
        sh = super(ScientificDoubleSpinBox, self).minimumSizeHint()
        fm = QtGui.QFontMetrics(QtGui.QFont())
        text_width = fm.width(self.text()) + 30  # Hard size for double spin box controls
        sh.setWidth(text_width)
        return sh


def format_float(value):
    """Modified form of the 'g' format specifier."""
    string = "{:g}".format(value).replace("e+", "e")
    string = re.sub("e(-?)0*(\d+)", r"e\1\2", string)
    return string
