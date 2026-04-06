<template>
  <div class="editor-section">
    <div class="editor-group">
      <h3 class="group-title">区块信息</h3>
      
      <div class="form-field">
        <label class="field-label">区块标题</label>
        <input 
          type="text" 
          class="field-input"
          :value="modelValue.title"
          @input="update('title', $event.target.value)"
          placeholder="如: 产品展示"
        >
      </div>
      
      <div class="form-field">
        <label class="field-label">区块描述</label>
        <textarea 
          class="field-textarea"
          :value="modelValue.description"
          @input="update('description', $event.target.value)"
          placeholder="区块的简短描述"
          rows="2"
        ></textarea>
      </div>
    </div>

    <div class="editor-group">
      <div class="group-header">
        <h3 class="group-title">产品分类</h3>
      </div>
      <div class="categories-list">
        <div 
          v-for="(category, index) in modelValue.categories" 
          :key="index"
          class="category-item"
        >
          <input 
            type="text"
            class="field-input"
            :value="category"
            @input="updateCategory(index, $event.target.value)"
            placeholder="分类名称"
          >
          <button 
            v-if="modelValue.categories.length > 1"
            class="remove-btn" 
            @click="removeCategory(index)" 
            title="删除"
          >×</button>
        </div>
        <button class="add-btn small" @click="addCategory">+ 添加分类</button>
      </div>
    </div>
    
    <div class="editor-group">
      <div class="group-header">
        <h3 class="group-title">产品章节 (Slides)</h3>
        <button class="add-btn" @click="addSlide">+ 添加章节</button>
      </div>
      
      <div class="slides-tabs">
        <button 
          v-for="(slide, index) in modelValue.slides" 
          :key="index"
          :class="['slide-tab', { active: activeSlide === index }]"
          @click="activeSlide = index"
        >
          {{ slide.tag || `章节 ${index + 1}` }}
        </button>
      </div>
      
      <div v-if="currentSlide" class="slide-editor">
        <div class="slide-header">
          <span class="slide-number">章节 {{ activeSlide + 1 }}</span>
          <button 
            v-if="modelValue.slides.length > 1"
            class="remove-btn" 
            @click="removeSlide(activeSlide)"
          >删除此章节</button>
        </div>
        
        <div class="form-field">
          <label class="field-label">章节标签</label>
          <input 
            type="text"
            class="field-input"
            :value="currentSlide.tag"
            @input="updateSlide('tag', $event.target.value)"
            placeholder="如: 精选总览"
          >
        </div>
        
        <div class="form-field">
          <label class="field-label">章节标题</label>
          <input 
            type="text"
            class="field-input"
            :value="currentSlide.title"
            @input="updateSlide('title', $event.target.value)"
            placeholder="章节的主标题"
          >
        </div>
        
        <div class="form-field">
          <label class="field-label">章节描述</label>
          <textarea 
            class="field-textarea"
            :value="currentSlide.description"
            @input="updateSlide('description', $event.target.value)"
            placeholder="章节的描述文字"
            rows="2"
          ></textarea>
        </div>

        <div class="projects-section">
          <div class="section-header">
            <h4>章节内项目</h4>
            <button class="add-btn small" @click="addProject">+ 添加项目</button>
          </div>
          
          <div class="projects-list">
            <div 
              v-for="(project, pIndex) in currentSlide.projects" 
              :key="pIndex"
              class="project-item"
            >
              <div class="project-header">
                <span class="project-name">{{ project.name || '未命名项目' }}</span>
                <button class="remove-btn small" @click="removeProject(pIndex)">×</button>
              </div>
              
              <div class="project-fields">
                <div class="form-row">
                  <div class="form-field">
                    <label class="field-label">项目名称</label>
                    <input 
                      type="text"
                      class="field-input"
                      :value="project.name"
                      @input="updateProject(pIndex, 'name', $event.target.value)"
                      placeholder="如: 星图导航"
                    >
                  </div>
                  <div class="form-field">
                    <label class="field-label">所属分类</label>
                    <select 
                      class="field-input"
                      :value="project.category"
                      @change="updateProject(pIndex, 'category', $event.target.value)"
                    >
                      <option value="">选择分类</option>
                      <option 
                        v-for="cat in modelValue.categories" 
                        :key="cat" 
                        :value="cat"
                      >{{ cat }}</option>
                    </select>
                  </div>
                </div>
                
                <div class="form-field">
                  <label class="field-label">项目描述</label>
                  <textarea 
                    class="field-textarea small"
                    :value="project.description"
                    @input="updateProject(pIndex, 'description', $event.target.value)"
                    placeholder="项目简介"
                    rows="2"
                  ></textarea>
                </div>
                
                <div class="form-row">
                  <div class="form-field">
                    <label class="field-label">链接地址</label>
                    <input 
                      type="text"
                      class="field-input"
                      :value="project.link"
                      @input="updateProject(pIndex, 'link', $event.target.value)"
                      placeholder="/pages/xxx.html"
                    >
                  </div>
                  <div class="form-field">
                    <label class="field-label">封面样式</label>
                    <select 
                      class="field-input"
                      :value="project.coverClass"
                      @change="updateProject(pIndex, 'coverClass', $event.target.value)"
                    >
                      <option value="aurora">极光 (Aurora)</option>
                      <option value="meteor">流星 (Meteor)</option>
                      <option value="nebula">星云 (Nebula)</option>
                      <option value="cosmos">宇宙 (Cosmos)</option>
                      <option value="pulse">脉冲 (Pulse)</option>
                      <option value="horizon">地平线 (Horizon)</option>
                    </select>
                  </div>
                </div>

                <div class="form-field">
                  <ImageUploadField
                    :model-value="project.coverImage || ''"
                    label="项目封面图"
                    hint="上传后将优先显示图片，未上传时使用渐变封面"
                    @update:model-value="updateProject(pIndex, 'coverImage', $event)"
                  />
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="!currentSlide.projects?.length" class="empty-state small">
            <p>暂无项目，点击上方按钮添加</p>
          </div>
        </div>
      </div>
      
      <div v-else class="empty-state">
        <p>暂无章节，点击上方按钮添加</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ImageUploadField from './ImageUploadField.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const activeSlide = ref(0)

const currentSlide = computed(() => props.modelValue.slides?.[activeSlide.value])

function update(key, value) {
  emit('update:modelValue', { ...props.modelValue, [key]: value })
}

function updateCategory(index, value) {
  const categories = [...props.modelValue.categories]
  categories[index] = value
  emit('update:modelValue', { ...props.modelValue, categories })
}

function addCategory() {
  const categories = [...props.modelValue.categories, '']
  emit('update:modelValue', { ...props.modelValue, categories })
}

function removeCategory(index) {
  const categories = props.modelValue.categories.filter((_, i) => i !== index)
  emit('update:modelValue', { ...props.modelValue, categories })
}

function updateSlide(key, value) {
  const slides = [...props.modelValue.slides]
  slides[activeSlide.value] = { ...slides[activeSlide.value], [key]: value }
  emit('update:modelValue', { ...props.modelValue, slides })
}

function addSlide() {
  const slides = [...props.modelValue.slides, {
    tag: '',
    title: '',
    description: '',
    metrics: [],
    projects: []
  }]
  emit('update:modelValue', { ...props.modelValue, slides })
  activeSlide.value = slides.length - 1
}

function removeSlide(index) {
  const slides = props.modelValue.slides.filter((_, i) => i !== index)
  emit('update:modelValue', { ...props.modelValue, slides })
  if (activeSlide.value >= slides.length) {
    activeSlide.value = Math.max(0, slides.length - 1)
  }
}

function updateProject(pIndex, key, value) {
  const slides = [...props.modelValue.slides]
  const projects = [...(slides[activeSlide.value].projects || [])]
  projects[pIndex] = { ...projects[pIndex], [key]: value }
  slides[activeSlide.value] = { ...slides[activeSlide.value], projects }
  emit('update:modelValue', { ...props.modelValue, slides })
}

function addProject() {
  const slides = [...props.modelValue.slides]
  const projects = [...(slides[activeSlide.value].projects || []), {
    category: '',
    name: '',
    description: '',
    link: '',
    coverImage: '',
    coverClass: 'aurora'
  }]
  slides[activeSlide.value] = { ...slides[activeSlide.value], projects }
  emit('update:modelValue', { ...props.modelValue, slides })
}

function removeProject(pIndex) {
  const slides = [...props.modelValue.slides]
  const projects = (slides[activeSlide.value].projects || []).filter((_, i) => i !== pIndex)
  slides[activeSlide.value] = { ...slides[activeSlide.value], projects }
  emit('update:modelValue', { ...props.modelValue, slides })
}
</script>

<style scoped>
.editor-section {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.editor-group {
  background: rgba(12, 24, 42, 0.5);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  padding: 24px;
}

.group-header,
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.group-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: var(--text);
}

.group-header .group-title {
  margin: 0;
}

.section-header h4 {
  font-size: 14px;
  font-weight: 600;
  margin: 0;
  color: var(--muted);
}

.form-field {
  margin-bottom: 16px;
}

.form-field:last-child {
  margin-bottom: 0;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.field-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--muted);
  margin-bottom: 8px;
}

.field-input,
.field-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.03);
  color: var(--text);
  font-size: 14px;
  transition: border-color 0.2s, background 0.2s;
}

.field-input:focus,
.field-textarea:focus {
  outline: none;
  border-color: var(--primary);
  background: rgba(121, 168, 255, 0.05);
}

.field-textarea {
  resize: vertical;
  min-height: 60px;
  line-height: 1.6;
}

.field-textarea.small {
  min-height: 50px;
}

select.field-input {
  cursor: pointer;
}

.add-btn {
  padding: 8px 16px;
  border: 1px solid var(--primary);
  border-radius: 8px;
  background: transparent;
  color: var(--primary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn:hover {
  background: rgba(121, 168, 255, 0.1);
}

.add-btn.small {
  padding: 6px 12px;
  font-size: 12px;
}

.categories-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.category-item {
  display: flex;
  gap: 8px;
  align-items: center;
}

.category-item .field-input {
  width: 140px;
  padding: 8px 12px;
}

.slides-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.slide-tab {
  padding: 10px 18px;
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  background: transparent;
  color: var(--muted);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.slide-tab:hover {
  background: rgba(121, 168, 255, 0.05);
}

.slide-tab.active {
  background: rgba(121, 168, 255, 0.15);
  border-color: var(--primary);
  color: var(--primary);
}

.slide-editor {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(121, 168, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
}

.slide-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--panel-border);
}

.slide-number {
  font-size: 12px;
  font-weight: 600;
  color: var(--primary);
  background: rgba(121, 168, 255, 0.1);
  padding: 4px 12px;
  border-radius: 6px;
}

.projects-section {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid var(--panel-border);
}

.projects-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.project-item {
  background: rgba(12, 24, 42, 0.5);
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  overflow: hidden;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: rgba(121, 168, 255, 0.05);
  border-bottom: 1px solid var(--panel-border);
}

.project-name {
  font-weight: 500;
  color: var(--text);
  font-size: 14px;
}

.project-fields {
  padding: 16px;
}

.remove-btn {
  padding: 6px 12px;
  border: 1px solid rgba(255, 100, 100, 0.3);
  border-radius: 6px;
  background: transparent;
  color: #ff6b6b;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-btn:hover {
  background: rgba(255, 100, 100, 0.1);
}

.remove-btn.small {
  padding: 4px 8px;
  font-size: 14px;
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--muted);
}

.empty-state.small {
  padding: 24px;
}
</style>
