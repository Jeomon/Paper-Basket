<template>
    <div class="fixed left-0 top-[10vh] flex flex-col w-[40%] sm:w-[30%] lg:w-[20%] h-[90vh]">
        <div class="grid grid-rows-10 w-full h-full">
            <div class="row-span-8 bg-slate-300 w-full h-full flex flex-col-reverse items-center justify-start">
                <div v-if="user" class="text-center">
                    <img class="mx-auto my-1 w-20 h-20 sm:w-24 sm:h-24 rounded-full" :src="'http://127.0.0.1:5000/user/static/'+user.profile_image" alt="profile image of user">
                    <p class="text-xl mt-4">{{ wishMessage }},</p>
                    <h1 class="text-xl md:text-2xl font-medium">{{ `${user.first_name} ${user.last_name}` }}</h1>
                </div>
            </div>
            <!-- menu -->
            <slot name="menu">
            </slot>
        </div>
    </div>
    <div class="absolute w-[60%] sm:w-[70%] lg:w-[80%] top-0 right-0">
        <!-- content -->
        <slot name="content">
        </slot>
    </div>
</template>
<script>
    import { mapGetters } from 'vuex';
    export default{
        data(){
            return {
                hrs: new Date().getHours()
            }
        },
        computed: {
            ...mapGetters(['user']),
            wishMessage(){
                if(this.hrs<12){
                    return "Good Morning"
                }
                else if(this.hrs<16){
                    return "Good Afternoon"
                }
                else{
                    return "Good Evening"
                }
            }
        }
    }
</script>