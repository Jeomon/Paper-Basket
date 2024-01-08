<template>
    <div class="relative w-full bg-slate-200 min-h-[90vh] top-[10vh]">
        <div class="mx-6 flex flex-col">
            <div class="w-full p-3 bg-slate-100 mt-10 mb-6 shadow-md">
                <h1 class="text-center sm:text-left text-4xl text-slate-700">Purchase History</h1>
            </div>
            <div class="overflow-x-auto">
            <div class="inline-block min-w-full py-2 sm:px-6 lg:px-8">
                <div class="overflow-hidden">
                    <table class="w-[72vw] mx-auto text-sm font-light text-center">
                        <thead class="border-b-2 border-neutral-500 text-base">
                            <tr class="text-slate-600  uppercase">
                                <th scope="col" class="px-5 py-3">Purchased Date</th>
                                <th scope="col" class="px-5 py-3">Product Name</th>
                                <th scope="col" class="px-5 py-3">Category Name</th>
                                <th scope="col" class="px-5 py-3">Supplier Name</th>
                                <th scope="col" class="px-5 py-3">Qty.</th>
                                <th scope="col" class="px-5 py-3">Price</th>
                            </tr>
                        </thead>
                        <tbody v-if="orders&&orders.length">
                            <tr v-for="order in SortByLatestOrders" :key="order.id" class="border-b border-slate-400 font-medium text-base">
                                <td class="whitespace-nowrap px-5 py-4">{{ PurchaseDate(order.order_date) }}</td>
                                <td class="whitespace-nowrap px-5 py-4">{{ order.name }}</td>
                                <td class="whitespace-nowrap px-5 py-4">{{ order.category }}</td>
                                <td class="whitespace-nowrap px-5 py-4">{{ order.supplier }}</td>
                                <td class="whitespace-nowrap px-5 py-4">{{ order.quantity }} {{ order.unit }}</td>
                                <td class="whitespace-nowrap px-5 py-4">${{ (order.price).toFixed(2) }}</td>
                            </tr>
                        </tbody>
                        <div v-else class="absolute flex flex-col w-full justify-center mt-[15vh]">
                            <img class="w-20 h-auto mx-auto opacity-70" src="../../../assets/empy-box.png" alt="empty box">
                            <h1 class="text-xl text-center my-0.5 w-full font-medium text-slate-500 opacity-80">No categories found...</h1>
                        </div>
                    </table>
                </div>
            </div>
        </div>
        </div>
    </div>
</template>
<script>
    import { mapGetters } from 'vuex'
    import moment from 'moment'
    export default {
        async created(){
            this.$store.dispatch('get_orders')
        },
        computed: {
            ...mapGetters(['orders']),
            SortByLatestOrders(){
                return this.orders.reverse()
            }
        },
        methods: {
            PurchaseDate(date){
                let dateString=new Date(date).toISOString()
                let formatedDate= moment(dateString).format("DD/MM/YYYY")
                return formatedDate
            }
        }
    }
</script>