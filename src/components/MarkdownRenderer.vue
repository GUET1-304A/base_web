<template>
  <div class="md-content" v-html="rendered"></div>
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  text: { type: String, default: '' }
})

marked.setOptions({
  breaks: true,
  gfm: true
})

const rendered = computed(() => {
  if (!props.text) return ''
  try {
    return marked.parse(props.text)
  } catch {
    return props.text
  }
})
</script>

<style scoped>
.md-content {
  font-size: inherit;
  color: inherit;
  line-height: 1.8;
  overflow-wrap: break-word;
  word-break: break-word;
}

.md-content :deep(h1),
.md-content :deep(h2),
.md-content :deep(h3),
.md-content :deep(h4) {
  margin: 1.2em 0 0.6em;
  font-weight: 700;
  color: var(--text);
  line-height: 1.4;
}

.md-content :deep(h1) { font-size: 1.5em; }
.md-content :deep(h2) { font-size: 1.3em; }
.md-content :deep(h3) { font-size: 1.15em; }
.md-content :deep(h4) { font-size: 1.05em; }

.md-content :deep(p) {
  margin: 0 0 0.8em;
}

.md-content :deep(p:last-child) {
  margin-bottom: 0;
}

.md-content :deep(ul),
.md-content :deep(ol) {
  margin: 0.4em 0 0.8em;
  padding-left: 1.5em;
}

.md-content :deep(li) {
  margin-bottom: 0.3em;
}

.md-content :deep(strong) {
  font-weight: 700;
  color: var(--text);
}

.md-content :deep(em) {
  font-style: italic;
}

.md-content :deep(a) {
  color: var(--primary);
  text-decoration: underline;
  transition: opacity 0.2s;
}

.md-content :deep(a:hover) {
  opacity: 0.8;
}

.md-content :deep(code) {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.9em;
  padding: 2px 6px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 4px;
}

.md-content :deep(pre) {
  margin: 0.8em 0;
  padding: 14px 16px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  overflow-x: auto;
}

.md-content :deep(pre code) {
  padding: 0;
  background: none;
  font-size: 0.85em;
}

.md-content :deep(blockquote) {
  margin: 0.8em 0;
  padding: 8px 16px;
  border-left: 3px solid var(--primary);
  background: rgba(121, 168, 255, 0.06);
  border-radius: 0 8px 8px 0;
  color: var(--muted);
}

.md-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 0.8em 0;
}

.md-content :deep(hr) {
  border: none;
  height: 1px;
  background: var(--panel-border);
  margin: 1.2em 0;
}

.md-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 0.8em 0;
  font-size: 0.9em;
}

.md-content :deep(th),
.md-content :deep(td) {
  padding: 8px 12px;
  border: 1px solid var(--panel-border);
  text-align: left;
}

.md-content :deep(th) {
  background: rgba(121, 168, 255, 0.08);
  font-weight: 600;
  color: var(--text);
}

.md-content :deep(tr:nth-child(even)) {
  background: rgba(255, 255, 255, 0.02);
}
</style>
