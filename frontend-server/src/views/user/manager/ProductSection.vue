<template>
    <div class="relative w-full bg-slate-200 min-h-[90vh] top-[10vh]">
        <div class="flex flex-col mx-6">
            <div class="w-full py-3 px-3 bg-slate-100 my-10 shadow-md">
                <h1 class="text-center sm:text-left text-4xl text-slate-700">Product Section</h1>
            </div>
        </div>
        <div class="flex md:flex-row flex-col md:justify-between items-center mx-6">
            <div class="my-2 flex flex-row shadow-sm rounded-md overflow-hidden">
                <input @keyup="onTyping" class="sm:w-[30vw] md:w-[25vw] lg:w-[20vw] max-w-md px-3 h-10 bg-slate-100 outline-none text-slate-500 font-medium placeholder:text-slate-400 placeholder:font-medium" placeholder="Find Product Here" type="search" name="product">
                <button>
                    <svg class="p-2 text-slate-400 bg-slate-700 hover:text-slate-300 w-10 h-10" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clip-rule="evenodd" />
                    </svg>
                </button>
            </div>
            <div class="flex flex-row items-center space-x-1 cursor-pointer">
                <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>                            
                <RouterLink :to="{name: 'manager_add_product'}" class="text-xl text-slate-600 font-medium">Add Product</RouterLink>
            </div>
        </div>
        <div class="overflow-x-auto">
            <div class="inline-block min-w-full py-2 sm:px-6 lg:px-8">
                <div class="overflow-hidden">
                    <table class="w-[75vw] text-sm font-light text-center">
                        <thead class="border-b-2 border-neutral-500 text-base">
                            <tr class="text-slate-600 uppercase">
                                <th scope="col" class="px-6 py-3">Name</th>
                                <th scope="col" class="px-6 py-3">Category</th>
                                <th scope="col" class="px-6 py-3">Stock</th>
                                <th scope="col" class="px-6 py-3">Price</th>
                                <th scope="col" class="px-6 py-3">Discount</th>
                                <th scope="col" class="px-6 py-3">Update</th>
                                <th scope="col" class="px-6 py-3">Delete</th>
                            </tr>
                        </thead>
                        <tbody v-if="manager_products&&manager_products.length">
                            <tr v-for="product in manager_products" :key="product.id" class="border-b border-slate-400 font-medium text-base">
                                <td class="whitespace-nowrap px-6 py-4">{{ product.name }}</td>
                                <td class="whitespace-nowrap px-6 py-4">{{ product.category }}</td>
                                <td v-if="product.inventory>=50" class="whitespace-nowrap px-6 py-4 text-green-500">{{ product.inventory }} {{ product.unit }}</td>
                                <td v-else-if="product.inventory>=25" class="whitespace-nowrap px-6 py-4 text-orange-500">{{ product.inventory }} {{ product.unit }}</td>
                                <td v-else class="whitespace-nowrap px-6 py-4 text-red-500">{{ product.inventory }} {{ product.unit }}</td>
                                <td class="whitespace-nowrap px-6 py-4">$ {{ product.price }}</td>
                                <td class="whitespace-nowrap px-6 py-4">{{ product.discount }} %</td>
                                <td class="whitespace-nowrap px-6 py-4">
                                    <RouterLink :to="{name: 'manager_update_product',params: {id: product.id}}" class="p-2 bg-green-500 rounded-md shadow-md hover:text-white">Update</RouterLink>
                                </td>
                                <td class="whitespace-nowrap px-6 py-4">
                                    <span @click="onDelete($event,product.id)" class="p-2 bg-red-500 rounded-md shadow-md hover:text-white cursor-pointer">Delete</span>
                                </td>
                            </tr>
                        </tbody>
                        <div v-else class="absolute flex flex-col w-full justify-center mt-[15vh]">
                            <img class="w-20 h-auto mx-auto opacity-70" src="../../../assets/empy-box.png" alt="empty box">
                            <h1 class="text-xl text-center my-0.5 w-full font-medium text-slate-500 opacity-80">No products found...</h1>
                        </div>
                    </table>
                </div>
            </div>
        </div>
    </div>
    <DeleteProduct v-if="toggleModal" @afterDelete="onAfterDelete" @cancel="onCancel" :toggleModal="toggleModal" :product_id="product_id"/>
</template>
<script>
    import { mapGetters } from 'vuex'
    export default {
        data(){
            return {
                toggleModal: false,
                product_id: null
            }
        },
        computed: {
            ...mapGetters(['manager_products'])
        },
        methods: {
            onDelete(e,id){
                this.toggleModal =!this.togglModal,
                this.product_id=id
            },
            onCancel(value){
                this.toggleModal =value
            },
            onAfterDelete(value){
                this.toggleModal = value
            },
            onTyping(e){
                let search_content=e.target.value
                this.$store.commit('product_search',search_content)
            }
        },
        async created(){
            this.$store.dispatch('get_manager_products')
        },
        components: {
            DeleteProduct: require('../manager/DeleteProduct.vue').default
        }
    }
</script>