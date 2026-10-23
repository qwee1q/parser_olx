<script setup>
import { ref, onMounted } from "vue";

const API_URL = "http://127.0.0.1:8000";

const items = ref([]);
const loading = ref(false);
const error = ref(null);

async function loadItems() {
  loading.value = true;
  error.value = null;
  try {
    const res = await fetch(`${API_URL}/`);
    if (!res.ok) throw new Error(`Помилка сервера: ${res.status}`);
    const data = await res.json();
    items.value = data.items;
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

onMounted(loadItems);
</script>

<template>
  <div>
    <button @click="loadItems">Update</button>

    <p v-if="loading">Loading</p>
    <p v-else-if="error">{{ error }}</p>

    <ul v-else>
      <li v-for="item in items" :key="item.url">
        <a :href="item.url" target="_blank">{{ item.title }}</a>
        — {{ item.price }} ({{ item.location_date }})
      </li>
    </ul>
  </div>
</template>
