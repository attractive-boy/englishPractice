<template>
  <div>
    <el-button type="primary" @click="openDialog(null)" style="width:100%;margin-bottom: 20px;">生成学习计划</el-button>
    <el-table :data="plans" style="width: 100%">
      <el-table-column prop="content" label="内容" show-overflow-tooltip></el-table-column>
      <el-table-column prop="start_date" label="开始日期"></el-table-column>
      <el-table-column prop="end_date" label="结束日期"></el-table-column>
      <el-table-column prop="status" label="状态"></el-table-column>
      <el-table-column prop="priority" label="优先级"></el-table-column>
      <el-table-column prop="is_public" label="公开"></el-table-column>
      <el-table-column prop="category" label="类别"></el-table-column>
      <el-table-column label="操作">
        <template v-slot="scope">
          <el-button size="mini" @click="openDialog(scope.row)">编辑</el-button>
          <el-button size="mini" type="danger" @click="deletePlan(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="计划">
      <el-form :model="currentPlan">
        <el-form-item label="内容">
          <el-input v-model="currentPlan.content" type="textarea"></el-input>
        </el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker v-model="currentPlan.start_date" type="date" placeholder="选择开始日期"></el-date-picker>
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker v-model="currentPlan.end_date" type="date" placeholder="选择结束日期"></el-date-picker>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="currentPlan.status" placeholder="选择状态">
            <el-option label="活跃" value="active"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已取消" value="canceled"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="优先级">
          <el-input-number v-model="currentPlan.priority"></el-input-number>
        </el-form-item>
        <el-form-item label="公开">
          <el-switch v-model="currentPlan.is_public"></el-switch>
        </el-form-item>
        <el-form-item label="类别">
          <el-input v-model="currentPlan.category"></el-input>
        </el-form-item>
      </el-form>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="savePlan">保存</el-button>
        <el-button type="primary" @click="generatePlan" v-if="!isEdit">重新生成</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, getCurrentInstance } from 'vue';
import { ElMessageBox, ElMessage } from 'element-plus';
import 'element-plus/dist/index.css';
import { ElLoading } from 'element-plus'

const { proxy } = getCurrentInstance();

const plans = ref([]);
const dialogVisible = ref(false);
const currentPlan = ref({
  content: '',
  start_date: '',
  end_date: '',
  status: 'active',
  priority: 0,
  is_public: false,
  category: ''
});
const isEdit = ref(false);

const fetchPlans = async () => {
  try {
    const response = await proxy.$http.get('/plans');
    plans.value = response.data;
  } catch (error) {
    console.error('Error fetching plans:', error);
  }
};

const openDialog = async (plan) => {
  if (plan) {
    currentPlan.value = { ...plan };
    isEdit.value = true;
  } else {
    await generatePlan();
  }
  dialogVisible.value = true;
};

const generatePlan = async () => {
  const loading = ElLoading.service({
    lock: true,
    text: 'Loading',
    background: 'rgba(0, 0, 0, 0.7)',
  })
  try {
    const response = await proxy.$http.post('/plans/generate');
    currentPlan.value = response.data
    isEdit.value = false;
  } catch (error) {
    if (error.response && error.response.status === 404) {
      console.error('生成计划时出错: 暂无记录');
      ElMessage.error('生成计划时出错: 暂无聊天记录，请先进行答疑聊天');
    } else {
      console.error('生成计划时出错:', error);
    }
  }
  loading.close();
};


const savePlan = async () => {
  try {
    if (isEdit.value) {
      await proxy.$http.put(`/plans/${currentPlan.value.id}`, currentPlan.value);
      ElMessage.success('计划更新成功');
    } else {
      const response = await proxy.$http.post('/plans', currentPlan.value);
      plans.value.push(response.data);
      ElMessage.success('计划创建成功');
    }
    dialogVisible.value = false;
    fetchPlans();
  } catch (error) {
    console.error('保存计划时出错:', error);
    ElMessage.error('保存计划失败');
  }
};

const deletePlan = (id) => {
  ElMessageBox.confirm('您确定要删除这个计划吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    try {
      await proxy.$http.delete(`/plans/${id}`);
      ElMessage.success('计划删除成功');
      fetchPlans();
    } catch (error) {
      console.error('删除计划时出错:', error);
      ElMessage.error('删除计划失败');
    }
  }).catch(() => {
    ElMessage.info('已取消删除');
  });
};

onMounted(fetchPlans);
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
</style>
