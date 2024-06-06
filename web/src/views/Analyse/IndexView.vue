<template>
  <div>
    <el-button type="primary" @click="openDialog(null)" style="width:100%;margin-bottom: 20px;">生成学习报告和建议</el-button>
    <el-table :data="reports" style="width: 100%">
      <el-table-column prop="learning_report" label="学习报告" show-overflow-tooltip></el-table-column>
      <el-table-column prop="learning_suggestions" label="学习建议" show-overflow-tooltip></el-table-column>
      <el-table-column prop="created_at" label="创建日期"></el-table-column>
      <el-table-column label="操作">
        <template v-slot="scope">
          <el-button size="mini" @click="openDialog(scope.row)">编辑</el-button>
          <el-button size="mini" type="danger" @click="deleteReport(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="学习报告">
      <el-form :model="currentReport">
        <el-form-item label="学习报告">
          <el-input v-model="currentReport.learning_report" type="textarea" rows="10"></el-input>
        </el-form-item>
        <el-form-item label="学习建议">
          <el-input v-model="currentReport.learning_suggestions" type="textarea" rows="10"></el-input>
        </el-form-item>
      </el-form>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveReport">保存</el-button>
        <el-button type="primary" @click="generateReport" v-if="!isEdit">重新生成</el-button>
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

const reports = ref([]);
const dialogVisible = ref(false);
const currentReport = ref({
  learning_report: '',
  learning_suggestions: ''
});
const isEdit = ref(false);

const fetchReports = async () => {
  try {
    const response = await proxy.$http.get('/reports');
    reports.value = response.data;
  } catch (error) {
    console.error('Error fetching reports:', error);
  }
};

const openDialog = async (report) => {
  if (report) {
    currentReport.value = { ...report };
    isEdit.value = true;
  } else {
    await generateReport();
  }
  dialogVisible.value = true;
};

const generateReport = async () => {
  const loading = ElLoading.service({
    lock: true,
    text: 'Loading',
    background: 'rgba(0, 0, 0, 0.7)',
  })
  try {
    const response = await proxy.$http.post('/reports/generate');
    currentReport.value = response.data;
    isEdit.value = false;
  } catch (error) {
    if (error.response && error.response.status === 404) {
      console.error('生成报告时出错: 暂无记录');
      ElMessage.error('生成报告时出错: 暂无聊天记录，请先进行答疑聊天');
    } else {
      console.error('生成报告时出错:', error);
    }
  }
  loading.close()
};

const saveReport = async () => {
  try {
    if (isEdit.value) {
      await proxy.$http.put(`/reports/${currentReport.value.id}`, currentReport.value);
      ElMessage.success('学习报告更新成功');
    } else {
      const response = await proxy.$http.post('/reports', currentReport.value);
      reports.value.push(response.data);
      ElMessage.success('学习报告创建成功');
    }
    dialogVisible.value = false;
    fetchReports();
  } catch (error) {
    console.error('保存学习报告时出错:', error);
    ElMessage.error('保存学习报告失败');
  }
};

const deleteReport = (id) => {
  ElMessageBox.confirm('您确定要删除这个学习报告吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    try {
      await proxy.$http.delete(`/reports/${id}`);
      ElMessage.success('学习报告删除成功');
      fetchReports();
    } catch (error) {
      console.error('删除学习报告时出错:', error);
      ElMessage.error('删除学习报告失败');
    }
  }).catch(() => {
    ElMessage.info('已取消删除');
  });
};

onMounted(fetchReports);
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
</style>
