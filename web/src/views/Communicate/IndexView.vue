<template>
  <div class="container">
    <el-dialog v-model="dialogVisible" title="选择场景和难度" width="50%">
      <div class="scene-selection">
        <h3>选择场景</h3>
        <div class="cards">
          <el-card 
            v-for="scene in scenes" 
            :key="scene" 
            class="card" 
            :class="{ selected: scene === selectedScene }" 
            @click="selectScene(scene)">
            <h4>{{ scene }}</h4>
          </el-card>
        </div>
      </div>
      <div class="difficulty-selection">
        <h3>选择难度</h3>
        <el-select v-model="selectedDifficulty" placeholder="请选择难度" style="width: 100%">
          <el-option v-for="difficulty in difficulties" :key="difficulty" :label="difficulty" :value="difficulty"></el-option>
        </el-select>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmSelection">确认</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, getCurrentInstance } from 'vue';
import { ElMessage } from 'element-plus';

const { proxy } = getCurrentInstance() as any;

const dialogVisible = ref(true);
const selectedScene = ref('');
const selectedDifficulty = ref('');

const scenes = [
  '旅行咨询',
  '咨询租房',
  '夏季音乐节',
  '学生就业咨询',
  '图书馆资源申请'
];

const difficulties = [
  '英语四级',
  '英语六级',
  '雅思',
  '托福'
];

const selectScene = (scene: string) => {
  selectedScene.value = scene;
};

const confirmSelection = () => {
  if (!selectedScene.value || !selectedDifficulty.value) {
    ElMessage.error('请选择场景和难度');
    return;
  }
  ElMessage.success(`您选择了${selectedScene.value}和${selectedDifficulty.value}`);
  dialogVisible.value = false;
};

onMounted(() => {
  dialogVisible.value = true;
});
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
