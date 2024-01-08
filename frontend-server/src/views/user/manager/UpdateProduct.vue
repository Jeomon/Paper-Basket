<template>
    <div class="bg-slate-200 w-full min-h-[90vh] relative top-[10vh]">
        <div class="absolute top-[10vh] left-0 right-0 mx-auto w-full max-w-4xl py-6 px-6 bg-slate-100 shadow-md rounded-md">
            <h1 class="text-4xl mt-2 mb-4 px-3 text-slate-700">Update Product</h1>
            <form @submit.prevent="submit" class="w-full text-lg" method="post" enctype="multipart/form-data">
                <div class="flex flex-wrap">
                    <div class="w-full md:w-2/6 px-3 mb-6">
                        <div class="flex flex-row space-x-1">
                            <label class="uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Product Name</label>
                            <svg class="w-4 h-4 text-slate-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                                <path fill-rule="evenodd" d="M12 1.5a5.25 5.25 0 00-5.25 5.25v3a3 3 0 00-3 3v6.75a3 3 0 003 3h10.5a3 3 0 003-3v-6.75a3 3 0 00-3-3v-3c0-2.9-2.35-5.25-5.25-5.25zm3.75 8.25v-3a3.75 3.75 0 10-7.5 0v3h7.5z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <input type="text" name="name" :value="form.name" disabled class="bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10">
                    </div>
                    <div class="w-full md:w-1/2 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Product Image</label>
                        <input type="file" @change="imageLoader($event)" name="image" class="w-full text-slate-500 leading-tight focus:outline-none h-10">
                        <p v-if="v$.form.product_image.$error" class="text-red-500 font-medium">{{ v$.form.product_image.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-2/6 px-3 mb-6">
                        <div class="flex flex-row space-x-1">
                            <label class="uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Category</label>
                            <svg class="w-4 h-4 text-slate-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                                <path fill-rule="evenodd" d="M12 1.5a5.25 5.25 0 00-5.25 5.25v3a3 3 0 00-3 3v6.75a3 3 0 003 3h10.5a3 3 0 003-3v-6.75a3 3 0 00-3-3v-3c0-2.9-2.35-5.25-5.25-5.25zm3.75 8.25v-3a3.75 3.75 0 10-7.5 0v3h7.5z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <input type="text" name="category" :value="form.category" disabled class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                    </div>
                    <div class="w-full md:w-1/4 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Inventory</label>
                        <input v-model.number="form.inventory" type="text" name="inventory" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                        <p v-if="v$.form.inventory.$error" class="text-red-500 font-medium">{{ v$.form.inventory.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/4 px-3 mb-6">
                        <div class="flex flex-row space-x-1">
                            <label class="uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Unit</label>
                            <svg class="w-4 h-4 text-slate-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                                <path fill-rule="evenodd" d="M12 1.5a5.25 5.25 0 00-5.25 5.25v3a3 3 0 00-3 3v6.75a3 3 0 003 3h10.5a3 3 0 003-3v-6.75a3 3 0 00-3-3v-3c0-2.9-2.35-5.25-5.25-5.25zm3.75 8.25v-3a3.75 3.75 0 10-7.5 0v3h7.5z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <input type="text" name="unit" :value="form.unit" disabled class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                    </div>
                    <div class="w-full md:w-3/6 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Supplier</label>
                        <input v-model="form.supplier" type="text" name="supplier" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                        <p v-if="v$.form.supplier.$error" class="text-red-500 font-medium">{{ v$.form.supplier.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-2/6 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Origin</label>
                        <input v-model="form.origin" type="text" name="origin" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                        <p v-if="v$.form.origin.$error" class="text-red-500 font-medium">{{ v$.form.origin.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-2/6 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Expiry Date</label>
                        <input v-model="form.expiry_date" type="date" name="expiry_date" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                        <p v-if="v$.form.expiry_date.$error" class="text-red-500 font-medium">{{ v$.form.expiry_date.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/4 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Price($)</label>
                        <input v-model.number="form.price" type="text" name="price" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                        <p v-if="v$.form.price.$error" class="text-red-500 font-medium">{{ v$.form.price.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/4 px-3 mb-8">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Discount(%)</label>
                        <input v-model.number="form.discount" type="text" name="discount" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                        <p v-if="v$.form.discount.$error" class="text-red-500 font-medium">{{ v$.form.discount.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full px-3">
                        <input type="submit" class="h-fit my-auto font-medium cursor-pointer bg-slate-500 text-slate-300 text-lg p-2 rounded-md" value="Update Product">
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
    import axios from 'axios'
    import { helpers,required,numeric } from '@vuelidate/validators'
    import useVuelidate from '@vuelidate/core'
    export default {
        data(){
            return {
                v$:useVuelidate(),
                form: {
                    id: null,
                    name: null,
                    category: null,
                    product_image: {
                        type: null,
                        file: null,
                    },
                    supplier: null,
                    origin: null,
                    unit: null,
                    expiry_date: null,
                    inventory: null,
                    price: null,
                    discount: null,
                    description: null
                }
            }
        },
        async mounted(){
            let id=this.$route.params.id
            let response=await axios.get(`product/${id}`)
            let product = response.data.product
            this.form={
                id: product.id,
                name: product.name,
                category: product.category,
                supplier: product.supplier,
                product_image: {
                    type: null,
                    file: null
                },
                origin: product.origin,
                unit: product.unit,
                expiry_date: product.expiry_date,
                inventory: product.inventory,
                price: product.price,
                discount: product.discount,
                description: product.description
            }
        },
        validations: {
            form: {
                product_image: {
                    imageTypeCheck :helpers.withMessage("Invalid file type",value=>{
                        if(!value.file) return true
                        let image_types=['image/jpeg', 'image/png']
                        return image_types.includes(value.type)
                    })
                },
                inventory: {
                    required :helpers.withMessage("This field is required",required),
                    no_negative :helpers.withMessage("This field need positive numbers",value=>Number(value)>=0)
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
                }
            }
        },
        methods: {
            imageLoader(e){
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
                        file: null,
                    }
                }
            },
            async submit(){
                let data=this.form
                let id=this.$route.params.id
                let validate=await this.v$.$validate()
                if(validate){
                    this.$store.dispatch('update_product',{'data':data,'id':id})
                    this.$router.push({name: 'manager_product_section'})
                }
            }
        }
    }
</script>