<template>
  <div class="projects-editor">
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

    <!-- 筛选分类 -->
    <div class="form-section">
      <h3>筛选分类</h3>
      <div class="tags-input">
        <span v-for="(filter, index) in content.filters" :key="index" class="tag">
          {{ filter }}
          <button @click="removeFilter(index)">×</button>
        </span>
        <input 
          v-model="newFilter" 
          placeholder="添加分类..." 
          @keyup.enter="addFilter"
        />
      </div>
    </div>

    <!-- 项目列表 -->
    <div class="form-section">
      <h3>项目列表</h3>
      <div class="projects-grid">
        <div v-for="(project, index) in content.projects" :key="index" class="project-card">
          <div class="card-header">
            <span>{{ project.name || `项目 ${index + 1}` }}</span>
            <button class="remove-btn small" @click="removeProject(index)">×</button>
          </div>
          
          <div class="form-row">
            <input v-model="project.name" placeholder="项目名称" @input="emitUpdate" />
            <select v-model="project.category" @change="emitUpdate">
              <option value="">选择分类</option>
              <option v-for="cat in content.filters" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>
          
          <textarea v-model="project.description" placeholder="项目描述" rows="2" @input="emitUpdate"></textarea>
          
          <div class="form-row">
            <input v-model="project.link" placeholder="链接" @input="emitUpdate" />
            <select v-model="project.coverClass" @change="emitUpdate">
              <option value="aurora">Aurora 渐变</option>
              <option value="meteor">Meteor 渐变</option>
              <option value="nebula">Nebula 渐变</option>
              <option value="cosmos">Cosmos 渐变</option>
              <option value="pulse">Pulse 渐变</option>
              <option value="horizon">Horizon 渐变</option>
            </select>
          </div>

          <ImageUploadField
            v-model="project.coverImage"
            label="项目封面图"
            hint="上传后将优先显示图片，未上传时继续使用渐变封面"
            @update:model-value="emitUpdate"
          />
          
          <div class="sub-field">
            <label>标签（逗号分隔）</label>
            <input 
              :value="project.tags?.join(', ')" 
              @input="updateTags(index, $event.target.value)"
              placeholder="Vue, React, Python"
            />
          </div>
        </div>
      </div>
      <button class="add-btn" @click="addProject">+ 添加项目</button>
    </div>

    <!-- CTA 区域 -->
    <div class="form-section">
      <h3>CTA 区域</h3>
      <div class="form-group">
        <label>标题</label>
        <input v-model="content.cta.title" type="text" @input="emitUpdate" />
      </div>
      <div class="form-group">
        <label>描述</label>
        <textarea v-model="content.cta.description" rows="2" @input="emitUpdate"></textarea>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>主按钮文字</label>
          <input v-model="content.cta.primaryButton.text" type="text" @input="emitUpdate" />
        </div>
        <div class="form-group">
          <label>主按钮链接</label>
          <input v-model="content.cta.primaryButton.link" type="text" @input="emitUpdate" />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>次按钮文字</label>
          <input v-model="content.cta.secondaryButton.text" type="text" @input="emitUpdate" />
        </div>
        <div class="form-group">
          <label>次按钮链接</label>
          <input v-model="content.cta.secondaryButton.link" type="text" @input="emitUpdate" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch, onMounted } from 'vue'
import ImageUploadField from '../ImageUploadField.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue'])

const newFilter = ref('')

const defaultContent = {
  hero: { eyebrow: '', title: '', subtitle: '' },
  filters: ['全部'],
  projects: [],
  cta: {
    title: '',
    description: '',
    primaryButton: { text: '', link: '' },
    secondaryButton: { text: '', link: '' }
  }
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

function addFilter() {
  if (newFilter.value.trim() && !content.filters.includes(newFilter.value.trim())) {
    content.filters.push(newFilter.value.trim())
    newFilter.value = ''
    emitUpdate()
  }
}

function removeFilter(index) {
  content.filters.splice(index, 1)
  emitUpdate()
}

function addProject() {
  content.projects.push({
    name: '',
    category: '',
    description: '',
    link: '',
    coverImage: '',
    coverClass: 'aurora',
    tags: []
  })
  emitUpdate()
}

function removeProject(index) {
  content.projects.splice(index, 1)
  emitUpdate()
}

function updateTags(index, value) {
  content.projects[index].tags = value.split(',').map(s => s.trim()).filter(Boolean)
  emitUpdate()
}
</script>

<style scoped>
.projects-editor {
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
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.form-group label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
}

.form-group input,
.form-group textarea,
.form-group select {
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
  gap: 16px;
  margin-bottom: 16px;
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
  font-size: 14px;
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

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.project-card {
  padding: 20px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 14px;
  font-weight: 600;
  color: var(--primary);
}

.project-card input,
.project-card textarea,
.project-card select {
  padding: 10px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.project-card input:focus,
.project-card textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.sub-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.sub-field label {
  font-size: 12px;
  color: var(--muted);
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

.remove-btn {
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 6px;
  background: rgba(255, 100, 100, 0.1);
  color: #ff6b6b;
  font-size: 14px;
  cursor: pointer;
  flex-shrink: 0;
}

.remove-btn:hover {
  background: rgba(255, 100, 100, 0.2);
}
</style>
