import Vue from 'vue'
import Demo from './components/Demo.vue'
import VueAgile from 'vue-agile'
import Gallery from './components/Gallery.vue'

Vue.use(VueAgile)

window.Vue = Vue;
app = new Vue({
    el: '#app',
    components: {
        agile: VueAgile,
        Gallery,
        Demo,
    }
});
