<template>
  <div class="blog-editor">
    <!-- Hero 区域 -->
    <div class="form-section">
      <h3>Hero 区域</h3>
      <div class="form-group">
        <label>小标签</label>
        <input v-model="content.hero.eyebrow" type="text" @input="emitUpdate" />
      </div>
      <div class="form-group">
        <label>主标题</label>
        <input v-model="content.hero.title" type="text" @input="emitUpdate" />
      </div>
      <div class="form-group">
        <label>副标题</label>
        <input v-model="content.hero.subtitle" type="text" @input="emitUpdate" />
      </div>
    </div>

    <!-- 分类标签 -->
    <div class="form-section">
      <h3>分类标签</h3>
      <div class="tags-input">
        <span v-for="(cat, index) in content.categories" :key="index" class="tag">
          {{ cat }}
          <button @click="removeCategory(index)">×</button>
        </span>
        <input 
          v-model="newCategory" 
          placeholder="添加分类..." 
          @keyup.enter="addCategory"
        />
      </div>
    </div>

    <!-- 文章列表 -->
    <div class="form-section">
      <h3>文章列表</h3>
      <div class="posts-list">
        <div v-for="(post, index) in content.posts" :key="index" class="post-card">
          <div class="card-header">
            <span>{{ post.title || `文章 ${index + 1}` }}</span>
            <button class="remove-btn small" @click="removePost(index)">×</button>
          </div>
          
          <div class="form-group">
            <input v-model="post.title" placeholder="文章标题" @input="emitUpdate" />
          </div>
          
          <div class="form-group">
            <textarea v-model="post.excerpt" placeholder="文章摘要" rows="2" @input="emitUpdate"></textarea>
          </div>
          
          <div class="form-row">
            <select v-model="post.category" @change="emitUpdate">
              <option value="">选择分类</option>
              <option v-for="cat in content.categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
            <input v-model="post.date" type="date" @input="emitUpdate" />
          </div>
          
          <div class="form-group">
            <input v-model="post.readTime" placeholder="阅读时间 (如: 8 分钟)" @input="emitUpdate" />
          </div>

          <div class="form-group">
            <input v-model="post.link" placeholder="文章链接（可填外链或站内链接）" @input="emitUpdate" />
          </div>
        </div>
      </div>
      <button class="add-btn" @click="addPost">+ 添加文章</button>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch, onMounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue'])

const newCategory = ref('')

const defaultContent = {
  hero: { eyebrow: '', title: '', subtitle: '' },
  categories: ['全部'],
  posts: []
}

const content = reactive({ ...defaultContent })

onMounted(() => {
  Object.assign(content, JSON.parse(JSON.stringify({ ...defaultContent, ...props.modelValue })))
})

watch(() => props.modelValue, (newVal) => {
  Object.assign(content, JSON.parse(JSON.stringify({ ...defaultContent, ...newVal })))
}, { deep: true })

function emitUpdate() {
  emit('update:modelValue', JSON.parse(JSON.stringify(content)))
}

function addCategory() {
  if (newCategory.value.trim() && !content.categories.includes(newCategory.value.trim())) {
    content.categories.push(newCategory.value.trim())
    newCategory.value = ''
    emitUpdate()
  }
}

function removeCategory(index) {
  content.categories.splice(index, 1)
  emitUpdate()
}

function addPost() {
  content.posts.push({
    title: '',
    excerpt: '',
    category: '',
    date: new Date().toISOString().split('T')[0],
    readTime: '',
    link: ''
  })
  emitUpdate()
}

function removePost(index) {
  content.posts.splice(index, 1)
  emitUpdate()
}
</script>

<style scoped>
.blog-editor {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-section {
  padding: 24px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--panel-border);
  border-radius: 14px;
}

.form-section h3 {
  margin: 0 0 20px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-section h3::before {
  content: '';
  width: 4px;
  height: 16px;
  background: var(--primary);
  border-radius: 2px;
}

.form-group {
  margin-bottom: 12px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
  margin-bottom: 8px;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 14px;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 12px;
}

.form-row select,
.form-row input {
  padding: 10px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 14px;
}

.tags-input {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--panel-border);
  border-radius: 10px;
}

.tags-input .tag {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(121, 168, 255, 0.15);
  border-radius: 6px;
  font-size: 13px;
  color: var(--primary);
}

.tags-input .tag button {
  border: none;
  background: none;
  color: var(--primary);
  cursor: pointer;
  padding: 0;
}

.tags-input input {
  flex: 1;
  min-width: 120px;
  padding: 6px 12px;
  border: none;
  background: transparent;
  color: var(--text);
  font-size: 13px;
}

.tags-input input:focus {
  outline: none;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 16px;
}

.post-card {
  padding: 20px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-header span {
  font-size: 14px;
  font-weight: 600;
  color: var(--primary);
}

.add-btn {
  padding: 10px 20px;
  border: 1px dashed var(--panel-border);
  border-radius: 8px;
  background: transparent;
  color: var(--muted);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.remove-btn.small {
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 6px;
  background: rgba(255, 100, 100, 0.1);
  color: #ff6b6b;
  font-size: 14px;
  cursor: pointer;
}

.remove-btn.small:hover {
  background: rgba(255, 100, 100, 0.2);
}
</style>
