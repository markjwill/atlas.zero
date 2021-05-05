import time
from flask import Flask, render_template, flash, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sys
import random
import psycopg2
from inspect import currentframe, getframeinfo


from randomAgent import randomAgent
from humanAgent import humanAgent
from badAgent import badAgent
from booringAgent import booringAgent

agents = {
    'random' : randomAgent,
    'human' : humanAgent,
    'bad' : badAgent,
    'booring' : booringAgent
}

DBUSER = 'marco'
DBPASS = 'foobarbaz'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'testdb'


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# logging.getLogger('flask_cors').level = logging.DEBUG

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'foobarbaz'


db = SQLAlchemy(app)

playTypes = ['accepts', 'rejects', 'waits']
minMaxAccepts = 5
fractionalMultiple = 0.8
waitFractionalBump = 0.03
waitOfferBump = 3
totalTurns = 20

insertQuery = """ INSERT INTO public.turns ( "gameId", "playerType", "playerTurns_accepts", "playerTurns_waits", "playerTurns_rejects", "playerTurns_fractionalMultiple", "playerTurns_cumulativeScore", "playerTurns_acceptedScore", "playerTurns_totalScore", "playerTurns_offers", "oponnentType", "opponentTurns_accepts", "opponentTurns_waits", "opponentTurns_rejects", "opponentTurns_fractionalMultiple", "opponentTurns_cumulativeScore", "opponentTurns_acceptedScore", "opponentTurns_totalScore", "opponentTurns_offers", "state", "currentTurn", "winner") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

updateQuery = """ UPDATE public.turns SET "winner" = %s WHERE "gameId" = %s """

try:
    connection = psycopg2.connect("dbname='"+DBNAME+"' user='"+DBUSER+"' host='"+DBHOST+"' password='"+DBPASS+"'")
except psycopg2.OperationalError as e:
    print("I am unable to connect to the database"+str(e), file=sys.stderr)
    sys.exit(1)


class turns(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gameId = db.Column(db.Integer)
    playerType = db.Column(db.String(15), nullable=False)
    playerTurns_accepts = db.Column(db.ARRAY(db.Integer))
    playerTurns_waits = db.Column(db.ARRAY(db.Integer))
    playerTurns_rejects = db.Column(db.ARRAY(db.Integer))
    playerTurns_fractionalMultiple = db.Column(db.ARRAY(db.Integer))
    playerTurns_currentScore = db.Column(db.ARRAY(db.Integer))
    playerTurns_totalScore = db.Column(db.Integer)
    playerTurns_offers = db.Column(db.ARRAY(db.Integer))
    oponnentType = db.Column(db.String(15), nullable=False)
    opponentTurns_accepts = db.Column(db.ARRAY(db.Integer))
    opponentTurns_waits = db.Column(db.ARRAY(db.Integer))
    opponentTurns_rejects = db.Column(db.ARRAY(db.Integer))
    opponentTurns_fractionalMultiple = db.Column(db.ARRAY(db.Integer))
    opponentTurns_currentScore = db.Column(db.ARRAY(db.Integer))
    opponentTurns_totalScore = db.Column(db.Integer)
    opponentTurns_offers = db.Column(db.ARRAY(db.Integer))
    state = db.Column(db.Integer)
    currentTurn = db.Column(db.Integer)
    winner = db.Column(db.Integer)    

    def __init__(self, turnObj):
        self.gameId = turnObj['gameId']
        self.playerType = turnObj['playerType']
        self.playerTurns_accepts = turnObj['playerTurns_accepts']
        self.playerTurns_waits = turnObj['playerTurns_waits']
        self.playerTurns_rejects = turnObj['playerTurns_rejects']
        self.playerTurns_fractionalMultiple = turnObj['playerTurns_fractionalMultiple']
        self.playerTurns_currentScore = turnObj['playerTurns_currentScore']
        self.playerTurns_totalScore = turnObj['playerTurns_totalScore']
        self.playerTurns_offers = turnObj['playerTurns_offers']
        self.oponnentType = turnObj['oponnentType']
        self.opponentTurns_accepts = turnObj['opponentTurns_accepts']
        self.opponentTurns_waits = turnObj['opponentTurns_waits']
        self.opponentTurns_rejects = turnObj['opponentTurns_rejects']
        self.opponentTurns_fractionalMultiple = turnObj['opponentTurns_fractionalMultiple']
        self.opponentTurns_currentScore = turnObj['opponentTurns_currentScore']
        self.opponentTurns_totalScore = turnObj['opponentTurns_totalScore']
        self.opponentTurns_offers = turnObj['opponentTurns_offers']
        self.state = turnObj['state']
        self.currentTurn = turnObj['currentTurn']
        self.winner = turnObj['winner']

def database_initialization_sequence():
    db.create_all()
    test_rec = turns({
        "gameId": 1,
        "playerType": "human",
        "playerTurns_accepts": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "playerTurns_waits": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "playerTurns_rejects": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "playerTurns_fractionalMultiple": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        "playerTurns_acceptedScore": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "playerTurns_cumulativeScore": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "playerTurns_currentScore": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "playerTurns_totalScore": 0,
        "playerTurns_offers": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "oponnentType": "human",
        "opponentTurns_accepts": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "opponentTurns_waits": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "opponentTurns_rejects": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "opponentTurns_fractionalMultiple": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        "opponentTurns_acceptedScore": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "opponentTurns_cumulativeScore": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "opponentTurns_currentScore": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "opponentTurns_totalScore": 0,
        "opponentTurns_offers": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "state": 1,
        "currentTurn": -1,
        "winner": -1
    })

    db.session.add(test_rec)
    db.session.rollback()
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
# @cross_origin()
def home():
    print(request.method+' request arrived here.', file=sys.stderr)
    if request.method == 'POST':
        turn = request.get_json()
        print('turn is '+str(turn), file=sys.stderr)
        turn = processTurn(turn['turn'])
        print('turn processed', file=sys.stderr)
        return jsonify(turn)
    return render_template('show_all.html', turns=turns.query.all())

# @app.after_request
# def add_header(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization'
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
#     return response

# cors.init_app(app)

def processTurn(turn):
    debug=True
    turn = expandTurn(turn)
    ct = turn['currentTurn']
    tt = ct - 1
    nt = ct + 1

    if ct == -1:
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        turn['opponentTurns']['offers'][nt] = getNextOffer()
        turn['playerTurns']['offers'][nt] = getNextOffer()
        turn['currentTurn'] += 1
        return flattenTurn(turn)

    if debug:
        frameinfo = getframeinfo(currentframe())
        print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
   
    try:
        playerAgent = agents[turn['playerType']]()
        opponentAgent = agents[turn['oponnentType']]()

        turn['playerTurns'] = playerAgent.makePlay(turn['playerTurns'], ct)
        turn['opponentTurns'] = opponentAgent.makePlay(turn['opponentTurns'], ct)
    except TypeError as e:
        print('error1: '+str(e), file=sys.stderr)
    except:
        e = sys.exc_info()[0]
        print('error: '+str(e), file=sys.stderr)


    # # Temp
    # if turn['playerType'] == 'human':
    #     # do nothing
    # elif turn['playerType'] == 'random':
    #     turn['playerTurns'] = makeRandomPlay(turn['playerTurns'], ct)
    # elif turn['playerType'] == 'random':
    #     turn['playerTurns'] = makeRandomPlay(turn['playerTurns'], ct)

    # turn['opponentTurns'] = makeRandomPlay(turn['opponentTurns'], ct)
    # turn['playerTurns'] = makeBadPlay(turn['playerTurns'], ct) 
    # Temp  
    if debug:
        frameinfo = getframeinfo(currentframe())
        print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
    # app.logger.info('player: ')
    turn['opponentTurns'] = validatePlay(turn['opponentTurns'], ct)
    # app.logger.info('opponent: ')
    turn['playerTurns'] = validatePlay(turn['playerTurns'], ct) 
    if debug:
        frameinfo = getframeinfo(currentframe())
        print('line reached: '+str(frameinfo.lineno), file=sys.stderr)

    turn['opponentTurns'] = scorePlayerTurn(turn['opponentTurns'], tt, ct)
    if debug:
        frameinfo = getframeinfo(currentframe())
        print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
    turn['playerTurns'] = scorePlayerTurn(turn['playerTurns'], tt, ct)

    if ct == 19:
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        turn['currentTurn'] = -1
        if turn['playerTurns']['totalScore'] > turn['opponentTurns']['totalScore']:
            turn['winner'] = 1
        if turn['playerTurns']['totalScore'] < turn['opponentTurns']['totalScore']:
            turn['winner'] = 0
        turn = flattenTurn(turn)
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        saveGameTurns(turn)
    else:
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        turn = flattenTurn(turn)
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        cacheTurn(turn)
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        turn = expandTurn(turn)
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        turn['opponentTurns'] = setupPlayerTurn(turn['opponentTurns'], ct, nt)
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        turn['playerTurns'] = setupPlayerTurn(turn['playerTurns'], ct, nt)
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        turn['currentTurn'] += 1
    if debug:
        frameinfo = getframeinfo(currentframe())
        print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
    turn = flattenTurn(turn)
    return turn

def scorePlayerTurn(playerTurns, tt, ct):
    if playerTurns['accepts'][ct] == 1:
        playerTurns['acceptedScore'][ct] = round( playerTurns['offers'][ct] * playerTurns['fractionalMultiple'][ct] )
        playerTurns['cumulativeScore'][ct] = sum(playerTurns['acceptedScore']) 
        playerTurns['totalScore'] = playerTurns['cumulativeScore'][ct]
    
    if playerTurns['rejects'][ct] == 1:
        playerTurns['cumulativeScore'][ct] = playerTurns['cumulativeScore'][tt]

    
    if playerTurns['waits'][ct] == 1:
        playerTurns['cumulativeScore'][ct] = playerTurns['cumulativeScore'][tt]

    return playerTurns

def setupPlayerTurn(playerTurns, ct, nt):
    if playerTurns['accepts'][ct] == 1:
        playerTurns['offers'][nt] = getNextOffer()
    
    if playerTurns['rejects'][ct] == 1:
        playerTurns['fractionalMultiple'][nt] = playerTurns['fractionalMultiple'][ct] * fractionalMultiple
        playerTurns['offers'][nt] = getNextOffer()
    
    if playerTurns['waits'][ct] == 1:
        playerTurns['fractionalMultiple'][nt] = playerTurns['fractionalMultiple'][ct] + waitFractionalBump
        if playerTurns['fractionalMultiple'][nt] > 1:
            playerTurns['fractionalMultiple'][nt] = 1
        playerTurns['offers'][nt] = playerTurns['offers'][ct] + waitOfferBump
        if playerTurns['offers'][nt] > 100:
            playerTurns['offers'][nt] = 100

    return playerTurns


# def makeRandomPlay(playerTurns, ct):
#     play = random.choice(playTypes)
#     if play == 'accepts' or play == 'rejects':
#         play = random.choice(playTypes)    
#     playerTurns[play][ct] = 1
#     return playerTurns

# def makeBooringPlay(playerTurns, ct):
#     play = 'waits'
#     if (ct+1) % 4 == 0:
#         play = 'accepts'    
#     playerTurns[play][ct] = 1
#     return playerTurns

# def makeBadPlay(playerTurns, ct):
#     play = 'rejects'
#     if (ct+1) % 4 == 0:
#         play = 'accepts'    
#     playerTurns[play][ct] = 1
#     return playerTurns

def validatePlay(playerTurns, ct):
    debug=True
    if debug:
        frameinfo = getframeinfo(currentframe())
        print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
    acceptCount = sum(playerTurns['accepts'])
    if debug:
        frameinfo = getframeinfo(currentframe())
        print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
    turnsDelta = ( ct + 1 ) - ( totalTurns - minMaxAccepts )
    # app.logger.info('%s %s %s', ct, acceptCount, turnsDelta)
    if debug:
        frameinfo = getframeinfo(currentframe())
        print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
    if acceptCount > minMaxAccepts:
        play = 'waits'
    elif acceptCount < turnsDelta:
        play = 'accepts'
    else:
        play = 'waits'
        if playerTurns['accepts'][ct] == 1:
            play = 'accepts'
        if playerTurns['rejects'][ct] == 1:
            play = 'rejects'
    if debug:
        frameinfo = getframeinfo(currentframe())
        print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
    for type in playTypes:
        if type == play:
            playerTurns[type][ct] = 1
        else:
            playerTurns[type][ct] = 0
    acceptCount = sum(playerTurns['accepts'])
    # app.logger.info('%s %s %s', ct, acceptCount, turnsDelta)
    if debug:
        frameinfo = getframeinfo(currentframe())
        print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
    return playerTurns


def cacheTurn(turn):
    debug=False
    turn=expandTurn(turn)
    try:
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        cursor = connection.cursor()
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        turnData = (turn["gameId"],turn["playerType"],turn["playerTurns"]["accepts"],turn["playerTurns"]["waits"],turn["playerTurns"]["rejects"],turn["playerTurns"]["fractionalMultiple"],turn["playerTurns"]["cumulativeScore"],turn["playerTurns"]["acceptedScore"],turn["playerTurns"]["totalScore"],turn["playerTurns"]["offers"],turn["oponnentType"],turn["opponentTurns"]["accepts"],turn["opponentTurns"]["waits"],turn["opponentTurns"]["rejects"],turn["opponentTurns"]["fractionalMultiple"],turn["opponentTurns"]["cumulativeScore"],turn["opponentTurns"]["acceptedScore"],turn["opponentTurns"]["totalScore"],turn["opponentTurns"]["offers"],turn["state"],turn["currentTurn"],turn["winner"])
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        cursor.execute(insertQuery, turnData)
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        connection.commit()
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
    except psycopg2.ProgrammingError as e:
        print('Error1: '+str(e), file=sys.stderr)
    except psycopg2.InterfaceError as e:
        print('Error2: '+str(e), file=sys.stderr)
    except psycopg2.DataError as e:
        print('Error3: '+str(e), file=sys.stderr)
    except psycopg2.InternalError as e:
        print('Error5: '+str(e), file=sys.stderr)
    except:
        e = sys.exc_info()[0]
        print('Error4: '+str(e), file=sys.stderr)
    # finally:
        # connection.close()


def saveGameTurns(turn): 
    debug=False
    turn=expandTurn(turn)
    try:
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        cursor = connection.cursor()
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        turnData = (turn["winner"], str(turn["gameId"]))
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        cursor.execute(updateQuery, turnData)
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
        connection.commit()
        if debug:
            frameinfo = getframeinfo(currentframe())
            print('line reached: '+str(frameinfo.lineno), file=sys.stderr)
    except psycopg2.ProgrammingError as e:
        print('Error1: '+str(e), file=sys.stderr)
    except psycopg2.InterfaceError as e:
        print('Error2: '+str(e), file=sys.stderr)
    except psycopg2.DataError as e:
        print('Error3: '+str(e), file=sys.stderr)
    except psycopg2.InternalError as e:
        print('Error5: '+str(e), file=sys.stderr)
    except:
        e = sys.exc_info()[0]
        print('Error4: '+str(e), file=sys.stderr)


def getNextOffer():
    return random.randint(1, 100)

def flattenTurn(turn):
    if 'playerTurns_accepts' in turn.keys():
        return turn
    turn['playerTurns_accepts'] = turn['playerTurns']['accepts']
    del turn['playerTurns']['accepts']
    turn['playerTurns_waits'] = turn['playerTurns']['waits']
    del turn['playerTurns']['waits']
    turn['playerTurns_rejects'] = turn['playerTurns']['rejects']
    del turn['playerTurns']['rejects']
    turn['playerTurns_fractionalMultiple'] = turn['playerTurns']['fractionalMultiple']
    del turn['playerTurns']['fractionalMultiple']
    turn['playerTurns_acceptedScore'] = turn['playerTurns']['acceptedScore']
    del turn['playerTurns']['acceptedScore']
    turn['playerTurns_cumulativeScore'] = turn['playerTurns']['cumulativeScore']
    del turn['playerTurns']['cumulativeScore']
    turn['playerTurns_currentScore'] = turn['playerTurns']['currentScore']
    del turn['playerTurns']['currentScore']
    turn['playerTurns_offers'] = turn['playerTurns']['offers']
    del turn['playerTurns']['offers']
    turn['playerTurns_totalScore'] = turn['playerTurns']['totalScore']
    del turn['playerTurns']['totalScore']
    del turn['playerTurns']
    turn['opponentTurns_accepts'] = turn['opponentTurns']['accepts']
    del turn['opponentTurns']['accepts']
    turn['opponentTurns_waits'] = turn['opponentTurns']['waits']
    del turn['opponentTurns']['waits']
    turn['opponentTurns_rejects'] = turn['opponentTurns']['rejects']
    del turn['opponentTurns']['rejects']
    turn['opponentTurns_fractionalMultiple'] = turn['opponentTurns']['fractionalMultiple']
    del turn['opponentTurns']['fractionalMultiple']
    turn['opponentTurns_acceptedScore'] = turn['opponentTurns']['acceptedScore']
    del turn['opponentTurns']['acceptedScore']
    turn['opponentTurns_cumulativeScore'] = turn['opponentTurns']['cumulativeScore']
    del turn['opponentTurns']['cumulativeScore']
    turn['opponentTurns_currentScore'] = turn['opponentTurns']['currentScore']
    del turn['opponentTurns']['currentScore']
    turn['opponentTurns_offers'] = turn['opponentTurns']['offers']
    del turn['opponentTurns']['offers']
    turn['opponentTurns_totalScore'] = turn['opponentTurns']['totalScore']
    del turn['opponentTurns']['totalScore']
    del turn['opponentTurns']
    return turn

def expandTurn(turn):
    # print('expand turn here '+str(turn), file=sys.stderr)
    if 'playerTurns' in turn.keys():
        return turn
    turn['playerTurns'] = {}
    turn['opponentTurns'] = {}
    turn['playerTurns']['accepts'] = turn['playerTurns_accepts']
    del turn['playerTurns_accepts']
    turn['playerTurns']['waits'] = turn['playerTurns_waits']
    del turn['playerTurns_waits']
    turn['playerTurns']['rejects'] = turn['playerTurns_rejects']
    del turn['playerTurns_rejects']
    turn['playerTurns']['fractionalMultiple'] = turn['playerTurns_fractionalMultiple']
    del turn['playerTurns_fractionalMultiple']
    turn['playerTurns']['acceptedScore'] = turn['playerTurns_acceptedScore']
    del turn['playerTurns_acceptedScore']
    turn['playerTurns']['cumulativeScore'] = turn['playerTurns_cumulativeScore']
    del turn['playerTurns_cumulativeScore']
    turn['playerTurns']['currentScore'] = turn['playerTurns_currentScore']
    del turn['playerTurns_currentScore']
    turn['playerTurns']['offers'] = turn['playerTurns_offers']
    del turn['playerTurns_offers']
    turn['playerTurns']['totalScore'] = turn['playerTurns_totalScore']
    del turn['playerTurns_totalScore']
    turn['opponentTurns']['accepts'] = turn['opponentTurns_accepts']
    del turn['opponentTurns_accepts']
    turn['opponentTurns']['waits'] = turn['opponentTurns_waits']
    del turn['opponentTurns_waits']
    turn['opponentTurns']['rejects'] = turn['opponentTurns_rejects']
    del turn['opponentTurns_rejects']
    turn['opponentTurns']['fractionalMultiple'] = turn['opponentTurns_fractionalMultiple']
    del turn['opponentTurns_fractionalMultiple']
    turn['opponentTurns']['acceptedScore'] = turn['opponentTurns_acceptedScore']
    del turn['opponentTurns_acceptedScore']
    turn['opponentTurns']['cumulativeScore'] = turn['opponentTurns_cumulativeScore']
    del turn['opponentTurns_cumulativeScore']
    turn['opponentTurns']['currentScore'] = turn['opponentTurns_currentScore']
    del turn['opponentTurns_currentScore']
    turn['opponentTurns']['offers'] = turn['opponentTurns_offers']
    del turn['opponentTurns_offers']
    turn['opponentTurns']['totalScore'] = turn['opponentTurns_totalScore']
    del turn['opponentTurns_totalScore']
    return turn

if __name__ == '__main__':
    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
        else:
            dbstatus = True
    database_initialization_sequence()
    app.run(debug=True, host='0.0.0.0')
