
class badAgent:

	name='bad'

	def makePlay(self, playerTurns, ct):
	    play = 'rejects'
	    if (ct+1) % 4 == 0:
	        play = 'accepts'    
	    playerTurns[play][ct] = 1
	    return playerTurns

