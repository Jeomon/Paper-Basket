<template>
    <div class="w-full mt-[10%] text">
        <img class="mx-auto w-[40vh]" src="../../assets/404.svg" alt="404 error">
        <div class="text-center font-medium">
            <p class="text-xl">We can't seem to find the page you're lookin for...</p>
            <RouterLink :to="{name: 'home'}" class="text-lg text-blue-500 hover:underline underline-offset-2 decoration-2">Go back to Home page</RouterLink>
        </div>
    </div>
</template>