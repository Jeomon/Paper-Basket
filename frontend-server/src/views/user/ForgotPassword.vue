<template>
    <div class="bg-slate-200 w-full h-[100vh] relative">
        <div class="absolute top-[20%] left-0 right-0 w-full max-w-sm py-4 px-6 bg-slate-100 mx-auto shadow-md rounded-md">
            <h1 class="text-4xl mt-2 mb-4 text-slate-700">Forgot Password</h1>
            <p class=" bg-slate-200 p-3 rounded-md text-base mt-6 mb-4 font-medium w-full text-slate-500 leading-6">Enter your E-mail here and we'll send you a reset password mail.</p>
            <form @submit.prevent="submit" novalidate class="w-full max-w-md my-2">
                <div class="flex flex-wrap">
                    <div class="w-full mb-6">
                        <label for="email" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Email</label>
                        <input type="email" v-model="form.email" id="email" class="font-medium bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.email.$error" class="text-red-500 font-medium">{{ v$.form.email.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full">
                        <input type="submit" value="Reset Password" class="h-fit my-auto cursor-pointer bg-slate-500 font-medium text-slate-300 text-lg p-2 rounded-md">
                        <p class="my-2.5 text-slate-600 text-base font-medium">Back to  <RouterLink class="text-blue-400" :to="{name: `${role}_signin`}">Sign In</RouterLink></p>
                    </div>
                </div>
           </form>
        </div>
    </div>
</template>
<script>
    import { helpers,required,email } from '@vuelidate/validators'
    import useVuelidate from '@vuelidate/core'
    export default {
        data(){
            return {
                v$: useVuelidate(),
                role:this.$route.path.split('/')[2],
                form: {
                    email: null,
                    hostname: window.location.hostname,
                    port: window.location.port
                }
            }
        },
        validations: {
            form: {
                email: {
                    required :helpers.withMessage("This field is required",required),
                    email: helpers.withMessage("invalid email",email)
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