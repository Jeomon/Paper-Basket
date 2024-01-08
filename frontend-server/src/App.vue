<template>
    <Flash v-if="flash.show"/>
    <Navbar/>
    <RouterView/>
</template>
<script>
    import { mapGetters } from 'vuex'
    import Navbar from './components/Navbar.vue'
    import Flash from './components/Flash.vue'
    export default {        
        name: "App",
        computed: {
            ...mapGetters(['flash'])
        },
        components: {
            Navbar,Flash
        },
    }
</script>