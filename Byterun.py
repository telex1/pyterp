# Byterun is a python bytecode interpreter!


class VirtualMachineError(Exception):
	pass


# virtual machine stores the call stack, exception state, and return values 
# while they are being passed between frames, the argument is a compiled code object
class VirtualMachine(object):

	def __init__(self):
		self.frames = []		# call stack of frames
		self.frame = None		# current frame
		self.return_value = None
		self.last_exception = None

	def run_code(self, code, global_names=None, local_names=None):
		
		frame = self.make_frame(code, global_names=global_names,
					      local_names=local_names)
		
		self.run_frame(frame)


class Frame(object):
	
	def __init__(self, code_obj, global_names, local_names, prev_frame):
		self.code_obj = code_obj
		self.global_names = global_names
		self.local_names = local_names
		self.prev_frame = prev_frame
		self.stack = []

		if prev_frame:
			self.buitin_names = prev_frame.builtin_names
		else:
			self.builtin_names = local_names['__builtins__']
			if hasattr(self.builtin_names, '__dict__'):
				self.builtin_names = self.builtin_names.__dict__

		self.last_instruct = 0
		self.block_stack = []
	
