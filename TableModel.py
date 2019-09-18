from PyQt5.QtCore import QAbstractTableModel, QVariant
from PyQt5 import QtCore

from SortedDict import SortedDict

class TableModel(QAbstractTableModel):

	header_labels = ["Known As", "First Name", "Last Name", "Middle Names", "House Number", "Street","Town","Postal Town","Post Code","Telephone","Mobile","E-Mail"]



	def __init__(self,MyDict,parent=None):
		QtCore.QAbstractTableModel.__init__(self,parent)
		self.data = MyDict


	#Ensures the list is conistently sorted
	def getSortedListKeys(self, listType=None):

		if(listType==None):
			theList=list(sorted(iter(self.data.keys())))
		return theList


	def headerData(self,section,orientation,role=QtCore.Qt.DisplayRole):
		if role == QtCore.Qt.DisplayRole and orientation ==QtCore.Qt.Horizontal:
			return self.header_labels[section]
		return QAbstractTableModel.headerData(self,section,orientation,role)

	def rowCount(self,parent=None):
		return len(self.data)

	def columnCount(self,parent=None):
		return len(self.header_labels) 

	def data(self,index,role=QtCore.Qt.DisplayRole):

		if role == QtCore.Qt.DisplayRole:
			try:
				theData=""

				itemList = self.getSortedListKeys()

				myContactNumber = itemList[index.row()]
				#quick and dirty list printing
				if(index.column()==0):
					theData=self.data[myContactNumber]["KnownAs"]
				if(index.column()==1):
					theData=self.data[myContactNumber]["FirstName"]
				if(index.column()==2):
					theData=self.data[myContactNumber]["LastName"]
				if(index.column()==3):
					theData=self.data[myContactNumber]["MiddleName"]
				if(index.column()==4):
					theData=self.data[myContactNumber]["HouseNumber"]
				if(index.column()==5):
					theData=self.data[myContactNumber]["Street"]
				if(index.column()==6):
					theData=self.data[myContactNumber]["Town"]
				if(index.column()==7):
					theData=self.data[myContactNumber]["PostalTown"]
				if(index.column()==8):
					theData=self.data[myContactNumber]["PostCode"]
				if(index.column()==9):
					theData=self.data[myContactNumber]["Telephone"]
				if(index.column()==10):
					theData=self.data[myContactNumber]["Mobile"]
				if(index.column()==11):
					theData=self.data[myContactNumber]["Email"]

				return theData

			except IndexError:
				return "Empty"

		if role == QtCore.Qt.EditRole:
			try:
				itemList = list(sorted(iter(self.data.keys())))

				row = index.row()
				item=self.data[itemList[row]]	
				if(index.column()==0):
					theData=itemList[index.row()]
				if(index.column()==1):
					theData=self.data[itemList[index.row()]]	

				return theData

			except IndexError:
				return "Empty"

	#Get an Item at a specific index in the sorted list
	def getItemAtIndex(self, index):

		itemList = self.getSortedListKeys()
		return self.data[itemList[index]]

