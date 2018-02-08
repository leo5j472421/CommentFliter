def binarySearch(alist, item):
	first = 0
	last = len(alist) - 1
	found = -1

	while first <= last and found == -1:
		midpoint = (first + last) // 2
		if alist[midpoint] == item:
			found = midpoint
		else:
			if item < alist[midpoint]:
				last = midpoint - 1
			else:
				first = midpoint + 1

	return found