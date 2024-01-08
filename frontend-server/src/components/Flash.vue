<template>
<div :class="['fixed',flash.color ? `bg-${flash.color}-600` : '','w-fit','px-3','py-2','z-10','rounded-md','left-0','right-0','mx-auto','top-[12vh]','shadow-md']">
        <p class="text-xl font-semibold text-white">{{ flash.message }}</p>
    </div>
</template>
<script>
    import { mapGetters } from 'vuex'
    export default {
        data(){
            return {
                timer:null
            }
        },
        computed: {
            ...mapGetters(['flash'])
        },
        created(){
            this.timer=setTimeout(()=>{
                this.$store.commit('flash',{'show': false,'message':''})
            },3000)
        },
        beforeDestroy(){
            clearTimeout(this.timer)
        }
    }
</script>