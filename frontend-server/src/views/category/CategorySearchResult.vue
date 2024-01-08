<template>
    <div class="fixed left-0 top-[10vh] flex flex-col w-[40%] sm:w-[30%] lg:w-[20%] h-[90vh] bg-slate-100 overflow-y-auto">
        <div class="flex flex-col my-3 mx-6 font-medium text-slate-600">
            <div>
                <h1 class="border-b-2 py-1 border-slate-300 text-xl">Supplier</h1>
                <div v-if="categoryBasedProducts&&categoryBasedProducts.length">
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
                <div v-if="categoryBasedProducts&&categoryBasedProducts.length">
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
                <div v-if="categoryBasedProducts&&categoryBasedProducts.length">
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
                <div v-if="categoryBasedProducts&&categoryBasedProducts.length">
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
                <div v-if="categoryBasedProducts&&categoryBasedProducts.length">
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
                <div v-if="categoryBasedProducts&&categoryBasedProducts.length">
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
        <div class="bg-slate-300 w-full flex flex-row justify-between items-center p-2.5">
            <h1 class="text-lg text-slate-500 font-semibold">{{ categoryBasedProducts?categoryBasedProducts.length: "No"  }} results found in {{ query }}</h1>
        </div>
        <div class="container mx-auto px-5 sm:px-10 my-10 font-semibold">
            <div v-if="filterBasedData&&filterBasedData.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 justify-around gap-8">
                <Card v-for="product in filterBasedData" :key="product.id" :product="product"/>
            </div>
            <div v-else-if="categoryBasedProducts&&categoryBasedProducts.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 justify-around gap-8">
                <Card v-for="product in categoryBasedProducts" :key="product.id" :product="product"/>
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
                }
            }
        },
        computed: {
            ...mapGetters(['products']),
            query(){
                return this.$route.query.content
            },
            productSuppliers(){
                let suppliers=this.categoryBasedProducts.map(product=>product.supplier)
                return new Set(suppliers)
            },
            productOrigins(){
                let origins=this.categoryBasedProducts.map(product=>product.origin)
                return new Set(origins)
            },
            categoryBasedProducts(){
                if(this.query){
                    return this.products.filter(product=>{
                        let name=product.category.toLowerCase()
                        return name.includes(this.query.toLowerCase())
                    })
                }
                else{
                    this.$router.push({name: 'home'})
                    return []
                }
            },
            filterBasedData(){
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