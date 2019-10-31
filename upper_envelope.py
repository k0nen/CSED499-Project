# Input: n segments of slope 1, -1, 0 each
# Output: upper envelope


class BST:
	def __init__(self):
		self.values = []

	def insert(self, value, x_val=None):
		pass

	def delete(self, value):
		pass

	def pop(self):
		self.delete(self.values[0])

	def find_neighbors(self, value):
		return []

	def position(self, value):
		pass

	def empty(self):
		return len(self.values) == 0


def check_intersect(a, b):
	return False, None


def upper_envelope(line_segments):
	# List of (x_coord, code, index) in ascending x order
	event_queue = BST()
	for i, ((x1, _), (x2, _)) in enumerate(line_segments):
		event_queue.insert((x1, 1 if x1 <= x2 else 0, i))
		event_queue.insert((x2, 1 if x1 <= x2 else 0, i))

	# Maintain a search tree for sweep line
	table = BST()

	while not event_queue.empty():
		x_coord, code, data = event_queue.values[0]
		event_queue.pop()

		# Endpoints
		if code < 2:
			segment = line_segments[data]

			# Left endpoint
			if code == 1:
				table.insert(data)
				for n in table.find_neighbors(data):
					intersect, intersect_x = check_intersect(segment, line_segments[n])
					if n is not None and intersect:
						# segment and line_segments[n] intersect
						event_queue.insert((intersect_x, 2, ()))

			# Right endpoint
			else:
				t, b = table.find_neighbors(data)
				if t is not None and b is not None:
					top, bottom = line_segments[t], line_segments[b]
					intersect, intersect_x = check_intersect(top, bottom)
					if intersect:
						# top and bottom intersect
						pass

		# Intersection
		else:
			a, b = data

