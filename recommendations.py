from math import sqrt

critics={
			'lisa': 
				{
					'lady': 2.5,
					'snakes': 3.5,
					'just': 3.0,
					'superman': 3.5,
					'you': 2.5,
					'night': 3.0
				},

			'gene': 
				{
					'lady': 3.0,
					'snakes': 3.5,
					'just': 1.5,
					'superman': 5.0,
					'you': 3.0,
					'night': 3.5 
				},

			'michael': 
				{
					'lady': 2.5,
					'snakes': 3.0,
					'superman': 3.5,
					'night': 4.0
				},

			'claudia': 
				{
					'snakes': 3.5,
					'just': 3.0,
					'superman': 4.0,
					'you': 2.5,
					'night':4.5 
				},

			'mike': 
				{
					'lady': 3.0,
					'snakes': 4.0,
					'just': 2.0,
					'superman': 3.0,
					'you': 2.0,
					'night': 3.0
				},

			'jack': 
				{
					'lady': 3.0,
					'snakes': 4.0,
					'just': 2.0,
					'superman': 5.0,
					'you': 3.5,
					'night': 3.0
				},

			'tody': 
				{
					'snakes': 4.5,
					'superman': 4.0,
					'you': 1.0,
				},
}


# Return relative score based on distance of two person
def sim_distance(prefs, person1, person2):

	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item] = 1

	# if there are no item shares by two persons, return 0 as raletive score
	if len(si) == 0:
		return 0

	distance = sqrt(sum([ pow( prefs[person1][item] - prefs[person2][item], 2 ) for item in prefs[person1] if item in prefs[person2]]))

	return 1 / ( 1 + distance )


# Return relative score based on pearson index of two person
def sim_pearson(prefs, person1, person2):

	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item] = 1

	# if there are no item shares by two persons, return 0 as raletive score
	if len(si) == 0:
		return 0

	n = len(si)

	sum1 = sum( [prefs[person1][item] for item in si])
	sum2 = sum( [prefs[person2][item] for item in si])

	sum1sq = sum( [pow(prefs[person1][item], 2) for item in si] )
	sum2sq = sum( [pow(prefs[person2][item], 2) for item in si] )

	pSum = sum( [prefs[person1][item] * prefs[person2][item] for item in si] )

	num = pSum - (sum1 * sum2 / n)
	den = sqrt( (sum1sq - pow(sum1,2)/n) * (sum2sq-pow(sum2,2)/n) )

	if den == 0:
		return 0

	return num/den


# Return the top matches according to similarity
def topMatches(prefs, person, n=5, similarity=sim_pearson):

	# Calculate similarities
	scores=[ (similarity(prefs, person, other), other) for other in prefs if other!=person ]

	scores.sort()
	scores.reverse()

	return scores[0:n]


# Score items and get recommendations
def getRecommendations(prefs, person, similarity=sim_pearson):

	totals={}
	simSums={}

	for other in prefs:
		if other == person:
			continue
		sim=similarity(prefs, person, other)

		if sim <= 0:
			continue

		for item in prefs[other]:
			if item not in prefs[person] or prefs[person][item] == 0:
				totals.setdefault(item, 0)
				totals[item] += prefs[other][item]*sim

				simSums.setdefault(item, 0)
				simSums[item] += sim

		rankings = [ (total/simSums[item], item) for item, total in totals.items()]

		rankings.sort()
		rankings.reverse()

	return rankings


# Exchange persons and items
def transformPrefs(prefs):
	result = {}

	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item,{})
			result[item][person] = prefs[person][item]

	return result



