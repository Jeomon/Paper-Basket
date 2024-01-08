<template>
    <div class="bg-slate-200 w-full min-h-[90vh] relative top-[10vh]">
        <div class="absolute top-[15vh] left-0 right-0 mx-auto w-full max-w-4xl py-6 px-6 bg-slate-100 shadow-md rounded-md">
            <h1 class="text-4xl mt-2 mb-4 px-1 sm:px-3 text-slate-700">Update Profile</h1>
            <form @submit.prevent="submit" class="w-full text-lg" method="post" enctype="multipart/form-data" action="/">  
                <div class="flex flex-wrap">
                    <div class="w-full md:w-1/3 px-3 mb-6">
                        <label class="uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">First Name</label>
                        <input v-model="form.first_name" type="text" class="bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                    </div>
                    <div class="w-full md:w-1/3 px-3 mb-6">
                        <label class="uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Last Name</label>
                        <input v-model="form.last_name" type="text" class="bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                    </div>
                    <div class="w-full md:w-1/3 px-3 mb-6">
                        <label class="uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Profile Picture</label>
                        <input type="file" @change="imageLoader($event)" accept="image/*" class="appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                    </div>
                    <div class="w-full md:w-1/4 mb-2 px-3">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Gender</label>
                        <ul class="uppercase flex flex-row space-x-2 mt-4 font-medium w-full text-lg text-slate-500 leading-tight focus:outline-none h-10">
                            <li><input id="gender-0" v-model="form.gender" name="gender" type="radio" value="male"> <label for="gender-0">Male</label></li>
                            <li><input id="gender-1" v-model="form.gender" name="gender" type="radio" value="female"> <label for="gender-1">Female</label></li>
                        </ul>
                    </div>
                    <div class="w-full md:w-1/4 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Pin Code</label>
                        <input v-model.number="form.pin_code" type="text" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                    </div>
                    <div class="w-full md:w-1/4 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Date of Birth</label>
                        <input v-model="form.dob" type="date" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                    </div>
                    <div class="w-full md:w-1/4 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Mobile No.</label>
                        <input v-model.number="form.mobile_no" type="text" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                    </div>
                    <div class="w-full md:w-1/3 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">E-mail</label>
                        <input v-model="form.email" type="email" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                    </div>
                    <div class="w-full md:w-2/3 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Address</label>
                        <input v-model="form.address" type="text" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                    </div>        
                    <div class="w-full px-3">
                        <input type="submit" value="Edit Profile" class="h-fit my-auto font-medium cursor-pointer bg-slate-500 text-slate-300 text-lg p-2 rounded-md"/>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
    import { mapGetters } from 'vuex'
    export default {
        data(){
            return {
                form: {
                    first_name: null,
                    last_name: null,
                    profile_image: null,
                    gender: null,
                    dob: null,
                    address: null,
                    mobile_no: null,
                    pin_code: null,
                    email: null
                }
            }
        },
        computed: {
            ...mapGetters(['user'])
        },
        mounted(){
            this.form={
                first_name: this.user.first_name,
                last_name: this.user.last_name,
                profile_image: null,
                gender: this.user.gender,
                dob: this.user.dob,
                address: this.user.address,
                mobile_no: this.user.mobile_no,
                pin_code: this.user.pin_code,
                email: this.user.email
            }
        },
        methods: {
            imageLoader(e){
                if(e.target.files.length){
                    let reader=new FileReader()
                    reader.readAsDataURL(e.target.files[0])
                    reader.onload=()=>{
                        this.form.profile_image=reader.result.split(',').at(1)
                    }
                    reader.onerror=()=>{
                        console.log("Error in the image encoding process to base64")
                    }
                }
            },
            async submit(){
                let data=this.form
                let role='admin'
                this.$store.dispatch('update_user',{'data':data,'role':role})
                this.form={
                    first_name: data.first_name,
                    last_name: data.last_name,
                    profile_image: null,
                    gender: data.gender,
                    dob: data.dob,
                    address: data.address,
                    mobile_no: data.mobile_no,
                    pin_code: data.pin_code,
                    email: data.email
                }
            }
        }
    }
</script>