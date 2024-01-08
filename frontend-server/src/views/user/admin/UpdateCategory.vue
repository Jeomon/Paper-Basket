<template>
    <div class="bg-slate-200 w-full min-h-[90vh] relative top-[10vh]">
        <div class="absolute top-[10vh] left-0 right-0 mx-auto w-full max-w-3xl py-6 px-6 bg-slate-100 shadow-md rounded-md">
            <h1 class="text-4xl mt-2 mb-4 px-3 text-slate-700">Update Category</h1>
            <form @submit.prevent="submit" class="w-full" method="post" enctype="multipart/form-data">
                <div class="flex flex-wrap">
                    <div class="w-full md:w-2/6 px-3 mb-6">
                        <div class="flex flex-row space-x-1">
                            <label for="old_name" class="uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Old Name</label>
                            <svg class="w-4 h-4 text-slate-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                                <path fill-rule="evenodd" d="M12 1.5a5.25 5.25 0 00-5.25 5.25v3a3 3 0 00-3 3v6.75a3 3 0 003 3h10.5a3 3 0 003-3v-6.75a3 3 0 00-3-3v-3c0-2.9-2.35-5.25-5.25-5.25zm3.75 8.25v-3a3.75 3.75 0 10-7.5 0v3h7.5z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <input id="old_name" :value="form.old_name" type="text" disabled class="bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                    </div>
                    <div class="w-full md:w-3/6 px-3 mb-6">
                        <label for="new_name" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">New Name</label>
                        <input id="new_name" type="text" v-model="form.new_name" class="bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.new_name.$error" class="text-red-500 font-medium">{{ v$.form.new_name.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-2/6 px-3 mb-6">
                        <label for="consumable" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Consumable</label>
                        <select id="consumable" v-model="form.consumable" class="cursor-pointer bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                            <option value="null" selected disabled>Select an option</option>
                            <option value="yes">Yes</option>
                            <option value="no">No</option>
                            <option value="depends">Depends</option>
                            <option value="n/a">N/A</option>
                        </select>
                    </div>
                    <div class="w-full md:w-2/6 px-3 mb-6">
                        <label for="vegetarian" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Vegetarian</label>
                        <select id="vegetarian" v-model="form.vegetarian" class="cursor-pointer bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                            <option value="null" selected disabled>Select an option</option>
                            <option value="yes">Yes</option>
                            <option value="no">No</option>
                            <option value="depends">Depends</option>
                            <option value="n/a">N/A</option>
                        </select>
                    </div>
                    <div class="w-full px-3">
                        <input type="submit" class="h-fit my-auto font-medium cursor-pointer bg-slate-500 text-slate-300 text-lg p-2 rounded-md" value="Update Category">
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
    import axios from 'axios'
    import { helpers,required } from '@vuelidate/validators'
    import { mapGetters } from 'vuex'
    import useVuelidate from '@vuelidate/core'
    export default {
        data() {
            return {
                v$: useVuelidate(),
                form: {
                    id:null,
                    old_name: null,
                    new_name: null,
                    consumable: null,
                    vegetarian: null
                },
                categoryUpdateError: null
            }
        },
        validations: {
            form: {
                new_name: {
                    required :helpers.withMessage("This field is required",required)
                }
            }
        },
        computed: {
            ...mapGetters(['message'])
        },
        async created(){
            let id=this.$route.params.id
            const response=await axios.get(`category/${id}`)
            let category = response.data.category
            this.form={
                id: id,
                old_name: category.name,
                new_name: null,
                consumable: category.consumable,
                vegetarian: category.vegetarian
            }
        },
        methods: {
            async submit(){
                let data=this.form
                let id=this.$route.params.id
                let validate=await this.v$.$validate()
                if(validate){
                    this.$store.dispatch('update_category',{'data':data,'id':id})
                }
            }
        }
    }
</script>