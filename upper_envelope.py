import heapq
import matplotlib.pyplot as plt


def x_to_y(_l, _x):
	_x1, _y1, _x2, _y2 = _l
	return (_x - _x1) / (_x2 - _x1) * (_y2 - _y1) + _y1


def larger(i1, i2, x):
	y1 = x_to_y(i1, x)
	y2 = x_to_y(i2, x)
	if y1 != y2:
		return y1 > y2
	else:
		a1, b1, a2, b2 = i1
		a3, b3, a4, b4 = i2
		return (b2 - b1) / (a2 - a1) > (b4 - b3) / (a4 - a3)


def check_intersect(l1, l2):
	# https://stackoverflow.com/questions/20677795/

	def det(a, b):
		return a[0] * b[1] - a[1] * b[0]

	x1, y1, x2, y2 = l1
	a1, b1, a2, b2 = l2
	x_diff = (x1 - x2, a1 - a2)
	y_diff = (y1 - y2, b1 - b2)
	div = det(x_diff, y_diff)
	if div == 0:
		return None
	else:
		d = (x1 * y2 - x2 * y1, a1 * b2 - a2 * b1)
		x = det(d, x_diff) / div
		y = det(d, y_diff) / div
		return x, y


class BST:
	def __init__(self):
		self.tree = []

	def insert(self, l, x):
		i = 0
		while i < len(self.tree) and larger(l, self.tree[i], x):
			i += 1
		self.tree.insert(i, l)

	def remove(self, l):
		self.tree.remove(l)

	def prev(self, l):
		i = self.tree.index(l)
		return self.tree[i-1] if i > 0 else None

	def next(self, l):
		i = self.tree.index(l)
		return self.tree[i+1] if i + 1 < len(self.tree) else None

	def swap(self, l1, l2):
		i1, i2 = self.tree.index(l1), self.tree.index(l2)
		self.tree[i1], self.tree[i2] = self.tree[i2], self.tree[i1]

	def top(self):
		return None if len(self.tree) == 0 else self.tree[-1]


# Input: n segments of slope 1, -1, 0 each (x1, y1, x2, y2)
# Output: Upper envelope
def upper_envelope(lines):
	event_queue = []
	lines = [[float(i) for i in j] for j in lines]
	tree = BST()
	top_list = []

	# Create begin/end events
	for x1, y1, x2, y2 in lines:
		heapq.heappush(event_queue, (x1, y1, 0, (x1, y1, x2, y2)))
		heapq.heappush(event_queue, (x2, y2, 2, (x1, y1, x2, y2)))

	last_x = -100

	while len(event_queue) > 0:
		x, y, event, val = heapq.heappop(event_queue)
		print(f'Event: ({x}, {y}), type {event}, {val} {tree.tree}')

		if event == 0:  # Begin
			line = val
			tree.insert(line, x)
			p, n = tree.prev(line), tree.prev(line)

			if p is not None:
				point = check_intersect(line, p)
				if point is not None and point[0] > x:
					heapq.heappush(event_queue, (point[0], point[1], 1, (p, line)))
			if n is not None:
				point = check_intersect(line, n)
				if point is not None and point[0] > x:
					heapq.heappush(event_queue, (point[0], point[1], 1, (line, n)))

		elif event == 2:  # End
			line = val
			p, n = tree.prev(line), tree.next(line)
			tree.remove(line)

			if p is not None and n is not None:
				point = check_intersect(p, n)
				if point is not None and point[0] > x:
					heapq.heappush(event_queue, (point[0], point[1], 1, (p, n)))

		else:  # Intersect
			p, n = val
			tree.swap(p, n)
			p2, n2 = tree.prev(p), tree.next(n)

			if p2 is not None:
				point = check_intersect(p2, n)
				if point is not None and point[0] > x:
					heapq.heappush(event_queue, (point[0], point[1], 1, (p2, n)))
			if n2 is not None:
				point = check_intersect(p, n2)
				if point is not None and point[0] > x:
					heapq.heappush(event_queue, (point[0], point[1], 1, (p, n2)))

		if last_x < x:
			top_list.append((x, tree.top()))
			last_x = x
		else:
			top_list[-1] = (x, tree.top())

	return top_list


if __name__ == '__main__':
	lines = [(0, 0, 3, 3), (0, 0, 6, 0), (0, 0, 10, -10)]
	top_hull = upper_envelope(lines)
	print(top_hull)
	for i in range(len(top_hull) - 1):
		x1, l1 = top_hull[i]
		x2, l2 = top_hull[i+1]
		plt.plot([x1, x2], [x_to_y(l1, x1), x_to_y(l1, x2)])
	plt.show()
