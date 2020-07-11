from string import punctuation
from collections import OrderedDict

# punctuations to be stripped off from the string
strip_punctuation = punctuation+" "

#  file from where data would be read
input_file = "DataFile.txt"
# file where data would be written 
output_file = "output.csv"

# data list to hold lines
data = []	

# FirstName,LastName,DOB,Address,City,State dictionary 
data_keys = OrderedDict({ 
	"firstname":None,
	"lastname":None,
	"dob":None,
	"address":None,
	"city":None,
	"state":None,
	"country":None,
	"notes":None,
	"place of birth":None,
})

# ------------------------------------------------------------------------------
# FUNCTIONS FOR VARIOUS OPEARTIONS

def join_multiline_data(data):
	"""
		input: 
			data: A list of strings
		operation:
			In the lsit of strings, if single line is spread across multiple indexes 
			but is surrounded by bracktets then, all that is joined to form a single string
			For eg:- 
				This list ["word1 word2","word3 (word4","word5","word6","word7)"] is converted to 
				["word1 word2","word3 (word4 word5 word6 word7)"]
		returns:
			Returns a list of all joined string which is spread across multiple lines
	"""
	#  output list 
	new_data = []
	
	# count variable to count the no. of opening and closing brackets
	count = 0

	# itegrate over the lsit of data 
	for row in range(len(data)):	

		# if count>0 means ... some bracket is open ... so data would be 
		# appended to the previous string only
		if(count>0):
			new_data[-1]+=" "+data[row].strip()
		# if count<=0 then no bracket is open 
		else:
			new_data.append(data[row].strip())
		

		# iterate over all characters 
		for char in range(len(data[row])):

			# check if there is any opening bracket and increase count
			if(data[row][char] in {"(","{","[","<"}):
				count+=1
			
			# check if there is any closing bracket and decrease count
			if(data[row][char] in {")","}","]",">"}):
				count-=1
	
	return new_data

def add_data(data_keys,key,value):
	"""
		input:
			data_keys: dictionary storing the data of a row
			key: key for which we want to add data
			value: value of the key which we want to add 
		operation:
			What this function does is to assign a value to a given key in the data_keys dictionary.
			Further, if the key does not exists, key is created first.
			And special operation is done for "unknown" key, all the unknown values are appended in this key, separated by "~"
		returns:
			Nothing
	"""

	# print(key,value)

	# check if key is not present in the dictionay, and create it if it dosen't exists
	if(key not in data_keys):
		data_keys[key] = None
	
	# if we are adding value for "unknown" key, then all the values are added separated by "~" 
	# else assigning the value to the key
	if(key=="unknown"):
		if(data_keys["unknown"]==None):
			data_keys["unknown"] = value
		else:
			data_keys["unknown"] += "~"+value
	else:
		data_keys[key] = value

def processData(data,data_keys):
	"""
		input: 
			data: A list of strings, which constitute data for a single row in the final table
			data_keys: Dictionary to store this data
		operation:
			First of all data spread across multiple lines is joined to bring them to single line.
			Then for all the lines, it is checked if any of the already present key is present in that data
			Else, some from some speacial sybols, it is checked if we can sepatrate it b/w key and value, and if possible, new keys are added  
			else, data is added under the "unknown" category
		returns:
			nothing is returned 
	"""

	# join data spread across multiple lines but surrounded by brackets 
	new_data = join_multiline_data(data)

	# iterate across all the rows 
	for row in new_data:
		
		# iterate across all the keys we have in data_keys 
		for key in data_keys:
			# ans check if any of the key from our dict is present in the row, if yes, then this would be added in the dictionary
			if(key.lower() in row.lower()):
				add_data(data_keys,
					key.lower().strip(strip_punctuation),
					row[row.lower().find(key.lower())+len(key.lower()):].strip(strip_punctuation))
				break

		# if no key from our dictionary, then key is searched by locating a delimiter if any present 
		else:
			# iterating through every character of the row and check if it is a delimiter and separate according to it
			for i in range(len(row)):
				if(row[i] in {"{","(","[","<","=",":","-"}):
					add_data(data_keys,row[:i].lower().strip(strip_punctuation),row[i+1:].strip(strip_punctuation))
					break
			# if no delimiter is found, it is added under UNKNOWN heading 
			else:
				add_data(data_keys,"unknown",row)
	
	#  if "firstname" and "lastname" are None and we got some other field which contains "name" in it
	if(data_keys["firstname"]==None or data_keys["lastname"]==None):
		for key in data_keys:
			# if "name" is found in the key
			if("name" in key.lower() and data_keys[key]!=None):
				# splitted into firstname and lastname
				name = data_keys[key].split()

				# this is done to handle the case when we would be having name longer than 2 words
				data_keys["firstname"], data_keys["lastname"] = " ".join(name[:1]), " ".join(name[1:]) 
				
				# further that key is deleted
				del data_keys[key] 
				break

	# if "date of birth" key is found, then it is deletd and its value is put to "dob" key
	if("date of birth" in data_keys and data_keys["date of birth"]!=None):
		data_keys["dob"] = data_keys["date of birth"]
		del data_keys["date of birth"] 

def write_data(l):
	"""
		input:
			l: list to write in the CSV output file
		operation:
			Writes a list, 
			by replacing the None with empty string
			and surrounding string with (""), so that elements can contain (,) inside it and it won't affect the CSV file 
		ouput:
			Nothing
	"""
	# iterate over the list
	for i in range(len(l)):
		# if none, replace it with ""
		if(l[i]==None):
			l[i] = ""
		# surrounding it with (""), so that (,) can be present in the text 
		else:
			l[i] = "\"" + l[i] + "\""
	
	#  appending the data to the file
	with open(output_file,"a") as f:
		f.write(",".join(l)+"\n")


def extract(data,data_keys,write=False):
	"""
		input:
			data: list conating all the lines of codes
			data_keys: a dictionary containing all the keys
			write: True/False, based on wheter the resultant dictinary with key value pairs has to be written in file or not 
		operation:
			processes the complete data and writes if requried
			furter, after completion of operation, it clears the list and the dictionary so that its ready to insert new values 
		returns:
			Nothing
	"""

	# processing of complete data 
	processData(data,data_keys)
	
	if(write==False):
		print(data_keys.keys())
	else:
		print(data_keys)
	
	# if write=True, we would be writing the data to the file
	if(write):
		l = list(data_keys.values())
		write_data(l)
	
	# once the complete data has been extracted, all the values of the dictionary are put to None
	for key in data_keys:
		data_keys[key]=None
	# once the complete data has been extracted, list is also cleared t be emplye
	data.clear()
	
# ------------------------------------------------------------------------------

"""
Here, I would be extracting data 2 times
Since the no. of fields are not constant
So, when we do the first time, we would be exploring the total number of fields which we have
and the second time we woudl do the same, we would be writing all the details in the file
"""

# opening the input file to read data
with open(input_file,"r") as f:	
	# iterating through the lines of files
	for row in f:
		# ignore lines starting with "--" or "==" or if the lines is blank
		if(row.strip().startswith("--") or row.strip().startswith("==") or len(row.strip())==0):
			continue

		# if a line starts with "~~" and all the lenght of data >0, 
		# then information would be extarcted from data
		if(row.strip().startswith("~~") and len(data)>0):
			# data would be extracted and in this case we won't be writing data to output file
			extract(data,data_keys,write=False)
		
		# if line is valid and has content, then it is added to data list
		data.append(row.strip(strip_punctuation))	
	
	# this is a way to hanlde the last line of data, since we won't be having "~~" at the end, 
	# so, when we reach the end, then last line of data would be extarted   
	if(len(data)>0):
		extract(data,data_keys,write=False)

print("------------------------------------------")
print("all keys have been extracted")
print(data_keys.keys())
print("------------------------------------------")

# writng all the fields which have been extracted above
with open(output_file,"w") as f:
	f.write(",".join(data_keys.keys())+"\n")

# opening the input file to read data
with open(input_file,"r") as f:
	# iterating through the lines of files
	for row in f:

		# ignore lines starting with "--" or "==" or if the lines is blank
		if(row.strip().startswith("--") or row.strip().startswith("==") or len(row.strip())==0):
			continue

		# if a line starts with "~~" and all the lenght of data >0, 
		# then information would be extarcted from data
		if(row.strip().startswith("~~") and len(data)>0):
			# data would be extracted and in this case we would be writing data to output file
			extract(data,data_keys,write=True)	
		
		# if line is valid and has content, then it is added to data list
		data.append(row.strip(strip_punctuation))
	
	# this is a way to hanlde the last line of data, since we won't be having "~~" at the end, 
	# so, when we reach the end, then last line of data would be extarted   
	extract(data,data_keys,write=True)
	