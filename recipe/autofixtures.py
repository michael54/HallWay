from models import Vote
from autofixture import generators, register, AutoFixture

class VoteAutoFixture(AutoFixture):
	field_values = {
		'score': generators.PositiveSmallIntegerGenerator(min_value = 1, max_value = 5)
	}

register(Vote, VoteAutoFixture)