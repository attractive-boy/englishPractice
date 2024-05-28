<template>
  <div style="app-header">
    <el-menu :default-active="activeIndex" mode="horizontal" :ellipsis="false" class="el-menu" @select="handleSelect">
      <el-menu-item index="0" class="header-title">
        <h4>{{ title }}</h4>
      </el-menu-item>
      <div class="flex-grow" />
      <el-menu-item v-for="(item, index) in routes" :key="index" :index="item.path">{{
        item.meta.title
      }}</el-menu-item>
    </el-menu>
  </div>
</template>

<script setup >
import { ref, shallowRef, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const role = ref(localStorage.getItem('role'))
const title = ref(role.value === 'student' ? '英语练习平台' : '英语练习管理系统')
const activeIndex = ref(role.value === 'student' ? '英语练习平台' : '/StudentManager')

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

const routes = ref([])

const changeRoute = () => {
  routes.value = router.getRoutes().filter((route) => {
    return route.meta && route.meta.title && route.meta.role.includes(role.value)
  })

  routes.value = routes.value.sort((a, b) => {
    return a.meta.orderNum - b.meta.orderNum
  })
}

const handleStorageChange = (event) => {
  if (event.key === 'role') {
    role.value = localStorage.getItem('role')
    title.value = role.value === 'student' ? '英语练习平台' : '英语练习管理系统'
    activeIndex.value = role.value === 'student' ? '英语练习平台' : '/StudentManager'
    changeRoute()
  }
}

onMounted(() => {
  window.addEventListener('storage', handleStorageChange)
  changeRoute()
})

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
