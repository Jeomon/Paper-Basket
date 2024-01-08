<template>
    <div class="relative w-full bg-slate-200 min-h-[90vh] top-[10vh]">
        <div class="flex flex-col mx-6">
            <div class="w-full py-3 px-3 bg-slate-100 my-10 shadow-md">
                <h1 class="text-center sm:text-left text-4xl text-slate-700">Category Section</h1>
            </div>
        </div>
        <div class="flex md:flex-row flex-col md:justify-between items-center space-y-2 mx-6">
            <div class="my-2 flex flex-row shadow-sm rounded-md overflow-hidden">
                <input @keyup="onTyping" class="sm:w-[30vw] md:w-[25vw] lg:w-[20vw] max-w-md px-3 h-10 bg-slate-100 outline-none text-slate-500 font-medium placeholder:text-slate-400 placeholder:font-medium" placeholder="Find Category Here" type="search" name="category">
                <button>
                    <svg class="p-2 text-slate-400 bg-slate-700 hover:text-slate-300 w-10 h-10" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clip-rule="evenodd" />
                    </svg>
                </button>
            </div>
            <div class="flex flex-row items-center space-x-1 cursor-pointer">
                <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>                            
                <RouterLink :to="{name: 'admin_add_category'}" class="text-xl text-slate-600 font-medium">Add Category</RouterLink>
            </div>
        </div>
        <div class="overflow-x-auto">
            <div class="inline-block min-w-full py-2 sm:px-6 lg:px-8">
                <div class="overflow-hidden">
                    <table class="w-[75vw] text-sm font-light text-center">
                        <thead class="border-b-2 border-neutral-500 text-base">
                            <tr class="text-slate-600  uppercase">
                                <th scope="col" class="px-5 py-3">Category Name</th>
                                <th scope="col" class="px-5 py-3">Consumable</th>
                                <th scope="col" class="px-5 py-3">Vegetarian</th>
                                <th scope="col" class="px-5 py-3">Update Category</th>
                                <th scope="col" class="px-5 py-3">Delete Category</th>
                            </tr>
                        </thead>
                        <tbody v-if="categories&&categories.length">
                            <tr v-for="category in categories" :key="category.id" class="category border-b border-slate-400 font-medium text-base">
                                <td class="whitespace-nowrap px-5 py-4">{{ category.name }}</td>
                                <td class="whitespace-nowrap px-5 py-4">{{ category.consumable }}</td>
                                <td class="whitespace-nowrap px-5 py-4">{{ category.vegetarian }}</td>
                                <td class="whitespace-nowrap px-6 py-4">
                                    <RouterLink :to="{name: 'admin_update_category',params: {id: category.id}}" class="p-2 bg-green-500 rounded-md shadow-md hover:text-white">Update</RouterLink>
                                </td>
                                <td class="whitespace-nowrap px-6 py-4">
                                    <span @click="onDelete($event,category.id)" class="cursor-pointer p-2 bg-red-500 rounded-md shadow-md hover:text-white">Delete</span>
                                </td>
                            </tr>
                        </tbody>
                        <div v-else class="absolute flex flex-col w-full justify-center mt-[15vh]">
                            <img class="w-20 h-auto mx-auto opacity-70" src="../../../assets/empy-box.png" alt="empty box">
                            <h1 class="text-xl text-center my-0.5 w-full font-medium text-slate-500 opacity-80">No categories found...</h1>
                        </div>
                    </table>
                </div>
            </div>
        </div>
    </div>
    <DeleteCategory v-if="toggleModal" @afterDelete="onAfterDelete" @cancel="onCancel" :toggleModal="toggleModal" :category_id="category_id"/>
</template>
<script>
    import { mapGetters } from 'vuex'
    import DeleteCategory from './DeleteCategory.vue'
    export default {
        data(){
            return {
                toggleModal: false,
                category_id: null
            }
        },
        methods: {
            onDelete(e,id){
                this.toggleModal =!this.togglModal
                this.category_id=id
            },
            onCancel(value){
                this.toggleModal =value
            },
            onAfterDelete(value){
                this.toggleModal = value
            },
            onTyping(e){
                let search_content=e.target.value
                this.$store.commit('category_search',search_content)
            }
        },
        computed: {
            ...mapGetters(['categories'])
        },
        components: {
            DeleteCategory
        }
    }
</script>