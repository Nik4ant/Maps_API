# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(622, 528)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.vlayout_main = QtWidgets.QVBoxLayout()
        self.vlayout_main.setObjectName("vlayout_main")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_cordinates_2 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_cordinates_2.setFont(font)
        self.label_cordinates_2.setObjectName("label_cordinates_2")
        self.horizontalLayout_3.addWidget(self.label_cordinates_2)
        self.lineEdit_cordinates = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_cordinates.setFont(font)
        self.lineEdit_cordinates.setObjectName("lineEdit_cordinates")
        self.horizontalLayout_3.addWidget(self.lineEdit_cordinates)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_scale = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_scale.setFont(font)
        self.label_scale.setObjectName("label_scale")
        self.horizontalLayout_4.addWidget(self.label_scale)
        self.lineEdit_scale = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_scale.setFont(font)
        self.lineEdit_scale.setObjectName("lineEdit_scale")
        self.horizontalLayout_4.addWidget(self.lineEdit_scale)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.button_show = QtWidgets.QPushButton(Form)
        self.button_show.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(9)
        self.button_show.setFont(font)
        self.button_show.setObjectName("button_show")
        self.horizontalLayout.addWidget(self.button_show)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.vlayout_main.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pixmap_map = QtWidgets.QLabel(Form)
        self.pixmap_map.setText("")
        self.pixmap_map.setObjectName("pixmap_map")
        self.horizontalLayout_2.addWidget(self.pixmap_map)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.vlayout_main.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.vlayout_main)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Карты"))
        self.label_cordinates_2.setText(_translate("Form", "Координаты: "))
        self.label_scale.setText(_translate("Form", "Масштаб: "))
        self.button_show.setText(_translate("Form", "Показать"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
