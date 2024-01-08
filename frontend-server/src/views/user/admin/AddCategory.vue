<template>
    <div class="bg-slate-200 w-full min-h-[90vh] relative top-[10vh]">
        <div class="absolute top-[10vh] left-0 right-0 mx-auto w-full max-w-4xl py-6 px-6 bg-slate-100 shadow-md rounded-md">
            <h1 class="text-4xl mt-2 mb-4 px-3 text-slate-700">Add Category</h1>
            <form class="w-full" @submit.prevent="submit">
                <div class="flex flex-wrap">
                    <div class="w-full md:w-1/3 px-3 mb-6">
                        <label for="name" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Name</label>
                        <input v-model="form.name" type="text" class="bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10" />
                        <p v-if="v$.form.name.$error" class="text-red-500 font-medium">{{ v$.form.name.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/3 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Consumable</label>
                        <select v-model="form.consumable" class="cursor-pointer bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                            <option value="null" selected disabled>Select an option</option>
                            <option value="yes">Yes</option>
                            <option value="no">No</option>
                            <option value="depends">Depends</option>
                            <option value="n/a">N/A</option>
                        </select>
                        <p v-if="v$.form.consumable.$error" class="text-red-500 font-medium">{{ v$.form.consumable.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/3 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Vegetarian</label>
                        <select v-model="form.vegetarian" class="cursor-pointer bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                            <option value="null" selected disabled>Select an option</option>
                            <option value="yes">Yes</option>
                            <option value="no">No</option>
                            <option value="depends">Depends</option>
                            <option value="n/a">N/A</option>
                        </select>
                        <p v-if="v$.form.vegetarian.$error" class="text-red-500 font-medium">{{ v$.form.vegetarian.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full px-3">
                        <input type="submit" class="h-fit my-auto font-medium cursor-pointer bg-slate-500 text-slate-300 text-lg p-2 rounded-md" value="Add Category">
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
    import { helpers,required } from '@vuelidate/validators'
    import useVuelidate from '@vuelidate/core'
    import { mapGetters } from 'vuex'
    export default {
        data() {
            return {
                v$: useVuelidate(),
                form: {
                    name: null,
                    consumable: null,
                    vegetarian: null
                }
            }
        },
        validations: {
            form: {
                name: {
                    required :helpers.withMessage("This field is required",required)
                },
                consumable: {
                    required :helpers.withMessage("This field is required",required)
                },
                vegetarian: {
                    required :helpers.withMessage("This field is required",required)
                }
            }
        },        
        methods: {
            async submit(){
                let data=this.form
                let validate=await this.v$.$validate()
                if(validate){
                    this.$store.dispatch('add_category',data)
                    this.$router.push({name: 'admin_category_section'})
                }
            }
        }
    }
</script>
