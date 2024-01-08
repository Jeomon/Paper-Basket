<template>
    <div class="bg-slate-200 w-full h-[100vh] relative">
        <div class="absolute top-[20%] left-0 right-0 w-full max-w-sm py-4 px-6 bg-slate-100 mx-auto shadow-md rounded-md">
            <h1 class="text-4xl mt-2 mb-4 text-slate-700">Reset Password</h1>
            <form @submit.prevent="submit" class="w-full max-w-lg">
                <div class="flex flex-wrap">
                    <div class="w-full mb-6">
                        <label for="password" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">New Password</label>
                        <input type="password" v-model="form.password" id="email" class="font-medium bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.password.$error" class="text-red-500 font-medium">{{ v$.form.password.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full mb-4">
                        <label for="password" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Confirm Password</label>
                        <input type="password" v-model="form.confirm_password" id="password" class="font-medium bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.confirm_password.$error" class="text-red-500 font-medium">{{ v$.form.confirm_password.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full">
                        <input type="submit" value="Reset Password" class="h-fit my-auto cursor-pointer bg-slate-500 font-medium text-slate-300 text-lg p-2 rounded-md">
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
                    password: null,
                    confirm_password: null,
                    auth_token:this.$route.params.auth_token,
                    verify_token:this.$route.params.verify_token,
                    hostname: window.location.hostname,
                    port: window.location.port
                }
            }
        },
        validations: {
            form: {
                password: {
                    required :helpers.withMessage("This field is required",required)
                },
                confirm_password: {
                    required :helpers.withMessage("This field is required",required)
                }
            }
        },
        methods: {
            async submit(){
                const data= this.form
                let validate=await this.v$.$validate()
                if(validate){
                    this.$store.dispatch('user_forgot_password',data)
                }
            }
        }
    }
</script>