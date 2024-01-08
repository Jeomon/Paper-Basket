<template>
    <Dashboard>
        <template #menu>
            <div class="font-semibold row-span-2 text-center text-slate-700 text-lg sm:text-xl bg-slate-300 w-full h-full flex flex-col justify-center">
                <RouterLink :to="{name: 'admin_update_profile'}" class="py-4 hover:bg-slate-200 hover:ml-4px hover:border-r-4 border-green-500">
                    <h1>Update Profile</h1>
                </RouterLink>
                <RouterLink :to="{name: 'admin_change_password'}" class="py-4 hover:bg-slate-200 hover:ml-4px hover:border-r-4 border-green-500">
                    <h1>Change Password</h1>
                </RouterLink>
                <RouterLink :to="{name: 'admin_category_section'}" class="py-4 hover:bg-slate-200 hover:ml-4px hover:border-r-4 border-green-500">
                    <h1>Category Section</h1>
                </RouterLink>
                <RouterLink :to="{name: 'admin_category_approval'}" class="py-4 hover:bg-slate-200 hover:ml-4px hover:border-r-4 border-green-500">
                    <span class="flex flex-row justify-center space-x-0.5">
                        <h1>Category Approval</h1>
                        <div v-if="all_requests&&all_requests.length" class="bg-red-500 rounded-full w-2.5 h-2.5"></div>
                    </span>
                </RouterLink>
                <RouterLink :to="{name: 'admin_manager_approval'}" class="py-4 hover:bg-slate-200 hover:ml-4px hover:border-r-4 border-green-500">
                    <span class="flex flex-row justify-center space-x-0.5">
                        <h1>Manager Approval</h1>
                        <div v-if="managers&&managers.length" class="bg-red-500 rounded-full w-2.5 h-2.5"></div>
                    </span>
                </RouterLink>
            </div>
        </template>
        <template #content>
            <RouterView/>
        </template>
    </Dashboard>
</template>
<script>
    import Dashboard from '@/components/Dashboard.vue'
    import { mapGetters } from 'vuex'
    export default {
        computed: {
          ...mapGetters(['user','managers','all_requests'])
        },
        components: {
            Dashboard
        }
    }
</script>