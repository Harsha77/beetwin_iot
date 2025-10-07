
import router from '@/router'
import { computed, reactive } from 'vue'
import { createResource } from 'frappe-ui'

import { userResource } from './user'

export function sessionUser() {
  const cookies = new URLSearchParams(document.cookie.split('; ').join('&'))
  let _sessionUser = cookies.get('user_id')
  if (_sessionUser === 'Guest') {
    _sessionUser = null
  }
  return _sessionUser
}

export const session = reactive({
  login: createResource({
    url: 'login',
    makeParams({ email, password }) {
      return {
        usr: email,
        pwd: password,
      }
    },
    onSuccess(data) {
      userResource.reload()
      session.user = sessionUser()
      session.login.reset()
      router.replace(data.default_route || '/')

      // Start idle timeout detection
      startIdleTimeout()
    },
  }),
  logout: createResource({
    url: 'logout',
    onSuccess() {
      userResource.reset()
      session.user = sessionUser()
      router.replace({ name: 'Login' })

      // Clear the logout timeout if manually logged out
      if (session.logoutTimeout) {
        clearTimeout(session.logoutTimeout)
      }
    },
  }),
  user: sessionUser(),
  isLoggedIn: computed(() => !!session.user),
  logoutTimeout: null, // To store the logout timeout reference
})

// Function to start/reset the idle timeout
function startIdleTimeout() {
  if (session.logoutTimeout) {
    clearTimeout(session.logoutTimeout)
  }

  session.logoutTimeout = setTimeout(() => {
    session.logout.submit()
  }, 1800000) // Logout after 1 minute of inactivity
}

// Function to listen for user activity
function resetIdleTimeout() {
  startIdleTimeout()
}

// Attach user activity event listeners
['mousemove', 'keydown', 'scroll', 'click'].forEach(event => {
  window.addEventListener(event, resetIdleTimeout)
})

userResource.onSuccess = () => {
  // Reset timeout if needed when user information is reloaded
  startIdleTimeout()
}

// Cleanup event listeners when the component is destroyed
window.addEventListener('beforeunload', () => {
  if (session.logoutTimeout) {
    clearTimeout(session.logoutTimeout)
  }
  ['mousemove', 'keydown', 'scroll', 'click'].forEach(event => {
    window.removeEventListener(event, resetIdleTimeout)
  })
})

