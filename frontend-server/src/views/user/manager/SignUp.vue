<template>
    <div class="bg-slate-200 w-full h-auto py-[6vh] mt-16" >
        <div class="w-[90%] max-w-xl p-6 bg-slate-100 mx-auto shadow-md rounded-md">
            <h1 class="text-4xl mt-2 mb-6 text-slate-700">Sign Up<span class="text-base font-medium"> (Manager)</span></h1>
            <form @submit.prevent="submit" class="w-full max-w-xl mx-auto">
                <div class="flex flex-wrap">
                    <div class="w-full md:w-1/2 mb-6 md:px-1">
                        <label for="firstname" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">First Name</label>
                        <input v-model="form.first_name" id="firstname" type="text" class="font-medium bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.first_name.$error" class="text-red-500 font-medium">{{ v$.form.first_name.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/2 mb-6 md:px-1">
                        <label for="lastname" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Last Name</label>
                        <input v-model="form.last_name" id="lastname" type="text" class="font-medium bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.last_name.$error" class="text-red-500 font-medium">{{ v$.form.last_name.$errors[0].$message }}</p>
                    </div>
                    <div class="w-1/2 md:w-1/2 mb-2 md:px-1">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Gender</label>
                        <ul class="uppercase flex flex-row space-x-2 mt-4 font-medium w-full text-lg text-slate-500 leading-tight focus:outline-none h-10">
                            <li><input id="gender-0" v-model="form.gender" name="gender" type="radio" value="male"> <label for="gender-0">Male</label></li>
                            <li><input id="gender-1" v-model="form.gender" name="gender" type="radio" value="female"> <label for="gender-1">Female</label></li>
                        </ul>
                    </div>
                    <div class="w-1/2 md:w-1/2 mb-6 md:px-1">
                        <label for="dob" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Date of Birth</label>
                        <input v-model="form.dob" type="date" id="dob" class="cursor-pointer uppercase font-medium bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.dob.$error" class="text-red-500 font-medium">{{ v$.form.dob.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/2 mb-6 md:px-1">
                        <label for="address" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Address</label>
                        <input v-model="form.address" type="text" id="address" class="font-medium bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10"/> 
                        <p v-if="v$.form.address.$error" class="text-red-500 font-medium">{{ v$.form.address.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/2 mb-6 md:px-1">
                        <label for="mobile" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Mobile No.</label>
                        <input v-model="form.mobile_no" id="mobile" type="text" class="font-medium bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.mobile_no.$error" class="text-red-500 font-medium">{{ v$.form.mobile_no.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/2 mb-6 md:px-1">
                        <label for="pincode" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Pin code</label>
                        <input v-model="form.pin_code" type="text" id="pincode" class="font-medium bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.pin_code.$error" class="text-red-500 font-medium">{{ v$.form.pin_code.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/2 mb-6 md:px-1">
                        <label for="email" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">E-mail</label>
                        <input v-model="form.email" type="email" id="email" class="font-medium bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.email.$error" class="text-red-500 font-medium">{{ v$.form.email.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/2 mb-6 md:px-1">
                        <label for="password" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Password</label>
                        <input v-model="form.password" type="password" id="password" class="font-medium bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.password.$error" class="text-red-500 font-medium">{{ v$.form.password.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full md:w-1/2 mb-6 md:px-1">
                        <label for="confirm_password" class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Confirm Password</label>
                        <input v-model="form.confirm_password" type="password" id="confirm_password" class="font-medium bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                        <p v-if="v$.form.confirm_password.$error" class="text-red-500 font-medium">{{ v$.form.confirm_password.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full flex flex-row items-center space-x-2">
                        <input v-model="isagreed" id="agreement" type="checkbox" class="font-medium bg-slate-200 text-slate-500 leading-tight focus:outline-none"/>
                        <label for="agreement" class="cursor-pointer uppercase tracking-wide text-slate-600 text-xs font-bold">I agree to the terms and conditions</label>
                    </div>
                    <div class="w-full mb-4">
                        <p v-if="v$.isagreed.$error" class="text-red-500 font-medium">{{ v$.isagreed.$errors[0].$message }}</p>
                    </div>
                    <div class="w-full">
                        <input type="submit" value="Sign Up" class="h-fit my-auto cursor-pointer font-medium bg-slate-500 text-slate-300 text-lg p-2 rounded-md"/>
                        <p class="my-3 text-slate-600 text-base font-medium">Already have an account? 
                            <RouterLink class="text-blue-400" :to="{name: 'manager_signin'}">Sign In</RouterLink> now
                        </p>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
    import { helpers,required,maxLength,email } from '@vuelidate/validators'
    import useVuelidate from '@vuelidate/core'
    export default {
        data(){
            return {
                v$: useVuelidate(),
                form: {
                    first_name: null,
                    last_name: null,
                    gender: null,
                    dob: null,
                    address: null,
                    mobile_no: null,
                    pin_code: null,
                    email: null,
                    password: null,
                    confirm_password: null,
                    hostname: window.location.hostname,
                    port: window.location.port
                },
                isagreed: false
            }
        },
        validations: {
            form: {
                    first_name: {
                        required :helpers.withMessage("This field is required",required)
                    },
                    last_name: {
                        required :helpers.withMessage("This field is required",required)
                    },
                    dob: {
                        date :helpers.withMessage("Date of birth is wrong",value=>((new Date(value).getTime())-(new Date().getTime()))<0)
                    },
                    address: {
                        required :helpers.withMessage("This field is required",required)
                    },
                    mobile_no: {
                        required :helpers.withMessage("This field is required",required),
                        maxLength :helpers.withMessage("This field requires 10 numbers.",maxLength(10))
                    },
                    pin_code: {
                        required :helpers.withMessage("This field is required",required),
                        maxLength :helpers.withMessage("This field requires 6 numbers.",maxLength(6))
                    },
                    email: {
                        required :helpers.withMessage("This field is required",required),
                        email: helpers.withMessage("invalid email",email)
                    },
                    password: {
                        required :helpers.withMessage("This field is required",required)
                    },
                    confirm_password: {
                        required :helpers.withMessage("This field is required",required)
                    }
            },
            isagreed: {
                isagreed :helpers.withMessage("Your acknowledgment of our terms is required for submission.",value=>value)
            }
        },
        methods: {
            async submit(){
                const data= this.form
                let validate=await this.v$.$validate()
                let role='manager'
                if(validate){
                    this.$store.dispatch('user_signup',{'data':data,'role':role})
                    this.v$.$reset()
                }
            }
        }
    }
</script>