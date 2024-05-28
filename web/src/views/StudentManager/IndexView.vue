<template>
  <div class="student-management">
    <el-button type="primary" @click="showAddStudentDialog">添加学生</el-button>
    <el-table :data="students" style="width: 100%">
      <el-table-column prop="name" label="姓名"></el-table-column>
      <el-table-column prop="gender" label="性别"></el-table-column>
      <el-table-column prop="college" label="学院"></el-table-column>
      <el-table-column prop="major" label="专业"></el-table-column>
      <el-table-column prop="class_name" label="班级"></el-table-column>
      <el-table-column prop="phone" label="电话"></el-table-column>
      <el-table-column prop="email" label="邮箱"></el-table-column>
      <el-table-column label="操作">
        <template v-slot="scope">
          <el-button size="mini" @click="showEditStudentDialog(scope.row)">编辑</el-button>
          <el-button size="mini" type="danger" @click="deleteStudent(scope.row.student_id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="addStudentDialogVisible" title="添加学生">
      <el-form :model="newStudent" label-width="100">
        <el-form-item label="用户名" >
          <el-input v-model="newStudent.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" >
          <el-input type="password" v-model="newStudent.password"></el-input>
        </el-form-item>
        <el-form-item label="姓名" >
          <el-input v-model="newStudent.name"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-select v-model="newStudent.gender" placeholder="请选择性别">
            <el-option label="男" value="male"></el-option>
            <el-option label="女" value="female"></el-option>
            <el-option label="其他" value="other"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="学院">
          <el-input v-model="newStudent.college"></el-input>
        </el-form-item>
        <el-form-item label="专业">
          <el-input v-model="newStudent.major"></el-input>
        </el-form-item>
        <el-form-item label="班级" v-if="role == 'admin'">
          <el-input v-model="newStudent.class_name"></el-input>
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="newStudent.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="newStudent.email"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addStudentDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="addStudent">确认</el-button>
      </span>
    </el-dialog>

    <el-dialog v-model="editStudentDialogVisible" title="编辑学生">
      <el-form :model="currentStudent" label-width="100">
        <el-form-item label="姓名">
          <el-input v-model="currentStudent.name"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-input v-model="currentStudent.gender"></el-input>
        </el-form-item>
        <el-form-item label="学院">
          <el-input v-model="currentStudent.college"></el-input>
        </el-form-item>
        <el-form-item label="专业">
          <el-input v-model="currentStudent.major"></el-input>
        </el-form-item>
        <el-form-item label="班级" v-if="role == 'admin'">
          <el-input v-model="currentStudent.class_name"></el-input>
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="currentStudent.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="currentStudent.email"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editStudentDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="updateStudent">确认</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script setup >
import { ref, onMounted,getCurrentInstance } from 'vue';
import { ElMessage } from 'element-plus';
import { router } from '@/router/index';

const { proxy } = getCurrentInstance() as any;

const students = ref([]);
const newStudent = ref({
  username: '',
  password: '',
  name: '',
  gender: '',
  college: '',
  major: '',
  class_name: '',
  phone: '',
  email: '',
});
const currentStudent = ref({});
const addStudentDialogVisible = ref(false);
const editStudentDialogVisible = ref(false);
const role = localStorage.getItem('role')

const fetchStudents = async () => {
  try {
    const response = await proxy.$http.get('/students');
    students.value = response.data;
  } catch (error) {
    ElMessage.error('Failed to fetch students');
  }
};

const addStudent = async () => {
  try {
    await proxy.$http.post('/students', newStudent.value);
    ElMessage.success('Student added successfully');
    addStudentDialogVisible.value = false;
    fetchStudents();
  } catch (error) {
    ElMessage.error('Failed to add student');
  }
};

const showAddStudentDialog = () => {
  newStudent.value = {
    username: '',
    password: '',
    name: '',
    gender: '',
    college: '',
    major: '',
    class_name: '',
    phone: '',
    email: '',
  };
  addStudentDialogVisible.value = true;
};

const showEditStudentDialog = (student) => {
  currentStudent.value = { ...student };
  editStudentDialogVisible.value = true;
};

const updateStudent = async () => {
  try {
    await proxy.$http.put(`/students/${currentStudent.value.student_id}`, currentStudent.value);
    ElMessage.success('Student updated successfully');
    editStudentDialogVisible.value = false;
    fetchStudents();
  } catch (error) {
    ElMessage.error('Failed to update student');
  }
};

const deleteStudent = async (student_id) => {
  try {
    await proxy.$http.delete(`/students/${student_id}`);
    ElMessage.success('Student deleted successfully');
    fetchStudents();
  } catch (error) {
    ElMessage.error('Failed to delete student');
  }
};

onMounted(() => {
  fetchStudents();
});
</script>

<style scoped>
.student-management {
  padding: 20px;
}

.el-table .el-button {
  margin-right: 10px;
}
</style>
