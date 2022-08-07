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

	# frame methods
	def make_frame(self, code, callargs={}, global_names=None, local_names=None):
		if global_names is not None and local_names is not None:
			local_names = global_names
		elif self.frames:
			global_names = self.frame.global_names
			local_names = {}
		else:
			global_names = local_names = {
				'__builtins__': __builtins__,
				'__name__': '__main__',
				'__doc__': None,
				'__package__': None,
			}
		local_names.update(callargs)
		frame = Frame(code, global_names, local_names, self.frame)
		return frame
	
	def push_frame(self, frame):
		self.frames.append(frame)
		self.frame = frame
	
	def pop_frame(self):
		self.frames.pop()
		if self.frames:
			self.frame = self.frames[-1]
		else:
			self.frame = None
	
	def run_frame(self, frame):
		
		self.push_frame(frame)
		while True:
			byte_name, arguments = self.parse_byte_and_args()

			why = self.dispatch(byte_name, arguments)

			while why and frame.block_stack:
				why = self.manage_block_stack(why)

			if why:
				break

		self.pop_frame()

		if why == 'exception':
			exc, val, tb = self.last_exception
			e = exc(val)
			e.__traceback__ = tb
			raise e
		
		return self.return_value


# each frame instance is associated with one code object and manages
# the global and local namespaces, it also keeps a reference to the calling frame and the last bytecode instruction executed 
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

		self.last_instruction = 0
		self.block_stack = []

	

class Function(object):
	"""
	create a function object
	"""
	__slots__ = [
        	'func_code', 'func_name', 'func_defaults', 'func_globals',
        	'func_locals', 'func_dict', 'func_closure',
        	'__name__', '__dict__', '__doc__',
        	'_vm', '_func',
    	]
	
