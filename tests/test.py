#!/usr/bin/env python
import sys
sys.path.append("../")
import DataInterchangeFormat

if __name__ == "__main__":

	"""
	with open("./test.dif", "r") as f:
		#dif = DIFReader(f, first_row_keys=True)
		#dif = DIFDictReader(f, first_row_keys=True)
		dif = DIFObjReader(f, first_row_keys=True)
	dif.parseDates(["dates"])
	print dif.sheet
	#print dif.sheet[0].list
	#print dif.sheet[0].dict["dates"]
	#print dif.sheet[0].tuple
	#print dif.sheet[0].dates

	dif = DIFReader("./test.dif", first_row_keys=True)
	print dif.sheet

	with open("./test.dif", "r") as f:
		dif = DIFDictReader(f.read(), first_row_keys=True)
	print dif.sheet
	"""

	with open("./test.dif", "r") as f:
		dif = DataInterchangeFormat.DIFObjReader(f.read(), first_row_keys=True)
	dif.parseDates(["dates"])
	for row in dif.sheet:
		for k in dif.row_keys:
			print k, row.dict[k], type(row.dict[k])
		
	#help(DIFReader)
