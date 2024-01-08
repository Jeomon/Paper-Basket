<template>
    <div class="bg-slate-200 w-full h-[100vh] relative">
        <div class="absolute top-[20%] left-0 right-0 w-full max-w-sm py-4 px-6 bg-slate-100 mx-auto shadow-md rounded-md">
            <h1 class="text-4xl mt-2 mb-4 text-slate-700">Sign In<span class="text-base font-medium"> (Customer)</span></h1>
            <form @submit.prevent="submit" class="w-full max-w-lg">
                <div class="flex flex-wrap">
                    <div class="w-full mb-6">
                        <label for="email" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Email</label>
                        <input type="email" v-model="form.email" id="email" class="font-medium bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.email.$error" class="text-red-500 font-medium">{{ v$.form.email.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full mb-4">
                        <label for="password" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Password</label>
                        <input type="password" v-model="form.password" id="password" class="font-medium bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.password.$error" class="text-red-500 font-medium">{{ v$.form.password.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full">
                        <div class="flex flex-row items-center gap-x-3">
                            <input type="submit" value="Sign In" class="h-fit my-auto cursor-pointer bg-slate-500 font-medium text-slate-300 text-lg p-2 rounded-md">
                            <RouterLink class="text-base font-medium text-blue-400" :to="{name: 'customer_forgot_password',query:{next: undefined}}">Forgot Password?</RouterLink>
                        </div>
                        <p class="my-2.5 text-slate-600 text-base font-medium">Don't have an account? 
                            <RouterLink class="text-blue-400" :to="{name: 'customer_signup'}">Sign Up</RouterLink> now
                        </p>
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
                form: {
                    email: null,
                    password: null
                }
            }
        },
        validations: {
            form: {
                email: {
                    required :helpers.withMessage("This field is required",required),
                    email: helpers.withMessage("invalid email",email)
                },
                password: {
                    required :helpers.withMessage("This field is required",required)
                }
            }
        },
        methods: {
            async submit(){
                const data= this.form
                let validate=await this.v$.$validate()
                let next=this.$route.query.next
                if(validate){
                    this.$store.dispatch('user_signin',{'data':data,'role':'customer','next':next})
                }
            }
        }
    }
</script>