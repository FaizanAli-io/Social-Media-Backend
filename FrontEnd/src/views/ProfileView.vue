<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <!-- Left side of the Feed -->
        <div class="main-left col-span-1">

            <!-- Your profile -->
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img :src="user.avatar_url" class="mb-6 rounded-full">

                <p class="font-bold"> {{ user.name }} </p>

                <div class="mt-6 flex space-x-8 justify-around" v-if="user.id">
                    <RouterLink :to="{ name: 'friends', params: { id: user.id } }" class="text-xs text-gray-500">
                        {{ user.friend_count }} friends
                    </RouterLink>
                    <p class="text-xs text-gray-500">{{ user.post_count }} posts</p>
                </div>

                <div class="mt-6">
                    <button v-if="userStore.user.id !== user.id" @click="sendFriendRequest"
                        class="inline-block py-2 px-3 bg-purple-600 text-white rounded-lg">
                        Friend Request
                    </button>

                    <button v-if="userStore.user.id !== user.id" @click="sendMessage"
                        class="inline-block ml-4 py-2 px-3 bg-purple-600 text-white rounded-lg">
                        Message
                    </button>


                    <RouterLink v-if="userStore.user.id === user.id" :to="{ name: 'editprofile' }"
                        class="inline-block py-2 px-3 bg-purple-600 text-white rounded-lg">
                        Edit Profile
                    </RouterLink>

                    <button v-if="userStore.user.id === user.id" @click="signout"
                        class="inline-block ml-4 py-2 px-3 bg-red-600 text-white rounded-lg">
                        Sign Out
                    </button>
                </div>
            </div>

        </div>

        <!-- Center of the Feed -->
        <div class="main-center col-span-2 space-y-4">

            <!-- Make a post section -->
            <div class="bg-white border border-gray-200 rounded-lg" v-if="userStore.user.id === user.id">
                <form method="post" v-on:submit.prevent="submitForm">
                    <div class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
                            placeholder="What are you thinking about?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach image</a>
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                    </div>
                </form>
            </div>

            <!-- Text Post section -->
            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">
                <FeedItem v-bind:post="post" />
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
import FeedItem from '@/components/FeedItem.vue'
import { RouterLink } from 'vue-router'

export default {
    name: 'ProfileView',

    components: {
        PeopleYouMayKnow,
        CurrentTrends,
        FeedItem,
        RouterLink
    },

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()
        return { userStore, toastStore }
    },

    data() {
        return {
            user: { id: null },
            posts: [],
            body: '',

        }
    },

    mounted() {
        this.getFeed()
    },

    watch: {
        '$route.params.id': {
            handler: function () {
                this.getFeed()
            },
            immediate: true,
            deep: true,
        }
    },

    methods: {
        getFeed() {
            axios
                .get(`api/posts/profile/${this.$route.params.id}`)
                .then(response => {
                    this.user = response.data.user
                    this.posts = response.data.posts
                    console.log('Data: ', response.data)
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        submitForm() {
            console.log('Submit Form', this.body)

            axios
                .post('api/posts/create/', { 'body': this.body })
                .then(response => {
                    console.log('Data: ', response.data)
                    this.posts.unshift(response.data)
                    this.body = ''
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        sendFriendRequest() {
            axios
                .post(`api/friends/${this.$route.params.id}/request/`)
                .then(response => {
                    console.log('Data: ', response.data)
                    if (response.data.message == 'friend request already exists') {
                        this.toastStore.showToast(5000, 'Request has already been sent!', 'bg-red-300')
                    } else {
                        this.toastStore.showToast(5000, 'Request sent successfully!', 'bg-emerald-300')
                    }
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        sendMessage() {
            axios
                .get(`api/chat/${this.$route.params.id}/start/`)
                .then(response => {
                    console.log('Data: ', response.data)
                    this.$router.push('/chat')
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        signout() {
            console.log("Logging out")
            this.userStore.removeToken()
            this.$router.push('/signin')
        }
    }
}

</script>