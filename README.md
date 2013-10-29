python-dif
==========

Navy Data Interchange Format module. 

http://en.wikipedia.org/wiki/Data_Interchange_Format

Reader classes work fine. Writer classes not written yet.

Usage
-----

Depending on reader class DataInterchangeFormat can represent data in several different ways:

### as a list of tuples
	>>> import DataInterchangeFormat
	>>> dif = DataInterchangeFormat.DIFReader("./tests/test.dif", first_row_keys=True)
	>>> dif.sheet
	[
		[
			('boolean', True),
			('text', 'psychic'),
			('numeric', 1),
			('errors', 'ERROR'),
			('dates', '10/25/2013 19:21:51')
		],
		[
			('boolean', False),
			('text', 'powerless'),
			('numeric', 0.1),
			('errors', 'ERROR'),
			('dates', 'Fri Oct 25 15:31:08 2013')],
		[
			('boolean', ''),
			('text', 'another'),
			('numeric', 1000),
			('errors', ''),
			('dates', 1382729606.27435)
		] ...

	]
### as a list of dictionaries
	>>> dif = DataInterchangeFormat.DIFDictReader("./tests/test.dif", first_row_keys=True)
	>>> dif.sheet
	[
		{
			'text': 'psychic',
			'dates': '10/25/2013 19:21:51',
			'boolean': True,
			'errors': 'ERROR',
			'numeric': 1
		},
		{
			'text': 'powerless',
			'dates': 'Fri Oct 25 15:31:08 2013',
			'boolean': False,
			'errors': 'ERROR',
			'numeric': 0.1
		},
		{
			'text': 'another',
			'dates': 1382729606.27435,
			'boolean': '',
			'errors': '',
			'numeric': 1000
		} ...
	]

### as a list of objects
Each row object contains row data in tuple, dict and list formats.
List format has no header information and is accessed via index like tuples.

	>>> dif = DataInterchangeFormat.DIFObjReader("./tests/test.dif", first_row_keys=True)
	>>> dif.sheet
	[
		<DataInterchangeFormat.Row object at 0x1c7aa50>,
		<DataInterchangeFormat.Row object at 0x1c7a9d0>,
		<DataInterchangeFormat.Row object at 0x1c7a890> ...
	]

	>>> dif.sheet[0].list
	[True, 'psychic', 1, 'ERROR', '10/25/2013 19:21:51']

	>>> dif.sheet[0].dict
	{'text': 'psychic', 'dates': '10/25/2013 19:21:51', 'boolean': True, 'errors': 'ERROR', 'numeric': 1}

	>>> dif.sheet[0].tuple
	[('boolean', True), ('text', 'psychic'), ('numeric', 1), ('errors', 'ERROR'), ('dates', '10/25/2013 19:21:51')]

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
To use your first row as keys, invoke with first_row_keys=True.
Invoking without first_row_keys will result in keys being named for the column index.

DateTime Columns
----------------
If you have python-dateutils installed (http://labix.org/python-dateutil), supply a list of columns that have date/time values to self.parseDates.

	>>> import DataInterchangeFormat
	>>> dif = DataInterchangeFormat.DIFObjReader("./tests/test.dif", first_row_keys=True)
	>>> dif.sheet[0].dict
	{'text': 'psychic', 'dates': '10/25/2013 19:21:51', 'boolean': True, 'errors': 'ERROR', 'numeric': 1}
	>>> dif.parseDates(["dates"])
	>>> dif.sheet[0].dict
	{'text': 'psychic', 'dates': datetime.datetime(2013, 10, 25, 19, 21, 51), 'boolean': True, 'errors': 'ERROR', 'numeric': 1}
