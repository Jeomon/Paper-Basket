<template>
    <div v-if="product" class="absolute top-[10vh] grid grid-cols-7 grid-rows-6 w-full h-[90vh]">
        <div v-if="product.inventory" class="col-span-3 row-span-3 sm:row-span-4 px-1">
            <div class="flex flex-col items-center justify-center w-full h-full">
                <img class="rounded-md shadow-lg w-[90%] h-[70%] sm:w-[80%] sm:h-[80%] md:[70%] md:h-[80%] lg:w-[60%] lg:h-[80%]" :src="'http://127.0.0.1:5000/product/static/'+product.product_image" alt="dummy">
            </div>
        </div>
        <div v-else class="col-span-3 row-span-3 sm:row-span-4 px-1">
            <div class="flex flex-col items-center justify-center w-full h-full">
                <img class="rounded-md grayscale-[85%] shadow-lg w-[90%] h-[70%] sm:w-[80%] sm:h-[80%] md:[70%] md:h-[80%] lg:w-[60%] lg:h-[80%]" :src="'http://127.0.0.1:5000/product/static/'+product.product_image" alt="dummy">
            </div>
        </div>
        <div class="col-span-4 row-span-3 sm:row-span-4 px-1">
            <div class="flex flex-col justify-center w-full h-full">
                <p class="text-md font-medium"><RouterLink class="text-blue-400" :to="{name: 'home'}">Home</RouterLink> > <RouterLink class="text-blue-400" :to="{name: 'category_search', query: {content: product.category}}">{{ product.category }}</RouterLink> > <span class="text-blue-400">{{ product.name }}</span></p>
                <h1 class="text-3xl sm:text-4xl font-semibold">{{ product.name }}</h1>
                <p class="hidden text-sm md:my-1.5 md:block">Product ID: {{ product.id }}</p>
                <div class="flex flex-row space-x-3 items-center">
                    <p v-if="product.inventory" class="text-xl font-semibold text-green-500 w-fit">In Stock</p>
                    <p v-else class="text-xl font-semibold text-red-500 w-fit">Out of Stock</p>
                    <div class="flex flex-row items-center space-x-1">
                        <p><span>{{ product.rating }}</span>/5</p>
                        <svg class="w-5 h-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M10.868 2.884c-.321-.772-1.415-.772-1.736 0l-1.83 4.401-4.753.381c-.833.067-1.171 1.107-.536 1.651l3.62 3.102-1.106 4.637c-.194.813.691 1.456 1.405 1.02L10 15.591l4.069 2.485c.713.436 1.598-.207 1.404-1.02l-1.106-4.637 3.62-3.102c.635-.544.297-1.584-.536-1.65l-4.752-.382-1.831-4.401z" clip-rule="evenodd" />
                        </svg>
                    </div>
                </div>
                <h2 v-if="product.inventory" class="flex flex-row items-center text-2xl lg:text-3xl font-normal space-x-1">Price: $
                    <span>{{ (product.price*(form.quantity?form.quantity:1)*(1-(product.discount/100))).toFixed(2) }}</span>
                    <span class="text-red-700 line-through text-sm sm:text-lg font-medium decoration-2">{{ (product.price*(form.quantity?form.quantity:1)).toFixed(2) }}</span>
                </h2>
                <h2 v-else class="flex flex-row items-center text-2xl lg:text-3xl font-normal space-x-1">Price: $
                    <span>--</span>
                </h2>
                <p v-if="product.inventory" class="text-xl my-1">You Saved {{ product.discount }}%</p>
                <p v-else class="text-xl my-1">You Saved --%</p>
                <P class="text-normal  my-0.5">(Inclusive of all taxes)</P>
                <form v-if="product.inventory" @submit.prevent="submitOrder" class="flex flex-row space-x-2 lg:my-1 items-center">
                    <label for="qty">Qty.</label>
                    <select v-model="form.quantity" class="cursor-pointer outline-none rounded-md w-fit py-1 px-2 border-2 border-slate-500" name="qty">
                        <option value="null" disabled selected>Pick a qty</option>
                        <option v-for="qty in quantity_available" :value="qty">{{ qty }} {{ product.unit }}</option>
                    </select>
                    <button class="bg-amber-400 hover:text-white hover:bg-amber-500 w-fit text-slate-800 p-2 rounded flex flex-row items-center justify-center gap-1 md:gap-x-2 lg:text-xl" type="submit">
                        <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 00-16.536-1.84M7.5 14.25L5.106 5.272M6 20.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm12.75 0a.75.75 0 11-1.5 0 .75.75 0 011.5 0z" />
                        </svg>
                        <span>Add to Cart</span>
                    </button>
                </form>
                <div v-else class="flex flex-row space-x-2 lg:my-1 items-center">
                    <label for="qty">Qty.</label>
                    <select v-model="form.quantity" class="pointer-events-none outline-none rounded-md w-fit py-1 px-1 border-2 border-slate-500" name="qty">
                        <option value="null" disabled selected>Unavailable</option>
                    </select>
                    <button class="bg-red-500 pointer-events-none text-white w-fit p-2 rounded flex flex-row items-center justify-center gap-1 md:gap-x-2 lg:text-xl" type="submit">
                        <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 00-16.536-1.84M7.5 14.25L5.106 5.272M6 20.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm12.75 0a.75.75 0 11-1.5 0 .75.75 0 011.5 0z" />
                        </svg>
                        <span>------------</span>
                    </button>
                </div>
            </div>
        </div>
        <div class="col-span-7 row-span-3 sm:row-span-2 h-fit text-lg text-slate-500 font-normal">
            <div class="mt-4 bg-slate-100/80 rounded-md w-[95%] sm:w-[90%] mx-auto h-fit">
                <div class="px-16 pt-4 pb-8">
                    <h1 class="text-xl mt-6 mb-3 sm:text-3xl text-slate-600">Product Description</h1>
                    <p class="indent-6">{{ product.description }}</p>
                    <h1 class="text-xl mt-6 mb-3 sm:text-3xl text-slate-600">Supplier Info</h1>
                    <p>{{ product.supplier }}, {{ product.origin }}</p>
                </div>
            </div>
            <div class="mt-4 bg-slate-100/80 rounded-md w-[95%] sm:w-[90%] mx-auto h-fit">
                <div class="flex flex-col md:flex-row md:space-x-10 m-6 pt-4 pb-8 px-10">
                    <div class="w-full md:w-[30vw]">
                        <h1 class="text-xl mt-6 mb-2 sm:text-3xl text-slate-600">Overall rating</h1>
                        <div class="flex flex-row space-x-1 items-center">
                            <!-- stars -->
                            <svg class="w-6 h-6 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M10.868 2.884c-.321-.772-1.415-.772-1.736 0l-1.83 4.401-4.753.381c-.833.067-1.171 1.107-.536 1.651l3.62 3.102-1.106 4.637c-.194.813.691 1.456 1.405 1.02L10 15.591l4.069 2.485c.713.436 1.598-.207 1.404-1.02l-1.106-4.637 3.62-3.102c.635-.544.297-1.584-.536-1.65l-4.752-.382-1.831-4.401z" clip-rule="evenodd" />
                            </svg>            
                            <h2 class="text-lg font-medium px-2">{{ product.rating }}/5</h2>
                        </div>
                        <div class="flex flex-col my-2 space-y-3">
                            <h1 class="text-lg font-medium">{{ reviews?reviews.length:0  }} ratings</h1>
                            <!-- stars -->
                            <div v-for="[star,rating] of Object.entries(product.ratings)" class="flex flex-row items-center space-x-2">
                                <div class="flex flex-row space-x-1 items-center">
                                    <p class="font-medium text-lg tracking-wide">{{ star }}</p>
                                    <svg class="w-6 h-6 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                        <path fill-rule="evenodd" d="M10.868 2.884c-.321-.772-1.415-.772-1.736 0l-1.83 4.401-4.753.381c-.833.067-1.171 1.107-.536 1.651l3.62 3.102-1.106 4.637c-.194.813.691 1.456 1.405 1.02L10 15.591l4.069 2.485c.713.436 1.598-.207 1.404-1.02l-1.106-4.637 3.62-3.102c.635-.544.297-1.584-.536-1.65l-4.752-.382-1.831-4.401z" clip-rule="evenodd" />
                                    </svg>
                                </div>
                                <div class="h-2 w-52 bg-slate-200 rounded-e-md rounded-s-md overflow-hidden">
                                    <div :style="{width: `${reviews&&reviews.length?(rating/reviews.length)*2:0}%`}" class="h-full bg-amber-300 rounded-e-md"></div>    
                                </div>
                                <p>{{ rating }}</p>
                            </div>
                        </div>
                    </div>
                    <form @submit.prevent="submitReview" class="md:w-full">
                        <h1 class="text-xl mt-6 mb-3 sm:text-3xl text-slate-600">Write a review <span class="text-sm font-medium">(sign in required)</span></h1>
                        <input v-model="review.title" type="text" class="bg-slate-200/60 outline-none p-1.5 w-full rounded-md" placeholder="Give your review a title."/>
                        <p v-if="v$.review.title.$error" class="text-red-500 font-medium">{{ v$.review.title.$errors[0].$message }}</p>
                        <textarea v-model="review.content" class="bg-slate-200/60 outline-none p-1.5 mt-3 w-full rounded-md resize-none" placeholder="We are eager to hear from you.." cols="60" rows="6"></textarea>
                        <p v-if="v$.review.content.$error" class="text-red-500 font-medium">{{ v$.review.content.$errors[0].$message }}</p>
                        <div class="flex flex-row space-x-1 items-center mt-2">
                            <h2 class="text-xl my-1">Rate this product </h2>
                            <!-- rating -->
                            <div @mouseleave="resetRating" ref="ratingSection" class="flex flex-row space-x-1 items-center">
                                <div v-for="star in 5">
                                    <input v-model="review.rating" @change="ratingChange(star)" class="hidden" type="radio" :id="star" :value="star" required>
                                    <label @mouseover="starHover(star)" class="w-fit h-fit cursor-pointer" :for="star">
                                        <svg :rel="star" class="w-8 h-8 text-slate-200" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                            <path fill-rule="evenodd" d="M10.868 2.884c-.321-.772-1.415-.772-1.736 0l-1.83 4.401-4.753.381c-.833.067-1.171 1.107-.536 1.651l3.62 3.102-1.106 4.637c-.194.813.691 1.456 1.405 1.02L10 15.591l4.069 2.485c.713.436 1.598-.207 1.404-1.02l-1.106-4.637 3.62-3.102c.635-.544.297-1.584-.536-1.65l-4.752-.382-1.831-4.401z" clip-rule="evenodd" />
                                        </svg>
                                    </label>
                                </div>
                            </div>
                        </div>
                        <button type="submit" class="cursor-pointer my-3 block text-slate-300 p-2.5 bg-slate-500 hover:text-slate-200 rounded-md font-medium">
                            Post My Review
                        </button>
                    </form>
                </div>
            </div>
            <div class="w-[95%] sm:w-[90%] bg-slate-100/80 h-auto mx-auto rounded-md mb-10">
                <div class="pt-8 pb-5 px-16">
                    <h1 class="text-xl my-4 sm:text-3xl text-slate-600">Reviews</h1>
                    <div v-if="reviews&&reviews.length">
                        <div v-for="review in reviews" :key="review.user_id" class="w-[90%] my-8 py-5 px-8 mx-auto rounded-md bg-slate-200/50">
                            <div class="flex flex-row space-x-2 items-center">
                                <img class="w-14 h-14 rounded-full" :src="'http://127.0.0.1:5000/user/static/'+review.image">
                                <div class="flex flex-col">
                                    <h3 class="text-xl font-medium">{{ review.name }}</h3>
                                    <p class="text-sm font-medium">Posted {{ dateFromNow(review.posted_on) }}</p>
                                    <div class="flex flex-row space-x-1">
                                        <svg v-for="_ in review.rating" class="w-5 h-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                            <path fill-rule="evenodd" d="M10.868 2.884c-.321-.772-1.415-.772-1.736 0l-1.83 4.401-4.753.381c-.833.067-1.171 1.107-.536 1.651l3.62 3.102-1.106 4.637c-.194.813.691 1.456 1.405 1.02L10 15.591l4.069 2.485c.713.436 1.598-.207 1.404-1.02l-1.106-4.637 3.62-3.102c.635-.544.297-1.584-.536-1.65l-4.752-.382-1.831-4.401z" clip-rule="evenodd" />
                                        </svg>
                                    </div>
                                </div>
                                <span @click="onDelete" v-if="user&&user.id==review.user_id" class="p-1 cursor-pointer text-red-500 border-red-500 border-2 hover:border-white hover:bg-red-400 hover:text-white rounded-full">
                                    <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                                    </svg>                                      
                                </span>
                            </div>
                            <div class="mt-3">
                                <div>
                                    <h2 class="text-xl font-medium">{{ review.title }}</h2>
                                    <p class="mt-1 text-justify">{{ review.content }}</p>
                                </div>
                                <div class="flex flex-row gap-x-4 mt-3 mb-1 items-center text-slate-400">
                                    <span class="flex flex-row items-center gap-x-1.5">
                                        <svg @click="sentiment(review.user_id,product.id,'like',review.likes,review.dislikes)" class="w-6 h-6 cursor-pointer" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                                            <path d="M7.493 18.75c-.425 0-.82-.236-.975-.632A7.48 7.48 0 016 15.375c0-1.75.599-3.358 1.602-4.634.151-.192.373-.309.6-.397.473-.183.89-.514 1.212-.924a9.042 9.042 0 012.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 00.322-1.672V3a.75.75 0 01.75-.75 2.25 2.25 0 012.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 01-2.649 7.521c-.388.482-.987.729-1.605.729H14.23c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 00-1.423-.23h-.777zM2.331 10.977a11.969 11.969 0 00-.831 4.398 12 12 0 00.52 3.507c.26.85 1.084 1.368 1.973 1.368H4.9c.445 0 .72-.498.523-.898a8.963 8.963 0 01-.924-3.977c0-1.708.476-3.305 1.302-4.666.245-.403-.028-.959-.5-.959H4.25c-.832 0-1.612.453-1.918 1.227z" />
                                        </svg>
                                        <p class="font-medium text-slate-500">{{ review.likes }}</p>
                                    </span>
                                    <span class="flex flex-row items-center gap-x-1.5">
                                        <svg @click="sentiment(review.user_id,product.id,'dislike',review.likes,review.dislikes)" class="w-6 h-6 cursor-pointer" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                                            <path d="M15.73 5.25h1.035A7.465 7.465 0 0118 9.375a7.465 7.465 0 01-1.235 4.125h-.148c-.806 0-1.534.446-2.031 1.08a9.04 9.04 0 01-2.861 2.4c-.723.384-1.35.956-1.653 1.715a4.498 4.498 0 00-.322 1.672V21a.75.75 0 01-.75.75 2.25 2.25 0 01-2.25-2.25c0-1.152.26-2.243.723-3.218C7.74 15.724 7.366 15 6.748 15H3.622c-1.026 0-1.945-.694-2.054-1.715A12.134 12.134 0 011.5 12c0-2.848.992-5.464 2.649-7.521.388-.482.987-.729 1.605-.729H9.77a4.5 4.5 0 011.423.23l3.114 1.04a4.5 4.5 0 001.423.23zM21.669 13.773c.536-1.362.831-2.845.831-4.398 0-1.22-.182-2.398-.52-3.507-.26-.85-1.084-1.368-1.973-1.368H19.1c-.445 0-.72.498-.523.898.591 1.2.924 2.55.924 3.977a8.959 8.959 0 01-1.302 4.666c-.245.403.028.959.5.959h1.053c.832 0 1.612-.453 1.918-1.227z" />
                                        </svg>
                                        <p class="font-medium text-slate-500">{{ review.dislikes }}</p>
                                    </span>
                                    <span class="flex flex-row items-center gap-x-1 cursor-pointer">
                                        <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                                            <path fill-rule="evenodd" d="M3 2.25a.75.75 0 01.75.75v.54l1.838-.46a9.75 9.75 0 016.725.738l.108.054a8.25 8.25 0 005.58.652l3.109-.732a.75.75 0 01.917.81 47.784 47.784 0 00.005 10.337.75.75 0 01-.574.812l-3.114.733a9.75 9.75 0 01-6.594-.77l-.108-.054a8.25 8.25 0 00-5.69-.625l-2.202.55V21a.75.75 0 01-1.5 0V3A.75.75 0 013 2.25z" clip-rule="evenodd" />
                                        </svg>
                                        <p class="font-medium text-slate-500">Report</p>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-else class="w-[90%] mx-auto h-[30vh] my-8 bg-slate-300/30 rounded-lg border-dashed border-4 border-slate-300 sm:col-span-3 md:col-span-4 lg:col-span-5 flex flex-col justify-center items-center">
                        <h1 class="text-2xl sm:text-3xl text-slate-500">No reviews found..</h1>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import auth from '@/auth'
    import { mapGetters } from 'vuex'
    import { helpers,required } from '@vuelidate/validators'
    import useVuelidate from '@vuelidate/core'
    import moment from 'moment'

    export default {
        data(){
            return {
                form: {
                    id: this.$route.params.id,
                    quantity: null,
               },
               v$: useVuelidate(),
               review: {
                    id: this.$route.params.id,
                    title: null,
                    content: null,
                    rating: null,
               },
               ratingChecked:false,
               ratingValue:0,
               like:false,
               dislike:false,
               likeCount:0,
               dislikeCount:0,
               review_user_id:null,
               review_user_status:[]
            }
        },
        validations: {
            review: {
                title: {
                    required :helpers.withMessage("This field is required",required)
                },
                content: {
                    required :helpers.withMessage("This field is required",required)
                },
                rating: {
                    required :helpers.withMessage("This field is required",required)
                },
            }
        },
        computed: {
            ...mapGetters(['product','reviews','user']),
            quantity_available(){
                if(this.product.inventory<5){
                    return this.product.inventory
                }
                else{
                    return 5
                }
            }
        },
        created(){
            let id=this.$route.params.id
            this.$store.dispatch('get_product',id)
            if(auth.isAuthenticated()&&!this.user){
                this.$store.dispatch('get_user')
            }
        },
        watch: {
            '$route.params.id':function(id){
                this.$store.dispatch('get_product',id)
            }
        },
        methods: {
            dateFromNow(date){
                let dateString=new Date(date).toISOString()
                return moment(dateString,'YYYY-MM-DD HH:mm:ss').fromNow(false)
            },
            sentiment(user_id,product_id,sentiment,likes,dislikes){
                if(this.review_user_id!=user_id){
                    this.review_user_id=user_id
                    this.likeCount=likes
                    this.dislikeCount=dislikes
                    this.like=false
                    this.dislike=false
                }
                if(this.review_user_id==user_id){
                    switch(sentiment){
                        case 'like':{
                            if(this.like==false&&this.dislike==false){
                                this.like=true
                                this.likeCount+=1
                                console.log('Like',this.likeCount,'Dislike',this.dislikeCount);
                            }
                            else if(this.like==false&&this.dislike==true){
                                this.likeCount+=1
                                this.dislikeCount-=1
                                this.like=true
                                this.dislike=false
                                console.log('Like',this.likeCount,'Dislike',this.dislikeCount);
                            }
                            else{
                                console.log('Like',this.likeCount,'Dislike',this.dislikeCount);
                            }
                            break
                        }
                        case 'dislike':{
                            if(this.dislike==false&&this.like==false){
                                this.dislike=true
                                this.dislikeCount+=1
                                console.log('Like',this.likeCount,'Dislike',this.dislikeCount);
                            }
                            else if(this.dislike==false&&this.like==true){
                                this.dislikeCount+=1
                                this.likeCount-=1
                                this.dislike=true
                                this.like=false
                                console.log('Like',this.likeCount,'Dislike',this.dislikeCount);
                            }
                            else{
                                console.log('Like',this.likeCount,'Dislike',this.dislikeCount);
                            }
                            break
                        }
                    }
                }
                let data={'user_id':user_id,'product_id':product_id,'like_count':this.likeCount,'dislike_count':this.dislikeCount}
                this.$store.dispatch('sentiment',data)
            },
            ratingChange(rating){
                this.ratingValue=rating
                this.ratingChecked=true
            },
            starHover(rating){
                let ratingSection=this.$refs.ratingSection
                let light_clss='text-yellow-400'
                let dark_clss='text-slate-200'
                for(let star of ratingSection.children){
                    let star_no=star.children[1].children[0].getAttribute("rel")
                    if(star_no<=rating&&star.children[1].children[0].classList.contains(dark_clss)){
                        star.children[1].children[0].classList.replace(dark_clss,light_clss)
                    }
                    if(star_no>rating&&star.children[1].children[0].classList.contains(light_clss)){
                        star.children[1].children[0].classList.replace(light_clss,dark_clss)
                    }
                }
            },
            resetRating(){
                let ratingSection=this.$refs.ratingSection
                let light_clss='text-yellow-400'
                let dark_clss='text-slate-200'
                for(let star of ratingSection.children){
                    if(star.children[1].children[0].classList.contains(light_clss)){
                        star.children[1].children[0].classList.replace(light_clss,dark_clss)
                    }
                }
                if(this.ratingChecked){
                    let rating=this.ratingValue
                    for(let star of ratingSection.children){
                        let star_no=star.children[1].children[0].getAttribute("rel")
                        if(star_no<=rating&&star.children[1].children[0].classList.contains(dark_clss)){
                            star.children[1].children[0].classList.replace(dark_clss,light_clss)
                        }
                        if(star_no>rating&&star.children[1].children[0].classList.contains(light_clss)){
                            star.children[1].children[0].classList.replace(light_clss,dark_clss)
                        }
                    }
                }
            },
            async submitOrder(){    
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
            },
            async submitReview(){
                let data=this.review
                let id=this.$route.params.id
                let validate=await this.v$.$validate()
                let role='customer'
                let user=this.user
                if(!auth.getToken()){
                    let message="Sign in required to post the review"
                    this.$store.commit('flash',{'show': true,color:'red','message':message})
                    return null
                }
                if(user.role.toLowerCase()!=role){
                    let message='User with wrong role'
                    this.$store.commit('flash',{'show': true,color:'red','message':message})
                    return null
                }
                if(validate){
                    this.$store.dispatch('add_review',{data,id})
                }
            },
            async onDelete(){
                let id=this.$route.params.id
                this.$store.dispatch('delete_review',id)
            }
        }
    }
</script>