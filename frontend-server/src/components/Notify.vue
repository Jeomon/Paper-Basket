<template>
    <div class="fixed top-[10vh] w-[100vw] h-[90vh] bg-black/70 backdrop-blur-sm">
        <div class="w-fit py-8 px-10 mx-[10%] md:mx-[20%] lg:mx-[30%] my-[4vh] text-center bg-slate-300 rounded-md">
            <div v-if="notify.role=='manager'">
                <h1 class="text-3xl font-medium mb-4">Manager Account Verification</h1>
                <h2 class="font-medium my-1 text-xl">Welcome to Paper Basket</h2>
                <div class="my-3 text-justify text-lg italic">
                    <p class="indent-4 my-1.5">Thank you for registering as a manager with our platform. Your sign-up request is currently under review by our administrative team. Our team is working diligently to process your request. Once approved, you'll have full access to our manager portal and its functionalities.</p>
                    <p class="indent-4 my-1.5">You'll receive an email notification at the address provided during registration once your account is verified. This process helps ensure a secure environment for both our customers and our managerial staff.</p>
                    <p class="indent-4 my-1.5">Thank you for your patience and understanding. Should you have any queries or require further assistance, please don't hesitate to reach out to our support team.</p>
                </div>
            </div>
            <div v-if="notify.role=='customer'">
                <h1 class="text-3xl font-medium mb-4">Almost Ready to Shop!</h1>
                <h2 class="font-medium my-1 text-xl">Welcome to Paper Basket</h2>
                <div class="my-3 text-justify text-lg italic">
                    <p class="indent-4 my-1.5">Thanks for joining our grocery community! To ensure fresh and secure shopping, we've sent a verification email to your inbox.</p>
                    <p class="indent-4 my-1.5">Just tap on the link inside to start filling your cart with delicious finds. If you don't spot our email, give your spam folder a quick check. Happy shopping!</p>
                </div>
            </div>
            <div class="flex flex-row space-x-6 justify-center mt-6 mb-4">
                <span @click="onDisable" class="cursor-pointer bg-green-600 shadow-md px-3 py-2 rounded-md font-medium">Back to Home</span>
            </div>
        </div>
    </div>
</template>
<script>
    import { mapGetters } from 'vuex'
    export default {
        computed: {
            ...mapGetters(['notify'])
        },
        methods: {
            onDisable(){
                this.$store.commit('notify',{'show':false,'role':''})
            }
        }
    }
</script>