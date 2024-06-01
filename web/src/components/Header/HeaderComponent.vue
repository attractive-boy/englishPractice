<template>
  <div style="app-header">
    <el-menu :default-active="activeIndex" mode="horizontal" :ellipsis="false" class="el-menu" @select="handleSelect">
      <el-menu-item index="0" class="header-title">
        <h4>学科答疑系统</h4>
      </el-menu-item>
      <div class="flex-grow" />
      <el-menu-item v-for="(item, index) in routes" :key="index" :index="item.path">{{
        item.meta.title
      }}</el-menu-item>
    </el-menu>
  </div>
</template>
<script setup>

import { ref, shallowRef, onBeforeUnmount, defineEmits, watch, getCurrentInstance } from 'vue'

import { router } from '@/router/index'
const role = localStorage.getItem('role')
const title = ref(  )

const activeIndex = ref('/Chat' )

watch(
  () => router.currentRoute.value.path,
  (toPath) => {
    activeIndex.value = toPath
  },
  { immediate: true, deep: true }
)

const handleSelect = (key) => {
  router.push(key)
}

let routes

const changeRoute = () => {
  routes = router.getRoutes().filter((route) => {
    return route.meta && route.meta.title
  })

  routes = routes.sort((a, b) => {
    return a.meta.orderNum - b.meta.orderNum
  })
}
changeRoute()
</script>

<style scoped>
.el-menu {
  border-radius: 10px;
  overflow: hidden;
}

.flex-grow {
  flex-grow: 1;
}
</style>
