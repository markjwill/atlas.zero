
class randomAgent:

	name='random'

	playTypes = ['accepts', 'rejects', 'waits']

	def makePlay(self, playerTurns, ct):
	    play = random.choice(playTypes)
	    if play == 'accepts' or play == 'rejects':
	        play = random.choice(playTypes)    
	    playerTurns[play][ct] = 1
	    return playerTurns

