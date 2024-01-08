<template>
    <div class="fixed left-0 top-[10vh] flex flex-col w-[40%] sm:w-[30%] lg:w-[20%] h-[90vh] bg-slate-100 overflow-y-auto">
        <div class="flex flex-col my-3 mx-6 font-medium text-slate-600">
            <div>
                <h1 class="border-b-2 py-1 border-slate-300 text-xl">Supplier</h1>
                <div v-if="productBasedData&&productBasedData.length">
                    <div v-for="supplier in productSuppliers" class="flex flex-row my-2 space-x-1">
                        <input :id="supplier" v-model="queryParams.suppliers" type="checkbox" name="supplier" :value="supplier"/>
                        <label :for="supplier" class="text-base">{{ supplier }}</label>
                    </div>
                </div>
                <div v-else>
                    <span>Not Available</span>
                </div>
            </div>
            <div>
                <h1 class="border-b-2 py-1 border-slate-300 text-xl">Country of Origin</h1>
                <div v-if="productBasedData&&productBasedData.length">
                    <div v-for="origin in productOrigins" class="flex flex-row my-2 space-x-1">
                        <input :id="origin" v-model="queryParams.origins" type="checkbox" name="origin" :value="origin"/>
                        <label :for="origin" class="text-base">{{ origin }}</label>
                    </div>
                </div>
                <div v-else>
                    <span>Not Available</span>
                </div>
            </div>
            <div>
                <h1 class="border-b-2 py-1 border-slate-300 text-xl">Food Preference</h1>
                <div v-if="productBasedData&&productBasedData.length">
                    <div class="flex flex-row my-2 space-x-1">
                        <input type="checkbox" id="Vegetarian" name="preference" :value="true"/>
                        <label for="Vegetarian" class="text-base">Vegetarian</label>
                    </div>
                    <div class="flex flex-row my-2 space-x-1">
                        <input type="checkbox" id="Non Vegetarian" name="preference" :value="true"/>
                        <label for="Non Vegetarian" class="text-base">Non Vegetarian</label>
                    </div>
                </div>
                <div v-else>
                    <span>Not Available</span>
                </div>
            </div>
            <div>
                <h1 class="border-b-2 py-1 border-slate-300 text-xl">Availability</h1>
                <div v-if="productBasedData&&productBasedData.length">
                    <div class="flex flex-row my-2 space-x-1">
                        <input type="checkbox" name="availability" value="In stock"/>
                        <label class="text-base">In stock</label>
                    </div>
                    <div class="flex flex-row my-2 space-x-1">
                        <input type="checkbox" name="availability" value="Out of stock"/>
                        <label class="text-base">Out of stock</label>
                    </div>
                </div>
                <div v-else>
                    <span>Not Available</span>
                </div>
            </div>
            <div>
                <h1 class="border-b-2 py-1 border-slate-300 text-xl">Price</h1>
                <div v-if="productBasedData&&productBasedData.length">
                    <div class="flex flex-row my-2 space-x-1">
                        <input type="checkbox" name="price" value="123"/>
                        <p class="text-base">$0.50 - $2.00</p>
                    </div>
                    <div class="flex flex-row my-2 space-x-1">
                        <input type="checkbox" name="price" value="123"/>
                        <p class="text-base">$2.00 - $5.00</p>
                    </div>
                    <div class="flex flex-row my-2 space-x-1">
                        <input type="checkbox" name="price" value="123"/>
                        <p class="text-base">$5.00 - $10.00</p>
                    </div>
                    <div class="flex flex-row my-2 space-x-1">
                        <input type="checkbox" name="price" value="123"/>
                        <p class="text-base">$10.00 - $20.00</p>
                    </div>
                    <div class="flex flex-row my-2 space-x-1">
                        <input type="checkbox" name="price" value="123"/>
                        <p class="text-base">$20.00 - $50.00</p>
                    </div>
                    <div class="flex flex-row my-2 space-x-1">
                        <input type="checkbox" name="price" value="123"/>
                        <p class="text-base">$50.00 - $100.00</p>
                    </div>
                </div>
                <div v-else>
                    <span>Not Available</span>
                </div>
            </div>
            <div>
                <h1 class="border-b-2 py-1 border-slate-300 text-xl">Discount</h1>
                <div v-if="productBasedData&&productBasedData.length">
                    <div class="flex flex-row my-2 space-x-1">
                        <input type="checkbox" name="discount" value="1"/>
                        <p class="text-base">5%-15%</p>
                    </div>
                    <div class="flex flex-row my-2 space-x-1">
                        <input type="checkbox" name="discount" value="1"/>
                        <p class="text-base">15%-30%</p>
                    </div>
                    <div class="flex flex-row my-2 space-x-1">
                        <input type="checkbox" name="discount" value="1"/>
                        <p class="text-base">30%-50%</p>
                    </div>
                    <div class="flex flex-row my-2 space-x-1">
                        <input type="checkbox" name="discount" value="1"/>
                        <p class="text-base">50% and above</p>
                    </div>
                </div>
                <div v-else>
                    <span>Not Available</span>
                </div>
            </div>
        </div>
    </div>
    <div class="absolute top-[10vh] right-0 -z-10 w-[60%] sm:w-[70%] lg:w-[80%] min-h-[90vh] bg-slate-200">
        <div class="bg-slate-100 w-full flex flex-row flex-wrap items-center p-2.5 gap-x-4">
            <h1 class="text-lg text-slate-500 font-semibold">{{ productBasedData?productBasedData.length: "No"  }} results found for "{{ query }}"</h1>
            <p v-if="productBasedData.length" v-for="(ribbon,index) of ribbonData" :key="index" @click="ribbonHandler(index)" :ref="`ribbon_${index}`" class="bg-slate-200 px-2 py-1.5 my-1 text-center hover:bg-white cursor-pointer shadow-sm rounded-3xl font-medium text-base text-slate-600">{{ ribbon }}</p>
        </div>
        <div class="container mx-auto px-5 sm:px-10 my-10 font-semibold">
            <div v-if="ribbonBasedData&&ribbonBasedData.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 justify-around gap-8">
                <Card v-for="product in ribbonBasedData" :key="product.id" :product="product"/>
            </div>
            <div v-else-if="filterBasedData&&filterBasedData.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 justify-around gap-8">
                <Card v-for="product in filterBasedData" :key="product.id" :product="product"/>
            </div>
            <div v-else-if="productBasedData&&productBasedData.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 justify-around gap-8">
                <Card v-for="product in productBasedData" :key="product.id" :product="product"/>
            </div>
            <div v-else class="mx-6 mt-[20%]">
                <p class="text-center text-2xl text-slate-500">No results found for {{ query }}</p>
            </div>
        </div>
    </div>
</template>
<script>
    import { mapGetters } from 'vuex'
    import Card from '@/components/Card.vue'
    export default {
        data(){
            return {
                queryParams: {
                    suppliers: [],
                    origins: [],
                },
                ribbonBtnTracker:undefined,
                ribbonBtnName:undefined
            }
        },
        computed: {
            ...mapGetters(['products']),
            query(){
                return this.$route.query.content
            },
            productSuppliers(){
                let suppliers=this.productBasedData.map(product=>product.supplier)
                return new Set(suppliers)
            },
            productOrigins(){
                let origins=this.productBasedData.map(product=>product.origin)
                return new Set(origins)
            },
            productBasedData(){
                let products=this.products
                if(this.query){
                    return products.filter(product=>{
                        let name=product.name.toLowerCase()
                        return name.includes(this.query.toLowerCase())
                    })
                }
                else{
                    this.$router.push({name: 'home'})
                    return []
                }
            },
            ribbonData(){
                let categories=this.productBasedData.map(product=>product.category)
                let origins=this.productBasedData.map(product=>product.origin)
                let ribbon=['Discount','Rating','Price',...new Set(categories),...new Set(origins)]
                return ribbon.length>11?ribbon.slice(0,12):ribbon
            },
            filterBasedData(){
                if(this.ribbonBtnTracker){
                    this.ribbonBtnTracker=undefined
                    this.ribbonBtnName=undefined
                }
                let products=this.productBasedData
                let suppliers=this.queryParams.suppliers
                let origins=this.queryParams.origins
                let filteredData=[]
                if(products){
                    products.map(product=>{
                        let supplierMatch=!suppliers.length||suppliers.includes(product.supplier)
                        let originMatch=!origins.length||origins.includes(product.origin)
                        if(supplierMatch&&originMatch){
                            filteredData.push(product)
                        }
                    })
                }
                return filteredData
            },
            ribbonBasedData(){
                let ribbonData=[]
                let originSelected=this.queryParams.origins.length
                let supplierSelected=this.queryParams.suppliers.length
                if(originSelected||supplierSelected){
                    return ribbonData
                }
                switch(this.ribbonBtnTracker){
                    case 0: {
                        ribbonData=this.productBasedData.toSorted((a,b)=>b.discount-a.discount)
                        break
                    }
                    case 1: {
                        ribbonData=this.productBasedData.toSorted((a,b)=>b.rating-a.rating)
                        break
                    }
                    case 2: {
                        ribbonData=this.productBasedData.toSorted((a,b)=>b.price-a.price)
                        break
                    }
                    default: {
                        let btnName=this.ribbonBtnName
                        this.products.map(product=>{
                            if(product.origin==btnName||product.category==btnName){
                                ribbonData.push(product)
                            }
                        })
                    }
                }
                return ribbonData
            }

        },
        methods: {
            ribbonHandler(index){
                this.ribbonBtnTracker=index>11?undefined:index
                let ribbonName=this.$refs[`ribbon_${index}`][0].textContent
                this.ribbonBtnName=index>11?undefined:ribbonName
            }
        },
        beforeCreate(){
            this.$store.dispatch('get_products')
        },
        components: {
            Card
        }
    }
</script>