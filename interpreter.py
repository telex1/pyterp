


# the interpreter object uses a stack to keep track of the program
class Interpreter:
	
	# this empty list created when the interpreter object is created will be used
	# as the stack
	def __init__(self):
		self.stack = []
	
	def LOAD_VALUE(self, number):
		self.stack.append(number)
	
	def PRINT_ANSWER(self):
		answer = self.stack.pop()
		print(answer)
	
	def ADD_TWO_VALUES(self):
		first_num = self.stack.pop()
		second_num = self.stack.pop()
		total = first_num + second_num
		self.stack.append(total)
	
	# takes a dictionary (exec_code) which contains instructions and values for running the program and
	# loops and processes them
	def run_code(self, exec_code):
		instructions = exec_code["instructions"] 
		numbers = exec_code["numbers"]
		
		for step in instructions:
			instruction, argument = step
			if instruction == "LOAD_VALUE":
				number = numbers[argument]
				self.LOAD_VALUE(number)
			elif instruction == "ADD_TWO_VALUES":
				self.ADD_TWO_VALUES()
			elif instruction == "PRINT_ANSWER":
				self.PRINT_ANSWER()


# main

# examle instructions that adds two numbers
sample_instructions = {
	"instructions": [("LOAD_VALUE", 0), # frist number
			 ("LOAD_VALUE", 1), # second number
			 ("ADD_TWO_VALUES", None),
			 ("PRINT_ANSWER", None)],
	"numbers": [7, 8] }

# driver code
interpreter = Interpreter()
interpreter.run_code(sample_instructions)
