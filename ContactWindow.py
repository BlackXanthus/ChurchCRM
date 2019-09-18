##
# This will create the contact window
##

from PyQt5.QtWidgets import (QPushButton, QTextEdit,QLineEdit,QDialog)
from PyQt5 import QtCore

from SortedDict import SortedDict
from contactV1_ui import Ui_formContact

class ContactWindow(QDialog):

	_version="0.1 ALPHA"

	#PyQt5 Signals
	ContactAdd = QtCore.pyqtSignal(SortedDict)

	def __init__(self, *args, **kwargs):
		super(ContactWindow,self).__init__(*args, **kwargs)

		self.ui = Ui_formContact()
		self.ui.setupUi(self)

		self.buttonAdd = self.ui.buttonSubmitAdd
		self.buttonAdd.clicked.connect(self.readContact)
		self.currentKey=""

	def setData(self, tempContact):
		self.currentKey = tempContact["Key"]
		self.ui.inputFirstName.setText(tempContact["FirstName"]) 		
		self.ui.inputLastName.setText(tempContact["LastName"])
		self.ui.inputMiddleName.setText(tempContact["MiddleName"])
		self.ui.inputKnownAs.setText(tempContact["KnownAs"])
		self.ui.inputHouseNumber.setText(tempContact["HouseNumber"])
		self.ui.inputStreet.setText(tempContact["Street"])
		self.ui.inputTown.setText(tempContact["Town"])
		self.ui.inputPostalTown.setText(tempContact["PostalTown"])
		self.ui.inputPostCode.setText(tempContact["PostCode"])
		self.ui.inputTelephone.setText(tempContact["Telephone"])
		self.ui.inputMobile.setText(tempContact["Mobile"])
		self.ui.inputEmail.setText(tempContact["Email"])
		
	def readContact(self):
		tempContact=SortedDict()
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

		if(self.currentKey != ""):
			tempContact["Key"]=self.currentKey
		
		self.ContactAdd.emit(tempContact)
		self.currentKey=""
		self.hide()

