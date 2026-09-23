<template>
  <div class="login-page">
    <!-- Announcement bar -->
    <div
      class="login-ticker"
      @mouseenter="pauseMarquee"
      @mouseleave="resumeMarquee"
    >
      <div class="ticker-track" :class="{ 'ticker-paused': isPaused }">
        <span>Welcome to Beetwin-HS</span>
        <span class="ticker-separator">&quot;</span>
        <span>Smart water infrastructure monitoring</span>
        <span class="ticker-separator">&quot;</span>
        <a
          href="https://happyiotsolutions.com/"
          target="_blank"
          rel="noopener noreferrer"
        >
          Visit Happy IoT Solutions
        </a>
      </div>
    </div>

    <main class="login-card">
      <!-- Login panel -->
      <section class="login-panel">
        <div class="login-content">
          <header class="mobile-brand-row">
            <div class="logo">
              <img src="/HS.png" alt="Happy IoT Solutions" />
            </div>

            <div class="mobile-security-badge">
              <span class="security-dot"></span>
              Secure login
            </div>
          </header>

          <div class="welcome">
            <h1>Welcome to Happy Solutions</h1>
          </div>

          <form class="login-form" @submit.prevent="submit">
            <div class="form-group">
              <label for="email">Email or username</label>

              <div class="input-wrapper">
                <Mail :size="19" aria-hidden="true" />
                <input
                  id="email"
                  v-model.trim="email"
                  type="text"
                  placeholder="Enter your email or username"
                  autocomplete="username"
                  :disabled="loading"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="password">Password</label>

              <div class="input-wrapper">
                <LockKeyhole :size="19" aria-hidden="true" />
                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Enter your password"
                  autocomplete="current-password"
                  :disabled="loading"
                  required
                />

                <button
                  type="button"
                  class="password-toggle"
                  :aria-label="showPassword ? 'Hide password' : 'Show password'"
                  :title="showPassword ? 'Hide password' : 'Show password'"
                  @click="showPassword = !showPassword"
                >
                  <EyeOff v-if="showPassword" :size="19" aria-hidden="true" />
                  <Eye v-else :size="19" aria-hidden="true" />
                </button>
              </div>
            </div>

            <div class="form-options">
              <label class="remember">
                <input v-model="rememberMe" type="checkbox" />
                <span>Remember me</span>
              </label>

              <button type="button" class="forgot-btn" @click="forgotPassword">
                Forgot password?
              </button>
            </div>

            <div v-if="errorMessage" class="error-message" role="alert">
              <CircleAlert :size="18" aria-hidden="true" />
              <span>{{ errorMessage }}</span>
            </div>

            <button type="submit" class="login-btn" :disabled="loading">
              <LoaderCircle
                v-if="loading"
                class="spinner"
                :size="19"
                aria-hidden="true"
              />
              <span>{{ loading ? "Signing in..." : "Sign In" }}</span>
              <ArrowRight v-if="!loading" :size="19" aria-hidden="true" />
            </button>
          </form>

          <p class="copyright">
            &copy; {{ currentYear }} Happy IoT Solutions. All rights reserved.
          </p>
        </div>
      </section>

      <!-- Product showcase -->
      <section class="showcase-panel">
        <div class="showcase-content">
          <div class="showcase-topbar">
            <div class="showcase-brand"></div>

            <div class="live-status">
              <span></span>
              Monitoring active
            </div>
          </div>

          <div class="showcase-copy">
            <h2>
              Smarter IoT monitoring
              <br />
              starts here.
            </h2>
            <p>
              Monitor connected devices, analyze watermain telemetry, and turn
              real-time operational data into clear, actionable insights.
            </p>
          </div>

          <div class="showcase-image">
            <img src="/public/hs3.jpeg" alt="IoTweet dashboard analytics" />
            <div class="image-overlay">
              <div class="image-stat">
                <Activity :size="18" aria-hidden="true" />
                <span>Live telemetry</span>
              </div>
              <div class="image-stat">
                <ShieldCheck :size="18" aria-hidden="true" />
                <span>Secure monitoring</span>
              </div>
            </div>
          </div>

          <div class="showcase-footer">
            <div class="showcase-dots" aria-hidden="true">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <p>MIDC Mahape Watermain Dashboard</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from "vue";
import {
  Activity,
  ArrowRight,
  CircleAlert,
  Eye,
  EyeOff,
  LoaderCircle,
  LockKeyhole,
  Mail,
  ShieldCheck
} from "lucide-vue-next";
import { session } from "../data/session";

const REMEMBER_KEY = "iotweet_remember_me";
const EMAIL_KEY = "iotweet_remembered_email";

const isPaused = ref(false);
const email = ref("");
const password = ref("");
const showPassword = ref(false);
const rememberMe = ref(false);
const loading = ref(false);
const errorMessage = ref("");

const currentYear = computed(() => new Date().getFullYear());

const pauseMarquee = () => {
  isPaused.value = true;
};

const resumeMarquee = () => {
  isPaused.value = false;
};

const saveRememberedUser = () => {
  if (rememberMe.value) {
    localStorage.setItem(REMEMBER_KEY, "true");
    localStorage.setItem(EMAIL_KEY, email.value);
    return;
  }

  localStorage.removeItem(REMEMBER_KEY);
  localStorage.removeItem(EMAIL_KEY);
};

const forgotPassword = () => {
  window.location.href = "/forgot";
};

const submit = async () => {
  errorMessage.value = "";

  if (!email.value || !password.value) {
    errorMessage.value = "Please enter your email and password.";
    return;
  }

  loading.value = true;

  try {
    await session.login.submit({
      email: email.value,
      password: password.value
    });

    saveRememberedUser();
    errorMessage.value = "";
  } catch (error: any) {
    console.error("Login failed:", error);

    errorMessage.value =
      error?.messages?.[0] ||
      error?.message ||
      "Login failed. Please check your credentials.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  const shouldRemember = localStorage.getItem(REMEMBER_KEY) === "true";
  const rememberedEmail = localStorage.getItem(EMAIL_KEY);

  rememberMe.value = shouldRemember;

  if (shouldRemember && rememberedEmail) {
    email.value = rememberedEmail;
  }
});
</script>

<style scoped>
:global(*) {
  box-sizing: border-box;
}

.login-page {
  position: relative;
  display: flex;
  width: 100%;
  min-height: 100vh;
  min-height: 100dvh;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 4.25rem 2rem 2rem;
  color: #1f3344;
  background:
    radial-gradient(circle at 0% 0%, rgba(21, 164, 183, 0.13), transparent 28rem),
    radial-gradient(circle at 100% 100%, rgba(37, 183, 155, 0.11), transparent 30rem),
    linear-gradient(180deg, #f7fafc 0%, #eaf2f5 100%);
}

.login-page::before,
.login-page::after {
  position: absolute;
  border-radius: 9999px;
  content: "";
  pointer-events: none;
}

.login-page::before {
  top: 7rem;
  left: -8rem;
  width: 20rem;
  height: 20rem;
  border: 1px solid rgba(8, 127, 154, 0.08);
}

.login-page::after {
  right: -10rem;
  bottom: -10rem;
  width: 25rem;
  height: 25rem;
  border: 1px solid rgba(37, 183, 155, 0.1);
}

.login-ticker {
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  z-index: 30;
  display: flex;
  height: 2.35rem;
  align-items: center;
  overflow: hidden;
  white-space: nowrap;
  color: #ffffff;
  background: linear-gradient(90deg, #087f9a 0%, #159fb2 52%, #12856f 100%);
  box-shadow: 0 4px 14px rgba(8, 83, 105, 0.16);
}

.ticker-track {
  display: inline-flex;
  min-width: max-content;
  align-items: center;
  gap: 0.9rem;
  padding-left: 1.25rem;
  font-size: 0.78rem;
  font-weight: 700;
  animation: ticker-move 20s linear infinite;
  will-change: transform;
}

.ticker-track.ticker-paused {
  animation-play-state: paused;
}

.ticker-track span,
.ticker-track a {
  flex-shrink: 0;
}

.ticker-separator {
  color: rgba(255, 255, 255, 0.64);
}

.ticker-track a {
  color: #ffffff;
  text-decoration: underline;
  text-underline-offset: 0.18rem;
}

.ticker-track a:hover {
  color: #d7fffa;
}

@keyframes ticker-move {
  from { transform: translateX(100vw); }
  to { transform: translateX(-100%); }
}

.login-card {
  position: relative;
  z-index: 2;
  display: grid;
  width: min(76rem, 100%);
  min-height: min(44rem, calc(100dvh - 6.25rem));
  grid-template-columns: minmax(24rem, 0.88fr) minmax(31rem, 1.12fr);
  overflow: hidden;
  border: 1px solid rgba(207, 224, 231, 0.9);
  border-radius: 1.5rem;
  background: rgba(255, 255, 255, 0.97);
  box-shadow: 0 28px 75px rgba(20, 58, 72, 0.14);
}

.login-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: #ffffff;
}

.login-content {
  width: min(24rem, 100%);
}

.mobile-brand-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2.4rem;
  text-align: center;
}

.logo {
  display: flex;
  width: 11rem;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: 0;
  border-radius: 0;
  background: transparent;
  box-shadow: none;
}

.logo img {
  display: block;
  width: 100%;
  height: auto;
  object-fit: contain;
}

.mobile-security-badge {
  display: none;
  align-items: center;
  gap: 0.4rem;
  padding: 0.42rem 0.62rem;
  border: 1px solid #d6e8e6;
  border-radius: 9999px;
  font-size: 0.65rem;
  font-weight: 800;
  white-space: nowrap;
  color: #087f68;
  background: #f1fbf8;
}

.security-dot {
  width: 0.42rem;
  height: 0.42rem;
  border-radius: 9999px;
  background: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.12);
}

.welcome {
  margin-bottom: 1.75rem;
}

.eyebrow,
.showcase-eyebrow {
  margin: 0 0 0.5rem;
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: #168da4;
}

.welcome h1 {
  margin: 0 0 0.55rem;
  font-size: clamp(1.8rem, 3vw, 2.25rem);
  font-weight: 800;
  line-height: 1.12;
  letter-spacing: -0.025em;
  color: #173447;
}

.welcome > p:last-child {
  margin: 0;
  font-size: 0.86rem;
  line-height: 1.65;
  color: #6b7f8d;
}

.form-group {
  margin-bottom: 1.15rem;
}

.form-group > label {
  display: block;
  margin-bottom: 0.45rem;
  font-size: 0.75rem;
  font-weight: 800;
  color: #334b5b;
}

.input-wrapper {
  display: flex;
  height: 3.1rem;
  align-items: center;
  gap: 0.65rem;
  padding: 0 0.85rem;
  border: 1px solid #d5e2e8;
  border-radius: 0.8rem;
  color: #8aa0ad;
  background: #ffffff;
  box-shadow: 0 3px 10px rgba(31, 78, 94, 0.035);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.input-wrapper:focus-within {
  border-color: #159fb2;
  color: #087f9a;
  box-shadow: 0 0 0 3px rgba(21, 159, 178, 0.11);
}

.input-wrapper input {
  width: 100%;
  height: 100%;
  min-width: 0;
  border: 0;
  outline: 0;
  font-size: 0.86rem;
  color: #173447;
  background: transparent;
}

.input-wrapper input::placeholder {
  color: #9aabb5;
}

.input-wrapper input:disabled {
  cursor: not-allowed;
}

.password-toggle {
  display: flex;
  width: 2rem;
  height: 2rem;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  border: 0;
  border-radius: 0.5rem;
  color: #8aa0ad;
  background: transparent;
  cursor: pointer;
  transition: color 0.18s ease, background 0.18s ease;
}

.password-toggle:hover {
  color: #087f9a;
  background: #ecfbfc;
}

.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin: 0.2rem 0 1.3rem;
}

.remember {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.76rem;
  font-weight: 600;
  color: #5a7180;
  cursor: pointer;
}

.remember input {
  width: 1rem;
  height: 1rem;
  accent-color: #159fb2;
}

.forgot-btn {
  padding: 0;
  border: 0;
  font-size: 0.76rem;
  font-weight: 700;
  color: #087f9a;
  background: transparent;
  cursor: pointer;
}

.forgot-btn:hover {
  text-decoration: underline;
  text-underline-offset: 0.18rem;
}

.error-message {
  display: flex;
  align-items: flex-start;
  gap: 0.55rem;
  margin-bottom: 1rem;
  padding: 0.7rem 0.8rem;
  border: 1px solid #fecdd3;
  border-radius: 0.7rem;
  font-size: 0.76rem;
  font-weight: 600;
  line-height: 1.45;
  color: #be123c;
  background: #fff1f2;
}

.error-message svg {
  flex: 0 0 auto;
  margin-top: 0.05rem;
}

.login-btn {
  display: flex;
  width: 100%;
  height: 3.1rem;
  align-items: center;
  justify-content: center;
  gap: 0.55rem;
  border: 1px solid #087f9a;
  border-radius: 0.8rem;
  font-size: 0.86rem;
  font-weight: 800;
  color: #ffffff;
  background: linear-gradient(135deg, #087f9a, #159fb2);
  box-shadow: 0 8px 18px rgba(8, 127, 154, 0.23);
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  background: linear-gradient(135deg, #07697f, #087f9a);
  box-shadow: 0 11px 24px rgba(8, 127, 154, 0.3);
}

.login-btn:disabled {
  cursor: wait;
  opacity: 0.68;
}

.spinner {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.login-help {
  margin: 1rem 0 0;
  font-size: 0.68rem;
  line-height: 1.5;
  text-align: center;
  color: #9aabb5;
}

.copyright {
  margin: 2.4rem 0 0;
  font-size: 0.68rem;
  text-align: center;
  color: #94a3b8;
}

.showcase-panel {
  padding: 1rem;
  background: #f5f9fa;
}

.showcase-content {
  position: relative;
  display: flex;
  height: 100%;
  min-height: 41.5rem;
  flex-direction: column;
  overflow: hidden;
  padding: 2.25rem;
  border-radius: 1.15rem;
  color: #ffffff;
  background:
    radial-gradient(circle at 90% 10%, rgba(106, 255, 221, 0.18), transparent 17rem),
    linear-gradient(145deg, #075664 0%, #087b7d 55%, #178c78 100%);
}

.showcase-content::before {
  position: absolute;
  top: -8rem;
  right: -8rem;
  width: 22rem;
  height: 22rem;
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 9999px;
  content: "";
}

.showcase-topbar,
.showcase-footer {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.showcase-brand {
  display: flex;
  align-items: center;
  gap: 0.7rem;
}

.brand-icon {
  display: flex;
  width: 2.6rem;
  height: 2.6rem;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.75rem;
  color: #d7fffa;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(8px);
}

.showcase-brand p {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 800;
}

.showcase-brand div > span {
  display: block;
  margin-top: 0.12rem;
  font-size: 0.64rem;
  color: rgba(255, 255, 255, 0.7);
}

.live-status {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.48rem 0.7rem;
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 9999px;
  font-size: 0.67rem;
  font-weight: 800;
  color: #eafff9;
  background: rgba(255, 255, 255, 0.1);
}

.live-status span {
  width: 0.45rem;
  height: 0.45rem;
  border-radius: 9999px;
  background: #5eead4;
  box-shadow: 0 0 0 4px rgba(94, 234, 212, 0.13);
}

.showcase-copy {
  position: relative;
  z-index: 1;
  margin-top: auto;
  padding-top: 3rem;
}

.showcase-eyebrow {
  color: #8ff6eb;
}

.showcase-copy h2 {
  max-width: 34rem;
  margin: 0 0 0.9rem;
  font-size: clamp(2rem, 3.4vw, 3.15rem);
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: -0.03em;
}

.showcase-copy > p:last-child {
  max-width: 34rem;
  margin: 0;
  font-size: 0.86rem;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.78);
}

.showcase-image {
  position: relative;
  z-index: 1;
  margin-top: 1.6rem;
  overflow: hidden;
  border: 0.38rem solid rgba(255, 255, 255, 0.15);
  border-radius: 1rem;
  background: #ffffff;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
}

.showcase-image img {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 8;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  right: 0.8rem;
  bottom: 0.8rem;
  left: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.6rem;
}

.image-stat {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.45rem 0.62rem;
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: 0.65rem;
  font-size: 0.65rem;
  font-weight: 800;
  color: #ffffff;
  background: rgba(7, 73, 83, 0.76);
  backdrop-filter: blur(8px);
}

.showcase-footer {
  margin-top: 1rem;
}

.showcase-dots {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.showcase-dots span {
  width: 0.42rem;
  height: 0.42rem;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.38);
}

.showcase-dots span:first-child {
  width: 1.4rem;
  background: #ffffff;
}

.showcase-footer p {
  margin: 0;
  font-size: 0.64rem;
  color: rgba(255, 255, 255, 0.65);
}

@media (max-width: 1050px) {
  .login-page {
    overflow-y: auto;
  }

  .login-card {
    width: min(46rem, 100%);
    min-height: auto;
    grid-template-columns: 1fr;
  }

  .login-panel {
    padding: 3rem 2rem;
  }

  .login-content {
    width: min(25rem, 100%);
  }

  .mobile-security-badge {
    display: none;
  }

  .showcase-panel {
    display: block;
  }

  .showcase-content {
    min-height: 35rem;
  }
}

@media (max-width: 600px) {
  .login-page {
    min-height: 100dvh;
    align-items: flex-start;
    overflow-x: hidden;
    overflow-y: auto;
    padding: 3.15rem 0.75rem 0.75rem;
  }

  .login-ticker {
    height: 2.25rem;
  }

  .ticker-track {
    gap: 0.65rem;
    padding-left: 0.8rem;
    font-size: 0.7rem;
    animation-duration: 16s;
    animation-delay: -8s;
  }

  .login-card {
    width: 100%;
    min-height: auto;
    overflow: hidden;
    border-radius: 1.15rem;
  }

  .login-panel {
    align-items: flex-start;
    padding: 1.5rem 1.1rem 1.2rem;
  }

  .login-content {
    width: 100%;
  }

  .mobile-brand-row {
    margin-bottom: 1.65rem;
  }

  .logo {
    width: 9rem;
  }

  .mobile-security-badge {
    display: none;
  }

  .welcome {
    margin-bottom: 1.4rem;
  }

  .welcome h1 {
    font-size: 1.7rem;
  }

  .welcome > p:last-child {
    font-size: 0.8rem;
  }

  .input-wrapper,
  .login-btn {
    height: 3rem;
  }

  .copyright {
    margin-top: 1.8rem;
    padding-bottom: 0.25rem;
  }

  .showcase-panel {
    display: block;
    padding: 0.65rem;
    border-top: 1px solid #e3edf1;
  }

  .showcase-content {
    min-height: auto;
    padding: 1.2rem;
    border-radius: 0.95rem;
  }

  .showcase-topbar {
    align-items: flex-start;
  }

  .brand-icon {
    width: 2.3rem;
    height: 2.3rem;
  }

  .showcase-brand p {
    font-size: 0.85rem;
  }

  .showcase-brand div > span {
    max-width: 8.5rem;
    font-size: 0.58rem;
    line-height: 1.3;
  }

  .live-status {
    gap: 0.35rem;
    padding: 0.42rem 0.55rem;
    font-size: 0.58rem;
  }

  .showcase-copy {
    margin-top: 2.8rem;
    padding-top: 0;
  }

  .showcase-copy h2 {
    margin-bottom: 0.75rem;
    font-size: 1.85rem;
    line-height: 1.08;
  }

  .showcase-copy > p:last-child {
    font-size: 0.78rem;
    line-height: 1.6;
  }

  .showcase-image {
    margin-top: 1.2rem;
    border-width: 0.28rem;
    border-radius: 0.8rem;
  }

  .showcase-image img {
    aspect-ratio: 4 / 3;
  }

  .image-overlay {
    right: 0.45rem;
    bottom: 0.45rem;
    left: 0.45rem;
    gap: 0.35rem;
  }

  .image-stat {
    gap: 0.3rem;
    padding: 0.35rem 0.42rem;
    font-size: 0.54rem;
  }

  .showcase-footer {
    margin-top: 0.8rem;
  }
}

@media (max-width: 380px) {
  .login-page {
    padding-right: 0.5rem;
    padding-left: 0.5rem;
  }

  .login-panel {
    padding-right: 0.9rem;
    padding-left: 0.9rem;
  }

  .form-options {
    align-items: flex-start;
    flex-direction: column;
    gap: 0.75rem;
  }

  .forgot-btn {
    align-self: flex-start;
  }

  .showcase-content {
    padding: 1rem;
  }

  .live-status {
    padding-right: 0.45rem;
    padding-left: 0.45rem;
  }

  .showcase-copy h2 {
    font-size: 1.65rem;
  }

  .image-stat span {
    display: none;
  }

  .image-stat {
    width: 2rem;
    height: 2rem;
    justify-content: center;
    padding: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ticker-track,
  .spinner {
    animation: none;
  }

  .login-btn,
  .input-wrapper,
  .password-toggle {
    transition: none;
  }
}
</style>
