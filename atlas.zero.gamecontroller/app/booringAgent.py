
class booringAgent:

	name='booring'

	def makePlay(self, playerTurns, ct):
	    play = 'waits'
	    if (ct+1) % 4 == 0:
	        play = 'accepts'    
	    playerTurns[play][ct] = 1
	    return playerTurns

