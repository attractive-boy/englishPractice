<template>
    <div>
        <vue-advanced-chat height="75vh" :current-user-id="currentUserId" :rooms="JSON.stringify(rooms)"
            :rooms-loaded="true" :messages="JSON.stringify(messages)" :messages-loaded="messagesLoaded"
            :single-room="true" @send-message="sendMessage($event.detail[0])"
            @fetch-messages="fetchMessages($event.detail[0])" />
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { register } from 'vue-advanced-chat';
import { getCurrentInstance } from 'vue';
register();

const props = defineProps({
    selectedScene: Object,
    selectedDifficulty: String,
    showText: Boolean  // Add the showText prop
});
const { proxy } = getCurrentInstance();

const currentUserId = ref(localStorage.getItem('user_id'));
const rooms = ref([
    {
        roomId: '1',
        roomName: props.selectedScene.name || 'Room 1',
        avatar: 'https://66.media.tumblr.com/avatar_c6a8eae4303e_512.pnj',
        users: [
            { _id: localStorage.getItem('user_id'), username: localStorage.getItem('username') },
            { _id: 'AI', username: 'AI' }
        ]
    }
]);
const messages = ref([]);
const messagesLoaded = ref(false);

const fetchMessages = ({ options = {} }) => {

};

const sendMessage = (message) => {
    const payload = {
        content: message.content,
        senderId: currentUserId.value,
        timestamp: new Date().toISOString(),
        selectedScene: props.selectedScene,
        selectedDifficulty: props.selectedDifficulty
    };

    let formData = new FormData();
    formData.append('content', message.content);
    formData.append('senderId', currentUserId.value);
    formData.append('timestamp', new Date().toISOString());
    formData.append('selectedScene', JSON.stringify(props.selectedScene));
    formData.append('selectedDifficulty', props.selectedDifficulty);

    if (message.files && message.files.length > 0 && message.files[0].audio) {
        formData.append('audio_file', message.files[0].blob, message.files[0].name);

        proxy.$http.post('/transcribe', formData)
            .then((response) => {
                const transcription = response.data.transcription;
                const userMessage = transformMessage({
                    message_id: messages.value.length,
                    content: transcription,
                    is_user: true,
                    timestamp: new Date().toISOString()
                });
                messages.value = [...messages.value, userMessage];

                // Optionally send the transcription as a message to get a response from AI
                const aiPayload = {
                    content: transcription,
                    senderId: currentUserId.value,
                    timestamp: new Date().toISOString(),
                    selectedScene: props.selectedScene,
                    selectedDifficulty: props.selectedDifficulty
                };

                proxy.$http.post('/messages', aiPayload)
                    .then((response) => {
                        const audioMessage = transformMessage(response.data.ai_message);
                        const textMessage = JSON.parse(JSON.stringify(audioMessage))
                        // 传递到后台 获取音频
                        // Fetch audio from the backend
                        proxy.$http.post('/transcribeToVoice', { text: audioMessage.content })
                            .then((audioResponse) => {
                                const audioUrl = audioResponse.data.audio_url;
                                audioMessage.files = [{
                                    name: 'Audio Message',
                                    size: 0,
                                    type: 'audio/mpeg',
                                    audio: true,
                                    duration: 0, // Optionally set duration if available
                                    url: audioUrl,
                                    preview: '',
                                    progress: 100
                                }];
                                messages.value = [...messages.value, audioMessage];

                                if (props.showText) {
                                    messages.value = [...messages.value, textMessage];
                                }
                            })
                            .catch((error) => {
                                console.error('Error fetching audio:', error);
                            });
                    })
                    .catch((error) => {
                        console.error('Error sending AI message:', error);
                    });
            })
            .catch((error) => {
                console.error('Error sending audio message:', error);
            });
    } else {
        proxy.$http.post('/messages', payload)
            .then((response) => {
                const audioMessage = transformMessage(response.data.ai_message);
                const textMessage = JSON.parse(JSON.stringify(audioMessage))
                // 传递到后台 获取音频
                // Fetch audio from the backend
                proxy.$http.post('/transcribeToVoice', { text: audioMessage.content })
                    .then((audioResponse) => {
                        const audioUrl = audioResponse.data.audio_url;
                        audioMessage.files = [{
                            name: 'Audio Message',
                            size: 0,
                            type: 'audio/mpeg',
                            audio: true,
                            duration: 0, // Optionally set duration if available
                            url: audioUrl,
                            preview: '',
                            progress: 100
                        }];
                        messages.value = [...messages.value, audioMessage];

                        if (props.showText) {
                            messages.value = [...messages.value, textMessage];
                        }
                    })
                    .catch((error) => {
                        console.error('Error fetching audio:', error);
                    });


            })
            .catch((error) => {
                console.error('Error sending message:', error);
            });

        // Optimistic UI update for text messages
        if (message.type !== 'audio') {
            messages.value = [
                ...messages.value,
                {
                    _id: messages.value.length,
                    content: message.content,
                    senderId: currentUserId.value,
                    timestamp: new Date().toString().substring(16, 21),
                    date: new Date().toDateString()
                }
            ];
        }
    }
};

const sendFirstMessage = (message) => {
    const payload = {
        content: message.content,
        senderId: currentUserId.value,
        timestamp: new Date().toISOString(),
        selectedScene: props.selectedScene,
        selectedDifficulty: props.selectedDifficulty
    };

    let formData = new FormData();
    formData.append('content', message.content);
    formData.append('senderId', currentUserId.value);
    formData.append('timestamp', new Date().toISOString());
    formData.append('selectedScene', JSON.stringify(props.selectedScene));
    formData.append('selectedDifficulty', props.selectedDifficulty);

    if (message.files && message.files.length > 0 && message.files[0].audio) {
        formData.append('audio_file', message.files[0].blob, message.files[0].name);

        proxy.$http.post('/transcribe', formData)
            .then((response) => {
                const transcription = response.data.transcription;
                const userMessage = transformMessage({
                    message_id: messages.value.length,
                    content: transcription,
                    is_user: true,
                    timestamp: new Date().toISOString()
                });
                messages.value = [...messages.value, userMessage];

                // Optionally send the transcription as a message to get a response from AI
                const aiPayload = {
                    content: transcription,
                    senderId: currentUserId.value,
                    timestamp: new Date().toISOString(),
                    selectedScene: props.selectedScene,
                    selectedDifficulty: props.selectedDifficulty
                };

                proxy.$http.post('/messages/first', aiPayload)
                    .then((response) => {
                        const audioMessage = transformMessage(response.data.ai_message);
                        const textMessage = JSON.parse(JSON.stringify(audioMessage))
                        // 传递到后台 获取音频
                        // Fetch audio from the backend
                        proxy.$http.post('/transcribeToVoice', { text: audioMessage.content })
                            .then((audioResponse) => {
                                const audioUrl = audioResponse.data.audio_url;
                                audioMessage.files = [{
                                    name: 'Audio Message',
                                    size: 0,
                                    type: 'audio/mpeg',
                                    audio: true,
                                    duration: 0, // Optionally set duration if available
                                    url: audioUrl,
                                    preview: '',
                                    progress: 100
                                }];
                                messages.value = [...messages.value, audioMessage];

                                if (props.showText) {
                                    messages.value = [...messages.value, textMessage];
                                }
                            })
                            .catch((error) => {
                                console.error('Error fetching audio:', error);
                            });
                    })
                    .catch((error) => {
                        console.error('Error sending AI message:', error);
                    });
            })
            .catch((error) => {
                console.error('Error sending audio message:', error);
            });
    } else {
        proxy.$http.post('/messages/first', payload)
            .then((response) => {
                const audioMessage = transformMessage(response.data.ai_message);
                const textMessage = JSON.parse(JSON.stringify(audioMessage))
                // 传递到后台 获取音频
                // Fetch audio from the backend
                proxy.$http.post('/transcribeToVoice', { text: audioMessage.content })
                    .then((audioResponse) => {
                        const audioUrl = audioResponse.data.audio_url;
                        audioMessage.files = [{
                            name: 'Audio Message',
                            size: 0,
                            type: 'audio/mpeg',
                            audio: true,
                            duration: 0, // Optionally set duration if available
                            url: audioUrl,
                            preview: '',
                            progress: 100
                        }];
                        messages.value = [...messages.value, audioMessage];

                        if (props.showText) {
                            messages.value = [...messages.value, textMessage];
                        }
                    })
                    .catch((error) => {
                        console.error('Error fetching audio:', error);
                    });


            })
            .catch((error) => {
                console.error('Error sending message:', error);
            });

    }
};

// Watch for changes in selectedScene and update room name
watch(
    () => props.selectedScene,
    (newScene) => {
        if (newScene && newScene.name) {
            rooms.value[0].roomName = `${newScene.name}`;
        }
    },
    { immediate: true }
);

watch(
    () => props.selectedDifficulty,
    () => {
        sendFirstMessage({content:'hello'})
    }
);

// Transformation function to fit the desired message format
const transformMessage = (message) => {
    return {
        _id: message.message_id,
        content: message.content,
        senderId: message.is_user ? localStorage.getItem('user_id') : 'AI',
        username: message.is_user ? localStorage.getItem('username') : 'AI',
        timestamp: new Date(message.timestamp).toString().substring(16, 21),
        date: new Date(message.timestamp).toDateString()
    };
};

// Fetch messages when the component is mounted
onMounted(() => {
    proxy.$http.get('/messages')
        .then((response) => {
            messages.value = response.data.map(transformMessage);
            messagesLoaded.value = true;
        })
        .catch((error) => {
            console.error('Error fetching messages:', error);
            messagesLoaded.value = true;
        });
});


</script>

<style scoped></style>