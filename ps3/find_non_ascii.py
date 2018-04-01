import codecs

FILENAME = 'ps3.py' # replace with your filename, for ex. 'ps1.py'


def check_if_ascii(s):
	try:
		s.encode('ascii')
		return True
	except Exception as e:
		return False


with codecs.open(FILENAME, 'r', encoding='utf-8') as f:
    
    lines = f.readlines()
    count = 0
	
    for i, line in enumerate(lines):
        	if not check_if_ascii(line):
        		for j, char in enumerate(line):
        			if not check_if_ascii(char):
        				print("non-ASCII character in line %s at position %s." % (i+1, j+1))
        				count += 1
        				break
    
    if count == 0:
        	print("All good!")
    else:
        print("Try deleting the problematic lines and manually re-typing them.")
