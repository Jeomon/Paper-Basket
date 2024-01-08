<template>
    <div class="fixed -z-10 top-[10vh] right-0 w-[70%] max-w-sm h-[90vh] bg-slate-300 shadow-lg overflow-y-auto">
        <div class="mx-5 mt-5 sm:mx-6">
            <h1 class="text-3xl font-medium uppercase border-b-2 py-0.5">My Basket</h1>
            <div v-if="user" class="flex flex-col mt-4">
                <!-- cart items ny iteration -->
                <div v-if="cart&&cart.length">
                    <div v-for="product in cart" :key="product.id" class="flex flex-row rounded-md bg-slate-200/60 my-2 p-2">
                        <div class="w-2/6">
                            <img class="w-full h-full rounded shadow-md" :src="'http://127.0.0.1:5000/product/static/'+product.product_image" alt="{{ product.name }}">
                        </div>
                        <div class="w-3/6">
                            <div class="mx-2">
                                <h1 class="text-xl font-semibold hover:text-slate-700">
                                    <a href="">{{ product.name }}</a>
                                </h1>
                                <p class="text-xg">Quantity: {{ product.quantity }} {{ product.unit }}</p>
                                <p class="text-xg">Price: ${{ (product.price*product.quantity).toFixed(2) }}</p>
                            </div>
                        </div>
                        <!-- delete product -->
                        <div class="w-1/6 relative">
                            <button @click="onRemove($event,product.id,product.name)" class="absolute rounded-full top-0 right-0 text-black hover:text-white hover:bg-red-600">
                                <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                    <path class="pointer-events-none" d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
                                </svg>                                                  
                            </button>
                        </div>
                    </div>
                    <div class="border-t-2 my-5">
                        <h1 class="text-2xl my-2 font-medium">Cost:</h1>
                        <div class="mx-auto">
                            <div class="flex flex-row justify-between my-1">
                                <h1 class="w-3/6 text-xl font-semibold">Product</h1>
                                <h1 class="w-2/6 text-center text-xl font-semibold">Qty.</h1>
                                <h1 class="w-1/6 text-center text-xl font-semibold">Price</h1>
                            </div>
                                <!-- products price section-->
                            <div v-for="product in cart" :key="product.id" class="flex flex-row justify-between my-1 text-xg">
                                <h1 class="w-3/6">{{ product.name }}</h1>
                                <h1 class="w-2/6 text-center">{{ product.quantity }} {{ product.unit }}</h1>                                
                                <h1 class="w-1/6 text-center">$ {{ (product.price*product.quantity).toFixed(2) }}</h1>
                            </div>
                            <div class="flex flex-row justify-between mt-2 py-1 border-t-2 font-medium text-xg">
                                <h1 class="w-4/6">Total cost :</h1>
                                <h1 class="w-2/6 text-right tracking-tighter">$ {{ (calculate.cost).toFixed(2) }}</h1>
                            </div>
                            <div class="flex flex-row justify-between py-1 font-medium text-xg">
                                <h1 class="w-4/6">Delivery charges :</h1>
                                <h1 class="w-2/6 text-right tracking-tighter">$0.0</h1>
                            </div>
                            <div class="flex flex-row justify-between py-1 font-medium text-xg">
                                <h1 class="w-4/6">Total discount :</h1>
                                <h1 class="w-2/6 text-right tracking-tighter text-red-500">-$ {{ (calculate.discount).toFixed(2) }}</h1>
                            </div>
                            <div class="flex flex-row justify-between mt-1 py-1 border-t-2 font-medium text-2xl">
                                <h1 class="w-4/6">Grand Total :</h1>
                                <h1 class="w-2/6 text-right tracking-tighter text-green-500">$ {{ (calculate.amount).toFixed(2) }}</h1>
                            </div>
                            <div class="flex flex-row justify-center mt-7 py-1 font-medium text-2xl">
                                <button @click="onOrder" class="text-center px-2 py-1 bg-amber-400 text-slate-600 rounded-lg">Buy Now</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class=" my-[25%]" v-else-if="afterpurchase">
                    <svg class="mx-auto w-28 h-28 text-green-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                        <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm13.36-1.814a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z" clip-rule="evenodd" />
                    </svg>
                    <h2 class="text-center mx-8 mt-1 text-xl font-semibold">Thank you for choosing <br>Paper Basket!</h2>
                    <p class="text-center my-5 mx-4 text-lg font-medium">We appreciate your purchase and look forward to serving you again soon.</p>
                </div>
                <div v-else class="text-center w-fit mx-auto mt-[20vh]">
                    <img class="w-16 h-16 mx-auto" src="../assets/empty.svg" alt="empty cart">
                    <h1 class="font-semibold text-lg text-slate-500">Basket is Empty.</h1>
                </div>
            </div>
            <div v-else class="text-center w-fit mx-auto mt-[20vh]">
                <svg class="w-16 h-16 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
                </svg>                  
                <h1 class="font-semibold text-lg text-slate-500">You have to login to purchase.</h1>
            </div>
        </div>
    </div>
</template>
<script>
    import { mapGetters } from 'vuex'
    export default {
        data(){
            return {
                afterpurchase: false,
                timer: null
            }
        },
        computed: {
            ...mapGetters(['cart','user']),
            calculate(){
                let calculate={ cost: 0,discount: 0,amount: 0 }
                if(this.cart.length){  
                    for(let product of this.cart){
                        calculate.cost+=(product.price*product.quantity)
                        calculate.discount+=(product.price*product.quantity*(product.discount/100).toFixed(2))
                        calculate.amount=calculate.cost-calculate.discount
                    }
                }
                return calculate
            }
        },
        methods:{
            async onRemove(e,id,name){
                this.$store.dispatch('delete_cart',id)
                let message=`${name} removed from cart`
                this.$store.commit('flash',{'show': true,color:'red','message':message})
            },
            async onOrder(){
                this.$store.dispatch('place_order')
                this.afterpurchase=true
                this.timer=setTimeout(()=>{
                    this.afterpurchase=false
                },4000)
            }
        },
        beforeDestroy(){
           clearTimeout(this.timer)
        }
    }
</script>
