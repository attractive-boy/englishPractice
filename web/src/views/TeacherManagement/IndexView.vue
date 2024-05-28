<template>
  <div class="teacher-management">
    <el-button type="primary" @click="showAddTeacherDialog">添加老师</el-button>
    <el-table :data="teachers" style="width: 100%">
      <el-table-column prop="name" label="姓名"></el-table-column>
      <el-table-column prop="gender" label="性别"></el-table-column>
      <el-table-column prop="college" label="学院"></el-table-column>
      <el-table-column prop="teacher_number" label="教师编号"></el-table-column>
      <el-table-column prop="phone" label="电话"></el-table-column>
      <el-table-column prop="email" label="邮箱"></el-table-column>
      <el-table-column prop="class_responsible" label="负责班级"></el-table-column>
      <el-table-column label="操作">
        <template v-slot="scope">
          <el-button size="mini" @click="showEditTeacherDialog(scope.row)">编辑</el-button>
          <el-button size="mini" type="danger" @click="deleteTeacher(scope.row.teacher_id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="addTeacherDialogVisible" title="添加老师">
      <el-form :model="newTeacher" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="newTeacher.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input type="password" v-model="newTeacher.password"></el-input>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="newTeacher.name"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-select v-model="newTeacher.gender" placeholder="请选择性别">
            <el-option label="男" value="male"></el-option>
            <el-option label="女" value="female"></el-option>
            <el-option label="其他" value="other"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="学院">
          <el-input v-model="newTeacher.college"></el-input>
        </el-form-item>
        <el-form-item label="教师编号">
          <el-input v-model="newTeacher.teacher_number"></el-input>
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="newTeacher.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="newTeacher.email"></el-input>
        </el-form-item>
        <el-form-item label="负责班级">
          <el-input v-model="newTeacher.class_responsible"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addTeacherDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="addTeacher">确认</el-button>
      </span>
    </el-dialog>

    <el-dialog v-model="editTeacherDialogVisible" title="编辑老师">
      <el-form :model="currentTeacher" label-width="100px">
        <el-form-item label="姓名">
          <el-input v-model="currentTeacher.name"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-select v-model="currentTeacher.gender" placeholder="请选择性别">
            <el-option label="男" value="male"></el-option>
            <el-option label="女" value="female"></el-option>
            <el-option label="其他" value="other"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="学院">
          <el-input v-model="currentTeacher.college"></el-input>
        </el-form-item>
        <el-form-item label="教师编号">
          <el-input v-model="currentTeacher.teacher_number"></el-input>
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="currentTeacher.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="currentTeacher.email"></el-input>
        </el-form-item>
        <el-form-item label="负责班级">
          <el-input v-model="currentTeacher.class_responsible"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editTeacherDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="updateTeacher">确认</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script setup >
import { ref, onMounted, getCurrentInstance } from 'vue';
import { ElMessage } from 'element-plus';
import { router } from '@/router/index';

const { proxy } = getCurrentInstance() as any;

const teachers = ref([]);
const newTeacher = ref({
  username: '',
  password: '',
  name: '',
  gender: '',
  college: '',
  teacher_number: '',
  phone: '',
  email: '',
  class_responsible: '',
});
const currentTeacher = ref({});
const addTeacherDialogVisible = ref(false);
const editTeacherDialogVisible = ref(false);

const fetchTeachers = async () => {
  try {
    const response = await proxy.$http.get('/teachers');
    teachers.value = response.data;
  } catch (error) {
    ElMessage.error('Failed to fetch teachers');
  }
};

const addTeacher = async () => {
  try {
    await proxy.$http.post('/teachers', newTeacher.value);
    ElMessage.success('Teacher added successfully');
    addTeacherDialogVisible.value = false;
    fetchTeachers();
  } catch (error) {
    ElMessage.error('Failed to add teacher');
  }
};

const showAddTeacherDialog = () => {
  newTeacher.value = {
    username: '',
    password: '',
    name: '',
    gender: '',
    college: '',
    teacher_number: '',
    phone: '',
    email: '',
    class_responsible: '',
  };
  addTeacherDialogVisible.value = true;
};

const showEditTeacherDialog = (teacher) => {
  currentTeacher.value = { ...teacher };
  editTeacherDialogVisible.value = true;
};

const updateTeacher = async () => {
  try {
    await proxy.$http.put(`/teachers/${currentTeacher.value.teacher_id}`, currentTeacher.value);
    ElMessage.success('Teacher updated successfully');
    editTeacherDialogVisible.value = false;
    fetchTeachers();
  } catch (error) {
    ElMessage.error('Failed to update teacher');
  }
};

const deleteTeacher = async (teacher_id) => {
  try {
    await proxy.$http.delete(`/teachers/${teacher_id}`);
    ElMessage.success('Teacher deleted successfully');
    fetchTeachers();
  } catch (error) {
    ElMessage.error('Failed to delete teacher');
  }
};

onMounted(() => {
  fetchTeachers();
});
</script>

<style scoped>
.teacher-management {
  padding: 20px;
}

.el-table .el-button {
  margin-right: 10px;
}
</style>
