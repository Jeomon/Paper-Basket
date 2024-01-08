<template>
    <div class="bg-slate-200 w-full min-h-[90vh] relative top-[10vh]">
        <div class="absolute top-[15vh] left-0 right-0 mx-auto w-full max-w-2xl p-6 bg-slate-100 shadow-md rounded-md">
            <h1 class="text-center sm:text-left text-4xl mt-2 mb-6 px-3 text-slate-700">Make a Request</h1>
            <form @submit.prevent="submit" class="w-full">
                <div class="flex flex-wrap">
                    <div class="w-full md:w-1/2 px-3 mb-6">
                        <div class="flex flex-row space-x-1">
                            <label class="uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Manager Name</label>
                            <svg class="w-4 h-4 text-slate-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                                <path fill-rule="evenodd" d="M12 1.5a5.25 5.25 0 00-5.25 5.25v3a3 3 0 00-3 3v6.75a3 3 0 003 3h10.5a3 3 0 003-3v-6.75a3 3 0 00-3-3v-3c0-2.9-2.35-5.25-5.25-5.25zm3.75 8.25v-3a3.75 3.75 0 10-7.5 0v3h7.5z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <input :value="`${user.first_name} ${user.last_name}`" type="text" disabled class="bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10"/>
                    </div>
                    <div class="w-full md:w-1/2 px-3 mb-6">
                        <label class="block uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Request Type</label>
                        <select v-model="form.request_type" class="bg-slate-200 px-2 w-full cursor-pointer text-slate-500 leading-tight focus:outline-none h-10">
                            <option value="null" selected disabled>Select an option</option>
                            <option value="Add">Add a New Category</option>
                            <option value="Update">Update Existing Category</option>
                            <option value="Delete">Delete Exisiting Category</option>
                        </select>
                    </div>
                    <div class="w-full md:w-1/2 px-3 mb-6">
                        <div class="flex flex-row space-x-1">
                            <label class="uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">Current Category Name</label>
                            <svg v-if="form.request_type=='Add'||form.request_type==null" class="w-4 h-4 text-slate-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                                <path fill-rule="evenodd" d="M12 1.5a5.25 5.25 0 00-5.25 5.25v3a3 3 0 00-3 3v6.75a3 3 0 003 3h10.5a3 3 0 003-3v-6.75a3 3 0 00-3-3v-3c0-2.9-2.35-5.25-5.25-5.25zm3.75 8.25v-3a3.75 3.75 0 10-7.5 0v3h7.5z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <select :disabled="form.request_type=='Add'||form.request_type==null" v-model="form.old_category_name" class="bg-slate-200 px-2 w-full text-slate-500 leading-tight focus:outline-none h-10">
                            <option value="null" selected disabled>Select an option</option>
                            <option v-for="category in categories">{{ category.name }}</option>
                        </select>
                    </div>
                    <div class="w-full md:w-1/2 px-3 mb-6">
                        <div class="flex flex-row space-x-1">
                            <label class="uppercase tracking-wide text-slate-600 text-xs font-bold mb-2">New Category Name</label>
                            <svg v-if="form.request_type=='Delete'||form.request_type==null" class="w-4 h-4 text-slate-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                                <path fill-rule="evenodd" d="M12 1.5a5.25 5.25 0 00-5.25 5.25v3a3 3 0 00-3 3v6.75a3 3 0 003 3h10.5a3 3 0 003-3v-6.75a3 3 0 00-3-3v-3c0-2.9-2.35-5.25-5.25-5.25zm3.75 8.25v-3a3.75 3.75 0 10-7.5 0v3h7.5z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <input :disabled="form.request_type=='Delete'||form.request_type==null" v-model="form.new_category_name" id="new_category" type="text" class="bg-slate-200 px-2 appearance-none w-full text-slate-500 leading-tight focus:outline-none h-10" />
                    </div>
                    <div class="w-full px-3">
                        <button class="h-fit my-auto font-medium cursor-pointer bg-slate-500 text-slate-300 text-lg p-2 rounded-md">Send Request</button>
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
                    manager_name: null,
                    request_type: null,
                    old_category_name: null,
                    new_category_name: null
                }
            }
        },
        computed: {
            ...mapGetters(['user','categories'])
        },
        methods: {
            submit(){
                if (this.form.request_type=='Add'){
                    this.form.old_category_name=null
                }
                if (this.form.request_type=='Delete'){
                    this.form.new_category_name=null
                }
                let data=this.form
                this.$store.dispatch('add_manager_request',data)
                this.$router.push({name: 'manager_request_section'})
            }
        }
    }
</script>