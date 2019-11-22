# Input: n segments of slope 1, -1, 0 each (x1, y1, x2, y2)
# Output: upper envelope

import queue
import matplotlib.pyplot as plt


def x_to_y(_l, _x):
	_x1, _y1, _x2, _y2 = _l
	return (_x - _x1) / (_x2 - _x1) * (_y2 - _y1) + _y1


def larger(i1, i2, x):
	return x_to_y(i1, x) > x_to_y(i2, x)


class BST:
	def __init__(self, line_list):
		self.lines = line_list
		self.tree = []

	def insert(self, idx, x):
		i = 0
		while i < len(self.tree) and larger(self.lines[idx], self.lines[i], x):
			i += 1
		self.tree.insert(i, idx)

	def remove(self, idx):
		self.tree.remove(idx)

	def prev(self, idx):
		i = self.tree.index(idx)
		return i-1 if i > 0 else None

	def next(self, idx):
		i = self.tree.index(idx)
		return i+1 if i+1 < len(self.tree) else None

	def swap(self, i1, i2, x):
		j1, j2 = self.tree.index(i1), self.tree.index(i2)
		self.tree[j1], self.tree[j2] = self.tree[j2], self.tree[j1]

	def top(self):
		if len(self.tree) == 0:
			return None
		else:
			return self.tree[-1]


def check_intersect(l1, l2):
	# https://stackoverflow.com/questions/20677795/

	def det(a, b):
		return a[0] * b[1] - a[1] * b[0]

	x1, y1, x2, y2 = l1
	a1, b1, a2, b2 = l2
	xdiff = (x1 - x2, a1 - a2)
	ydiff = (y1 - y2, b1 - b2)
	div = det(xdiff, ydiff)
	if div == 0:
		return False, None
	else:
		d = (x1 * y2 - x2 * y1, a1 * b2 - a2 * b1)
		x = det(d, xdiff) / div
		# y = det(d, ydiff) / div
		return True, x


def upper_envelope(lines):
	event_queue = queue.PriorityQueue()
	lines = [[float(i) for i in j] for j in lines]
	print(lines)
	tree = BST(lines)
	top_list = []

	for i, (x1, y1, x2, y2) in enumerate(lines):
		event_queue.put((x1, 0, i))
		event_queue.put((x2, 2, i))

	last_x = -100

	while event_queue.qsize() > 0:
		x, event, val = event_queue.get()
		print('Event: {} {} {}'.format(x, event, val))

		if event == 0:  # Begin
			line = lines[val]
			tree.insert(val, x)
			prv, nxt = tree.prev(val), tree.next(val)

			if prv is not None:
				is_intersect, x_intersect = check_intersect(line, lines[prv])
				if is_intersect and x_intersect > x:
					event_queue.put((x_intersect, 1, (prv, val)))
			if nxt is not None:
				is_intersect, x_intersect = check_intersect(line, lines[nxt])
				if is_intersect and x_intersect > x:
					event_queue.put((x_intersect, 1, (val, nxt)))

		elif event == 2:  # End
			prv, nxt = tree.prev(val), tree.next(val)
			tree.remove(val)

			if prv is not None and nxt is not None:
				is_intersect, x_intersect = check_intersect(lines[prv], lines[nxt])
				if is_intersect and x_intersect > x:
					event_queue.put((x_intersect, 1, (prv, nxt)))

		else:  # Intersect
			prv, nxt = val
			print(prv, nxt, x)
			tree.swap(prv, nxt, x)

			prv2, nxt2 = tree.prev(nxt), tree.next(prv)
			if prv2 is not None:
				is_intersect, x_intersect = check_intersect(lines[prv2], lines[nxt])
				if is_intersect and x_intersect > x:
					event_queue.put((x_intersect, 1, (prv2, nxt)))
			if nxt2 is not None:
				is_intersect, x_intersect = check_intersect(lines[prv], lines[nxt2])
				if is_intersect and x_intersect > x:
					event_queue.put((x_intersect, 1, (prv, nxt2)))

		if last_x < x:
			top_list.append((x, tree.top()))
			last_x = x
		else:
			top_list[-1] = (x, tree.top())

	return top_list


if __name__ == '__main__':
	lines = [(0, 0, 3, 3), (2, 3, 5, 0), (1, 2, 4, 2), (3, 2, 4.5, 2)]
	top_hull = upper_envelope(lines)
	print(top_hull)
	for i in range(len(top_hull) - 1):
		x1, l1 = top_hull[i]
		x2, l2 = top_hull[i+1]
		line = lines[l1]
		plt.plot([x1, x2], [x_to_y(line, x1), x_to_y(line, x2)])
	plt.show()
