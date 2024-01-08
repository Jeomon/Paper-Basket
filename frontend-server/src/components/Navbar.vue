<template>
    <nav class="fixed top-0 z-10 flex flex-row justify-around items-center bg-slate-800 w-[100vw] h-[10vh]">
        <RouterLink class="flex flex-row space-x-2 items-center" :to="{name: 'home'}">
            <img class="w-11 h-11" src="../assets/logo.svg" alt="Paper Basket">
            <h1 class="hidden md:block text-slate-400 flex-auto my-auto text-xl font-semibold leading-6">Paper<br>Basket</h1>
        </RouterLink>
        <div class="flex flex-col items-center">
            <div class="flex flex-row">
                <div>
                    <span @click="onCategoryMenu" class="cursor-pointer">
                        <svg class="py-2 flex-none rounded-l-sm bg-slate-600/40 hover:text-slate-200 hover:bg-slate-600/70 w-10 h-12" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd" />
                        </svg>                      
                    </span>
                    <div :class="[{'hidden':!toggleCategoryMenu},'absolute','-mt-[0.25vh]']">
                        <div class="h-auto px-2 bg-slate-800 rounded-b-md pb-2">
                            <div v-if="categories&&categories.length" class="text-lg font-medium flex flex-nowrap flex-col mt-3 text-slate-500 text-left min-w-[12vw] px-2">
                                <p class="py-0.5 px-2 w-fit my-1 rounded-md mx-auto cursor-default bg-slate-700 text-center text-slate-400 block">Categories</p>
                                <RouterLink @click="e=>{toggleCategoryMenu=false}" v-for="category in categories" :key="category.id" :to="{name: 'category_search', query: {content: category.name}}" class="py-0.5 hover:text-slate-300 block">{{category.name }}</RouterLink>
                            </div>
                            <div v-else class="text-lg font-medium flex flex-nowrap flex-col mt-3 text-slate-500 text-left min-w-[12vw] px-2">
                                <span class="py-0.5 block">No categories found</span>
                            </div>
                        </div>
                    </div>
                </div>
                <form @submit.prevent="onSearch" class="flex flex-row my-auto items-center">
                    <input v-model="content" @keyup="onTyping" class="w-[55vw] sm:w-[45vw] md:w-[40vw] lg:max-w-lg placeholder:text-slate-400 placeholder:font-medium font-medium flex-1 px-2 py-3 outline-none" type="search" placeholder="Find your groceries here..." id="search">
                    <button class="flex-none" type="submit">
                        <svg class="p-2 rounded-r-sm bg-slate-600/40 hover:bg-slate-600/70 hover:text-slate-200 w-10 h-12" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clip-rule="evenodd" />
                        </svg>                          
                    </button>
                </form>
            </div>
            <div :class="[{'hidden':!showSearchPanel},'mt-[6.5vh]','absolute']">
                <div v-if="searchPanelContent&&searchPanelContent.length" class="py-2 w-[55vw] sm:w-[45vw] md:w-[40vw] bg-white lg:max-w-lg mx-auto rounded-b-md shadow-md border-t-2 border-slate-600">
                    <div v-for="product in searchPanelContent" class="mx-2 my-1 text-lg font-medium rounded-md">
                        <RouterLink @click="e=>{content=null;searchPanelContent=null;showSearchPanel=false}" :to="{name: 'product', params: { id: product.id }}" class="flex flex-row items-center hover:bg-slate-200 p-2 space-x-2">
                            <p class="block">{{ product.name }}</p>
                            <p v-if="product.discount" class="text-green-400 text-base">{{ product.discount }}% off</p>
                        </RouterLink>
                    </div>
                </div>
                <div v-else class="py-2 bg-white w-[55vw] sm:w-[45vw] md:w-[40vw] lg:max-w-lg mx-auto rounded-b-md shadow-md border-t-2 border-slate-600">
                    <div class="mx-2 my-1 text-lg font-medium">
                        <span class="block">No results found</span>
                    </div>
                </div>
            </div>
        </div>
        <!-- other nav buttons -->
        <div v-if="!user" class="hidden h-12 text-slate-400 font-medium text-xl md:flex sm:flex-row space-x-[2.5vw] items-center">
            <div class="relative">
                <p @click="onSignIn" class="hover:text-slate-200 cursor-pointer">Sign In</p>
                <div :class="[{'hidden':!toggleSignIn},'absolute','text-lg','top-10','-left-3','bg-slate-800','text-slate-500','font-medium','p-2','flex','flex-col','w-fit','mx-auto','rounded-b-md']">
                    <RouterLink @click="e=>{toggleSignIn=false}" class="hover:text-slate-200" :to="{name: 'manager_signin'}">Manager</RouterLink>
                    <RouterLink @click="e=>{toggleSignIn=false}" class="hover:text-slate-200" :to="{name: 'customer_signin'}">Customer</RouterLink>
                </div>
            </div>
            <div class="relative">
                <p @click="onSignUp" class="hover:text-slate-200 cursor-pointer">Sign Up</p>
                <div :class="[{'hidden':!toggleSignUp},'absolute','text-lg','top-10','-left-3','bg-slate-800','text-slate-500','font-medium','p-2','flex','flex-col','w-fit','mx-auto','rounded-b-md']">
                    <RouterLink @click="e=>{toggleSignUp=false}" class="hover:text-slate-200" :to="{name: 'manager_signup'}">Manager</RouterLink>
                    <RouterLink @click="e=>{toggleSignUp=false}" class="hover:text-slate-200" :to="{name: 'customer_signup'}">Customer</RouterLink>
                </div>
            </div>
            <div class="flex flex-row items-center">
                <div class="relative text-slate-400">
                    <!-- cart -->
                    <svg @click="onCartMenu" class="hover:text-slate-200 w-8 h-8 cursor-pointer" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 00-16.536-1.84M7.5 14.25L5.106 5.272M6 20.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm12.75 0a.75.75 0 11-1.5 0 .75.75 0 011.5 0z" />
                    </svg>
                </div>
                <Cart :class="{'hidden':!toggleCartMenu}"/>
            </div>
        </div>
        <div v-else class="hidden relative sm:flex flex-col">
            <div class="flex flex-row space-x-5">
                <div @click="onUserMenu" class="cursor-pointer flex flex-row items-center space-x-3 py-2 px-2 rounded-xl hover:bg-slate-700 " tabindex="0" href="#">
                    <img class="flex-none w-10 h-10 rounded-full" :src="'http://127.0.0.1:5000/user/static/'+user.profile_image" alt="profile_image">
                    <h3 class="text-slate-400 hover:text-slate-200 flex-1 hidden md:block text-xl font-semibold">{{ user.first_name }}</h3>
                </div>
                <div class="flex flex-row items-center">
                    <div class="relative text-slate-400">
                        <!-- cart -->
                        <p v-if="cart&&cart.length" class="shadow-md cursor-pointer font-medium absolute -top-0.5 -right-1.5 bg-red-600 text-xs text-white px-1.5 rounded-full">{{ cart.length }}</p>
                        <svg @click="onCartMenu" class="hover:text-slate-200 w-8 h-8 cursor-pointer" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 00-16.536-1.84M7.5 14.25L5.106 5.272M6 20.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm12.75 0a.75.75 0 11-1.5 0 .75.75 0 011.5 0z" />
                        </svg>
                    </div>
                    <Cart :class="{'hidden':!toggleCartMenu}"/>
                </div>
            </div>
            <!-- dropdown -->
            <div :class="['text-lg','text-center',{'hidden':!toggleUserMenu},'absolute','pt-3','top-[9vh]','-right-[3vw]','md:right-[2vw]','bg-slate-800','text-slate-500','font-medium','w-48','h-auto','py-3','rounded-b-lg','justify-center','flex-col','space-y-2']">
                <h3 class="py-1 px-2 w-fit mx-auto rounded-md text-lg text-slate-300 bg-slate-700">{{`${user.first_name} ${user.last_name}`}}</h3>
                <div class="mt-2">
                    <RouterLink @click="e=>{toggleUserMenu=false}" class="block hover:text-slate-200" :to="{name: `${user.role.toLowerCase()}_update_profile`}">My Dashboard</RouterLink>                        
                    <RouterLink @click="e=>{toggleUserMenu=false}" class="block hover:text-slate-200" :to="{name: `${user.role.toLowerCase()}_change_password`}">Change Password</RouterLink>                        
                </div>
                <div class="mt-2 flex flex-row space-x-1 items-center justify-center hover:text-slate-200">
                    <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
                    </svg>
                    <RouterLink @click="e=>{toggleUserMenu=false}" class="block" :to="{name: `${user.role.toLowerCase()}_signout`}">Sign Out</RouterLink>
                </div>
            </div>
        </div>
        <div :class="['cursor-pointer', 'relative', {'sm:hidden':user},'md:hidden', 'sm:static']">
            <svg @click="onBreadcrumbMenu" class="p-2 w-11 h-12 rounded-md bg-slate-600/40 hover:bg-slate-600/70 hover:text-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10zm0 5.25a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75a.75.75 0 01-.75-.75z" clip-rule="evenodd" />
            </svg>
            <div :class="[{'hidden':!toggleBreadcrumbMenu},'md:hidden','absolute','-right-[3vw]','top-12']">
                <!-- dropdown -->
                <div class="w-[32vw] h-auto bg-slate-800 rounded-b-md pb-2">
                    <div v-if="!user" class="text-slate-500 text-lg font-medium flex flex-col justify-center items-center py-1 my-2.5">
                        <div class="flex flex-col items-center">
                            <span class="m-0.5 bg-slate-700 text-center text-slate-400 py-0.5 px-5 rounded-md">Customer</span>
                            <RouterLink class="py-0.5 hover:text-slate-200" :to="{name: 'customer_signin'}">Sign In</RouterLink>
                            <RouterLink class="py-0.5 hover:text-slate-200" :to="{name: 'customer_signup'}">Sign Up</RouterLink>
                        </div>
                        <div class="flex flex-col items-center">
                            <span class="m-0.5 bg-slate-700 text-center text-slate-400 py-0.5 px-5 rounded-md">Manager</span>
                            <RouterLink class="py-0.5 hover:text-slate-200" :to="{name: 'manager_signin'}">Sign In</RouterLink>
                            <RouterLink class="py-0.5 hover:text-slate-200" :to="{name: 'manager_signup'}">Sign Up</RouterLink>
                        </div>
                    </div>
                    <div v-else class="text-lg flex flex-col justify-center font-medium items-center my-2.5 text-slate-500">
                        <h3 class="py-1 px-1.5 rounded-md text-lg bg-slate-700">{{`${user.first_name} ${user.last_name}`}}</h3>
                        <RouterLink class="py-0.5 hover:text-slate-200" :to="{name: `${user.role.toLowerCase()}_update_profile`}">My Dashboard</RouterLink>
                        <RouterLink class="py-0.5 hover:text-slate-200" :to="{name: `${user.role.toLowerCase()}_change_password`}">Change Password</RouterLink>
                        <div class="mt-2 flex flex-row space-x-1 items-center justify-center hover:text-slate-200">
                            <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
                            </svg>
                            <RouterLink @click="e=>{toggleUserMenu=false}" class="block" :to="{name: `${user.role.toLowerCase()}_signout`}">Sign Out</RouterLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </nav>
</template>
<script>
    import { mapGetters } from 'vuex'
    import Cart from '../components/Cart.vue'
    import ProductSearchResult from '@/views/product/ProductSearchResult.vue'
    export default {
        data(){
            return {
                content:null,
                showSearchPanel:false,
                toggleBreadcrumbMenu: false,
                toggleUserMenu: false,
                toggleCategoryMenu: false,
                toggleCartMenu: false,
                toggleSignIn: false,
                toggleSignUp: false,
                searchPanelContent: null
                }
        },
        computed: {
            ...mapGetters(['user','cart','categories','products'])
        },
        async mounted(){
            if(this.categories){
                this.$store.dispatch('get_categories')
            }
            if(this.products){
                this.$store.dispatch('get_products')
            }
        },
        methods: {
            onTyping(e){
                let query=e.target.value
                if(query!=""&&query.match(/^[a-zA-Z ]+/)){
                    this.showSearchPanel=true
                    this.searchPanelContent=this.products.filter(product=>{
                        let name=product.name.toLowerCase()
                        return name.includes(query.toLowerCase())
                    })
                    let size=this.searchPanelContent.length<3?this.searchPanelContent.length:3
                    this.searchPanelContent=this.searchPanelContent.slice(0,size)
                }
                else{
                    this.showSearchPanel=false
                }
                if(!this.searchPanelContent){
                    this.showSearchPanel=false
                }
            },
            onSearch(){
                if(this.content){
                    this.$router.push({name: 'product_search', query: {content: this.content}})
                }
                this.showSearchPanel=false
                this.content=null
                this.searchPanelContent=null
            },
            onBreadcrumbMenu(){
                this.toggleBreadcrumbMenu =!this.toggleBreadcrumbMenu
            },
            async onCategoryMenu(){
                this.toggleCategoryMenu =!this.toggleCategoryMenu
            },
            onUserMenu(){
                this.toggleUserMenu =!this.toggleUserMenu
            },
            async onCartMenu(){
                this.toggleCartMenu=!this.toggleCartMenu
            },
            onSignIn(){
                this.toggleSignIn =!this.toggleSignIn
            },
            onSignUp(){
                this.toggleSignUp =!this.toggleSignUp
            }
        },
        components: {
            Cart,ProductSearchResult
        }
    }
</script>