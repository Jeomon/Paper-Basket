<template>
    <div class="relative w-full bg-slate-200 min-h-[90vh] top-[10vh]">
        <div class="flex flex-col mx-6">
            <div class="w-full p-3 bg-slate-100 my-10 shadow-md">
                <h1 class="text-center sm:text-left text-4xl text-slate-700">Trend Analysis</h1>
            </div>
        </div>
        <div class="flex flex-col mx-auto bg-white lg:w-[60vw] p-1 sm:p-2 rounded-md">
            <div class="mt-8 mx-12 flex flex-col md:flex-row justify-between items-center h-fit text-lg space-x-3 space-y-3 md:space-y-0">
                <div class="flex flex-col sm:flex-row items-center space-y-3 sm:space-y-0 sm:space-x-2">
                    <label class="text-slate-500 font-medium" for="selector">Pick a Category</label>
                    <select v-model="category" class="cursor-pointer border-[1.5px] px-2 border-gray-600 py-0.5 rounded-md">
                        <option selected disabled :value=null>Select a Category</option>
                        <option v-for="category in categories" :value="category.name.toLowerCase()">{{ category.name }}</option>
                    </select>
                </div>
                <div @click="onDownload" v-if="categories&&categories.length&&category!=null" class="flex flex-row items-center space-x-2 bg-green-700 hover:bg-green-600 text-white p-2 rounded-md cursor-pointer">
                    <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                    </svg>
                    <span class="text-base text-center font-medium cursor-pointer">Generate CSV</span>                    
                </div>
            </div>
            <div v-if="categories&&categories.length" class="min-h-[55vh] flex flex-col items-center mx-auto relative w-fit">
                <img v-if="category" class="w-[70vw] sm:w-[40vw] md:w-[60vw] lg:w-[40vw] h-auto" :src="'http://127.0.0.1:5000/svg/'+category.toLowerCase()" :alt="category">
                <p v-else class="mt-[20%] italic text-xl text-slate-500 font-medium border-[3.2px] border-slate-300 rounded-md p-16 border-dashed">
                    "To visualize data, start by selecting a category."
                </p>
            </div>
            <div v-else class="min-h-[50vh] flex flex-col items-center mx-auto relative w-fit">
                <img class="w-[30vw] h-auto mt-6" src="../../../assets/no-data.png">
                <p class="absolute bottom-11 text-xl font-medium">We found no data..</p>
            </div>
        </div>
    </div>
</template>
<script>
    import { mapGetters } from 'vuex'
    import axios from 'axios'
    export default {
        data(){
            return {
                category:null
            }
        },
        computed: {
            ...mapGetters(['categories'])
        },
        beforeCreate(){
            this.$store.dispatch('get_categories')
        },
        async created(){
            await axios.get('user/manager/trend_analysis')
        },
        methods: {
            async onDownload(){
                if(this.category){
                    let response=await axios.get(`user/manager/trend_analysis/csv/${this.category}`)
                    this.downloader(response.data.id)
                }
            },
            async downloader(id){
                let response=await axios.get(`/csv/${id}`)
                let blob_csv=new Blob([response.data],{type: 'text/csv'})
                let download=document.createElement('a')
                download.href=URL.createObjectURL(blob_csv)
                download.click()
                let message='CSV downloaded successfully'
                this.$store.commit('flash',{'show': true,color:'green','message':message})
            }
        }
    }
</script>