# Cluster algorithems

from math import sqrt
from PIL import Image, ImageDraw
import random

def readfile(filename):

	# Read lines from data fila
	lines = [line for line in file(filename)]

	# The first line is the words
	colnames = lines[0].strip().split('\t')[1:]

	rownames = []
	data= []

	for line in lines[1:]:
		p = line.strip().split('\t')

		# The first colum is the blog names
		rownames.append(p[0])
		data.append( [float(x) for x in p[1:]] )

	return rownames, colnames, data


def pearson(v1, v2):

	sum1 = sum(v1)
	sum2 = sum(v2)

	sum1sq = sum( [pow(v,2) for v in v1] )
	sum2sq = sum( [pow(v,2) for v in v2] )

	psum = sum( [v1[i]*v2[i] for i in range(len(v1))] )

	num = psum - ( sum1 * sum2 / len(v1))
	den = sqrt( (sum1sq-pow(sum1,2)/len(v1)) * (sum2sq-pow(sum2,2)/len(v2)) )

	if den == 0:
		return 0

	return 1.0-num/den


class bicluster:
	def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
		self.left = left
		self.right = right
		self.vec = vec
		self.id = id
		self.distance = distance


def hcluster(rows, distance=pearson):
	distances = {}
	currentclustid = -1

	# Initialize the clust with rows in data
	clust = [ bicluster(rows[i], id = i) for i in range(len(rows)) ]

	# Loop on every pair to find the minimum distance, and merge them into one class. Stop when there is only one class
	while ( len(clust) > 1 ):
		lowestpair = (0, 1)
		closest = distance( clust[0].vec, clust[1].vec)

		for i in range(len(clust)):
			for j in range(i+1, len(clust)):

				# If the distance of this pair is not stored, calculate the distance and store it
				if ( clust[i].id, clust[j].id ) not in distances:
					distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)

				# Get the distance of this pair from stored distances

				d = distances[(clust[i].id, clust[j].id)]

				if d < closest:
					closest = d
					lowestpair = (i, j)

		# Merge the closest pair
		mergevec = [ (clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0 for i in range(len(clust[0].vec)) ]

		newcluster = bicluster( mergevec, left = clust[lowestpair[0]], right = clust[lowestpair[1]], distance = closest, id = currentclustid)

		currentclustid -= 1
		del clust[lowestpair[1]]
		del clust[lowestpair[0]]
		clust.append(newcluster)

	return clust[0]


# Print the clust in tree style
def printclust(clust, labels = None, n = 0):

	for i in range(n): print ' ',

	if clust.id < 0:
		print '-'
	else:
		if labels == None:
			print clust.id
		else:
			print labels[clust.id]

	if clust.left != None:
		printclust(clust.left, labels = labels, n = n+1)

	if clust.right != None:
		printclust(clust.right, labels = labels, n = n+1)

	return


# Rotate matrix to do colum clust
def rotatematrix(data):
	newdata = []

	for i in range(len(data[0])):
		newrow = [ data[j][i] for j in range(len(data))  ]
		newdata.append(newrow)

	return newdata


# K-means clust
def kcluster(rows, distance=pearson, k=4):

	ranges = [ (min([row[i] for row in rows]), max([ row[i] for row in rows])) for i in range(len(rows[0])) ]

	# Create k centers randomly
	clusters = [ [random.random() * (ranges[i][1]-ranges[i][0]) + ranges[i][0] for i in range(len(rows[0]))] for j in range(k) ]

	lastmatches = None

	# Try 100 times at maximum
	for t in range(100):
		print 'Iteration %d' % t
		bestmatches = [ [] for i in range(k) ]

		# Find the closet center for different row
		for j in range(len(rows)):
			row = rows[j]
			bestmatch = 0

			for i in range(k):
				d = distance(clusters[i], row)
				if d < distance(clusters[bestmatch], row):
					bestmatch = i

			bestmatches[bestmatch].append(j)

		# If the present result and the last result is the same, stop
		if bestmatches == lastmatches:
			break

		lastmatches = bestmatches

		# Modify the position of k centers
		for i in range(k):
			avgs = [0.0] * len(rows[0])

			if len(bestmatches[i]) > 0:
				for rowid in bestmatches[i]:
					for m in range(len(rows[rowid])):
						avgs[m] += rows[rowid][m]

				for j in range(len(avgs)):
					avgs[j] /= len(bestmatches[i])

				clusters[i] = avgs

	return bestmatches


# Multidimensional scaling
def scaledown(data, distance=pearson, rate=0.01):

	n = len(data)

	# Calculate the real distance between each data item
	realdist = [ [distance(data[i], data[j]) for j in range(n)] for i in range(0,n)]

	outersum = 0.0

	# Set initial positions in two-dimensional space
	loc = [ [random.random(), random.random()] for i in range(n) ]

	# Set initial fake distances
	fakedist = [ [0.0 for j in range(n)] for i in range(n) ]

	lasterror = None

	for m in range(0, 1000):
		for i in range(n):
			for j in range(n):

				# Calculate the distance of fack points
				fakedist[i][j] = sqrt( sum([ pow(loc[i][x]-loc[j][x],2) for x in range(len(loc[i]))]) )

		# Now, move the fack points according to fack distance and real distance
		grad = [ [0.0, 0.0] for i in range(n) ]

		totalerror = 0
		for k in range(n):
			for j in range(n):
				if j == k: continue

				errorterm = ( fakedist[j][k] - realdist[j][k]) / realdist[j][k]

				grad[k][0] += ( (loc[k][0] - loc[j][0])/fakedist[j][k] ) * errorterm
				grad[k][1] += ( (loc[k][1] - loc[j][1])/fakedist[j][k] ) * errorterm

				totalerror += abs(errorterm)
		print totalerror

		# If the totalerror is larger than the last totalerror, stop
		if lasterror and lasterror < totalerror: break

		lasterror = totalerror

		for k in range(n):
			loc[k][0] -= rate * grad[k][0]
			loc[k][1] -= rate * grad[k][1]


	return loc


def draw2d(data, labels, jpeg = 'mds2d.jpg'):
	img = Image.new('RGB', (2000, 2000), (255, 255, 255))
	draw = ImageDraw.Draw(img)

	for i in range(len(data)):
		x = (data[i][0] + 0.5) * 1000
		y = (data[i][1] + 0.5) * 1000
		draw.text((x,y), labels[i], (0, 0, 0))

	img.save(jpeg, 'JPEG')




