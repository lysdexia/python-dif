import os, sys, re, datetime, types
__author__ = "Doug Shawhan <lysdexia@gmail.com>"
__license__ = "GPL"
"""
Read and write "Navy DIF" documents as defined at
	http://en.wikipedia.org/wiki/Data_Interchange_Format

Vectors correspond to columns.
Tuples correspond to rows.

Attempts to use python-dateutil to parse dates.
"""

class Row(object):
	"""Dummy row object"""
	pass

class DIFReader(object):
	"""
	Populate self.sheet with a list of lists. Lists contain tuples 
	corresponding to column name.

	Tuple[0] is the column name, tuple[1] is the cell value.

	Invoking with first_row_keys=True will take the first .dif tuple as
	a list of column names.

	Passing a list of strings to row_keys will use row_keys values as
	column names.

	Accepts "dif_obj" as:
		a .dif-formatted string
		a path to a .dif file
		a file-like object
	"""
	vectors = False
	tuples = False
	row_keys = False
	first_row_keys = False
	sheet = []

	def __init__(self, dif_obj, first_row_keys=False, row_keys=False):
		"""
		Invoking with first_row_keys=True will take the first dif tuple as
		a list of column names.

		Passing a list of strings to row_keys will use row_keys values as
		column names.

		Invoking with only dif_obj will create a row_keys list with
		enumerated column names.
		["col0", "col1", "col2" ...]
		"""

		if first_row_keys:
			if not isinstance(first_row_keys, bool):
				raise ValueError("first_row_keys value '%s' not boolean"%frk)
			self.first_row_keys = first_row_keys

		if row_keys:
			if not isinstance(row_keys, list):
				raise ValueError("row_keys must be a list")
			# always use keys we pass, in case someone gets froggy
			self.first_row_keys = False

		# we want an iterable
		dif_obj = self.toIterable(dif_obj)

		# make sure we have a valid headerchunk
		self.headerChunk(dif_obj)

		if not self.row_keys:
			self.getRowKeys(dif_obj)

		while True:
			try:
				row = self.getRow(dif_obj)
				if row == False:
					break

				self.sheet.append(row)
			except StopIteration:
				break

	def getRowKeys(self, dif_obj):
		"""
		names of keys
		"""
		if not self.first_row_keys:
			self.row_keys = ["col%s"%i for i in range(self.vectors)]
			return

		self.row_keys = self.getRowList(dif_obj)

	def toIterable(self, dif_obj):
		"""
		return a generator for a string, filename or file-like object
		"""
		# are we being provided with a file-like object?
		if isinstance(dif_obj, file):
			#sys.exit("i'm a file")
			return self.stream(dif_obj)

		# must be a string, I'm thinking ...
		if any([isinstance(dif_obj, unicode), isinstance(dif_obj, str)]):
			if os.path.isfile(dif_obj):
				#sys.exit("i'm an object")
				f = open(dif_obj, "r")
				return self.stream(f)

		# well, this looks like a string.
		#sys.exit("i'm an string")
		return self.stream(dif_obj.strip().split("\n"))

	def stream(self, dif_obj):
		"""assure dif_obj is a generator"""
		for s in dif_obj:
			yield s.strip()

	def headerChunk(self, dif_obj):
		"""
		Extract comment (which is most likely the sheet name if this .dif
		was produced by a spreadsheet), vector and tuple counts.
		DATA portion is ignored per spec.
		Raise an error if any of the fields are missing or mal-formed.
		"""
		d = {}
		for i in range(4):
			key = dif_obj.next().strip()
			value = int(dif_obj.next().strip().split(",")[1])
			comment = dif_obj.next().strip()
			d[key] = {
					"value": value,
					"comment": comment
					}

		if not all([i in d for i in ["TABLE", "VECTORS", "TUPLES"]]):
			raise SyntaxError("malformed header chunk")

		self.comment = d["TABLE"]["comment"]
		self.vectors = d["VECTORS"]["value"]
		self.tuples = d["TUPLES"]["value"]

	def getRow(self, dif_obj):
		"""
		parse (self.vectors) columns from dif_obj
		return a list of tuples as row
		"""
		try:
			return [(k, v) for k, v in
					zip(self.row_keys, self.getRowList(dif_obj))]
		except TypeError:
			return False

	def getRowList(self, dif_obj):
		"""
		establish row directive type and value
		"""

	 	# check for directive and properly formatted tuple
		directive = int(dif_obj.next().strip().split(",")[0])
		if not directive == -1:
			raise ValueError("row does not have directive type")

		bot_eod = dif_obj.next().strip()

		# if we have no more data, bail
		if bot_eod == "EOD":
			return

		# whoops. invalid format
		if not bot_eod == "BOT":
			raise ValueError("Invalid keyword: '%s'"%bot_eod)

		# well, the headerish bit is okay
		return [self.cellValue(dif_obj.next(), dif_obj.next()) for i in range(self.vectors)]

	def cellValue(self, tv, cmt):
		"""
		Parse out value of the cell according to spec. Basically only
		handles strings, integers and tuples.
		"""

		typ, value = tv.strip().split(",")
		typ = int(typ)

		cmt = cmt.strip().strip('"').strip("'")

		# we're numericish
		if not typ:

			# are we valid?
			if cmt != "V":
				return cmt

			# are we boolean?
			if value == "TRUE":
				return True

			if value == "FALSE":
				return False

			# ignoring the chance of commas, since format should not use them
			if "." in value:
				return float(value)

			try:
				return int(value)
			except ValueError:
				return value

		return cmt

	def parseDates(self, date_columns):
		"""
		Parse date time values that are listed in date_columns list
		"""
		try:
			from dateutil import parser as dt_parser
			self.dt_parser = dt_parser
		except ImportError:
			raise Exception("dateutil not available.")
			return

		for row in self.sheet:

			# we are a list of tuples
			if isinstance(row, list):
				row = self.dateTimeValueTuple(row, date_columns)
				print row[4]

			# we are a list of dictionaries
			elif isinstance(row, dict):
				row = self.dateTimeValueDict(row, date_columns)

			# we are a list of class objects
			else:
				row = self.dateTimeValueClass(row, date_columns)

	def dateTimeValueClass(self, row, date_columns):
		"""
		Parse date time values from class values in date_columns
		"""
		for k in date_columns:
			setattr(row, k, self.dateTimeValue(getattr(row, k)))

		row.tuple = self.dateTimeValueTuple(row.tuple, date_columns)
		row.dict = self.dateTimeValueDict(row.dict, date_columns)
		row.list = self.dateTimeValueList(row.list, date_columns)

		return row

	def dateTimeValueList(self, row, date_columns):
		"""
		Parse date time values from list values which correspond
		to date_columns index
		"""
		positions = []
		for i in enumerate(self.row_keys):
			if i[1] in date_columns:
				positions.append(i[0])

		for p in positions:
			row[p] = self.dateTimeValue(row[p])

		return row

	def dateTimeValueDict(self, row, date_columns):
		"""
		Parse date time values from a dictionary row
		"""
		for k in date_columns:
			row[k] = self.dateTimeValue(row[k])
		return row

	def dateTimeValueTuple(self, row, date_columns):
		"""
		Parse date time values from a tuple row
		"""
		for col in row:
			if col[0] in date_columns:
				row[row.index(col)] = (col[0], self.dateTimeValue(col[1]))
		return row

	def dateTimeValue(self, v):
		"""
		try and get a proper datetime value from a string or float
		"""
		if isinstance(v, float): 
			try:
				return datetime.datetime.fromtimestamp(v).isoformat()
			except:
				return v
		try:
			return self.dt_parser.parse(v)
		except ValueError:
			return v
		except AttributeError:
			return v

class DIFDictReader(DIFReader):
	"""
	Populate self.sheet with a list of dictionaries.
	Keys are column names.
	Row order may be obtained from self.row_keys.
	"""

	def getRow(self, dif_obj):
		"""
		parse (self.vectors) columns from dif_obj
		return a dictionary as row
		"""
		try:
			return dict([(k, v) for k, v in
				zip(self.row_keys, self.getRowList(dif_obj))])

		except TypeError:
			return False

class DIFObjReader(DIFReader):
	"""
	Populate self.sheet with Row objects.
	Row objects contain:

		Row.tuple - a list of tuples in the same format as 
		DIFReader.sheet.

		Row.dict - a dictionary in the same format as
		DIFDictReader.sheet.

		Row.list - a list with values ordered by self.row_keys.

		Row.<attribute> where attribute name corresponds to values in
		self.row_keys.

	Tentatively a convenience ...
	"""

	def getRow(self, dif_obj):
		"""
		parse (self.vectors) columns from dif_obj
		for the lazy man ...

		returns an object with row as tuple, row as dict and each as value
		as an object value. 
		"""

		try:
			row = Row()
			row.tuple = [(k, v) for k, v in zip(self.row_keys, self.getRowList(dif_obj))]
			row.dict = dict(row.tuple)

			row.list = [i[1] for i in row.tuple]

			for k in row.dict:
				setattr(row, k, row.dict[k])

			return row

		except TypeError:
			return False


