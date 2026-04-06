<template>
  <div class="about-editor">
    <!-- Hero 区域 -->
    <div class="form-section">
      <h3>Hero 区域</h3>
      <div class="form-row">
        <div class="form-group">
          <label>小标签</label>
          <input v-model="content.hero.eyebrow" type="text" @input="emitUpdate" />
        </div>
        <div class="form-group">
          <label>主标题</label>
          <input v-model="content.hero.title" type="text" @input="emitUpdate" />
        </div>
      </div>
      <div class="form-group">
        <label>副标题</label>
        <input v-model="content.hero.subtitle" type="text" @input="emitUpdate" />
      </div>
      
      <div class="sub-section">
        <h4>徽章列表</h4>
        <div class="items-list">
          <div v-for="(badge, index) in content.hero.badges" :key="index" class="item-row">
            <input v-model="badge.icon" placeholder="图标名" @input="emitUpdate" />
            <input v-model="badge.text" placeholder="文字" class="flex-1" @input="emitUpdate" />
            <button class="remove-btn" @click="removeBadge(index)">×</button>
          </div>
        </div>
        <button class="add-btn" @click="addBadge">+ 添加徽章</button>
      </div>
    </div>

    <!-- 价值观区域 -->
    <div class="form-section">
      <h3>价值观</h3>
      <div class="form-row">
        <div class="form-group">
          <label>标题</label>
          <input v-model="content.values.title" type="text" @input="emitUpdate" />
        </div>
        <div class="form-group">
          <label>副标题</label>
          <input v-model="content.values.subtitle" type="text" @input="emitUpdate" />
        </div>
      </div>
      
      <div class="sub-section">
        <h4>价值观卡片</h4>
        <div class="cards-grid">
          <div v-for="(item, index) in content.values.items" :key="index" class="card-editor">
            <div class="card-header">
              <span>卡片 {{ index + 1 }}</span>
              <button class="remove-btn small" @click="removeValue(index)">×</button>
            </div>
            <ImageUploadField
              v-model="item.image"
              label="图标图片"
              hint="上传图片后前台将优先显示图片"
              @update:model-value="emitUpdate"
            />
            <input v-model="item.title" placeholder="标题" @input="emitUpdate" />
            <textarea v-model="item.description" placeholder="描述" rows="3" @input="emitUpdate"></textarea>
          </div>
        </div>
        <button class="add-btn" @click="addValue">+ 添加价值观</button>
      </div>
    </div>

    <!-- 四大星系 -->
    <div class="form-section">
      <h3>四大星系</h3>
      <div class="form-row">
        <div class="form-group">
          <label>标题</label>
          <input v-model="content.groups.title" type="text" @input="emitUpdate" />
        </div>
        <div class="form-group">
          <label>副标题</label>
          <input v-model="content.groups.subtitle" type="text" @input="emitUpdate" />
        </div>
      </div>
      
      <div class="sub-section">
        <h4>小组列表</h4>
        <div class="cards-grid cols-2">
          <div v-for="(group, index) in content.groups.items" :key="index" class="card-editor">
            <div class="card-header">
              <span>{{ group.name || `小组 ${index + 1}` }}</span>
              <button class="remove-btn small" @click="removeGroup(index)">×</button>
            </div>
            <input v-model="group.name" placeholder="名称" @input="emitUpdate" />
            <input v-model="group.tag" placeholder="标签" @input="emitUpdate" />
            <textarea v-model="group.description" placeholder="描述" rows="2" @input="emitUpdate"></textarea>
          </div>
        </div>
        <button class="add-btn" @click="addGroup">+ 添加小组</button>
      </div>
    </div>

    <!-- 时间线 -->
    <div class="form-section">
      <h3>时间线</h3>
      <div class="form-row">
        <div class="form-group">
          <label>小标签</label>
          <input v-model="content.timeline.eyebrow" type="text" @input="emitUpdate" />
        </div>
        <div class="form-group">
          <label>标题</label>
          <input v-model="content.timeline.title" type="text" @input="emitUpdate" />
        </div>
      </div>
      
      <div class="sub-section">
        <h4>时间节点</h4>
        <div class="items-list vertical">
          <div v-for="(item, index) in content.timeline.items" :key="index" class="timeline-item">
            <div class="item-header">
              <input v-model="item.year" placeholder="年份" class="year-input" @input="emitUpdate" />
              <button class="remove-btn small" @click="removeTimelineItem(index)">×</button>
            </div>
            <input v-model="item.title" placeholder="标题" @input="emitUpdate" />
            <textarea v-model="item.description" placeholder="描述" rows="2" @input="emitUpdate"></textarea>
          </div>
        </div>
        <button class="add-btn" @click="addTimelineItem">+ 添加时间节点</button>
      </div>
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
import { reactive, watch, onMounted } from 'vue'
import ImageUploadField from '../ImageUploadField.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue'])

const defaultContent = {
  hero: { eyebrow: '', title: '', subtitle: '', badges: [] },
  values: { title: '', subtitle: '', items: [] },
  groups: { title: '', subtitle: '', items: [] },
  timeline: { eyebrow: '', title: '', items: [] },
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

function addBadge() {
  content.hero.badges.push({ icon: '', text: '' })
  emitUpdate()
}

function removeBadge(index) {
  content.hero.badges.splice(index, 1)
  emitUpdate()
}

function addValue() {
  content.values.items.push({ icon: '', image: '', title: '', description: '' })
  emitUpdate()
}

function removeValue(index) {
  content.values.items.splice(index, 1)
  emitUpdate()
}

function addGroup() {
  content.groups.items.push({ name: '', tag: '', description: '' })
  emitUpdate()
}

function removeGroup(index) {
  content.groups.items.splice(index, 1)
  emitUpdate()
}

function addTimelineItem() {
  content.timeline.items.push({ year: '', title: '', description: '' })
  emitUpdate()
}

function removeTimelineItem(index) {
  content.timeline.items.splice(index, 1)
  emitUpdate()
}
</script>

<style scoped>
.about-editor {
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

.sub-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid var(--panel-border);
}

.sub-section h4 {
  margin: 0 0 16px;
  font-size: 14px;
  font-weight: 500;
  color: var(--muted);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.form-group:last-child {
  margin-bottom: 0;
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
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.form-group textarea {
  resize: vertical;
  min-height: 60px;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.item-row {
  display: flex;
  gap: 12px;
  align-items: center;
}

.item-row input {
  padding: 10px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 14px;
}

.item-row input:first-child {
  width: 120px;
}

.flex-1 {
  flex: 1;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.cards-grid.cols-2 {
  grid-template-columns: repeat(2, 1fr);
}

.card-editor {
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.card-header span {
  font-size: 13px;
  font-weight: 500;
  color: var(--primary);
}

.card-editor input,
.card-editor textarea {
  padding: 10px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.card-editor input:focus,
.card-editor textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.timeline-item {
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.year-input {
  width: 100px;
  padding: 8px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--primary);
  font-size: 16px;
  font-weight: 600;
}

.timeline-item input,
.timeline-item textarea {
  padding: 10px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
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
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 6px;
  background: rgba(255, 100, 100, 0.1);
  color: #ff6b6b;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.remove-btn:hover {
  background: rgba(255, 100, 100, 0.2);
}

.remove-btn.small {
  width: 24px;
  height: 24px;
  font-size: 14px;
}
</style>
