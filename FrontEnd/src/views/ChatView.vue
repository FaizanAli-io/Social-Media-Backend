<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <!-- Left side of the Screen -->
        <div class="main-left col-span-1">

            <!-- List of DM's -->
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <div class="space-y-4">

                    <div v-for="convo in conversations" v-bind:key="convo.id" v-on:click="setActiveConvo(convo.id)"
                        class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">

                            <div v-for="user in convo.users" v-bind:key="user.id">
                                <p v-if="user.id !== userStore.user.id" class="text-xs font-bold">
                                    {{ user.name }}
                                </p>
                            </div>
                        </div>

                        <span class="text-xs text-gray-500">{{ convo.modified_at_formatted }} ago</span>
                    </div>

                </div>
            </div>

        </div>

        <!-- Right side of the Screen -->
        <div class="main-center col-span-3 space-y-4">

            <!-- Chat display section -->
            <div class="bg-white border border-gray-200 rounded-lg ">
                <div class="flex flex-col flex-grow p-4">

                    <template v-for="message in activeConvo.messages" v-bind:key="message.id">
                        <div v-if="message.sent_by.id === userStore.user.id"
                            class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
                            <div>
                                <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                                    <p class="text-sm">{{ message.body }}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">
                                    {{ message.created_at_formatted }} ago
                                </span>
                            </div>
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                            </div>
                        </div>

                        <div v-else class="flex w-full mt-2 space-x-3 max-w-md">
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                            </div>
                            <div>
                                <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                                    <p class="text-sm">{{ message.body }}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">
                                    {{ message.created_at_formatted }} ago
                                </span>
                            </div>
                        </div>
                    </template>

                </div>
            </div>

            <!-- Send a message section -->
            <div class="bg-white border border-gray-200 rounded-lg">
                <form method="post" v-on:submit.prevent="sendMessage">
                    <div class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg resize-none"
                            placeholder="What do you want to say?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Send</button>
                    </div>
                </form>
            </div>

        </div>

    </div>
</template>

<script>

import axios from 'axios'

import { useUserStore } from '@/stores/user'

export default {
    name: 'ChatView',

    setup() {
        const userStore = useUserStore()
        return { userStore }
    },

    data() {
        return {
            conversations: [],
            activeConvo: {},
            body: '',
        }
    },

    mounted() {
        this.getConversations()
    },

    methods: {
        getConversations() {
            console.log("Getting Conversations")

            axios
                .get('api/chat/')
                .then(response => {
                    console.log('Data: ', response.data)
                    this.conversations = response.data
                    if (this.conversations.length > 0) {
                        this.activeConvo = this.conversations[0]
                        this.getMessages()
                    }
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        getMessages() {
            console.log("Getting Messages")

            axios
                .get(`api/chat/${this.activeConvo.id}/`)
                .then(response => {
                    console.log('Data: ', response.data)
                    this.activeConvo = response.data
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        sendMessage() {
            console.log("Sending Message", this.body)

            axios
                .post(`api/chat/${this.activeConvo.id}/send/`, { body: this.body })
                .then(response => {
                    console.log('Data: ', response.data)
                    this.activeConvo.messages.push(response.data)
                    this.body = ''
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        setActiveConvo(id) {
            this.activeConvo.id = id
            this.getMessages()
        }
    }
}

</script>