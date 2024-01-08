<template>
    <div class="bg-slate-200 relative top-[10vh] w-full min-h-[90vh]">
        <div class="mx-auto max-w-4xl p-6 bg-slate-100 shadow-md rounded-md">
            <h1 class="text-4xl mt-2 mb-4 px-3 text-slate-700">Add Product</h1>
            <form @submit.prevent="submit" class="w-full">
                <div class="flex flex-wrap">
                    <div class="w-full md:w-1/2 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Product Name</label>
                        <input type="text" v-model="form.name" class="bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10">
                        <p v-if="v$.form.name.$error" class="text-red-500 font-medium">{{ v$.form.name.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/2 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Product Image</label>
                        <input type="file" @change="imageLoader($event)" class="w-full text-slate-500 leading-tight focus:outline-none h-10">
                        <p v-if="v$.form.product_image.$error" class="text-red-500 font-medium">{{ v$.form.product_image.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/3 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Category</label>
                        <select v-model="form.category" class="cursor-pointer bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                            <option value="null" selected disabled>Select a category</option>
                            <option v-for="category in categories" :value="category.name">{{category.name}}</option>
                        </select>
                        <p v-if="v$.form.category.$error" class="text-red-500 font-medium">{{ v$.form.category.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/3 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Inventory</label>
                        <input type="text" v-model.number="form.inventory" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                        <p v-if="v$.form.inventory.$error" class="text-red-500 font-medium">{{ v$.form.inventory.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/3 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Unit</label>
                        <select v-model="form.unit" class="cursor-pointer bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                            <option value="null" selected disabled>Select the unit</option>
                            <option value="g">g</option>
                            <option value="Kg">Kg</option>
                            <option value="mL">mL</option>
                            <option value="L">L</option>
                            <option value="Pc">Pc</option>
                            <option value="Pkt">Pkt</option>
                            <option value="Can">Can</option>
                            <option value="Btl">Btl</option>
                        </select>
                        <p v-if="v$.form.unit.$error" class="text-red-500 font-medium">{{ v$.form.unit.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-3/6 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Supplier</label>
                        <input type="text" v-model="form.supplier" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                        <p v-if="v$.form.supplier.$error" class="text-red-500 font-medium">{{ v$.form.supplier.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-3/6 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Origin</label>
                        <input type="text" v-model="form.origin" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                        <p v-if="v$.form.origin.$error" class="text-red-500 font-medium">{{ v$.form.origin.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-2/4 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Expiry Date</label>
                        <input type="date" v-model="form.expiry_date" class="cursor-pointer bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                        <p v-if="v$.form.expiry_date.$error" class="text-red-500 font-medium">{{ v$.form.expiry_date.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/4 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Price($)</label>
                        <input type="text" v-model.number="form.price" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                        <p v-if="v$.form.price.$error" class="text-red-500 font-medium">{{ v$.form.price.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/4 px-3 mb-8">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Discount(%)</label>
                        <input type="text" v-model.number="form.discount" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                        <p v-if="v$.form.discount.$error" class="text-red-500 font-medium">{{ v$.form.discount.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Description</label>
                        <textarea v-model="form.description" placeholder="Enter product description here..." class="resize-none h-[30vh] bg-slate-200 p-2 w-full text-slate-500 leading-tight focus:outline-none"></textarea>
                        <p v-if="v$.form.description.$error" class="text-red-500 font-medium">{{ v$.form.description.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/4 px-3">
                        <button type="submit" class="h-fit my-auto font-medium cursor-pointer bg-slate-500 text-slate-300 text-lg p-2 rounded-md">Add Product</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
    import { mapGetters } from 'vuex'
    import { helpers,required,numeric } from '@vuelidate/validators'
    import useVuelidate from '@vuelidate/core'
    export default {
        data(){
            return {
                v$: useVuelidate(),
                form: {
                    name: null,
                    product_image: {
                        type: null,
                        file: null,
                    },
                    category: null,
                    inventory: null,
                    unit: null,
                    supplier: null,
                    origin: null,
                    expiry_date: null,
                    price: null,
                    discount: null,
                    description: null
                }
            }
        },
        validations: {
            form: {
                name: {
                    required :helpers.withMessage("This field is required",required)
                },
                product_image: {
                    required :helpers.withMessage("Image is missing",value=>!!(value.file)),
                    imageTypeCheck :helpers.withMessage("Invalid file type",value=>{
                    if(!value.file) return true
                        let image_types=['image/jpeg', 'image/png']
                        return image_types.includes(value.type)
                    })
                },
                category: {
                    required :helpers.withMessage("This field is required",required)
                },
                inventory: {
                    required :helpers.withMessage("This field is required",required),
                    no_negative :helpers.withMessage("This field need positive numbers",value=>Number(value)>=0)
                },
                unit: {
                    required :helpers.withMessage("This field is required",required)
                },
                supplier: {
                    required :helpers.withMessage("This field is required",required)
                },
                origin: {
                    required :helpers.withMessage("This field is required",required)
                },
                expiry_date: {
                    required :helpers.withMessage("This field is required",required),
                    date :helpers.withMessage("Wrong expiry date",value=>((new Date(value).getTime())-(new Date().getTime()))>0)
                },
                price: {
                    required :helpers.withMessage("This field is required",required),
                    numeric :helpers.withMessage("This field need numbers",numeric),
                    priceLimit :helpers.withMessage('Price (Max. $1000)',value=>Number(value)<1000)
                },
                discount: {
                    numeric :helpers.withMessage("This field need numbers",numeric),
                    discountLimit :helpers.withMessage("Discount (Max. 30%)",value=>Number(value)<=30)
                },
                description: {
                    required :helpers.withMessage("This field is required",required)
                }
            }
        },
        computed: {
            ...mapGetters(['categories','message'])
        },
        methods: {
            async imageLoader(e){
                if(e.target.files.length){
                    let reader=new FileReader()
                    reader.readAsDataURL(e.target.files[0])
                    reader.onload=()=>{
                        let type=reader.result.split(';').at(0).split(':').at(1)
                        let file=reader.result.split(',').at(1)
                        this.form.product_image.type=type
                        this.form.product_image.file=file
                    }
                    reader.onerror=()=>{
                        console.log("Error in the image encoding process to base64")
                    }
                }
                else{
                    this.form.product_image={
                        type: null,
                        file: null
                    }
                }
            },
            async submit(){
                let data=this.form
                let validate=await this.v$.$validate()
                if(validate){
                    this.$store.dispatch('add_manager_product',data)
                    this.$router.push({name: 'manager_product_section'})
                }
            }
        }
    }
</script>