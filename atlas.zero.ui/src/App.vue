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
        <b-button class="m-1" size="lg" variant="primary">accept<br><small>keyboard [ a ]</small></b-button>
        <b-button class="m-1" size="lg" variant="secondary">wait<br><small>keyboard [ s ]</small></b-button>
        <b-button class="m-1" size="lg" variant="warning">reject<br><small>keyboard [ d ]</small></b-button>
      </b-col>
      <b-col cols="1"></b-col>
      <b-col>
        <b-button class="m-1" size="lg" variant="primary">accept<br><small>keyboard [ j ]</small></b-button>
        <b-button class="m-1" size="lg" variant="secondary">wait<br><small>keyboard [ k ]</small></b-button>
        <b-button class="m-1" size="lg" variant="warning">reject<br><small>keyboard [ l ]</small></b-button>
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

  }
}
</script>

<style>
  @import './assets/azui.css';
</style>
