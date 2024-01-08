<template>
    <div class="fixed top-[10vh] left-[20vw] w-[80vw] h-[90vh] bg-black/70 backdrop-blur-sm">
        <div class="w-fit p-6 mx-[10%] md:mx-[20%] lg:mx-[30%] my-[15vh] text-center bg-slate-300 rounded-md">
            <h2 class="text-3xl font-medium mb-4">Confirm Product Deletion</h2>
            <p class="font-medium my-1">Are you sure you want to delete this product?</p>
            <p class="font-medium my-1">This action is unrecoverable.</p>
            <div class="flex flex-row space-x-6 justify-center mt-6">
                <span @click="submit" class="cursor-pointer bg-red-600 shadow-md px-3 py-2 rounded-md font-medium">Delete</span>
                <span @click="$emit('cancel',!toggleModal)" class="cursor-pointer bg-slate-400 shadow-md px-3 py-2 rounded-md font-medium">Cancel</span>
            </div>
        </div>
    </div>
</template>
<script>
    export default {
        props: {
            toggleModal: {
                type: Boolean,
                required: true
            },
            product_id: {
                type: String,
                required: true
            }
        },
        methods: {
            submit(){
                let id=this.product_id
                this.$store.dispatch('delete_product',id)
                this.$emit('afterDelete',!this.toggleModal)
            }
        }
    }
</script>