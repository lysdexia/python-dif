python-dif
==========

Navy Data Interchange Format module. 

http://en.wikipedia.org/wiki/Data_Interchange_Format

Reader classes work fine. Writer classes not written yet.

Usage
-----

Depending on reader class DataInterchangeFormat can represent data in several different ways:

### as a list of tuples
	dif = DataInterchangeFormat.DIFReader("./test.dif", first_row_keys=True)

### as a list of dictionaries
	dif = DataInterchangeFormat.DIFDictReader("./test.dif", first_row_keys=True)

### as a list of objects
	dif = DataInterchangeFormat.DIFObjReader("./test.dif", first_row_keys=True)

Input
-----
Reader classes can accept a string, a file path or a file-like object as input.
### as a file path
	dif = DataInterchangeFormat.DIFReader("./test.dif", first_row_keys=True)

### as an open file
	with open("./test.dif", "r") as f:
		dif = DataInterchangeFormat.DIFReader(f, first_row_keys=True)

### as a string
	with open("./test.dif", "r") as f:
		dif = DataInterchangeFormat.DIFReader(f.read(), first_row_keys=True)

"Header" Row
------------
To use your first row as keys, invoke with first_row_keys=True

DateTime Columns
----------------
If you have python-dateutils installed (http://labix.org/python-dateutil), supply a list of columns that have date/time values to self.parseDates.

	dif.parseDates(["dates"])

Play with the tests to see how it works.
