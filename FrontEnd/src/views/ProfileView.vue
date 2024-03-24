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
                    <button v-if="userStore.user.id !== user.id && canRequest" @click="sendFriendRequest"
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
                <FeedForm v-bind:user="user" v-bind:posts="posts" v-on:postCreated="postCreated" />
            </div>

            <!-- Text Post section -->
            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">
                <FeedItem v-bind:post="post" v-on:deletePost="deletePost" />
            </div>

        </div>

        <!-- Right side of the Feed -->
        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
            <CurrentTrends />
        </div>

    </div>
</template>

<style>
input [type="file"] {
    display: none;
}
</style>

<script>

import axios from 'axios'

import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

import FeedForm from '@/components/FeedForm.vue'
import FeedItem from '@/components/FeedItem.vue'
import CurrentTrends from '@/components/CurrentTrends.vue'
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue'

import { RouterLink } from 'vue-router'

export default {
    name: 'ProfileView',

    components: {
        FeedForm,
        FeedItem,
        RouterLink,
        CurrentTrends,
        PeopleYouMayKnow,
    },

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()
        return { userStore, toastStore }
    },

    data() {
        return {
            posts: [],
            canRequest: null,
            user: { id: null },
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
                    this.canRequest = response.data.can_request
                    console.log('Data: ', response.data)
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
                .post('api/chat/', { id: this.$route.params.id })
                .then(response => {
                    console.log('Data: ', response.data)
                    this.$router.push('/chat')
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        postCreated(post) {
            this.posts.unshift(post)
            this.user.post_count += 1
        },

        deletePost(id) {
            this.posts = this.posts.filter(post => post.id != id)
        },

        signout() {
            console.log("Logging out")
            this.userStore.removeToken()
            this.$router.push('/signin')
        },
    }
}

</script>