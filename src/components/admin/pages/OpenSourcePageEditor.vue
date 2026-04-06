<template>
  <div class="opensource-editor">
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

    <!-- 仓库列表 -->
    <div class="form-section">
      <h3>开源仓库</h3>
      <div class="form-group">
        <label>区块标题</label>
        <input v-model="content.sections.reposTitle" type="text" @input="emitUpdate" />
      </div>
      <div class="repos-grid">
        <div v-for="(repo, index) in content.repos" :key="index" class="repo-card">
          <div class="card-header">
            <span>{{ repo.name || `仓库 ${index + 1}` }}</span>
            <button class="remove-btn small" @click="removeRepo(index)">×</button>
          </div>
          <input v-model="repo.name" placeholder="仓库名称" @input="emitUpdate" />
          <textarea v-model="repo.description" placeholder="描述" rows="2" @input="emitUpdate"></textarea>
          <div class="form-row">
            <input v-model.number="repo.stars" type="number" placeholder="Star 数" @input="emitUpdate" />
            <input v-model="repo.language" placeholder="主要语言" @input="emitUpdate" />
          </div>
          <input v-model="repo.link" placeholder="GitHub 链接" @input="emitUpdate" />
        </div>
      </div>
      <button class="add-btn" @click="addRepo">+ 添加仓库</button>
    </div>

    <!-- 技术栈 -->
    <div class="form-section">
      <h3>技术栈</h3>
      <div class="form-group">
        <label>区块标题</label>
        <input v-model="content.sections.techStackTitle" type="text" @input="emitUpdate" />
      </div>
      <div class="tags-input">
        <span v-for="(tech, index) in content.techStack" :key="index" class="tag">
          {{ tech }}
          <button @click="removeTech(index)">×</button>
        </span>
        <input 
          v-model="newTech" 
          placeholder="添加技术..." 
          @keyup.enter="addTech"
        />
      </div>
    </div>

    <!-- 贡献者 -->
    <div class="form-section">
      <h3>核心贡献者</h3>
      <div class="form-group">
        <label>区块标题</label>
        <input v-model="content.sections.contributorsTitle" type="text" @input="emitUpdate" />
      </div>
      <div class="contributors-list">
        <div v-for="(contributor, index) in content.contributors" :key="index" class="contributor-item">
          <ImageUploadField
            v-model="contributor.avatar"
            label="贡献者头像"
            hint="支持上传或填写 URL"
            @update:model-value="emitUpdate"
          />
          <input v-model="contributor.name" placeholder="姓名" @input="emitUpdate" />
          <input v-model.number="contributor.commits" type="number" placeholder="Commits" @input="emitUpdate" />
          <button class="remove-btn small" @click="removeContributor(index)">×</button>
        </div>
      </div>
      <button class="add-btn" @click="addContributor">+ 添加贡献者</button>
    </div>

    <!-- 社区链接 -->
    <div class="form-section">
      <h3>社区链接</h3>
      <div class="form-group">
        <label>区块标题</label>
        <input v-model="content.community.title" type="text" @input="emitUpdate" />
      </div>
      <div class="form-group">
        <label>区块描述</label>
        <input v-model="content.community.description" type="text" @input="emitUpdate" />
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>GitHub 组织</label>
          <input v-model="content.community.github" type="text" @input="emitUpdate" />
        </div>
        <div class="form-group">
          <label>Discord 链接</label>
          <input v-model="content.community.discord" type="text" @input="emitUpdate" />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>GitHub 按钮文字</label>
          <input v-model="content.community.githubText" type="text" @input="emitUpdate" />
        </div>
        <div class="form-group">
          <label>Discord 按钮文字</label>
          <input v-model="content.community.discordText" type="text" @input="emitUpdate" />
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

const newTech = ref('')

const defaultContent = {
  hero: { eyebrow: '', title: '', subtitle: '' },
  repos: [],
  techStack: [],
  contributors: [],
  sections: { reposTitle: '', techStackTitle: '', contributorsTitle: '' },
  community: {
    title: '',
    description: '',
    github: '',
    githubText: '',
    discord: '',
    discordText: ''
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

function addRepo() {
  content.repos.push({ name: '', description: '', stars: 0, language: '', link: '' })
  emitUpdate()
}

function removeRepo(index) {
  content.repos.splice(index, 1)
  emitUpdate()
}

function addTech() {
  if (newTech.value.trim() && !content.techStack.includes(newTech.value.trim())) {
    content.techStack.push(newTech.value.trim())
    newTech.value = ''
    emitUpdate()
  }
}

function removeTech(index) {
  content.techStack.splice(index, 1)
  emitUpdate()
}

function addContributor() {
  content.contributors.push({ name: '', commits: 0, avatar: '' })
  emitUpdate()
}

function removeContributor(index) {
  content.contributors.splice(index, 1)
  emitUpdate()
}
</script>

<style scoped>
.opensource-editor {
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
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
  margin-bottom: 8px;
}

.form-group input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 14px;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.repos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.repo-card {
  padding: 20px;
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
}

.card-header span {
  font-size: 14px;
  font-weight: 600;
  color: var(--primary);
}

.repo-card input,
.repo-card textarea {
  padding: 10px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.repo-card input:focus,
.repo-card textarea:focus {
  outline: none;
  border-color: var(--primary);
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

.contributors-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}

.contributor-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--panel-border);
  border-radius: 10px;
}

.contributor-item input {
  padding: 8px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.contributor-item input:first-child {
  width: 150px;
}

.contributor-item input[type="number"] {
  width: 100px;
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
  flex-shrink: 0;
}

.remove-btn.small:hover {
  background: rgba(255, 100, 100, 0.2);
}
</style>
