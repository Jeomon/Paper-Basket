<template>
    <div class="relative w-full bg-slate-200 min-h-[90vh] top-[10vh]">
        <div class="mx-6 flex flex-col">
            <div class="bg-slate-200 w-full">
                <div class="w-full py-3 px-3 bg-slate-100 my-10 shadow-md">
                    <h1 class="text-center sm:text-left text-4xl text-slate-700">Delete Account</h1>
                </div>
            </div>
            <div class="mx-[3%] py-7">
                <p class="indent-10 text-justify font-medium text-slate-500 text-lg">
                    By proceeding with the deletion of your store manager account, please note that all products associated with your 
                    store will be permanently removed from our store catalog, and any supplier and inventory data linked to your account 
                    will also be deleted. This action is irreversible, and you will lose access to your store manager dashboard and account 
                    privileges. Customer orders and related data will remain unaffected. If you have any questions or concerns, we recommend 
                    contacting our support team before finalizing the account deletion.
                </p>
                <span @click="onDeleteRequest" class="text-white font-medium text-lg flex flex-row cursor-pointer items-center mx-auto p-2 mt-10 bg-red-500 rounded-md w-fit" href="#">
                    <svg class="w-7 h-7 mx-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                    </svg>
                    Delete Account
                </span>
            </div>
        </div>
        <div :class="[{'hidden':!toggleDelete}, 'fixed', 'top-[10vh]', 'w-[60%]', 'sm:w-[70%]', 'lg:w-[80%]', 'h-[90vh]', 'bg-black/70', 'backdrop-blur-sm']">
            <div class="w-[55vw] sm:w-fit p-6 mx-[5%] md:mx-[20%] lg:mx-[30%] my-[10vh] text-center bg-slate-300 rounded-md">
                <h2 class="text-3xl font-medium mb-6">Confirm Account Deletion</h2>
                <p class="font-medium text-justify mx-4">Before we proceed with deleting your account, we need to verify your identity. Please enter your account password below to confirm the deletion.</p>
                <form @submit.prevent="onDelete($event)" class="mt-4 mb-2 w-[70%] mx-auto">
                    <div class="flex flex-row space-x-12 justify-center mt-8">
                        <input type="submit" class="cursor-pointer bg-red-600 shadow-md px-3 py-2 rounded-md font-medium" value="Delete">
                        <span @click="onDeleteRequest" class="cursor-pointer bg-slate-400 shadow-md px-3 py-2 rounded-md font-medium">Cancel</span>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
<script>
    export default {
        data(){
            return {
                toggleDelete: false,
            }
        },
        methods: {
            onDeleteRequest(){
                this.toggleDelete=!this.toggleDelete
            },
            async onDelete(e){
                this.$store.dispatch('delete_user','manager')
            }
        },
    }
</script>