#!/usr/bin/env python
import sys
sys.path.append("../")
import DataInterchangeFormat

if __name__ == "__main__":

	print("as a file path")
	dif = DataInterchangeFormat.DIFReader("./test.dif", first_row_keys=True)
	dif.parseDates(["dates"])
	for row in dif.sheet:
		for col in row:
			for k in dif.row_keys:
				if col[0] == k:
					print k, col[1], type(col[1])
		
	print("as open file")
	with open("./test.dif", "r") as f:
		dif = DataInterchangeFormat.DIFReader(f, first_row_keys=True)
	dif.parseDates(["dates"])
	for row in dif.sheet:
		for col in row:
			for k in dif.row_keys:
				if col[0] == k:
					print k, col[1], type(col[1])

	print("as string")
	with open("./test.dif", "r") as f:
		dif = DataInterchangeFormat.DIFReader(f.read(), first_row_keys=True)
	dif.parseDates(["dates"])
	for row in dif.sheet:
		for col in row:
			for k in dif.row_keys:
				if col[0] == k:
					print k, col[1], type(col[1])
