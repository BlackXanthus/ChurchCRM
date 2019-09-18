from PyQt5.QtCore import QAbstractTableModel, QVariant
from PyQt5 import QtCore

from SortedDict import SortedDict

class TableModel(QAbstractTableModel):

	header_labels = ["Known As", "First Name", "Last Name", "Middle Name", "Middle Names", "House Number", "Street","Town","Postal Town","Post Code","Telephone","Mobile","E-Mail"]



	def __init__(self,MyDict,parent=None):
		QtCore.QAbstractTableModel.__init__(self,parent)
		self.data = MyDict

	def headerData(self,section,orientation,role=QtCore.Qt.DisplayRole):
		if role == QtCore.Qt.DisplayRole and orientation ==QtCore.Qt.Horizontal:
			return self.header_labels[section]
		return QAbstractTableModel.headerData(self,section,orientation,role)

	def rowCount(self,parent=None):
		return len(self.data)

	def columnCount(self,parent=None):
		return 11

	def data(self,index,role=QtCore.Qt.DisplayRole):

		if role == QtCore.Qt.DisplayRole:
			try:
				theData=""

				print(str(index.column()) +" " + str(index.row()))
				itemList = list(sorted(iter(self.data.keys())))

				print(itemList[index.row()])

				myContactNumber = itemList[index.row()]
				#quick and dirty list printing
				if(index.column()==0):
					theData=self.data[myContactNumber]["KnownAs"]
					print("Column0:"+theData)
				if(index.column()==1):
					theData=self.data[myContactNumber]["FirstName"]
					print("Column1:"+theData)
				if(index.column()==2):
					theData=self.data[myContactNumber]["LastName"]
					print("Column3:"+theData)
				if(index.column()==3):
					theData=self.data[myContactNumber]["MiddleName"]
					print("Column0:"+theData)
				if(index.column()==4):
					theData=self.data[myContactNumber]["HouseNumber"]
					print("Column1:"+theData)
				if(index.column()==5):
					theData=self.data[myContactNumber]["Street"]
					print("Column3:"+theData)
				if(index.column()==6):
					theData=self.data[myContactNumber]["Town"]
					print("Column0:"+theData)
				if(index.column()==7):
					theData=self.data[myContactNumber]["PostalTown"]
					print("Column1:"+theData)
				if(index.column()==8):
					theData=self.data[myContactNumber]["PostCode"]
					print("Column3:"+theData)
				if(index.column()==9):
					theData=self.data[myContactNumber]["Telephone"]
					print("Column0:"+theData)
				if(index.column()==10):
					theData=self.data[myContactNumber]["Mobile"]
					print("Column1:"+theData)
				if(index.column()==11):
					theData=self.data[myContactNumber]["Email"]
					print("Column3:"+theData)


				print("Item-Display:"+theData)
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
					print(theData)
				if(index.column()==1):
					theData=self.data[itemList[index.row()]]	
					print(theData)

				print("Item-Display:"+theData)
				return theData

			except IndexError:
				return "Empty"

