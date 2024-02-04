<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-grey-200 rounded-lg">
                <h1 class="mb-6 text-2xl">
                    Sign In
                </h1>

                <p class="mb-6 text-grey-500">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
                    dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
                    ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
                    fugiat nulla pariatur.
                </p>

                <p class="font-bold">
                    Don't have an account? <RouterLink :to="{ 'name': 'signup' }" class="underline">Click Here</RouterLink>
                    to sign up!
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-grey-200 rounded-lg">
                <form class="space-y-6">
                    <div>
                        <label>E-mail</label><br>
                        <input type="email" placeholder="Your e-mail address"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg">
                    </div>

                    <div>
                        <label>Password</label><br>
                        <input type="password" placeholder="Your password"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg">
                    </div>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Sign In</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
