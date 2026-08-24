<template>
  <div class="login-page">

     <!-- Moving Announcement Bar -->
  <div class="login-ticker">
    <div class="ticker-track">
      <span>Welcome to IoTweet </span>
      <span class="ticker-separator">|</span>

      <span>.needs your for platform best The</span>
      <span class="ticker-separator">|</span>

      <a
        href="https://happyiotsolutions.com/"
        target="_blank"
        rel="noopener noreferrer"
      >
        Join us today!
      </a>

     
    </div>
  </div>

    <div class="login-card">

      <!-- LEFT: LOGIN -->
      <section class="login-panel">

        <div class="login-content">

          <!-- Logo -->
          <div class="logo">
            <img
              src="/HS.png"
              alt="IoTweet"
            />
          </div>

        

          <!-- Login Form -->
          <form @submit.prevent="submit">

            <!-- Email -->
            <div class="form-group">
              <label for="email">Email or Username</label>

              <div class="input-wrapper">
                <Mail :size="19" />

                <input
                  id="email"
                  v-model="email"
                  type="text"
                  placeholder="Enter your email"
                  autocomplete="username"
                  :disabled="loading"
                />
              </div>
            </div>

            <!-- Password -->
            <div class="form-group">
              <label for="password">Password</label>

              <div class="input-wrapper">

                <LockKeyhole :size="19" />

                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Enter your password"
                  autocomplete="current-password"
                  :disabled="loading"
                />

                <button
                  type="button"
                  class="password-toggle"
                  @click="showPassword = !showPassword"
                  :aria-label="
                    showPassword
                      ? 'Hide password'
                      : 'Show password'
                  "
                >
                  <EyeOff
                    v-if="showPassword"
                    :size="19"
                  />

                  <Eye
                    v-else
                    :size="19"
                  />
                </button>

              </div>
            </div>

            <!-- Options -->
            <div class="form-options">

              <label class="remember">
                <input
                  v-model="rememberMe"
                  type="checkbox"
                />

                <span>Remember me</span>
              </label>

              <button
                type="button"
                class="forgot-btn"
                @click="forgotPassword"
              >
                Forgot password?
              </button>

            </div>

            <!-- Error -->
            <div
              v-if="errorMessage"
              class="error-message"
            >
              <CircleAlert :size="18" />
              <span>{{ errorMessage }}</span>
            </div>

            <!-- Login Button -->
            <button
              type="submit"
              class="login-btn"
              :disabled="loading"
            >

              <LoaderCircle
                v-if="loading"
                class="spinner"
                :size="19"
              />

              <span>
                {{ loading ? "Signing in..." : "Sign In" }}
              </span>

              <ArrowRight
                v-if="!loading"
                :size="19"
              />

            </button>

          </form>

          <p class="copyright">
            © {{ new Date().getFullYear() }} happyiotsolutions. All rights reserved.
          </p>

        </div>

      </section>


      <!-- RIGHT: SHOWCASE -->
      <section class="showcase-panel">

        <div class="showcase-content">

        

          <div class="showcase-text">

            <h2>
              Smarter IoT
              <br />
              Monitoring Starts Here
            </h2>

            <p>
              Monitor devices, analyze telemetry, and turn
              real-time IoT data into actionable insights.
            </p>

          </div>

          <div class="showcase-image">

             <img
              src="/public/hs3.jpeg"
              alt="IoT Dashboard Analytics"
            />

          

          </div>

          <div class="showcase-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>

        </div>

      </section>

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

/* =========================================================
   LOGIN MOVING TEXT BAR
========================================================= */

.login-ticker {

  position: absolute;

  top: 0;
  left: 0;

  width: 100%;

  height: 38px;

  display: flex;

  align-items: center;

  overflow: hidden;

  background: #00a3d3;

  color: #ffffff;

  z-index: 10;

  white-space: nowrap;

 

}


.ticker-track {

  display: inline-flex;

  align-items: center;

  gap: 14px;

  padding-left: 20px;

  font-size: 13px;

  font-weight: 500;

  animation: tickerMove 18s linear infinite;

}


.ticker-track span {

  flex-shrink: 0;
  font-size: 18px;
  text-transform: capitalize;
  font-weight: 600;

}


.ticker-separator {

  opacity: .65;

  font-weight: 400;

}


.ticker-track a {

  flex-shrink: 0;

  color: #ffffff;

  font-weight: 600;

  font-size: 18px;

}


.ticker-track a:hover {

  opacity: .8;

}


/* Left → Right movement */

@keyframes tickerMove {

  0% {

    transform: translateX(-100%);

  }

  100% {

    transform: translateX(100vw);

  }

}

.login-page {

  min-height: 100vh;

  width: 100%;

  display: flex;

  align-items: center;

  justify-content: center;

  padding: 52px 32px 32px;

  box-sizing: border-box;

  background: #eef1f5;

  position: relative;

  overflow: hidden;

}


.login-card {

  width: min(1280px, 100%);

  min-height: 720px;

  background: #ffffff;

  border-radius: 26px;

  overflow: hidden;

  display: grid;

  grid-template-columns: 0.95fr 1.05fr;

  box-shadow:
    0 30px 80px rgba(15, 23, 42, 0.12);

}


/* =========================
   LEFT LOGIN
========================= */

.login-panel {

  display: flex;

  align-items: center;

  justify-content: center;

  background: #ffffff;

}


.login-content {

  width: min(390px, 82%);

  padding: 50px 0;

}


.logo {

  width: 155px;

  margin-bottom: 58px;

}


.logo img {

  width: 100%;

  height: auto;

  display: block;

  margin-left: 100px;

  

}


.welcome {

  margin-bottom: 30px;

}


.welcome h1 {

  margin: 0 0 8px;

  color: #111827;

  font-size: 32px;

  line-height: 1.15;

  font-weight: 750;

}


.welcome p {

  margin: 0;

  color: #64748b;

  font-size: 14px;

  line-height: 1.6;

}


/* =========================
   FORM
========================= */

.form-group {

  margin-bottom: 20px;

}


.form-group label {

  display: block;

  margin-bottom: 8px;

  color: #111827;

  font-size: 14px;

  font-weight: 600;

}


.input-wrapper {

  height: 50px;

  display: flex;

  align-items: center;

  gap: 10px;

  padding: 0 14px;

  box-sizing: border-box;

  border: 1px solid #d7dce3;

  border-radius: 10px;

  color: #94a3b8;

  background: #ffffff;

  transition:
    border-color .2s ease,
    box-shadow .2s ease;

}


.input-wrapper:focus-within {

  border-color: #1d9e75;

  box-shadow:
    0 0 0 3px rgba(29, 158, 117, .12);

}


.input-wrapper input {

  width: 100%;

  height: 100%;

  border: none;

  outline: none;

  background: transparent;

  color: #111827;

  font-size: 14px;

}


.input-wrapper input::placeholder {

  color: #94a3b8;

}


.password-toggle {

  flex-shrink: 0;

  display: flex;

  align-items: center;

  justify-content: center;

  border: none;

  background: transparent;

  color: #94a3b8;

  cursor: pointer;

}


.password-toggle:hover {

  color: #1d9e75;

}


/* =========================
   OPTIONS
========================= */

.form-options {

  display: flex;

  align-items: center;

  justify-content: space-between;

  margin: 4px 0 22px;

}


.remember {

  display: flex;

  align-items: center;

  gap: 8px;

  color: #475569;

  font-size: 13px;

  cursor: pointer;

}


.remember input {

  width: 16px;

  height: 16px;

  accent-color: #1d9e75;

}


.forgot-btn {

  padding: 0;

  border: none;

  background: transparent;

  color: #1d9e75;

  font-size: 13px;

  cursor: pointer;

}


.forgot-btn:hover {

  text-decoration: underline;

}


/* =========================
   ERROR
========================= */

.error-message {

  display: flex;

  align-items: center;

  gap: 8px;

  margin-bottom: 16px;

  padding: 11px 13px;

  border-radius: 9px;

  background: #fef2f2;

  color: #dc2626;

  font-size: 13px;

}


/* =========================
   LOGIN BUTTON
========================= */

.login-btn {

  width: 100%;

  height: 50px;

  display: flex;

  align-items: center;

  justify-content: center;

  gap: 8px;

  border: none;

  border-radius: 10px;

  background: #00a3d3;

  color: #ffffff;

  font-size: 15px;

  font-weight: 650;

  cursor: pointer;

  transition:
    background .2s ease,
    transform .2s ease;

}


.login-btn:hover:not(:disabled) {

  background: #168a65;

  transform: translateY(-1px);

}


.login-btn:disabled {

  opacity: .65;

  cursor: not-allowed;

}


.spinner {

  animation: spin 1s linear infinite;

}


@keyframes spin {

  to {

    transform: rotate(360deg);

  }

}


/* =========================
   COPYRIGHT
========================= */

.copyright {

  margin: 60px 0 0;

  text-align: center;

  color: #94a3b8;

  font-size: 12px;

}


/* =========================
   RIGHT SHOWCASE
========================= */

.showcase-panel {

  padding: 20px;

  background: #f8fafc;

}


.showcase-content {

  height: 100%;

  min-height: 680px;

  padding: 42px;

  box-sizing: border-box;

  border-radius: 20px;

  overflow: hidden;

  display: flex;

  flex-direction: column;

  background:
    linear-gradient(
      145deg,
      #075e68 0%,
      #087b7d 55%,
      #1d9e75 100%
    );

  color: white;

}


.showcase-brand {

  display: flex;

  align-items: center;

  gap: 10px;

  font-size: 17px;

  font-weight: 700;

}


.brand-icon {

  width: 42px;

  height: 42px;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 10px;

  background: rgba(255,255,255,.8);

  backdrop-filter: blur(8px);

}


.showcase-text {

  margin-top: auto;

}


.showcase-text h2 {

  max-width: 600px;

  margin: 0 0 14px;

  font-size: clamp(28px, 3vw, 44px);

  line-height: 1.1;

  font-weight: 750;

}


.showcase-text p {

  max-width: 580px;

  margin: 0;

  color: rgba(255,255,255,.82);

  font-size: 14px;

  line-height: 1.7;

}


/* =========================
   IMAGE
========================= */

.showcase-image {

  margin-top: 28px;

  border-radius: 18px;

  overflow: hidden;

  border: 7px solid rgba(255,255,255,.16);

  background: white;

  box-shadow:
    0 20px 50px rgba(0,0,0,.18);

}


.showcase-image img {

  display: block;

  width: 100%;

  aspect-ratio: 16 / 9;

  object-fit: cover;

}


/* =========================
   DOTS
========================= */

.showcase-dots {

  display: flex;

  gap: 6px;

  margin-top: 18px;

}


.showcase-dots span {

  width: 7px;

  height: 7px;

  border-radius: 50%;

  background: rgba(255,255,255,.4);

}


.showcase-dots span:first-child {

  width: 22px;

  border-radius: 10px;

  background: #ffffff;

}


/* =========================
   TABLET
========================= */

@media (max-width: 1000px) {

  .login-page {

    padding: 20px;

  }

  .login-card {

    grid-template-columns: 1fr;

    max-width: 560px;

    min-height: auto;

  }

  .showcase-panel {

    display: none;

  }

  .login-content {

    width: min(420px, 86%);

    padding: 55px 0;

  }

}


/* =========================
   MOBILE
========================= */

@media (max-width: 600px) {

  /* .login-page {

    padding: 0;

    align-items: stretch;

  } */

    .login-page {

    padding: 48px 0 0;

  }

  .login-ticker {

    height: 36px;

  }

  .ticker-track {

    gap: 10px;

    font-size: 12px;

    animation-duration: 14s;

  }

  .login-card {

    width: 100%;

    min-height: 100vh;

    border-radius: 0;

    box-shadow: none;

  }

  .login-content {

    width: calc(100% - 40px);

    padding: 35px 0;

  }

  .logo {

    width: 135px;

    margin-bottom: 48px;

  }

  .welcome h1 {

    font-size: 28px;

  }

  .form-options {

    align-items: flex-start;

    gap: 12px;

  }

  .copyright {

    margin-top: 50px;

  }

}


/* =========================
   SMALL MOBILE
========================= */

@media (max-width: 380px) {

  .form-options {

    flex-direction: column;

  }

  .forgot-btn {

    align-self: flex-start;

  }

}

</style>