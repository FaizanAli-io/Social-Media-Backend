<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <!-- Center of the Feed -->
        <div class="main-center col-span-3 space-y-4">

            <!-- Text Post section -->
            <div v-if="post.id" class="p-4 bg-white border border-gray-200 rounded-lg">
                <FeedItem v-bind:post="post" />
            </div>

            <!-- List of comments -->
            <div v-for="comment in post.comments" v-bind:key="comment.id"
                class="p-4 ml-6 bg-white border border-gray-200 rounded-lg">
                <CommentItem v-bind:comment="comment" />
            </div>

            <!-- Make a comment -->
            <div class="bg-white border border-gray-200 rounded-lg">
                <form method="post" v-on:submit.prevent="submitForm">
                    <div class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
                            placeholder="What do you think?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100">
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Comment</button>
                    </div>
                </form>
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

import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue'
import CurrentTrends from '@/components/CurrentTrends.vue'
import CommentItem from '@/components/CommentItem.vue'
import FeedItem from '@/components/FeedItem.vue'

export default {
    name: 'PostView',

    components: {
        PeopleYouMayKnow,
        CurrentTrends,
        CommentItem,
        FeedItem,
    },

    data() {
        return {
            post: {
                id: null,
                comments: [],
            },
            body: '',
        }
    },

    mounted() {
        this.getPost()
    },

    methods: {
        getPost() {
            axios
                .get(`api/posts/${this.$route.params.id}`)
                .then(response => {
                    console.log('Data: ', response.data)
                    this.post = response.data
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        submitForm() {
            axios
                .post(`api/posts/${this.$route.params.id}/comment/`,
                    { 'body': this.body })
                .then(response => {
                    console.log('Data: ', response.data)

                    this.post.comments.push(response.data)
                    this.post.comment_count += 1
                    this.body = ''
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        }
    }
}

</script>