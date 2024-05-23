<template>
    <div class="container">
        <el-card class="edit-student-profile">
            <h2 class="title">修改学生信息</h2>
            <el-form :model="student" ref="studentForm" label-width="120px" class="form">
                <el-form-item label="姓名" prop="name">
                    <el-input v-model="student.name" placeholder="请输入姓名"></el-input>
                </el-form-item>
                <el-form-item label="性别" prop="gender">
                    <el-select v-model="student.gender" placeholder="请选择性别">
                        <el-option label="男" value="male"></el-option>
                        <el-option label="女" value="female"></el-option>
                        <el-option label="其他" value="other"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="学院" prop="college">
                    <el-input v-model="student.college" placeholder="请输入学院"></el-input>
                </el-form-item>
                <el-form-item label="专业" prop="major">
                    <el-input v-model="student.major" placeholder="请输入专业"></el-input>
                </el-form-item>
                <el-form-item label="班级" prop="class_name">
                    <el-input v-model="student.class_name" placeholder="请输入班级"></el-input>
                </el-form-item>
                <el-form-item label="电话" prop="phone">
                    <el-input v-model="student.phone" placeholder="请输入电话"></el-input>
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="student.email" placeholder="请输入邮箱"></el-input>
                </el-form-item>
                <div class="form-actions">
                    <el-button type="primary" @click="updateStudentProfile">保存</el-button>
                    <el-button @click="resetForm">取消</el-button>
                    <el-button type="warning" @click="showPasswordDialog">修改密码</el-button>
                </div>
            </el-form>
        </el-card>

        <!-- 修改密码弹窗 -->
        <el-dialog v-model="passwordDialogVisible" title="修改密码">
            <el-form :model="passwordForm" ref="password" label-width="120px">
                <el-form-item label="当前密码" prop="current_password">
                    <el-input type="password" v-model="passwordForm.current_password" placeholder="请输入当前密码"></el-input>
                </el-form-item>
                <el-form-item label="新密码" prop="new_password">
                    <el-input type="password" v-model="passwordForm.new_password" placeholder="请输入新密码"></el-input>
                </el-form-item>
                <el-form-item label="确认新密码" prop="confirm_new_password">
                    <el-input type="password" v-model="passwordForm.confirm_new_password"
                        placeholder="请确认新密码"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="passwordDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="updatePassword">确认</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, getCurrentInstance } from 'vue';
import { ElMessage } from 'element-plus';

const { proxy } = getCurrentInstance() as any;

const student = ref({
    name: '',
    gender: '',
    college: '',
    major: '',
    class_name: '',
    phone: '',
    email: ''
});

const fetchStudentProfile = async () => {
    try {
        const response = await proxy.$http.get('/students/profile');
        student.value = response.data;
    } catch (error) {
        ElMessage.error('获取学生信息失败');
    }
};

const updateStudentProfile = async () => {
    try {
        await proxy.$http.put('/students/profile', student.value);
        ElMessage.success('学生信息更新成功');
    } catch (error) {
        ElMessage.error('更新学生信息失败');
    }
};

const resetForm = () => {
    fetchStudentProfile();
};

const showPasswordDialog = () => {
    passwordDialogVisible.value = true;
};

const passwordForm = ref({
    current_password: '',
    new_password: '',
    confirm_new_password: ''
});

const passwordDialogVisible = ref(false);

const updatePassword = async () => {
    if (passwordForm.value.new_password !== passwordForm.value.confirm_new_password) {
        ElMessage.error('新密码和确认新密码不匹配');
        return;
    }
    try {
        await proxy.$http.put('/students/password', passwordForm.value);
        ElMessage.success('密码更新成功');
        passwordDialogVisible.value = false;
    } catch (error) {
        ElMessage.error('密码更新失败');
    }
};

onMounted(() => {
    fetchStudentProfile();
});
</script>

<style scoped>
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
    padding: 20px;
}

.edit-student-profile {
    width: 600px;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #fff;
}

.title {
    text-align: center;
    margin-bottom: 20px;
    font-size: 28px;
    font-weight: bold;
    color: #333;
    border-bottom: 2px solid #fda085;
    padding-bottom: 10px;
}

.form {
    margin-top: 20px;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

.el-form-item {
    margin-bottom: 15px;
}

.el-input,
.el-select {
    width: 100%;
}

.el-button {
    border-radius: 5px;
}

.el-button--primary {
    background-color: #fda085;
    border-color: #fda085;
}

.el-button--primary:hover {
    background-color: #f6d365;
    border-color: #f6d365;
}
</style>