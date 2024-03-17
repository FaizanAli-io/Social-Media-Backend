<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <!-- Center of the Feed -->
        <div class="main-center col-span-3 space-y-4">

            <!-- Make a post section -->
            <div class="bg-white border border-gray-200 rounded-lg">
                <FeedForm v-bind:user="null" v-bind:posts="posts" v-on:postCreated="postCreated" />
            </div>

            <!-- Text Post section -->
            <div v-for="post in posts" v-bind:key="post.id" class="p-4 bg-white border border-gray-200 rounded-lg">
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

<script>

import axios from 'axios'

import FeedForm from '@/components/FeedForm.vue'
import FeedItem from '@/components/FeedItem.vue'
import CurrentTrends from '@/components/CurrentTrends.vue'
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue'

export default {
    name: 'FeedView',

    components: {
        FeedForm,
        FeedItem,
        CurrentTrends,
        PeopleYouMayKnow,
    },

    data() {
        return {
            posts: [],
            body: '',
        }
    },

    mounted() {
        this.getFeed()
    },

    methods: {
        getFeed() {
            axios
                .get('api/posts/')
                .then(response => {
                    this.posts = response.data
                    console.log('Data: ', response.data)
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        postCreated(post) {
            this.posts.unshift(post)
        },

        deletePost(id) {
            this.posts = this.posts.filter(post => post.id != id)
        },
    }
}

</script>