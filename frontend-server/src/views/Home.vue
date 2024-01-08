<template>
    <div class="grid grid-flow-row auto-rows-max mt-[10vh]">
        <div class="w-full h-[44vh] bg-contain sm:bg-cover sm:h-[65vh] bg-opacity-20 flex flex-row bg-[url('../assets/banner.jpg')]">
            <div class="mx-4 my-[5em] sm:m-auto text-center md:text-left text-slate-950 py-4 px-6 drop-shadow-lg bg-slate-200/40 backdrop-blur-sm rounded-lg">
                <h1 class="text-3xl sm:text-4xl">Get extra 10% off for your first purchase</h1>
                <p class="text-lg font-medium mt-2">So what you waiting for grab a basket?</p>
            </div>
        </div>
        <div class="w-full bg-slate-200 font-semibold">
            <div class="container mx-auto px-5 sm:px-10 mt-12 mb-1">
                <div class="flex flex-row items-center justify-between">
                    <h1 class="text-4xl text-slate-500 my-8">Today's Top Deals</h1>
                    <RouterLink :to="{name: 'products'}" class="text-blue-400 text-lg decoration-2 underline underline-offset-4">View All</RouterLink>
                </div>
                <div v-if="products_home&&products_home.length" class="grid grid-flow-row grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 auto-cols-auto justify-around gap-8">
                    <Card v-for="product in products_home" :key="product.id" :product="product"/>
                </div>
                <div v-else class="h-[25vh] sm:h-[40vh] bg-slate-300/30 rounded-lg border-dashed border-4 border-slate-300 sm:col-span-3 md:col-span-4 lg:col-span-5 flex flex-col justify-center items-center">
                    <h1 class="text-3xl text-slate-500">No products available...</h1>
                </div>
            </div>
        </div>
        <div class="w-full bg-slate-200 font-semibold">
            <div class="container mx-auto px-5 sm:px-10 mt-12 pb-10">
                <div class="flex flex-row items-center justify-between">
                    <h1 class="text-4xl text-slate-500 my-8">Popular Products</h1>
                    <RouterLink :to="{name: 'products'}" class="text-blue-400 text-lg decoration-2 underline underline-offset-4">View All</RouterLink>
                </div>
                <div v-if="products_based_on_rating_home&&products_based_on_rating_home.length" class="grid grid-flow-row grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 auto-cols-auto justify-around gap-8">
                    <Card v-for="product in products_based_on_rating_home" :key="product.id" :product="product"/>
                </div>
                <div v-else class="h-[25vh] sm:h-[40vh] bg-slate-300/30 rounded-lg border-dashed border-4 border-slate-300 sm:col-span-3 md:col-span-4 lg:col-span-5 flex flex-col justify-center items-center">
                    <h1 class="text-3xl text-slate-500">No products available...</h1>
                </div>
            </div>
        </div>
    </div>
    <Notify v-if="notify.show"/>
</template>
<script>
    import { mapGetters } from 'vuex'
    import Card from '../components/Card.vue'
    import Notify from '../components/Notify.vue'
    export default {
        computed: {
            ...mapGetters(['products_home','notify','products_based_on_rating_home'])
        },
        async mounted(){
            this.$store.dispatch('get_products')
        },
        components:{
            Card,Notify
        }
    }
</script>