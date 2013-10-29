#!/usr/bin/env python
import sys
sys.path.append("../")
import DataInterchangeFormat

if __name__ == "__main__":

	print("as a file path")
	dif = DataInterchangeFormat.DIFObjReader("./test.dif", first_row_keys=True)
	dif.parseDates(["dates"])
	for row in dif.sheet:
		for k in dif.row_keys:
			print k, row.dict[k], type(row.dict[k])
		
	print("as open file")
	with open("./test.dif", "r") as f:
		dif = DataInterchangeFormat.DIFObjReader(f, first_row_keys=True)
	dif.parseDates(["dates"])
	for row in dif.sheet:
		for k in dif.row_keys:
			print k, row.dict[k], type(row.dict[k])
	
	print("as string")
	with open("./test.dif", "r") as f:
		dif = DataInterchangeFormat.DIFObjReader(f.read(), first_row_keys=True)
	dif.parseDates(["dates"])
	for row in dif.sheet:
		for k in dif.row_keys:
			print k, row.dict[k], type(row.dict[k])
