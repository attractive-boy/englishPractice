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
        <el-form-item >
          <el-button class="login-btn" type="primary" @click="login()">登录</el-button>
        </el-form-item>
        <el-form-item class="switch-btn">
          <el-button @click="switchToPractice()">{{ switchText }}</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, getCurrentInstance  } from 'vue';
import { ElMessage } from 'element-plus';
import { router } from '@/router/index';

const form = ref({
  username: '',
  password: ''
});

const title = ref("英语练习管理系统");
const switchText = ref("切换到练习平台");

const { proxy } = getCurrentInstance() as any;

// 登录方法
const login = async () => {
  try {
    const response = await proxy.$http.post('/auth/login', form.value);
    ElMessage.success(response.data.message);
    //本地存储 role 判断跳转
    localStorage.setItem('role', response.data.role);
    localStorage.setItem('user_id', response.data.user_id);
    localStorage.setItem('username', response.data.username);

    if (response.data.role == "student") {
      router.push('/Communicate');
    }else if (response.data.role == "admin") {
      router.push('/StudentManager');
    }else{
      router.push('/UserInfo');
    }
  } catch (error) {
    ElMessage.error(error.response.data.message || '登录失败');
  }
};

// 切换到练习平台的方法
const switchToPractice = () => {
  if(title.value === "英语练习管理系统"){
    title.value = "英语练习平台"
    switchText.value = "切换到管理平台"
  }else{
    title.value = "英语练习管理系统"
    switchText.value = "切换到练习平台"
  }
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

.switch-btn :deep() .el-form-item__content .el-button {
  width: 100%;
}
</style>
