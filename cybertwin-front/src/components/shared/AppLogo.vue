<script setup>
defineProps({ size: { type: Number, default: 32 } })
</script>

<template>
  <svg :width="size" :height="size" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <defs>
      <linearGradient id="ctg" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
        <stop stop-color="#38bdf8" />
        <stop offset="1" stop-color="#0284c7" />
      </linearGradient>
    </defs>
    <path d="M24 3l16 6v10c0 11-6.8 18.6-16 23C14.8 37.6 8 30 8 19V9l16-6z" fill="url(#ctg)" />
    <path d="M24 3l16 6v10c0 11-6.8 18.6-16 23V3z" fill="#000" opacity="0.12" />
    <path d="M17 24l4.5 4.5L31 19" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" />
  </svg>
</template>
