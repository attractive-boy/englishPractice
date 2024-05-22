<template>
  <div class="container">
    <el-dialog v-model="dialogVisible" title="选择场景和难度" width="50%">
      <div class="scene-selection">
        <h3>选择场景</h3>
        <div class="cards">
          <el-card 
            v-for="scene in scenes" 
            :key="scene.name" 
            class="card" 
            :class="{ selected: scene.name === selectedScene.name }" 
            @click="selectScene(scene)">
            <h4>{{ scene.name }}</h4>
          </el-card>
        </div>
      </div>
      <div class="difficulty-selection" v-if="selectedScene.difficulties && selectedScene.difficulties.length > 0">
        <h3>选择难度</h3>
        <el-select v-model="selectedDifficulty" placeholder="请选择难度" style="width: 100%">
          <el-option v-for="difficulty in selectedScene.difficulties" :key="difficulty" :label="difficulty" :value="difficulty"></el-option>
        </el-select>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmSelection">确认</el-button>
      </span>
    </el-dialog>


    <vue-advanced-chat
      height="75vh"
      :current-user-id="currentUserId"
      :rooms="rooms"
      :rooms-loaded="true"
      :messages="messages"
      :messages-loaded="messagesLoaded"
      @send-message="sendMessage"
      @fetch-messages="fetchMessages"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';

import { getCurrentInstance } from 'vue';
import { register } from 'vue-advanced-chat'


const { proxy } = getCurrentInstance() as any;


const dialogVisible = ref(true);
const selectedScene = ref<any>({});
const selectedDifficulty = ref('');
const scenes = ref([]);

const fetchScenes = async () => {
  try {
    const response = await proxy.$http.get('/scenarios');
    const rawData = response.data;

    // 处理数据，将相同场景下的难度整合到一起
    const sceneMap: { [key: number]: any } = {};
    rawData.forEach((item: any) => {
      if (item.name && item.difficulty && item.status == "public") { // 添加属性检查
        if (!sceneMap[item.name]) {
          sceneMap[item.name] = {
            name: item.name,
            description: item.description,
            prompt: item.prompt,
            difficulties: [item.difficulty]
          };
        } else {
          sceneMap[item.name].difficulties.push(item.difficulty);
        }
      }
    });

    scenes.value = Object.values(sceneMap);

  } catch (error) {
    ElMessage.error('获取场景列表失败');
  }
};

const selectScene = (scene: any) => {
  selectedScene.value = scene;
  selectedDifficulty.value = ''; // 重置已选择的难度
};

const confirmSelection = () => {
  if (!selectedScene.value.name || !selectedDifficulty.value) {
    ElMessage.error('请选择场景和难度');
    return;
  }
  ElMessage.success(`您选择了${selectedScene.value.name}和${selectedDifficulty.value}`);
  dialogVisible.value = false;
};

onMounted(() => {
  fetchScenes();
});



register();
const currentUserId = ref('1234');
const rooms = ref([
  {
    roomId: '1',
    roomName: 'Room 1',
    avatar: 'https://66.media.tumblr.com/avatar_c6a8eae4303e_512.pnj',
    users: [
      { _id: '1234', username: 'John Doe' },
      { _id: '4321', username: 'John Snow' }
    ]
  }
]);
const messages = ref<any[]>([]);
const messagesLoaded = ref(false);

const fetchMessages = ({ detail: [{ options = {} }] }: any) => {
  setTimeout(() => {
    if (options.reset) {
      messages.value = addMessages(true);
    } else {
      messages.value = [...addMessages(), ...messages.value];
      messagesLoaded.value = true;
    }
  });
};

const addMessages = (reset = false) => {
  const newMessages = [];

  for (let i = 0; i < 30; i++) {
    newMessages.push({
      _id: reset ? i : messages.value.length + i,
      content: `${reset ? '' : 'paginated'} message ${i + 1}`,
      senderId: '4321',
      username: 'John Doe',
      date: '13 November',
      timestamp: '10:20'
    });
  }

  return newMessages;
};

const sendMessage = ({ detail: [message] }: any) => {
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
};

const addNewMessage = () => {
  setTimeout(() => {
    messages.value = [
      ...messages.value,
      {
        _id: messages.value.length,
        content: 'NEW MESSAGE',
        senderId: '1234',
        timestamp: new Date().toString().substring(16, 21),
        date: new Date().toDateString()
      }
    ];
  }, 2000);
};
</script>

<style scoped>
.container {
  padding: 20px;
}

.scene-selection, .difficulty-selection {
  margin-bottom: 20px;
}

.cards {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.card {
  width: 120px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.card.selected {
  box-shadow: 0 0 10px rgba(0, 123, 255, 0.8);
  transform: scale(1.05);
}

.dialog-footer {
  text-align: right;
}

.el-select {
  width: 100%;
}
</style>
