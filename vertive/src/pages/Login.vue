<template>
  <div class="min-h-screen flex flex-col items-center justify-center">
    <div class="flex flex-col items-center space-y-4">
      <!-- Logo Section -->
      <img src="/IOtweet Logo_2.0 Teal .png" alt="IoTweet Logo" class="w-20 h-20" />
      <!-- Card Section -->
      <Card title=" " class="w-full max-w-md mt-4">
        <form class="flex flex-col space-y-2 w-full" @submit.prevent="submit">
          <Input required v-model="email" type="text" placeholder="vertiv@email.com" label="User ID" />
          <Input required v-model="password" type="password" placeholder="••••••" label="Password" />
          <Button :loading="session.login.loading" class="bg-[#08444c] hover:bg-[#062f34] text-white" variant="solid">
            Login
          </Button>
          <!-- Error Message -->
          <p v-if="errorMessage" class="text-red-500 text-sm">{{ errorMessage }}</p>
        </form>
      </Card>
    </div>

    <!-- Marquee Section -->
    <div class="marquee-wrapper w-full mt-6" @mouseenter="pauseMarquee" @mouseleave="resumeMarquee">
      <div class="marquee flex items-center space-x-2 whitespace-nowrap" :class="{ paused: isPaused }">
        <span>Welcome to</span>
        <img src="/IOtweet Logo_2.0 Teal .png" alt="IoTweet Logo" class="h-5 w-auto inline-block" />
        <span>| The best platform for your needs. |</span>
        <a href="#" target="_blank" class="marquee-link text-blue-500 underline">Join us today!</a>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { session } from '../data/session'

// State
const isPaused = ref(false)
const email = ref('')
const password = ref('')
const errorMessage = ref('') // Error message state

function pauseMarquee() {
  isPaused.value = true
}

function resumeMarquee() {
  isPaused.value = false
}

async function submit() {
  errorMessage.value = '' // Reset error message before login attempt

  try {
    console.log('Attempting login with:', { email: email.value, password: password.value })

    const response = await session.login.submit({
      email: email.value,
      password: password.value,
    })

    console.log('Login response:', response) // Debugging log

    if (response && response.success) {
      console.log('Login successful!')
      errorMessage.value = '' // Clear error message on success
      // Redirect user or handle success here
    } else {
      console.warn('Invalid credentials')
      errorMessage.value = 'Invalid credentials. Please try again.'
    }
  } catch (error) {
    console.error('Login failed:', error)
    errorMessage.value = 'Login failed. Please check your credentials.'
  }
}
</script>

<style scoped>
/* Adjust the logo dimensions */
.w-20 {
  width: 21rem;
}

.h-20 {
  height: 4rem;
}

/* Marquee Styles */
.marquee-wrapper {
  overflow: hidden;
  white-space: nowrap;
  background-color: #f1f1f1;
  padding: 0.5rem 0;
  position: absolute;
  bottom: 0;
}

.marquee {
  display: inline-block;
  animation: marquee 10s linear infinite;
  color: #333;
  font-size: 1rem;
  transform: translateX(100%);
}

.marquee.paused {
  animation-play-state: paused;
}

.marquee-link {
  color: #007bff;
  text-decoration: none;
}

.marquee-link:hover {
  text-decoration: underline;
}

@keyframes marquee {
  0% {
    transform: translateX(100%);
  }

  100% {
    transform: translateX(-100%);
  }
}
</style>
