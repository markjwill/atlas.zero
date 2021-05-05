<template>
  <div id="app">
    <b-container fluid="lg" class="mx-1">
      

      <b-row> 
        <b-col>
          <b-form label="Player Type">
            <b-form-radio-group
              v-model="turn.playerType"
              :options="playerAgents"
              name="radios-stacked"
              stacked
            ></b-form-radio-group>
          </b-form>
        </b-col>
        
        <b-col cols="1">
          <b-button 
            v-on:click="startGame">
            START
          </b-button>
        </b-col>
        
        <b-col>
          <b-form label="Opponent Type">
            <b-form-radio-group
              v-model="turn.opponentType"
              :options="opponentAgents"
              name="radios-stacked"
              stacked
            ></b-form-radio-group>
          </b-form>
        </b-col>
      </b-row>
      

      <b-row>
        <b-col>
          <span class="currentPlayerOffer">
            <span class="score">
              <span :class="{ 'winner': 1 == turn.winner }">
                {{ this.turn.playerTurns_totalScore }}
              </span>
            </span>
            <br>
            {{ currentPlayerOffer }}
          </span>
          <img alt="Vue logo" src="./assets/logo.png">
          <span class="currentOpponentOffer">      
            <span class="score">
              <span :class="{ 'winner': 0 == turn.winner }">
                {{ this.turn.opponentTurns_totalScore }}
              </span>
            </span>
            <br>
            {{ currentOpponentOffer }}
          </span>
        </b-col>
      </b-row>



      <b-row>
        <b-col>
          <div class="progress">
            <div 
              class="progress-bar" 
              role="progressbar" 
              :style="currentTurnStyleFormatted" 
              :aria-valuenow="currentTurnConverted" 
              aria-valuemin="0" 
              aria-valuemax="100">
                t# {{ uiTurn }} of 20
            </div>
          </div>
          <p>
            <span class="accepts">
              accepts
            </span>
            &nbsp;
            <span class="waits">
              waits
            </span>
            &nbsp;
            <span class="rejects">
              rejects
            </span>
            &nbsp;
            <span class="penalty">
              penalty
            </span>
            &nbsp;
            <span>
              offer
            </span>
            &nbsp;
            <span class="score">
              score
            </span>
          </p>
        </b-col>
      </b-row>




      <b-row>
        <b-col>
          <b-button 
              class="m-1" 
              size="lg" 
              variant="primary" 
              :pressed.sync="ui.player.accept"
              v-on:click="playerAccept">
            accept<br>
            <small>keyboard [ a ]</small>
          </b-button>
          <b-button 
              class="m-1" 
              size="lg" 
              variant="secondary"
              :pressed.sync="ui.player.wait"
              v-on:click="playerWait">
            wait<br>
            <small>keyboard [ s ]</small>
          </b-button>
          <b-button 
              class="m-1" 
              size="lg" 
              variant="warning"
              :pressed.sync="ui.player.reject"
              v-on:click="playerReject">
            reject<br>
            <small>keyboard [ d ]</small>
          </b-button>
        </b-col>
        
        <b-col cols="1"></b-col>
          
        <b-col>
          <b-button 
              class="m-1" 
              size="lg" 
              variant="primary"
              :pressed.sync="ui.opponent.accept"
              v-on:click="opponentAccept">
            accept<br>
            <small>keyboard [ j ]</small></b-button>
          <b-button 
              class="m-1" 
              size="lg" 
              variant="secondary"
              :pressed.sync="ui.opponent.wait"
              v-on:click="opponentWait">
            wait<br>
            <small>keyboard [ k ]</small>
          </b-button>
          <b-button 
              class="m-1" 
              size="lg" 
              variant="warning"
              :pressed.sync="ui.opponent.reject"
              v-on:click="opponentReject">
            reject<br>
            <small>keyboard [ l ]</small>
          </b-button>
        </b-col>
      </b-row>



      <b-row>
        <b-col>
          <div class="scoreBoard">
            <p>
              <span class="accepts">
                a
              </span>
              &nbsp;
              <span class="waits">
                w
              </span>
              &nbsp;
              <span class="rejects">
                r
              </span>
              &nbsp;
              <span class="penalty">
                p
              </span>
              &nbsp;
              <span>
                o
              </span>
              &nbsp;
              <span class="score">
                s
              </span>
            </p>
            <p v-for="i in 20" v-bind:key="i" 
                :class="{ 'currentTurn' : (i) == uiTurn }">
              <span class="accepts">
                {{ turn.playerTurns_accepts[i-1] }}
              </span>
              &nbsp;
              <span class="waits">
                {{ turn.playerTurns_waits[i-1] }}
              </span>
              &nbsp;
              <span class="rejects">
                {{ turn.playerTurns_rejects[i-1] }}
              </span>
              &nbsp;
              <span class="penalty">
              <span :class="{ 'penalty-inactive': 1 == turn.playerTurns_fractionalMultiple[i-1] }">
                {{ turn.playerTurns_fractionalMultiple[i-1] | rightPad }}
              </span>
              </span>
              &nbsp;
              <span :class="{ 'accepts': 1 == turn.playerTurns_accepts[i-1] }">
                {{ turn.playerTurns_offers[i-1] | leftPad3 }}
              </span>
              &nbsp;
              <span class="score">
                {{ turn.playerTurns_cumulativeScore[i-1] | leftPad3 }}
              </span>
            </p>
          </div>
        </b-col>

        <b-col cols="1">
          <div class="scoreBoard">
            <p>
              <span class="turns">  
                t#
              </span>
            </p>
            <p v-for="i in 20" v-bind:key="i" 
                  :class="{ 'currentTurn' : (i) == uiTurn }">
              <span class="turns">  
                {{ i | leftPad }} &nbsp;
              </span>
            </p>
          </div>
        </b-col>

        <b-col>
          <div class="scoreBoard">
            <p>
              <span class="accepts">
                a
              </span>
              &nbsp;
              <span class="waits">
                w
              </span>
              &nbsp;
              <span class="rejects">
                r
              </span>
              &nbsp;
              <span class="penalty">
                p
              </span>
              &nbsp;
              <span>
                o
              </span>
              &nbsp;
              <span class="score">
                s
              </span>
            </p>
            <p v-for="i in 20" v-bind:key="i" 
                :class="{ 'currentTurn' : (i) == uiTurn }">
              <span class="accepts">
                {{ turn.opponentTurns_accepts[i-1] }}
              </span>
              &nbsp;
              <span class="waits">
                {{ turn.opponentTurns_waits[i-1] }}
              </span>
              &nbsp;
              <span class="rejects">
                {{ turn.opponentTurns_rejects[i-1] }}
              </span>
              &nbsp;
              <span class="penalty">
              <span :class="{ 'penalty-inactive': 1 == turn.opponentTurns_fractionalMultiple[i-1] }">
                {{ turn.opponentTurns_fractionalMultiple[i-1] | rightPad }}
              </span>
              </span>
              &nbsp;
              <span :class="{ 'accepts': 1 == turn.opponentTurns_accepts[i-1] }">
                {{ turn.opponentTurns_offers[i-1] | leftPad3 }}
              </span>
              &nbsp;
              <span class="score">
                {{ turn.opponentTurns_cumulativeScore[i-1] | leftPad3 }}
              </span>
            </p>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";  

export default {
  name: 'App',
  data: function() {
    return {
      ui: {
        player: {
          accept: false,
          wait: false,
          reject: false, 
        },
        opponent: {
          accept: false,
          wait: false,
          reject: false, 
        },
        hundreth: 0,
        timerInterval: null,
      },
      playerAgents: [
        { text: 'Human Player', value: 'human' },
        { text: 'Booring Agent', value: 'booring' },
        { text: 'Random Agent', value: 'random' },
        { text: 'Bad Agent', value: 'bad' },
      ],
      opponentAgents: [
        { text: 'Human Player', value: 'human' },
        { text: 'Booring Agent', value: 'booring' },
        { text: 'Random Agent', value: 'random' },
        { text: 'Bad Agent', value: 'bad' },
      ],
      turn: {
        gameId: Math.round(+new Date()/1000),
        playerType: "human",
        playerTurns_accepts: [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ],
        playerTurns_waits: [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ],
        playerTurns_rejects: [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ],
        playerTurns_fractionalMultiple: [
          1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
        ],
        playerTurns_acceptedScore: [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ],
        playerTurns_cumulativeScore: [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ],
        playerTurns_currentScore: [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ],
        playerTurns_totalScore: 0,
        playerTurns_offers: [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ],
        opponentType: "human",
        opponentTurns_accepts: [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ],
        opponentTurns_waits: [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ],
        opponentTurns_rejects: [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ],
        opponentTurns_fractionalMultiple: [
          1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
        ],
        opponentTurns_acceptedScore: [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ],
        opponentTurns_cumulativeScore: [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ],
        opponentTurns_currentScore: [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ],
        opponentTurns_totalScore: 0,
        opponentTurns_offers: [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ],
        state: 1,
        currentTurn: -1,
        winner: -1
      }
    };
  },
  mounted: function() {
    
    this._keyListener = function(event) {
        console.log(event.key);
        if (event.key == "a"){
          this.playerAccept();
        }
        if (event.key == "s"){
          this.playerWait();
        }
        if (event.key == "d"){
          this.playerReject();
        }
        if (event.key == "j"){
          this.opponentAccept();
        }
        if (event.key == "k"){
          this.opponentWait();
        }
        if (event.key == "l"){
          this.opponentReject();
        }
    }
    document.addEventListener('keydown', this._keyListener.bind(this));
  },
  beforeDestroy() {
      document.removeEventListener('keydown', this._keyListener);
  },
  methods: {
    startGame: function (){
      if (this.turn.currentTurn == -1 ){
        this.resetGame();
        this.ui.hundreth = 0;
        this.startTurnsTimer();
      }
    },
    resetGame: function(){
      
      this.turn.playerTurns_accepts = [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ];
      this.turn.playerTurns_waits = [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ];
      this.turn.playerTurns_rejects = [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ];
      this.turn.playerTurns_fractionalMultiple = [
          1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
        ];
      this.turn.playerTurns_acceptedScore = [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ];
      this.turn.playerTurns_cumulativeScore = [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ];
      this.turn.playerTurns_currentScore = [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ];
      this.turn.playerTurns_totalScore = 0;
      this.turn.playerTurns_offers = [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ];
      this.turn.opponentTurns_accepts = [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ];
      this.turn.opponentTurns_waits = [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ];
      this.turn.opponentTurns_rejects = [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ];
      this.turn.opponentTurns_fractionalMultiple = [
          1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
        ];
      this.turn.opponentTurns_acceptedScore = [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ];
      this.turn.opponentTurns_cumulativeScore = [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ];
      this.turn.opponentTurns_currentScore = [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ];
      this.turn.opponentTurns_totalScore = 0;
      this.turn.opponentTurns_offers = [
          0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ];
      this.turn.state = 1;
      this.turn.winner = -1;
    },
    sendTurnData: function (){
      let self = this;
      console.log("sending ajax");
      console.log(self.turn);
      // myAx.post("http://localhost:5000", {
      // axios.defaults.headers.common = {};
      // axios.defaults.headers.post = {};
      axios({ 
        method: 'post',
        url: 'http://127.0.0.1:5000/',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          // 'CrossOrigin': true,
          // 'Access-Control-Allow-Origin': '*',
        }, 
        data: {
          'turn': self.turn
        }
      })
      .then(function(response) {
        console.log("ajax response is in");
        console.log(response);
        console.log(response.data.currentTurn);
        self.turn = response.data;
        self.ui.player.accept = false;
        self.ui.player.wait = false;
        self.ui.player.reject = false;
        self.ui.opponent.accept = false;
        self.ui.opponent.wait = false;
        self.ui.opponent.reject = false;
      })
      .catch(function(error) {
        console.log("error here");
        console.log(error);
        clearInterval(self.timerInterval);
      });
    },
    playerAccept() {
      let t = this.turn.currentTurn;
      if ( this.turn.playerTurns_waits[t]
        + this.turn.playerTurns_rejects[t]
        == 0 ){
          this.ui.player.accept = true;
          this.ui.player.wait = false;
          this.ui.player.reject = false;
          this.turn.playerTurns_accepts[t] = 1;
      }
    },
    playerWait() {
      let t = this.turn.currentTurn;
      if ( this.turn.playerTurns_accepts[t]
        + this.turn.playerTurns_rejects[t]
        == 0 ){
          this.ui.player.wait = true;
          this.ui.player.accept = false;
          this.ui.player.reject = false;
          this.turn.playerTurns_waits[t] = 1;
      }
    },
    playerReject() { 
      let t = this.turn.currentTurn;
      if ( this.turn.playerTurns_waits[t]
        + this.turn.playerTurns_accepts[t]
        == 0 ){
          this.ui.player.reject = true;
          this.ui.player.wait = false;
          this.ui.player.accept = false;
          this.turn.playerTurns_rejects[t] = 1;
      }
    },
    opponentAccept() {
      let t = this.turn.currentTurn;
      if ( this.turn.opponentTurns_waits[t]
        + this.turn.opponentTurns_rejects[t]
        == 0 ){
          this.ui.opponent.accept = true;
          this.ui.opponent.wait = false;
          this.ui.opponent.reject = false;
          this.turn.opponentTurns_accepts[t] = 1;
      }
    },
    opponentWait() {
      let t = this.turn.currentTurn;
      if ( this.turn.opponentTurns_accepts[t]
        + this.turn.opponentTurns_rejects[t]
        == 0 ){
          this.ui.opponent.wait = true;
          this.ui.opponent.accept = false;
          this.ui.opponent.reject = false;
          this.turn.opponentTurns_waits[t] = 1;
      }
    },
    opponentReject() {
      let t = this.turn.currentTurn;
      if ( this.turn.opponentTurns_waits[t]
        + this.turn.opponentTurns_accepts[t]
        == 0 ){
          this.ui.opponent.reject = true;
          this.ui.opponent.wait = false;
          this.ui.opponent.accept = false;
          this.turn.opponentTurns_rejects[t] = 1;
      }
    },
    startTurnsTimer() {
      // this.data
      this.timerInterval = setInterval(this.updateTime, 200);
    },
    updateTime: function() {
      this.ui.hundreth += 1;
      if (this.ui.hundreth % 5 == 0) {
        // this.turn.currentTurn +=1;
        this.sendTurnData();
      }
      if (this.ui.hundreth == 106){
        clearInterval(this.timerInterval);
      }
    }
  },
  computed:{
    currentTurnStyleFormatted: function () {
      return "width: "+this.ui.hundreth+"%";
    },
    uiTurn: function () {
      return this.turn.currentTurn + 1;
    },
    currentTurnConverted: function () {
      return (this.uiTurn) * 5;
    },
    currentPlayerOffer: function () {
      if (this.turn.currentTurn == -1) {
        return '';
      }
      if ( typeof(this.turn.playerTurns_accepts) == "object" ){
        let sum = this.turn.playerTurns_accepts.reduce((a, b) => a + b, 0);
        if (sum == 5) {
          return "x";
        }
      }
      return this.turn.playerTurns_offers[this.turn.currentTurn]
    },
    currentOpponentOffer: function () {
      if (this.turn.currentTurn == -1) {
        return '';
      }
      if ( typeof(this.turn.opponentTurns_accepts) == "object" ){
        let sum = this.turn.opponentTurns_accepts.reduce((a, b) => a + b, 0);
        if (sum == 5) {
          return "x";
        }
      }
      return this.turn.opponentTurns_offers[this.turn.currentTurn]
    },
  },
  filters: {
    leftPad: function (value) {
      return ('00'+value).slice(-2);
    },
    leftPad3: function (value) {
      return ('000'+value).slice(-3);
    },
    rightPad: function (value) {
      return (Math.round(value * 100) / 100).toFixed(2);
    }
  }
}
</script>

<style>
  @import './assets/azui.css';
</style>
