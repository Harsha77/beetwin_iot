<template>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white p-8 rounded-lg w-1/2">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold">Plant List</h2>
        <button @click="$emit('close')" class="text-red-500">Close</button>
      </div>
      <ul>
        <li v-for="plant in plants" :key="plant.value" class="text-lg text-gray-700">
          {{ plant.label }}
        </li>
      </ul>
    </div>
  </div>
</template>


<script setup>
defineProps({
  plants: {
    type: Array,
    required: true
  }
});
</script>