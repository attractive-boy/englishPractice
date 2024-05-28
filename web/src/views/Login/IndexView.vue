<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="login-title">{{ title }}</h2>
      <el-form ref="loginForm" :model="form" label-width="0" class="login-form">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input type="password" v-model="form.password" placeholder="密码"></el-input>
        </el-form-item>
        <el-form-item v-if="isRegistering" prop="confirmPassword">
          <el-input type="password" v-model="form.confirmPassword" placeholder="确认密码"></el-input>
        </el-form-item>
        <el-form-item v-if="isRegistering" prop="email">
          <el-input v-model="form.email" placeholder="邮箱"></el-input>
        </el-form-item>
        <el-form-item v-if="isRegistering" prop="firstName">
          <el-input v-model="form.firstName" placeholder="名字"></el-input>
        </el-form-item>
        <el-form-item v-if="isRegistering" prop="lastName">
          <el-input v-model="form.lastName" placeholder="姓氏"></el-input>
        </el-form-item>
        <el-form-item v-if="isRegistering" prop="phoneNumber">
          <el-input v-model="form.phoneNumber" placeholder="电话"></el-input>
        </el-form-item>
        <el-form-item v-if="isRegistering" prop="address">
          <el-input v-model="form.address" placeholder="地址"></el-input>
        </el-form-item>
        <el-form-item >
          <el-button class="login-btn" type="primary" @click="isRegistering ? register() : login()">{{ isRegistering ? '注册' : '登录' }}</el-button>
        </el-form-item>
        <el-form-item class="switch-btn">
          <el-button @click="switchToPractice()">{{ switchText }}</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, getCurrentInstance } from 'vue';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';

const form = ref({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  firstName: '',
  lastName: '',
  phoneNumber: '',
  address: ''
});

const title = ref("学科答疑系统");
const switchText = ref("还没有账号？ 注册");
const isRegistering = ref(false);
const { proxy } = getCurrentInstance();
const router = useRouter();

// 登录方法
const login = async () => {
  try {
    const response = await proxy.$http.post('/auth/login', form.value);
    ElMessage.success(response.data.message);
    router.push('/dashboard');
  } catch (error) {
    ElMessage.error(error.response.data.message || '登录失败');
  }
};

// 注册方法
const register = async () => {
  if (form.value.password !== form.value.confirmPassword) {
    ElMessage.error('密码和确认密码不一致');
    return;
  }

  try {
    const response = await proxy.$http.post('/auth/register', form.value);
    ElMessage.success(response.data.message);
    switchToPractice();
  } catch (error) {
    ElMessage.error(error.response.data.message || '注册失败');
  }
};

// 切换登录和注册界面
const switchToPractice = () => {
  isRegistering.value = !isRegistering.value;
  switchText.value = isRegistering.value ? "已有账号？ 登录" : "还没有账号？ 注册";
};
</script>

<style scoped>
.login-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
}

.login-box {
  width: 400px;
  padding: 20px;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.login-form {
  margin-top: 20px;
}

.login-btn {
  text-align: center;
  margin: auto;
}

.switch-btn {
  text-align: center;
  margin-top: 10px;
}

.switch-label {
  margin-right: 10px;
}

.switch-btn :deep() .el-form-item__content .el-button {
  width: 100%;
}
</style>
