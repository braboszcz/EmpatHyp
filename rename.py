import os

for filename in os.listdir('Test'):
	if filename.startswith('c'):
		os.rename(filename, 'R_' + filename)




