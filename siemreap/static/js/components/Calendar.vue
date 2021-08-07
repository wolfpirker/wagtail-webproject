<template>
  <div id="calendar">
    <VRangeSelector :start-date.sync="range.start" :end-date.sync="range.end"/>
    <div>Selected range:</div>
    <div>Start: {{range.start}}</div>
    <div>End: {{range.end}}</div>
  </div>
</template>

<script>
import VRangeSelector from 'vuelendar/components/vl-range-selector';
export default {
  components: {
    VRangeSelector
  }
};
</script>
