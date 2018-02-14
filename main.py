import sys

def main():
	dbNames = []

	try:
		sqlInput = input()
		while sqlInput.lower() != ".exit":
			parse_line(sqlInput.split(";")[0])
			sqlInput = input()
	except EOFError:
		pass # exit
	print("Exiting")

def parse_line(line):
	words = line.split(" ")

	if line[:2] == "--" or len(line) == 0:
		pass #ignore
	else:
		try:
			if words[0].lower() == "create":
				if words[1].lower() == "table":
					print("create_table(" + words[2] + ")")

					print(" -- If create_table returns true:")
					currentWord = 3
					wordCount = len(words)
					nextWord = words[currentWord]

					while currentWord < wordCount:
						if words[currentWord + 1][:3] == "int":
							print(" add_column(" + words[2] + ", int" + ", " + words[currentWord].strip("()") + ")")
						elif words[currentWord + 1][:5] == "float":
							print(" add_column(" + words[2] + ", float" + ", " + words[currentWord].strip("()") + ")")
						elif words[currentWord + 1][:4] == "char":
							print(" add_column(" + words[2] + ", char" + ", " + words[currentWord + 1][4:].strip("()") + ", " + words[currentWord].strip("()") + ")")
						elif words[currentWord + 1][:7] == "varchar":
							print(" add_column(" + words[2] + ", varchar" + ", " + words[currentWord + 1][7:].strip("()") + ", " + words[currentWord].strip("()") + ")")
						currentWord += 2

					print(" --")
				elif words[1].lower() == "database":
					print("create_database("  + words[2] + ")")

			elif words[0].lower() == "drop":
				if words[1].lower() == "table":
					print("drop_table(" + words[2] + ")")
				elif words[1].lower() == "database":
					print("drop_database(" + words[2] + ")")

			elif words[0].lower() == "select":
				print("select(" + words[3] + ", " + words[1] + ")")

			elif words[0].lower() == "use":
				print("use_database(" + words[1] + ")")

			elif words[0].lower() == "alter":
				if words[1].lower() == "table":
					if words[3].lower() == "add":
						if words[5] == "int":
							print("add_column(" + words[2] + ", int" + ", " + words[4] + ")")
						elif words[5]== "float":
							print("add_column(" + words[2] + ", float" + ", " + words[4] + ")")
						elif words[5][:4] == "char":
							print("add_column(" + words[2] + ", char" + ", " + words[5][4:].strip("()") + ", " + words[4] + ")")
						elif words[5][:7] == "varchar":
							print("add_column(" + words[2] + ", varchar" + ", " + words[5][7:].strip("()") + ", " + words[4] + ")")
			else:
				print("Invalid keyword: " + words[0])
		except IndexError:
			print("Invalid line: " + line)

if __name__ == "__main__":
	main()

