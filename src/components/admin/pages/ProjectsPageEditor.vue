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
            <div class="card-header-actions">
              <span v-if="project.status === 'wip'" class="status-badge wip">开发中</span>
              <span v-else-if="project.status === 'archived'" class="status-badge archived">已归档</span>
              <span v-if="project.featured" class="status-badge featured">精选</span>
              <button class="remove-btn small" @click="removeProject(index)">×</button>
            </div>
          </div>

          <div class="form-row">
            <div class="sub-field">
              <label>项目名称</label>
              <input v-model="project.name" placeholder="项目名称" @input="onNameChange(index, $event.target.value)" />
            </div>
            <div class="sub-field">
              <label>URL 标识 (slug)</label>
              <input v-model="project.slug" placeholder="如: star-chart" @input="emitUpdate" />
            </div>
          </div>

          <div class="form-row">
            <div class="sub-field">
              <label>分类</label>
              <select v-model="project.category" @change="emitUpdate">
                <option value="">选择分类</option>
                <option v-for="cat in content.filters" :key="cat" :value="cat">{{ cat }}</option>
              </select>
            </div>
            <div class="sub-field">
              <label>状态</label>
              <select v-model="project.status" @change="emitUpdate">
                <option value="active">进行中</option>
                <option value="wip">开发中</option>
                <option value="archived">已归档</option>
              </select>
            </div>
          </div>

          <div class="sub-field">
            <label>简短描述</label>
            <textarea v-model="project.description" placeholder="卡片上显示的简短描述" rows="2" @input="emitUpdate"></textarea>
          </div>

          <div class="sub-field">
            <label>详细介绍</label>
            <textarea v-model="project.longDescription" placeholder="详情页显示的完整介绍，支持换行分段" rows="4" @input="emitUpdate"></textarea>
          </div>

          <div class="form-row">
            <div class="sub-field">
              <label>内部链接</label>
              <input v-model="project.link" placeholder="/onboarding" @input="emitUpdate" />
            </div>
            <div class="sub-field">
              <label>开始时间</label>
              <input v-model="project.startDate" placeholder="2024-09" @input="emitUpdate" />
            </div>
          </div>

          <div class="form-row">
            <div class="sub-field">
              <label>GitHub 链接</label>
              <input v-model="project.githubUrl" placeholder="https://github.com/..." @input="emitUpdate" />
            </div>
            <div class="sub-field">
              <label>在线演示</label>
              <input v-model="project.demoUrl" placeholder="https://..." @input="emitUpdate" />
            </div>
          </div>

          <div class="form-row">
            <div class="sub-field">
              <label>封面样式</label>
              <select v-model="project.coverClass" @change="emitUpdate">
                <option value="aurora">Aurora 渐变</option>
                <option value="meteor">Meteor 渐变</option>
                <option value="nebula">Nebula 渐变</option>
                <option value="cosmos">Cosmos 渐变</option>
                <option value="pulse">Pulse 渐变</option>
                <option value="horizon">Horizon 渐变</option>
              </select>
            </div>
            <div class="sub-field">
              <label>精选项目</label>
              <label class="toggle-label">
                <input type="checkbox" v-model="project.featured" @change="emitUpdate" />
                <span class="toggle-text">{{ project.featured ? '是' : '否' }}</span>
              </label>
            </div>
          </div>

          <ImageUploadField
            v-model="project.coverImage"
            label="项目封面图"
            hint="上传后将优先显示图片，未上传时继续使用渐变封面"
            @update:model-value="emitUpdate"
          />

          <div class="sub-field">
            <label>技术栈（逗号分隔）</label>
            <input
              :value="project.techStack?.join(', ')"
              @input="updateTechStack(index, $event.target.value)"
              placeholder="Vue 3, Flask, MySQL"
            />
          </div>

          <div class="sub-field">
            <label>标签（逗号分隔）</label>
            <input
              :value="project.tags?.join(', ')"
              @input="updateTags(index, $event.target.value)"
              placeholder="Vue, React, Python"
            />
          </div>

          <!-- Contributors -->
          <div class="sub-field">
            <label>贡献成员</label>
            <div class="contributors-editor">
              <div v-for="(contributor, cIndex) in project.contributors" :key="cIndex" class="contributor-row">
                <div class="contributor-avatar-inline" :title="contributor.avatar ? '已匹配头像' : '未匹配头像'">
                  <img v-if="contributor.avatar" :src="contributor.avatar" :alt="contributor.name" />
                  <span v-else>{{ contributor.name?.charAt(0) || '?' }}</span>
                </div>
                <input
                  class="contributor-name-input"
                  :value="contributor.name"
                  placeholder="姓名"
                  @input="onContributorNameChange(index, cIndex, $event.target.value)"
                />
                <input
                  class="contributor-role-input"
                  v-model="contributor.role"
                  placeholder="角色"
                  @input="emitUpdate"
                />
                <button type="button" class="remove-btn small" @click.stop="removeContributor(index, cIndex)">×</button>
              </div>
              <button class="add-btn tiny" @click="addContributor(index)">+ 添加成员</button>
            </div>
          </div>

          <!-- Screenshots -->
          <div class="sub-field">
            <label>项目截图</label>
            <div class="screenshots-editor">
              <div v-for="(shot, sIndex) in project.screenshots" :key="sIndex" class="screenshot-row">
                <div class="screenshot-upload-wrapper">
                  <ImageUploadField
                    :model-value="project.screenshots[sIndex]"
                    :label="`截图 ${sIndex + 1}`"
                    hint="支持上传或填写 URL"
                    @update:model-value="updateScreenshot(index, sIndex, $event)"
                  />
                </div>
                <button class="remove-btn small" @click="removeScreenshot(index, sIndex)">×</button>
              </div>
              <button class="add-btn tiny" @click="addScreenshot(index)">+ 添加截图</button>
            </div>
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
import { api } from '../../../services/api.js'

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
  filters: ['全部', '精选'],
  projects: [],
  cta: {
    title: '',
    description: '',
    primaryButton: { text: '', link: '' },
    secondaryButton: { text: '', link: '' }
  }
}

const content = reactive({ ...defaultContent })
const membersList = ref([])

onMounted(() => {
  Object.assign(content, JSON.parse(JSON.stringify({ ...defaultContent, ...props.modelValue })))
  loadMembers()
})

async function loadMembers() {
  try {
    const data = await api.getPage('members')
    if (data?.members) {
      membersList.value = data.members
    }
  } catch {}
}

function findMemberByName(name) {
  if (!name?.trim()) return null
  const trimmed = name.trim()
  return membersList.value.find(m => m.name === trimmed) || null
}

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

function slugify(text) {
  return text
    .toString()
    .trim()
    .toLowerCase()
    .replace(/[\s_]+/g, '-')
    .replace(/[^\w一-鿿-]/g, '')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
}

function onNameChange(index, value) {
  content.projects[index].name = value
  if (!content.projects[index].slug) {
    content.projects[index].slug = slugify(value)
  }
  emitUpdate()
}

function addProject() {
  content.projects.push({
    name: '',
    slug: '',
    category: '',
    description: '',
    longDescription: '',
    link: '',
    coverImage: '',
    coverClass: 'aurora',
    tags: [],
    techStack: [],
    contributors: [],
    screenshots: [],
    githubUrl: '',
    demoUrl: '',
    status: 'active',
    featured: false,
    startDate: ''
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

function updateTechStack(index, value) {
  content.projects[index].techStack = value.split(',').map(s => s.trim()).filter(Boolean)
  emitUpdate()
}

function addContributor(projectIndex) {
  if (!content.projects[projectIndex].contributors) {
    content.projects[projectIndex].contributors = []
  }
  content.projects[projectIndex].contributors.push({ name: '', role: '', avatar: '' })
  emitUpdate()
}

function removeContributor(projectIndex, contributorIndex) {
  content.projects[projectIndex].contributors.splice(contributorIndex, 1)
  emitUpdate()
}

function onContributorNameChange(projectIndex, contributorIndex, value) {
  const contributor = content.projects[projectIndex].contributors[contributorIndex]
  contributor.name = value
  const member = findMemberByName(value)
  if (member?.avatar) {
    contributor.avatar = member.avatar
  }
  emitUpdate()
}

function addScreenshot(projectIndex) {
  if (!content.projects[projectIndex].screenshots) {
    content.projects[projectIndex].screenshots = []
  }
  content.projects[projectIndex].screenshots.push('')
  emitUpdate()
}

function updateScreenshot(projectIndex, screenshotIndex, value) {
  content.projects[projectIndex].screenshots[screenshotIndex] = value
  emitUpdate()
}

function removeScreenshot(projectIndex, screenshotIndex) {
  content.projects[projectIndex].screenshots.splice(screenshotIndex, 1)
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

.card-header > span {
  font-size: 14px;
  font-weight: 600;
  color: var(--primary);
}

.card-header-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-badge {
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 600;
}

.status-badge.wip {
  background: rgba(255, 183, 77, 0.15);
  color: #ffb74d;
}

.status-badge.archived {
  background: rgba(158, 158, 158, 0.15);
  color: #9e9e9e;
}

.status-badge.featured {
  background: rgba(255, 215, 0, 0.15);
  color: #ffd700;
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

.add-btn.tiny {
  padding: 6px 12px;
  font-size: 12px;
  margin-top: 8px;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 10px 0;
}

.toggle-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: var(--primary);
  cursor: pointer;
}

.toggle-text {
  font-size: 13px;
  color: var(--text);
}

.contributors-editor,
.screenshots-editor {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.contributor-row {
  display: flex;
  gap: 6px;
  align-items: center;
}

.contributor-avatar-inline {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  pointer-events: none;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: grid;
  place-items: center;
}

.contributor-avatar-inline img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.contributor-avatar-inline span {
  font-size: 11px;
  font-weight: 700;
  color: #04101f;
  line-height: 1;
}

.contributor-name-input {
  flex: 1;
  min-width: 0;
}

.contributor-role-input {
  flex: 1;
  min-width: 0;
}

.contributor-row input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.contributor-row input:focus {
  outline: none;
  border-color: var(--primary);
}

.screenshot-row {
  display: flex;
  gap: 8px;
  align-items: flex-start;
}

.screenshot-upload-wrapper {
  flex: 1;
  min-width: 0;
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
