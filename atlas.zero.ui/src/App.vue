<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
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
      <div>
  <b-container fluid="lg" class="mx-1">
    <b-row>
      <b-col>
        <b-row>
          <b-col>
            <b-button 
                class="m-1" 
                size="lg" 
                variant="primary" 
                :pressed.sync="ui.player.accept">
              accept<br>
              <small>keyboard [ a ]</small>
            </b-button>
            <b-button 
                class="m-1" 
                size="lg" 
                variant="secondary"
                :pressed.sync="ui.player.wait">
              wait<br>
              <small>keyboard [ s ]</small>
            </b-button>
            <b-button 
                class="m-1" 
                size="lg" 
                variant="warning"
                :pressed.sync="ui.player.reject">
              reject<br>
              <small>keyboard [ d ]</small>
            </b-button>
          </b-col>
          <b-col cols="1"></b-col>
          <b-col>
            <b-row>
              <b-button 
                  class="m-1" 
                  size="lg" 
                  variant="primary"
                  :pressed.sync="ui.opponent.accept">
                accept<br>
                <small>keyboard [ j ]</small></b-button>
              <b-button 
                  class="m-1" 
                  size="lg" 
                  variant="secondary"
                  :pressed.sync="ui.opponent.wait">
                wait<br>
                <small>keyboard [ k ]</small>
              </b-button>
              <b-button 
                  class="m-1" 
                  size="lg" 
                  variant="warning"
                  :pressed.sync="ui.opponent.reject">
                reject<br>
                <small>keyboard [ l ]</small>
              </b-button>
            </b-row>
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
                <span class="score">
                  s
                </span>
              </p>
              <p v-for="i in 20" v-bind:key="i" 
                  :class="{ 'currentTurn' : (i) == uiTurn }">
                <span class="accepts">
                  {{ turn.playerTurns.accepts[i-1] }}
                </span>
                &nbsp;
                <span class="waits">
                  {{ turn.playerTurns.waits[i-1] }}
                </span>
                &nbsp;
                <span class="rejects">
                  {{ turn.playerTurns.rejects[i-1] }}
                </span>
                &nbsp;
                <span class="penalty">
                <span :class="{ 'penalty-inactive': 1 == turn.playerTurns.fractionalMultiple[i-1] }">
                  {{ turn.playerTurns.fractionalMultiple[i-1] | rightPad }}
                </span>
                </span>
                &nbsp;
                <span class="score">
                  {{ turn.playerTurns.cumulativeScore[i-1] }}
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
                <span class="score">
                  s
                </span>
              </p>
              <p v-for="i in 20" v-bind:key="i" 
                  :class="{ 'currentTurn' : (i) == uiTurn }">
                <span class="accepts">
                  {{ turn.opponentTurns.accepts[i-1] }}
                </span>
                &nbsp;
                <span class="waits">
                  {{ turn.opponentTurns.waits[i-1] }}
                </span>
                &nbsp;
                <span class="rejects">
                  {{ turn.opponentTurns.rejects[i-1] }}
                </span>
                &nbsp;
                <span class="penalty">
                <span :class="{ 'penalty-inactive': 1 == turn.opponentTurns.fractionalMultiple[i-1] }">
                  {{ turn.opponentTurns.fractionalMultiple[i-1] | rightPad }}
                </span>
                </span>
                &nbsp;
                <span class="score">
                  {{ turn.opponentTurns.cumulativeScore[i-1] }}
                </span>
              </p>
            </div>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
    </b-container>
  </div>
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
      turn: {
        gameId: 15865713850000,
        playerType: "human",
        playerTurns: {
          accepts: [
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          waits: [
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          rejects: [
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          fractionalMultiple: [
            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
          ],
          cumulativeScore: [
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          totalScore: 0,
          offers: [
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ]
        },
        oponnentType: "human",
        opponentTurns: {
          accepts: [
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          waits: [
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          rejects: [
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          fractionalMultiple: [
            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
          ],
          cumulativeScore: [
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          totalScore: 0,
          offers: [
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ]
        },
        state: 1,
        currentTurn: -1,
        winner: -1
      }
    };
  },
  methods: {
    sendTurnData: function (){
      axios.post("https://jsonplaceholder.typicode.com/todos/", this.data.turn)
        .then(response => {
           this.todosList = [...response.data].slice(0, 10)
        })
    },
    startTurnsTimer() {
      this.timerInterval = setInterval(this.updateTime, 200);
    },
    updateTime: function() {
      this.ui.hundreth += 1;
      if (this.ui.hundreth % 5 == 0) {
        this.turn.currentTurn +=1;
      }
      if (this.ui.hundreth == 100){
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
    }
  },
  filters: {
    leftPad: function (value) {
      return ('00'+value).slice(-2);
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
