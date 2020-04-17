<template>
  <div>
  <b-container fluid="lg" class="mx-1">
    <b-row>
      <b-col>
        <b-button class="w-25 mx-3" size="lg" variant="primary">accept<br><small>keyboard [ a ]</small></b-button>
        <b-button class="w-25 mx-3" size="lg" variant="secondary">wait<br><small>keyboard [ s ]</small></b-button>
        <b-button class="w-25 mx-3" size="lg" variant="warning">reject<br><small>keyboard [ d ]</small></b-button>
      </b-col>
      <b-col cols="1"></b-col>
      <b-col>
        <b-button class="w-25 mx-3" size="lg" variant="primary">accept<br><small>keyboard [ j ]</small></b-button>
        <b-button class="w-25 mx-3" size="lg" variant="secondary">wait<br><small>keyboard [ k ]</small></b-button>
        <b-button class="w-25 mx-3" size="lg" variant="warning">reject<br><small>keyboard [ l ]</small></b-button>
      </b-col>
    </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
