<template>
    <div class="relative w-full bg-slate-200 min-h-[90vh] top-[10vh]">
        <div class="flex flex-col mx-6">
            <div class="w-full py-3 px-3 bg-slate-100 my-10 shadow-md">
                <h1 class="text-center sm:text-left text-4xl text-slate-700">Manager Approval</h1>
            </div>
            <div class="overflow-x-auto sm:-mx-6 lg:-mx-8">
                <div class="inline-block min-w-full py-2 sm:px-6 lg:px-8">
                    <div class="overflow-hidden">
                        <table class="w-[75vw] text-left text-sm font-light">
                            <thead class="border-b-2 border-neutral-500 text-base">
                                <tr class="text-center text-slate-600  uppercase">
                                    <th scope="col" class="px-5 py-3">First Name</th>
                                    <th scope="col" class="px-5 py-3">Last Name</th>
                                    <th scope="col" class="px-5 py-3">Store Name</th>
                                    <th scope="col" class="px-5 py-3">Email Address</th>
                                    <th scope="col" class="px-5 py-3">Contact No.</th>
                                    <th scope="col" class="px-5 py-3">Pin Code</th>
                                    <th scope="col" class="px-5 py-3">Approval</th>
                                </tr>
                            </thead>
                            <tbody v-if="managers&&managers.length">
                                <tr v-for="manager in managers" :key="manager.id" class="text-center border-b border-slate-400 font-medium text-base">
                                    <td class="whitespace-nowrap px-5 py-4">{{ manager.first_name }}</td>
                                    <td class="whitespace-nowrap px-5 py-4">{{ manager.last_name }}</td>
                                    <td class="whitespace-nowrap px-5 py-4">{{ manager.first_name }} Store</td>
                                    <td class="whitespace-nowrap px-5 py-4">{{ manager.email }}</td>
                                    <td class="whitespace-nowrap px-5 py-4">{{ manager.mobile_no }}</td>
                                    <td class="whitespace-nowrap px-5 py-4">{{ manager.pin_code }}</td>
                                    <td class="whitespace-nowrap px-5 py-4 flex flex-row text-sm justify-center space-x-2">
                                        <span @click="onApproval($event,manager.email,true)" class="p-2 bg-green-500 rounded-md shadow-md hover:text-white cursor-pointer">Allow</span>
                                        <span @click="onApproval($event,manager.email,false)" class="p-2 bg-red-500 rounded-md shadow-md hover:text-white cursor-pointer">Deny</span>
                                    </td>
                                </tr>
                            </tbody>
                            <div v-else class="absolute flex flex-col w-full justify-center mt-[20vh]">
                                <img class="w-20 h-auto mx-auto opacity-70" src="../../../assets/empy-box.png" alt="empty box">
                                <h1 class="text-xl text-center my-0.5 w-full font-medium text-slate-500 opacity-80">No requests found...</h1>
                            </div>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import { mapGetters } from 'vuex'
    export default {
        methods: {
            onApproval(e,email,status){
                let hostname=window.location.hostname
                let port=window.location.port
                let data={email,status,hostname,port}
                this.$store.dispatch('manager_approval',data)
            }
        },
        computed: {
            ...mapGetters(['managers'])
        },
        created(){
            this.$store.dispatch('get_managers')
        }
    }
</script>