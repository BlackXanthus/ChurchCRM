##
# This will create the contact window
##

from PyQt5.QtWidgets import (QPushButton, QTextEdit,QLineEdit,QDialog)
from PyQt5 import QtCore

from contactV1_ui import Ui_formContact

class ContactWindow(QDialog):

	_version="0.1 ALPHA"

	#PyQt5 Signals
	ContactAdd = QtCore.pyqtSignal(dict)

	def __init__(self, *args, **kwargs):
		super(ContactWindow,self).__init__(*args, **kwargs)

		self.ui = Ui_formContact()
		self.ui.setupUi(self)

		self.buttonAdd = self.ui.buttonSubmitAdd
		self.buttonAdd.clicked.connect(self.readContact)

	def readContact(self):
		tempContact=dict()
		tempContact["FirstName"]=self.ui.inputFirstName.text()
		tempContact["LastName"]=self.ui.inputLastName.text()
		tempContact["MiddleName"]=self.ui.inputMiddleName.text()
		tempContact["KnownAs"]=self.ui.inputKnownAs.text()
		tempContact["HouseNumber"]=self.ui.inputHouseNumber.text()
		tempContact["Street"]=self.ui.inputStreet.text()
		tempContact["Town"]=self.ui.inputTown.text()
		tempContact["PostalTown"]=self.ui.inputPostalTown.text()
		tempContact["PostCode"]=self.ui.inputPostCode.text()
		tempContact["Telephone"]=self.ui.inputTelephone.text()
		tempContact["Mobile"]=self.ui.inputMobile.text()
		tempContact["Email"]=self.ui.inputEmail.text()
		
		self.ContactAdd.emit(tempContact)
		self.hide()

