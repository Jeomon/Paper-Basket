<template>
    <Dashboard>
        <template #menu>
            <div class="font-semibold row-span-2 text-center text-slate-700 text-lg sm:text-xl bg-slate-300 w-full h-full flex flex-col justify-center">
                <RouterLink :to="{name: 'manager_update_profile'}" class="py-4 hover:bg-slate-200 hover:ml-4px hover:border-r-4 border-green-500">
                    <h1>Update Profile</h1>
                </RouterLink>
                <RouterLink :to="{name: 'manager_change_password'}" class="py-4 hover:bg-slate-200 hover:ml-4px hover:border-r-4 border-green-500">
                    <h1>Change Password</h1>
                </RouterLink>
                <RouterLink :to="{name: 'manager_trend_analysis'}" class="py-4 hover:bg-slate-200 hover:ml-4px hover:border-r-4 border-green-500">
                    <h1>Trend Analysis</h1>
                </RouterLink>
                <RouterLink :to="{name: 'manager_product_section'}" class="py-4 hover:bg-slate-200 hover:ml-4px hover:border-r-4 border-green-500">
                    <h1>Product Section</h1>
                </RouterLink>
                <RouterLink :to="{name: 'manager_request_section'}" class="py-4 hover:bg-slate-200 hover:ml-4px hover:border-r-4 border-green-500">
                    <h1>Request Section</h1>
                </RouterLink>
                <RouterLink :to="{name: 'manager_delete_account'}" class="py-4 hover:bg-slate-200 hover:ml-4px hover:border-r-4 border-green-500">
                    <h1>Delete Account</h1>
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
          ...mapGetters(['user'])
        },
        components: {
            Dashboard
        }
    }
</script>