<template>
    <div class="bg-slate-300/50 w-full h-88 rounded-lg overflow-hidden shadow-md">
        <div class="relative">
            <RouterLink v-if="product.inventory" :to="{name: 'product',params: {id: product.id}}">
                <!-- discount -->
                <span v-if="product.discount" class="absolute top-2.5 left-2.5 p-2 inline-block bg-slate-700/80 rounded-full text-sm text-green-500 tracking-tight">{{ product.discount }}% off</span>
                <!-- product image -->
                <img class="w-full h-48 object-cover" :src="'http://127.0.0.1:5000/product/static/'+product.product_image" alt="product image">
                <div class="absolute bottom-0 left-0 py-1 px-1.5 bg-white/70 flex flex-row justify-evenly items-center w-full">
                    <!-- product title -->
                    <h1 class="w-full text-xl text-black product-name">{{ product.name }}</h1>
                    <div class="flex flex-row items-center space-x-1 text-sm">
                        <!-- rating -->
                        <p><span class="text-green-600">{{ product.rating }}</span>/5</p>
                        <svg class="w-5 h-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M10.868 2.884c-.321-.772-1.415-.772-1.736 0l-1.83 4.401-4.753.381c-.833.067-1.171 1.107-.536 1.651l3.62 3.102-1.106 4.637c-.194.813.691 1.456 1.405 1.02L10 15.591l4.069 2.485c.713.436 1.598-.207 1.404-1.02l-1.106-4.637 3.62-3.102c.635-.544.297-1.584-.536-1.65l-4.752-.382-1.831-4.401z" clip-rule="evenodd" />
                        </svg>                                      
                    </div>
                </div>  
            </RouterLink>
            <RouterLink v-else :to="{name: 'product',params: {id: product.id}}">
                <span class="absolute top-2.5 left-2.5 p-2 inline-block bg-slate-700/80 rounded-full text-sm text-green-500 tracking-tight">--% off</span>
                <img class="w-full h-48 object-cover grayscale-[85%]" :src="'http://127.0.0.1:5000/product/static/'+product.product_image" alt="product image">
                <div class="absolute bottom-0 left-0 py-1 px-1.5 bg-white/70 flex flex-row justify-evenly items-center w-full">
                    <h1 class="w-full text-xl text-black product-name">{{ product.name }}</h1>
                    <div class="flex flex-row items-center space-x-1 text-sm">
                        <p><span class="text-green-600">{{ product.rating }}</span>/5</p>
                        <svg class="w-5 h-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M10.868 2.884c-.321-.772-1.415-.772-1.736 0l-1.83 4.401-4.753.381c-.833.067-1.171 1.107-.536 1.651l3.62 3.102-1.106 4.637c-.194.813.691 1.456 1.405 1.02L10 15.591l4.069 2.485c.713.436 1.598-.207 1.404-1.02l-1.106-4.637 3.62-3.102c.635-.544.297-1.584-.536-1.65l-4.752-.382-1.831-4.401z" clip-rule="evenodd" />
                        </svg>                                      
                    </div>
                </div> 
            </RouterLink>
        </div>
        <div v-if="product.inventory" class="flex flex-col mx-2 my-3">
            <div class="flex flex-row justify-around items-center space-x-1">
                <!-- price -->
                <div class="flex flex-row space-x-1 items-center">
                    <h2 class="flex flex-row items-center space-x-0.5 text-green-500 font-semibold text-2xl">
                        <span class="text-xl">$</span>
                        <span>{{ (product.price*(form.quantity?form.quantity:1)*(1-(product.discount/100))).toFixed(2) }}</span>
                    </h2>
                    <span class="text-red-700 line-through text-lg actual-price font-medium decoration-2">{{ (product.price*(form.quantity?form.quantity:1)).toFixed(2) }}</span>
                </div>
                <!-- in stock/out of stock -->
                <p class="p-1 text-green-500 bg-slate-200 rounded-md">in stock</p>
            </div>
            <!-- quantity selector -->
            <form @submit.prevent="submit" class="flex flex-col justify-center items-center m-2.5 gap-y-4">
                <div class="flex flex-row justify-center space-x-2">
                    <label for="qty">Qty.</label>
                    <select v-model="form.quantity" class="cursor-pointer w-fit py-1 px-2 rounded-md outline-none">
                        <option value="0" disabled selected>Pick a qty</option>
                        <option v-for="qty in quantity_available" :key="qty" :value="qty">{{ qty }} {{ product.unit }}</option>
                    </select>
                </div>
                <!-- add to cart -->
                <button class="bg-amber-400 w-fit text-base text-slate-700 p-2 hover:text-white hover:bg-amber-500 rounded flex flex-row items-center justify-center gap-x-2 shadow-sm" type="submit">
                    <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 00-16.536-1.84M7.5 14.25L5.106 5.272M6 20.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm12.75 0a.75.75 0 11-1.5 0 .75.75 0 011.5 0z" />
                    </svg>
                    Add to Cart
                </button>
            </form>
        </div>
        <div v-else class="flex flex-col mx-4 my-3 pointer-events-none">
            <div class="flex flex-row justify-between items-center">
                <div class="flex flex-row space-x-1 items-center">
                    <h2 class="flex flex-row items-center space-x-0.5 text-red-500 font-semibold text-2xl">
                        <span class="text-xl">$</span>
                        <span>--</span>
                    </h2>
                </div>
                <p class="p-1 text-red-500 bg-slate-200 rounded-md">out of stock</p>
            </div>
            <!-- quantity selector -->
            <div class="flex flex-col justify-center items-center m-2.5 gap-y-4">
                <div class="flex flex-row justify-center space-x-2">
                    <label for="qty">Qty.</label>
                    <select disabled v-model="form.quantity" class="w-fit py-1 px-2 rounded-md outline-none" name="qty">
                        <option value="0" selected>Not Available</option>
                    </select>
                </div>
                <!-- add to cart -->
                <button disabled class="bg-red-500 w-fit text-base p-2 text-white rounded flex flex-row items-center justify-center gap-x-2 shadow-sm" type="submit">
                    <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 00-16.536-1.84M7.5 14.25L5.106 5.272M6 20.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm12.75 0a.75.75 0 11-1.5 0 .75.75 0 011.5 0z" />
                    </svg>
                    ------------
                </button>
            </div>
        </div>
    </div>
</template>
<script>
    import auth from '@/auth'
    import { mapGetters } from 'vuex'
    export default {
        data(){
            return {
               form: {
                id: this.product.id,
                quantity: 0,
               }
            }
        },
        props: {
            product: {
                type: Object,
                required: true
            }
        },
        computed: {
            ...mapGetters(['user']),
            quantity_available(){
                if(this.product.inventory<5){
                    return this.product.inventory
                }
                else{
                    return 5
                }
            }
        },
        methods: {
            async submit(){
                let role='customer'
                let user=this.user
                if(!auth.getToken()){
                    let message='Sign in required'
                    this.$router.push({name: 'customer_signin'})
                    this.$store.commit('flash',{'show': true,color:'red','message':message})
                    return null
                }
                if(user.role.toLowerCase()!=role){
                    let message='User with invalid role'
                    this.$store.commit('flash',{'show': true,color:'red','message':message})
                    return null
                }
                if(!this.form.quantity){
                    let message="Oops! 🛒 Forgot to set the quantity!"
                    this.$store.commit('flash',{'show': true,color:'red','message':message})
                    return null
                }
                let data=this.form
                this.$store.dispatch('add_cart',data)
                let message=`${this.product.name} added to cart`
                this.$store.commit('flash',{'show': true,color:'green','message':message})
                this.form.quantity=0
            }
        }
    }
</script>