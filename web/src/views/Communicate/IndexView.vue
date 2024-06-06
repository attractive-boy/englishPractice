<template>
  
    <div>
      <vue-advanced-chat height="75vh" current-user-id="User" :rooms="JSON.stringify(rooms)" :rooms-loaded="true"
        :messages="JSON.stringify(messages)" :single-room="true" :messages-loaded="messagesLoaded" :show-files="false"
        :show-audio="false" @send-message="sendMessage($event.detail[0])" @fetch-messages="fetchMessages()" />
    </div>
  
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { register } from 'vue-advanced-chat';
import { getCurrentInstance } from 'vue';
import { ElLoading } from 'element-plus'
register();

const { proxy } = getCurrentInstance();

const rooms = ref([
  {
    roomId: '1',
    roomName: 'Room 1',
    avatar: 'https://66.media.tumblr.com/avatar_c6a8eae4303e_512.pnj',
    users: [
      { _id: 'User', username: 'User' },
      { _id: 'AI', username: 'AI' }
    ]
  }
]);
const messages = ref([]);
const messagesLoaded = ref(false);

const fetchMessages = () => {
  messagesLoaded.value = false;

  // use timeout to imitate async server fetched data
  setTimeout(() => {
    messagesLoaded.value = true;
  }
  );
};

const sendMessage = (message) => {
  const loading = ElLoading.service({
    lock: true,
    text: 'Loading',
    background: 'rgba(0, 0, 0, 0.7)',
  })
  const payload = {
    question: message.content,
    senderId: 'User',
    timestamp: new Date().toISOString(),
  };

  messages.value = [
    ...messages.value,
    {
      _id: messages.value.length,
      content: message.content,
      senderId: 'User',
      timestamp: new Date().toString().substring(16, 21),
      date: new Date().toDateString()
    }
  ];

  proxy.$http.post('/chat_records', payload)
    .then((response) => {
      const newMessage = {
        _id: messages.value.length,
        content: response.data.answer,
        senderId: 'AI',
        username: 'AI',
        timestamp: new Date().toString().substring(16, 21),
        date: new Date().toDateString()
      };
      messages.value = [...messages.value, newMessage];
      loading.close()
    })
    .catch((error) => {
      console.error('Error sending message:', error);
    });
};

</script>

<style scoped></style>
