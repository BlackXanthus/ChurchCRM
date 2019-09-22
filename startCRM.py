#!/usr/bin/env python

import pickle
import random
import copy

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from PyQt5.QtCore import QFile, QIODevice, Qt, QTextStream
from PyQt5.QtWidgets import (QDialog, QFileDialog, QGridLayout, QHBoxLayout,
		QLabel, QLineEdit, QMessageBox, QPushButton, QTextEdit, QVBoxLayout,
		QWidget,QMainWindow)

from SortedDict import SortedDict
from FindDialog import FindDialog
from TableModel import TableModel
from ContactWindow import ContactWindow


#UI Imports
from crmV1_ui import Ui_MainWindow
from contactV1_ui import Ui_formContact

class MainWindow(QMainWindow):

	_version="0.1 ALPHA"

	UpdateContacts = QtCore.pyqtSignal(str)


	def __init__(self,parent=None):
	
		self.contacts = SortedDict()

		QWidget.__init__(self,parent)

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.initUI()
		
		self.setWindowTitle("Xen CRM "+self._version)

		self.UpdateContacts.connect(self.updateContactsTable)

		self.tableModel = TableModel(self.contacts)
		self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.ui.tableView.setModel(self.tableModel)

	def temploadFromFile(self):
		fileName, _ = QFileDialog.getOpenFileName(self, "Open Address Book",
				'', "Address Book (*.abk);;All Files (*)")

		if not fileName:
			return

		try:
			in_file = open(str(fileName), 'rb')
		except IOError:
			QMessageBox.information(self, "Unable to open file",
					"There was an error opening \"%s\"" % fileName)
			return

		self.contacts = pickle.load(in_file)
		in_file.close()

		if len(self.contacts) == 0:
			QMessageBox.information(self, "No contacts in file",
					"The file you are attempting to open contains no "
					"contacts.")
		#else:
		#	for name, address in self.contacts:
		#		print("Name:"+name+" Address"+address)
		   #	 self.nameLine.setText(name)
		   #	 self.addressText.setText(address)

		self.tableModel = TableModel(self.contacts)
		self.ui.tableView.setModel(self.tableModel)


		#self.updateInterface(self.NavigationMode)

	def addContact(self):

		self.contactUi = ContactWindow()
		self.contactUi.ContactAdd.connect(self.storeContact)
		self.contactUi.show()


	def updateContactsTable(self):
		self.tableModel = TableModel(self.contacts)
		self.ui.tableView.setModel(self.tableModel)


	def initUI(self):

   #Connecting Buttons to new UI
   #	 self.loadButton = QPushButton("&Load...")
		self.loadButton = self.ui.buttonLoad
		self.loadButton.setToolTip("Load contacts from a file")

		self.addButton = self.ui.buttonAdd
		self.addButton.setToolTip("Add New Contact")
 
		self.saveButton = self.ui.buttonSave
		self.saveButton.setToolTip("Save contacts to a file")

		self.deleteButton = self.ui.buttonRemove
		self.deleteButton.setToolTip("Delete Contact")

		self.undoButton = self.ui.buttonUndo
		self.undoButton.setToolTip("Undo Contact Removal")
		self.undoButton.setEnabled(False)
		
   #Adding Connections	  
		self.loadButton.clicked.connect(self.temploadFromFile)
		self.addButton.clicked.connect(self.addContact)
		self.saveButton.clicked.connect(self.saveToFile)
		self.deleteButton.clicked.connect(self.removeContact)
		self.undoButton.clicked.connect(self.undoContactRemoval)

		self.ui.tableView.doubleClicked.connect(self.editContact)

	def storeContact(self,myContact):
		#this needs a primary key. Probably should be random
		#Perhaps a record of this needs to be kept somewhere?
		number=random.randint(0,234234222342339983422)	

		if "Key" in myContact:
				self.contacts[myContact["Key"]]=myContact
		else:	
			print("No Key Found, moving to add")
			theList=list(iter(self.Contacts.keys()))	
			#If the count is creater than 1, then there's trouble!
			while (theList.count(number) > 0):
				number=random.randint(0,234234298923423)
			myContact["Key"]=str(number)
			self.contacts[myContact["Key"]]=myContact

		self.UpdateContacts.emit("ContactStored")


	def undoContactRemoval(self):
		tempContacts = copy.deepcopy(self.contacts)
		self.contacts = copy.deepcopy(self.undoContacts)
		self.undoContacts = copy.deepcopy(tempContacts)
		self.UpdateContacts.emit("ContactRemoved")

	def editContact(self, MyIndex):
	
		print("Row Selected "+str(MyIndex.row()))
		myContact = self.tableModel.getItemAtIndex(MyIndex.row())
		print("Contact Known As:"+myContact["KnownAs"])

		self.contactUi = ContactWindow()
		self.contactUi.ContactAdd.connect(self.storeContact)

		#Fill out the data

		self.contactUi.setData(myContact)

		self.contactUi.show()

	def removeContact(self):

		indexes = self.ui.tableView.selectionModel().selectedRows()
		for index in sorted(indexes):
			print('Row %d is selected' % index.row())
			item =self.tableModel.getItemAtIndex(index.row())
			print("Name For Removal:" + item["FirstName"])
			
			self.undoContacts = copy.deepcopy(self.contacts)
			del self.contacts[item["Key"]]
			self.undoButton.setEnabled(True)
			self.UpdateContacts.emit("ContactRemoved")

	def saveToFile(self):
		fileName, _ = QFileDialog.getSaveFileName(self, "Save Address Book",
				'', "Address Book (*.abk);;All Files (*)")

		if not fileName:
			return

		try:
			out_file = open(str(fileName), 'wb')
		except IOError:
			QMessageBox.information(self, "Unable to open file",
					"There was an error opening \"%s\"" % fileName)
			return

		pickle.dump(self.contacts, out_file)
		out_file.close()


class AddressBook(QWidget):
	NavigationMode, AddingMode, EditingMode = range(3)

	def __init__(self, parent=None):
		super(AddressBook, self).__init__(parent)

		self.contacts = SortedDict()
		self.oldName = ''
		self.oldAddress = ''
		self.currentMode = self.NavigationMode

		nameLabel = QLabel("Name:")
		self.nameLine = QLineEdit()
		self.nameLine.setReadOnly(True)

		addressLabel = QLabel("Address:")
		self.addressText = QTextEdit()
		self.addressText.setReadOnly(True)

		self.addButton = QPushButton("&Add")
		self.addButton.show()
		self.editButton = QPushButton("&Edit")
		self.editButton.setEnabled(False)
		self.removeButton = QPushButton("&Remove")
		self.removeButton.setEnabled(False)
		self.findButton = QPushButton("&Find")
		self.findButton.setEnabled(False)
		self.submitButton = QPushButton("&Submit")
		self.submitButton.hide()
		self.cancelButton = QPushButton("&Cancel")
		self.cancelButton.hide()

		self.nextButton = QPushButton("&Next")
		self.nextButton.setEnabled(False)
		self.previousButton = QPushButton("&Previous")
		self.previousButton.setEnabled(False)

		self.loadButton = QPushButton("&Load...")
		self.loadButton.setToolTip("Load contacts from a file")
		self.saveButton = QPushButton("Sa&ve...")
		self.saveButton.setToolTip("Save contacts to a file")
		self.saveButton.setEnabled(False)

		self.exportButton = QPushButton("Ex&port")
		self.exportButton.setToolTip("Export as vCard")
		self.exportButton.setEnabled(False)

		self.dialog = FindDialog()

		self.addButton.clicked.connect(self.addContact)
		self.submitButton.clicked.connect(self.submitContact)
		self.editButton.clicked.connect(self.editContact)
		self.removeButton.clicked.connect(self.removeContact)
		self.findButton.clicked.connect(self.findContact)
		self.cancelButton.clicked.connect(self.cancel)
		self.nextButton.clicked.connect(self.next)
		self.previousButton.clicked.connect(self.previous)
		self.loadButton.clicked.connect(self.loadFromFile)
		self.saveButton.clicked.connect(self.saveToFile)
		self.exportButton.clicked.connect(self.exportAsVCard)

		buttonLayout1 = QVBoxLayout()
		buttonLayout1.addWidget(self.addButton)
		buttonLayout1.addWidget(self.editButton)
		buttonLayout1.addWidget(self.removeButton)
		buttonLayout1.addWidget(self.findButton)
		buttonLayout1.addWidget(self.submitButton)
		buttonLayout1.addWidget(self.cancelButton)
		buttonLayout1.addWidget(self.loadButton)
		buttonLayout1.addWidget(self.saveButton)
		buttonLayout1.addWidget(self.exportButton)
		buttonLayout1.addStretch()

		buttonLayout2 = QHBoxLayout()
		buttonLayout2.addWidget(self.previousButton)
		buttonLayout2.addWidget(self.nextButton)

		mainLayout = QGridLayout()
		mainLayout.addWidget(nameLabel, 0, 0)
		mainLayout.addWidget(self.nameLine, 0, 1)
		mainLayout.addWidget(addressLabel, 1, 0, Qt.AlignTop)
		mainLayout.addWidget(self.addressText, 1, 1)
		mainLayout.addLayout(buttonLayout1, 1, 2)
		mainLayout.addLayout(buttonLayout2, 2, 1)

		self.setLayout(mainLayout)
		self.setWindowTitle("Simple Address Book")

	def addContact(self):
		self.oldName = self.nameLine.text()
		self.oldAddress = self.addressText.toPlainText()

		self.nameLine.clear()
		self.addressText.clear()

		self.updateInterface(self.AddingMode)

	def editContact(self):
		self.oldName = self.nameLine.text()
		self.oldAddress = self.addressText.toPlainText()

		self.updateInterface(self.EditingMode)

	def submitContact(self):
		name = self.nameLine.text()
		address = self.addressText.toPlainText()

		if name == "" or address == "":
			QMessageBox.information(self, "Empty Field",
					"Please enter a name and address.")
			return

		if self.currentMode == self.AddingMode:
			if name not in self.contacts:
				self.contacts[name] = address
				QMessageBox.information(self, "Add Successful",
						"\"%s\" has been added to your address book." % name)
			else:
				QMessageBox.information(self, "Add Unsuccessful",
						"Sorry, \"%s\" is already in your address book." % name)
				return

		elif self.currentMode == self.EditingMode:
			if self.oldName != name:
				if name not in self.contacts:
					QMessageBox.information(self, "Edit Successful",
							"\"%s\" has been edited in your address book." % self.oldName)
					del self.contacts[self.oldName]
					self.contacts[name] = address
				else:
					QMessageBox.information(self, "Edit Unsuccessful",
							"Sorry, \"%s\" is already in your address book." % name)
					return
			elif self.oldAddress != address:
				QMessageBox.information(self, "Edit Successful",
						"\"%s\" has been edited in your address book." % name)
				self.contacts[name] = address

		self.updateInterface(self.NavigationMode)

	def cancel(self):
		self.nameLine.setText(self.oldName)
		self.addressText.setText(self.oldAddress)
		self.updateInterface(self.NavigationMode)

	def removeContact(self):
		name = self.nameLine.text()
		address = self.addressText.toPlainText()

		if name in self.contacts:
			button = QMessageBox.question(self, "Confirm Remove",
					"Are you sure you want to remove \"%s\"?" % name,
					QMessageBox.Yes | QMessageBox.No)

			if button == QMessageBox.Yes:
				self.previous()
				del self.contacts[name]

				QMessageBox.information(self, "Remove Successful",
						"\"%s\" has been removed from your address book." % name)

		self.updateInterface(self.NavigationMode)

	def next(self):
		name = self.nameLine.text()
		it = iter(self.contacts)

		try:
			while True:
				this_name, _ = it.next()

				if this_name == name:
					next_name, next_address = it.next()
					break
		except StopIteration:
			next_name, next_address = iter(self.contacts).next()

		self.nameLine.setText(next_name)
		self.addressText.setText(next_address)

	def previous(self):
		name = self.nameLine.text()

		prev_name = prev_address = None
		for this_name, this_address in self.contacts:
			if this_name == name:
				break

			prev_name = this_name
			prev_address = this_address
		else:
			self.nameLine.clear()
			self.addressText.clear()
			return

		if prev_name is None:
			for prev_name, prev_address in self.contacts:
				pass

		self.nameLine.setText(prev_name)
		self.addressText.setText(prev_address)

	def findContact(self):
		self.dialog.show()

		if self.dialog.exec_() == QDialog.Accepted:
			contactName = self.dialog.getFindText()

			if contactName in self.contacts:
				self.nameLine.setText(contactName)
				self.addressText.setText(self.contacts[contactName])
			else:
				QMessageBox.information(self, "Contact Not Found",
						"Sorry, \"%s\" is not in your address book." % contactName)
				return

		self.updateInterface(self.NavigationMode)

	def updateInterface(self, mode):
		self.currentMode = mode

		if self.currentMode in (self.AddingMode, self.EditingMode):
			self.nameLine.setReadOnly(False)
			self.nameLine.setFocus(Qt.OtherFocusReason)
			self.addressText.setReadOnly(False)

			self.addButton.setEnabled(False)
			self.editButton.setEnabled(False)
			self.removeButton.setEnabled(False)

			self.nextButton.setEnabled(False)
			self.previousButton.setEnabled(False)

			self.submitButton.show()
			self.cancelButton.show()

			self.loadButton.setEnabled(False)
			self.saveButton.setEnabled(False)
			self.exportButton.setEnabled(False)

		elif self.currentMode == self.NavigationMode:
			if not self.contacts:
				self.nameLine.clear()
				self.addressText.clear()

			self.nameLine.setReadOnly(True)
			self.addressText.setReadOnly(True)
			self.addButton.setEnabled(True)

			number = len(self.contacts)
			self.editButton.setEnabled(number >= 1)
			self.removeButton.setEnabled(number >= 1)
			self.findButton.setEnabled(number > 2)
			self.nextButton.setEnabled(number > 1)
			self.previousButton.setEnabled(number >1 )

			self.submitButton.hide()
			self.cancelButton.hide()

			self.exportButton.setEnabled(number >= 1)

			self.loadButton.setEnabled(True)
			self.saveButton.setEnabled(number >= 1)

	def saveToFile(self):
		fileName, _ = QFileDialog.getSaveFileName(self, "Save Address Book",
				'', "Address Book (*.abk);;All Files (*)")

		if not fileName:
			return

		try:
			out_file = open(str(fileName), 'wb')
		except IOError:
			QMessageBox.information(self, "Unable to open file",
					"There was an error opening \"%s\"" % fileName)
			return

		pickle.dump(self.contacts, out_file)
		out_file.close()

	def loadFromFile(self):
		fileName, _ = QFileDialog.getOpenFileName(self, "Open Address Book",
				'', "Address Book (*.abk);;All Files (*)")

		if not fileName:
			return

		try:
			in_file = open(str(fileName), 'rb')
		except IOError:
			QMessageBox.information(self, "Unable to open file",
					"There was an error opening \"%s\"" % fileName)
			return

		self.contacts = pickle.load(in_file)
		in_file.close()

		if len(self.contacts) == 0:
			QMessageBox.information(self, "No contacts in file",
					"The file you are attempting to open contains no "
					"contacts.")
		else:
			for name, address in self.contacts:
				self.nameLine.setText(name)
				self.addressText.setText(address)

		self.updateInterface(self.NavigationMode)

	def exportAsVCard(self):
		name = str(self.nameLine.text())
		address = self.addressText.toPlainText()

		nameList = name.split()

		if len(nameList) > 1:
			firstName = nameList[0]
			lastName = nameList[-1]
		else:
			firstName = name
			lastName = ''

		fileName, _ = QFileDialog.getSaveFileName(self, "Export Contact", '',
				"vCard Files (*.vcf);;All Files (*)")

		if not fileName:
			return

		out_file = QFile(fileName)

		if not out_file.open(QIODevice.WriteOnly):
			QMessageBox.information(self, "Unable to open file",
					out_file.errorString())
			return

		out_s = QTextStream(out_file)

		out_s << 'BEGIN:VCARD' << '\n'
		out_s << 'VERSION:2.1' << '\n'
		out_s << 'N:' << lastName << ';' << firstName << '\n'
		out_s << 'FN:' << ' '.join(nameList) << '\n'

		address.replace(';', '\\;')
		address.replace('\n', ';')
		address.replace(',', ' ')

		out_s << 'ADR;HOME:;' << address << '\n'
		out_s << 'END:VCARD' << '\n'

		QMessageBox.information(self, "Export Successful",
				"\"%s\" has been exported as a vCard." % name)


if __name__ == '__main__':
	import sys

	from PyQt5.QtWidgets import QApplication

	app = QApplication(sys.argv)

#	 addressBook = AddressBook()
#	 addressBook.show()
	mainWindow = MainWindow()
	mainWindow.show()

	sys.exit(app.exec_())
