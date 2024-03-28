<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-3 space-y-4">
            <div v-for="notification in notifications" v-bind:key="notification.id"
                class="p-4 bg-white border border-gray-200 rounded-lg" v-if="notifications.length">
                {{ notification.body }} <button class="underline" @click="readNotification(notification)">Read
                    More</button>
            </div>
            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-else>
                You don't have any unread notifications.
            </div>
        </div>
    </div>
</template>

<script>

import axios from 'axios'

export default {
    name: 'NotificationView',

    data() {
        return {
            notifications: [],
        }
    },

    mounted() {
        this.getNotifications()
    },

    methods: {
        getNotifications() {
            axios
                .get('api/notification/')
                .then(response => {
                    console.log('Data: ', response.data)
                    this.notifications = response.data
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        readNotification(notif) {
            console.log(notif.id)

            axios
                .patch('api/notification/', {id: notif.id})
                .then(response => {
                    console.log('Data: ', response.data)

                    if (notif.notification_type == 'postlike' || notif.notification_type == 'postcomment') {
                        this.$router.push({ name: 'postdetail', params: { id: notif.post_id } })
                    } else {
                        this.$router.push({ name: 'friends', params: { id: notif.created_for_id } })
                    }
                })
                .catch(error => {
                    console.log('Error: ', error)
                })

        }
    },
}

</script>