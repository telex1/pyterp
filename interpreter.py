

# small change
# the interpreter object uses a stack to keep track of the program
class Interpreter:
	
	# this empty list, created when the interpreter object is created will be used
	# as the stack
	def __init__(self):
		self.stack = []
		self.envrionment = {}
	
	def STORE_NAME(self, name):
		val = self.stack.pop()
		self.envrionment[name] = val
	
	def LOAD_NAME(self, name):
		val = self.environment[name]
		self.stack.append(val)
	
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
	
	def parse_argument(self, instruction, argument, what_to_exec):
		""" Understand what the argument to each instruction is """

		numbers = ["LOAD_VALUE"]
		names = ["LOAD_NAME", "STORE_NAME"]

		if instruction in numbers:
			argument = what_to_exec["numbers"][argument]
		elif instruction in names:
			argument = what_to_exec["names"][argument]

		return argument
	
	# takes a dictionary (exec_code) which contains instructions and values for running the program and
	# loops and processes them
	def execute(self, exec_code):

		# unpack exec_code
		instructions = exec_code["instructions"] 
		
		for step in instructions:
			
			# unpack each instruction
			instruction, argument = step

			# is the argument in "numbers" or "names" of the program
			argument = self.parse_argument(instruction, argument, exec_code)

			# look up method to execute. instruction "LOAD_VALUE" corresponds to LOAD_VALUE method
			bytecode_method = getattr(self, instruction)

			if argument is None:
				bytecode_method()

			else: 
				bytecode_method(argument)


# main

# program to execute
what_to_execute = {
        "instructions": [("LOAD_VALUE", 0),
                         ("STORE_NAME", 0),
                         ("LOAD_VALUE", 1),
                         ("STORE_NAME", 1),
                         ("LOAD_NAME", 0),
                         ("LOAD_NAME", 1),
                         ("ADD_TWO_VALUES", None),
                         ("PRINT_ANSWER", None)],
        "numbers": [1, 2],
        "names":   ["a", "b"] 

# driver code
interpreter = Interpreter()
interpreter.execute(what_to_execute)
