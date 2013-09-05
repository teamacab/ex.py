class Queue:
	
	def __self__(self):
		self.QUEUE=[];
	
	def add(self, message):
		self.QUEUE.append(message)
	
	def next(self):
		self.QUEUE.pop(0)