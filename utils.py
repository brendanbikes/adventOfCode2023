def read_input(file: str):
	with open(file, 'r') as f:
		data = f.readlines()

	return [x.strip() for x in data]