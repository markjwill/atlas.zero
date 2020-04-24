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
          Turn {{ currentTurn }} of 20
      </div>
    </div>
      <div>
  <b-container fluid="lg" class="mx-1">
    <b-row>
      <b-col>
        <b-row>
          <b-button class="m-1" size="lg" variant="primary">accept<br><small>keyboard [ a ]</small></b-button>
          <b-button class="m-1" size="lg" variant="secondary">wait<br><small>keyboard [ s ]</small></b-button>
          <b-button class="m-1" size="lg" variant="warning">reject<br><small>keyboard [ d ]</small></b-button>
        </b-row>
        <b-row>
          <div class="scoreBoard">
            <p>
              <span class="turns">  
                t &nbsp;
              </span>
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
                :class="{ 'currentTurn' : (i-1) == currentTurn }">
              <span class="turns">  
                {{ i | leftPad }} &nbsp;
              </span>
              <span class="accepts">
                {{ playerTurns.accepts[i-1] }}
              </span>
              &nbsp;
              <span class="waits">
                {{ playerTurns.waits[i-1] }}
              </span>
              &nbsp;
              <span class="rejects">
                {{ playerTurns.rejects[i-1] }}
              </span>
              &nbsp;
              <span class="penalty">
              <span :class="{ 'penalty-inactive': 1 == playerTurns.fractionalMultiple[i-1] }">
                {{ playerTurns.fractionalMultiple[i-1] | rightPad }}
              </span>
              </span>
              &nbsp;
              <span class="score">
                {{ playerTurns.cumulativeScore[i-1] }}
              </span>
            </p>
          </div>
        </b-row>
      </b-col>
      <b-col cols="1"></b-col>
      <b-col>
        <b-row>
          <b-button class="m-1" size="lg" variant="primary">accept<br><small>keyboard [ j ]</small></b-button>
          <b-button class="m-1" size="lg" variant="secondary">wait<br><small>keyboard [ k ]</small></b-button>
          <b-button class="m-1" size="lg" variant="warning">reject<br><small>keyboard [ l ]</small></b-button>
        </b-row>
        <b-row>
          <div class="scoreBoard">
            <p>
              <span class="turns">  
                t &nbsp;
              </span>
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
                :class="{ 'currentTurn' : (i-1) == currentTurn }">
              <span class="turns">  
                {{ i | leftPad }} &nbsp;
              </span>
              <span class="accepts">
                {{ opponentTurns.accepts[i-1] }}
              </span>
              &nbsp;
              <span class="waits">
                {{ opponentTurns.waits[i-1] }}
              </span>
              &nbsp;
              <span class="rejects">
                {{ opponentTurns.rejects[i-1] }}
              </span>
              &nbsp;
              <span class="penalty">
              <span :class="{ 'penalty-inactive': 1 == opponentTurns.fractionalMultiple[i-1] }">
                {{ opponentTurns.fractionalMultiple[i-1] | rightPad }}
              </span>
              </span>
              &nbsp;
              <span class="score">
                {{ opponentTurns.cumulativeScore[i-1] }}
              </span>
            </p>
          </div>
        </b-row>
      </b-col>
    </b-row>
    </b-container>
  </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data: function() {
    return {
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
      currentTurn: 0,
      winner: -1
    };
  },
  computed:{
    currentTurnStyleFormatted: function () {
      return "width: "+this.currentTurnConverted+"%";
    },
    currentTurnConverted: function () {
      return this.currentTurn * 5;
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
