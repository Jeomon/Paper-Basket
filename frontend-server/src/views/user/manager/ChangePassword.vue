<template>
    <div class="bg-slate-200 w-full min-h-[90vh] relative top-[10vh]">
        <div class="absolute top-[10vh] left-0 right-0 w-full max-w-sm py-6 px-6 bg-slate-100 mx-auto shadow-md rounded-md">
            <h1 class="text-3xl sm:text-4xl mt-2 mb-4 px-1 text-slate-700">Change Password</h1>
            <form @submit.prevent="submit" class="w-full text-lg" method="post" action="/">
                <div class="flex flex-col">
                    <div class="w-full px-3 mb-6">
                        <label class="uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Current Password</label>
                        <input v-model="form.current_password" type="password" class="bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.current_password.$error" class="text-red-500 font-medium">{{ v$.form.current_password.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full px-3 mb-6">
                        <label class="uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">New Password</label>
                        <input v-model="form.new_password" type="password" class="bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.new_password.$error" class="text-red-500 font-medium">{{ v$.form.new_password.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full px-3 mb-6">
                        <label class="uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Confirm Password</label>
                        <input v-model="form.confirm_password" type="password" class="bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.confirm_password.$error" class="text-red-500 font-medium">{{ v$.form.confirm_password.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full px-3">
                        <input type="submit" class="h-fit my-auto font-medium cursor-pointer bg-slate-500 text-slate-300 text-lg p-2 rounded-md"/>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
    import { helpers,required } from '@vuelidate/validators'
    import useVuelidate from '@vuelidate/core'
    export default {
        data(){
            return {
                v$: useVuelidate(),
                form: {
                    current_password: null,
                    new_password: null,
                    confirm_password: null
                }
            }
        },
        validations: {
            form: {
                current_password: {
                    required :helpers.withMessage("This field is required",required)
                },
                new_password: {
                        required :helpers.withMessage("This field is required",required)
                },
                confirm_password: {
                        required :helpers.withMessage("This field is required",required)
                }
            }
        },
        methods: {
            async submit(){
                let data=this.form
                let validate=await this.v$.$validate()
                if(validate){
                    this.$store.dispatch('update_password_user',data)
                }
            }
        }
    }
</script>