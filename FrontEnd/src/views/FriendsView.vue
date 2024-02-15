<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <!-- Left side of the Feed -->
        <div class="main-left col-span-1">

            <!-- Your profile -->
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img :src="user.avatar_url" class="mb-6 rounded-full">

                <p class="font-bold">{{ user.name }}</p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <p class="text-xs text-gray-500">{{ user.friend_count }} friends</p>
                    <p class="text-xs text-gray-500">{{ user.post_count }} posts</p>
                </div>
            </div>

        </div>

        <!-- Center of the Screen -->
        <div class="main-center col-span-2 space-y-4">

            <!-- Friends -->
            <div v-if="friends.length > 0" class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-2 gap-4">

                <div v-for="user in friends" v-bind:key="user.id" class="p-4 text-center bg-gray-100 rounded-lg">
                    <img :src="user.avatar_url" class="mb-6 rounded-full">

                    <p class="font-bold">
                        <RouterLink :to="{ name: 'profile', params: { id: user.id } }">
                            {{ user.name }}
                        </RouterLink>
                    </p>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">{{ user.friend_count }} friends</p>
                        <p class="text-xs text-gray-500">{{ user.post_count }} posts</p>
                    </div>
                </div>

            </div>

            <!-- Friend Requests -->
            <div v-if="friendRequests.length > 0"
                class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-2 gap-4">

                <div v-for="request in friendRequests" v-bind:key="request.id"
                    class="p-4 text-center bg-gray-100 rounded-lg">
                    <img :src="request.created_by.avatar_url" class="mb-6 mx-auto rounded-full">

                    <p class="font-bold">
                        <RouterLink :to="{ name: 'profile', params: { id: request.created_by.id } }">
                            {{ request.created_by.name }}
                        </RouterLink>
                    </p>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">{{ request.created_by.friend_count }} friends</p>
                        <p class="text-xs text-gray-500">{{ request.created_by.post_count }} posts</p>
                    </div>

                    <div class="mt-6 space-x-4">
                        <button @click="handleRequest('accepted', request.created_by.id)"
                            class="inline-block py-4 px-6 bg-green-600 text-white rounded-lg">Accept</button>
                        <button @click="handleRequest('rejected', request.created_by.id)"
                            class="inline-block py-4 px-6 bg-red-600 text-white rounded-lg">Reject</button>
                    </div>
                </div>

            </div>

        </div>

        <!-- Right side of the Feed -->
        <div class="main-right col-span-1 space-y-4">

            <PeopleYouMayKnow />

            <CurrentTrends />

        </div>

    </div>
</template>

<script>

import axios from 'axios'

import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue'
import CurrentTrends from '@/components/CurrentTrends.vue'

export default {
    name: 'FriendsView',

    components: {
        PeopleYouMayKnow,
        CurrentTrends,
    },

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()
        return { userStore, toastStore }
    },

    data() {
        return {
            user: {},
            friends: [],
            friendRequests: [],
        }
    },

    mounted() {
        this.getFriends()
    },

    methods: {
        getFriends() {
            axios
                .get(`api/friends/${this.$route.params.id}/`)
                .then(response => {
                    console.log('Data: ', response.data)
                    this.friendRequests = response.data.requests
                    this.friends = response.data.friends
                    this.user = response.data.user
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        handleRequest(status, pk) {
            console.log(status, pk)

            axios
                .post(`api/friends/${pk}/${status}/`)
                .then(response => {
                    console.log('Data: ', response.data)
                    this.toastStore.showToast(5000, `Friend Request has been ${status}`, 'bg-emerald-300')
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        }
    }
}

</script>