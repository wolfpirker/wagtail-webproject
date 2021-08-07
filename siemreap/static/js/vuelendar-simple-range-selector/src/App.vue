<template>
  <div id="app">
    <VRangeSelector :start-date.sync="range.start" :end-date.sync="range.end"/>
    <div>Selected range:</div>
    <div>Start: {{range.start}}</div>
    <div>End: {{range.end}}</div>
  </div>
</template>

<script>
import VRangeSelector from '../vuelendar/components/vl-range-selector';
export default {
  name: "App",
  data() {
    return {
      range: {}
    };
  },
  components: {
    VRangeSelector
  }
};
</script>

<style lang="scss">
@import "~vuelendar/scss/vuelendar.scss";
</style>
