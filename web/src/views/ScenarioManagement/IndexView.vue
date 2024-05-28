<template>
  <div class="scenario-management">
    <el-button type="primary" @click="showAddScenarioDialog">添加场景</el-button>
    <el-table :data="scenarios" style="width: 100%">
      <el-table-column prop="name" label="名称"></el-table-column>
      <el-table-column prop="prompt" label="提示"></el-table-column>
      <el-table-column prop="difficulty" label="难度"></el-table-column>
      <el-table-column prop="description" label="描述"></el-table-column>
      <el-table-column prop="status" label="状态"></el-table-column>
      <el-table-column label="操作">
        <template v-slot="scope">
          <el-button size="mini" @click="showEditScenarioDialog(scope.row)">编辑</el-button>
          <el-button size="mini" type="danger" @click="deleteScenario(scope.row.scenario_id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="addScenarioDialogVisible" title="添加场景">
      <el-form :model="newScenario" label-width="100px">
        <el-form-item label="名称">
          <el-input v-model="newScenario.name"></el-input>
        </el-form-item>
        <el-form-item label="提示">
          <el-input v-model="newScenario.prompt"></el-input>
        </el-form-item>
        <el-form-item label="难度">
          <el-select v-model="newScenario.difficulty" placeholder="请选择难度">
            <el-option label="CET4" value="CET4"></el-option>
            <el-option label="CET6" value="CET6"></el-option>
            <el-option label="IELTS" value="IELTS"></el-option>
            <el-option label="TOEFL" value="TOEFL"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="newScenario.description"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="newScenario.status" placeholder="请选择状态">
            <el-option label="public" value="public"></el-option>
            <el-option label="private" value="private"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addScenarioDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="addScenario">确认</el-button>
      </span>
    </el-dialog>

    <el-dialog v-model="editScenarioDialogVisible" title="编辑场景">
      <el-form :model="currentScenario" label-width="100px">
        <el-form-item label="名称">
          <el-input v-model="currentScenario.name"></el-input>
        </el-form-item>
        <el-form-item label="提示">
          <el-input v-model="currentScenario.prompt"></el-input>
        </el-form-item>
        <el-form-item label="难度">
          <el-select v-model="currentScenario.difficulty" placeholder="请选择难度">
            <el-option label="CET4" value="CET4"></el-option>
            <el-option label="CET6" value="CET6"></el-option>
            <el-option label="IELTS" value="IELTS"></el-option>
            <el-option label="TOEFL" value="TOEFL"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="currentScenario.description"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="currentScenario.status" placeholder="请选择状态">
            <el-option label="public" value="public"></el-option>
            <el-option label="private" value="private"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editScenarioDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="updateScenario">确认</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, getCurrentInstance } from 'vue';
import { ElMessage } from 'element-plus';
import { router } from '@/router/index';

const { proxy } = getCurrentInstance() as any;

const scenarios = ref([]);
const newScenario = ref({
  name: '',
  prompt: '',
  difficulty: '',
  description: '',
  status: 'public',
});
const currentScenario = ref({});
const addScenarioDialogVisible = ref(false);
const editScenarioDialogVisible = ref(false);

const fetchScenarios = async () => {
  try {
    const response = await proxy.$http.get('/scenarios');
    scenarios.value = response.data;
  } catch (error) {
    ElMessage.error('Failed to fetch scenarios');
  }
};

const addScenario = async () => {
  try {
    await proxy.$http.post('/scenarios', newScenario.value);
    ElMessage.success('Scenario added successfully');
    addScenarioDialogVisible.value = false;
    fetchScenarios();
  } catch (error) {
    ElMessage.error('Failed to add scenario');
  }
};

const showAddScenarioDialog = () => {
  newScenario.value = {
    name: '',
    prompt: '',
    difficulty: '',
    description: '',
    status: 'public',
  };
  addScenarioDialogVisible.value = true;
};

const showEditScenarioDialog = (scenario) => {
  currentScenario.value = { ...scenario };
  editScenarioDialogVisible.value = true;
};

const updateScenario = async () => {
  try {
    await proxy.$http.put(`/scenarios/${currentScenario.value.scenario_id}`, currentScenario.value);
    ElMessage.success('Scenario updated successfully');
    editScenarioDialogVisible.value = false;
    fetchScenarios();
  } catch (error) {
    ElMessage.error('Failed to update scenario');
  }
};

const deleteScenario = async (scenario_id) => {
  try {
    await proxy.$http.delete(`/scenarios/${scenario_id}`);
    ElMessage.success('Scenario deleted successfully');
    fetchScenarios();
  } catch (error) {
    ElMessage.error('Failed to delete scenario');
  }
};

onMounted(() => {
  fetchScenarios();
});
</script>

<style scoped>
.scenario-management {
  padding: 20px;
}

.el-table .el-button {
  margin-right: 10px;
}
</style>
