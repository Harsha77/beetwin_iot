<template>
  <div class="dashboard-shell min-h-screen">
    <!-- Fixed application header -->
    <header class="app-header fixed inset-x-0 top-0 z-50 h-24">
      <div class="flex h-full items-center gap-3 px-4 sm:px-6 lg:px-8">
        <div class="flex min-w-0 items-center gap-3 lg:w-[22rem]">
          <button
            type="button"
            class="icon-button"
            :aria-label="isSidebarOpen ? 'Close navigation' : 'Open navigation'"
            :title="isSidebarOpen ? 'Close menu' : 'Open menu'"
            @click="toggleSidebar"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-6 w-6">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          <div class="brand-logo-wrap">
            <img
              src="/public/HS.png"
              alt="Happy Solutions Logo"
              class="h-12 w-auto object-contain sm:h-14"
            />
          </div>
        </div>

        <div class="min-w-0 flex-1 text-center">
          <p class="header-eyebrow hidden text-[10px] font-bold uppercase tracking-[0.28em] sm:block">
            Water Infrastructure Monitoring
          </p>
          <h1 class="header-title truncate text-base font-extrabold tracking-tight sm:text-xl lg:text-2xl">
            MIDC Mahape - Watermain Dashboard
          </h1>
        </div>

        <div class="flex items-center justify-end gap-3 lg:w-[22rem]">
          <div class="system-status hidden xl:flex">
            <span class="status-pulse"></span>
            <span class="system-status-label">System status:</span>
            <span class="system-status-value">Monitoring active</span>
          </div>

          <img
            src="/public/MIDC.png"
            alt="MIDC Logo"
            class="midc-logo hidden h-12 w-auto object-contain sm:block lg:h-14"
          />

          <!-- User dropdown -->
          <div class="relative">
            <button
              type="button"
              class="user-button"
              aria-label="Open user menu"
              @click.stop="toggleDropdown"
            >
              <img :src="userImage" alt="User profile" class="h-full w-full rounded-full object-cover" />
              <span class="absolute bottom-0 right-0 h-3 w-3 rounded-full border-2 border-white bg-emerald-500"></span>
            </button>

            <transition name="dropdown">
              <div v-if="isDropdownOpen" class="user-menu absolute right-0 mt-3 w-72 overflow-hidden rounded-2xl bg-white shadow-2xl">
                <div class="border-b border-slate-100 bg-slate-50 px-5 py-4">
                  <p class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Signed in as</p>
                  <p class="mt-1 break-all text-sm font-semibold text-slate-800">{{ currentUser }}</p>
                </div>

                <div class="p-2">
                  <button type="button" class="menu-item" @click="openPasswordModal">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-5 w-5">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M15 7a4 4 0 11-7.9 1M9 11l-5 5v3h3v-2h2v-2h2l2-2" />
                    </svg>
                    Change password
                  </button>

                  <button type="button" class="menu-item menu-item-danger" @click="logout">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-5 w-5">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M10 17l5-5-5-5M15 12H3m10-8h5a2 2 0 012 2v12a2 2 0 01-2 2h-5" />
                    </svg>
                    Logout
                  </button>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </header>

    <!-- Mobile navigation overlay -->
    <div
      v-if="isSidebarOpen"
      class="fixed inset-0 z-30 bg-slate-950/40 backdrop-blur-sm lg:hidden"
      @click="toggleSidebar"
    ></div>

    <main class="flex min-h-screen pt-24">
      <!-- Sidebar -->
      <aside
        :class="[
          'sidebar fixed bottom-0 left-0 top-24 z-40 w-72 transform transition-transform duration-300',
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        ]"
      >
        <div class="flex h-full flex-col p-5 pt-7">
          <nav class="flex-1">
            <ul>
              <li>
                <a href="#" class="nav-item nav-item-active" @click.prevent="setDashboardTab">
                  <span class="nav-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-5 w-5">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4 4h6v6H4V4zm10 0h6v6h-6V4zM4 14h6v6H4v-6zm10 0h6v6h-6v-6z" />
                    </svg>
                  </span>
                  <span>Dashboard</span>
                  <span class="ml-auto h-1.5 w-1.5 rounded-full bg-cyan-300"></span>
                </a>
              </li>
            </ul>
          </nav>

        </div>
      </aside>

      <!-- Dashboard content -->
      <section
        v-if="selectedTab === 2"
        :class="[
          'min-w-0 flex-1 px-4 py-6 transition-[margin] duration-300 sm:px-6 lg:px-8 lg:py-8',
          isSidebarOpen ? 'lg:ml-72' : 'lg:ml-0'
        ]"
      >
        <div class="mx-auto max-w-[1600px]">
          <!-- Compact dashboard toolbar -->
          <div class="dashboard-toolbar">
            <div class="toolbar-title">
              <div class="mb-2 flex items-center gap-2 text-xs font-semibold text-slate-400">
                
              </div>
              <h2 class="text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">Device Telemetry</h2>
             
            </div>

            <div class="toolbar-actions">
              <label class="search-box group">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-5 w-5 shrink-0 text-slate-400 transition group-focus-within:text-cyan-600">
                  <circle cx="11" cy="11" r="7" stroke-width="2" />
                  <path stroke-linecap="round" stroke-width="2" d="M20 20l-4-4" />
                </svg>
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search serial number..."
                  class="min-w-0 flex-1 bg-transparent text-sm text-slate-800 outline-none placeholder:text-slate-400"
                />
                <span v-if="searchQuery" class="hidden rounded border border-slate-200 bg-slate-50 px-1.5 py-0.5 text-[10px] font-semibold text-slate-400 sm:inline">FILTER</span>
              </label>

              <button type="button" class="export-button" title="Download Excel report" @click="downloadReport">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-5 w-5">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M6 3h9l4 4v14H6V3zM14 3v5h5" />
                  <path stroke-linecap="round" stroke-width="1.8" d="M9 12l6 6m0-6l-6 6" />
                </svg>
                <span>Export Excel</span>
              </button>
            </div>
          </div>

          <!-- Device table panel -->
          <div class="data-panel overflow-hidden">
            <div class="flex flex-col gap-3 border-b border-slate-100 px-5 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6">
              <div class="flex items-center gap-3">
                <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-50 text-cyan-700">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-5 w-5">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4 5h16v14H4V5zm0 5h16M9 5v14" />
                  </svg>
                </span>
                <div>
                 
                </div>
              </div>

              <div class="flex items-center gap-2 text-xs font-semibold text-slate-500">
                <span class="h-2 w-2 rounded-full bg-cyan-500"></span>
                {{ sortedDeviceList.length }} record{{ sortedDeviceList.length === 1 ? "" : "s" }} found
              </div>
            </div>

            <div class="device-table-wrap">
              <table class="device-table w-full">
                <thead>
                  <tr>
                    <th><span>Serial Number</span></th>
                    <th><span>Device ID</span></th>
                    <th><span>Timestamp</span></th>
                    <th class="text-right"><span>Flowrate</span></th>
                    <th class="text-right"><span>Totaliser</span></th>
                    <th class="text-right"><span>Pressure</span></th>
                    <th class="w-14"><span class="sr-only">Open</span></th>
                  </tr>
                </thead>

                <tbody>
                  <tr v-if="deviceList.length === 0">
                    <td colspan="7" class="empty-state-cell">
                      <div class="empty-state">
                        <span class="empty-state-icon">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-8 w-8">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.6" d="M12 9v4m0 4h.01M10.3 4.4L2.8 17.5A2 2 0 004.5 20h15a2 2 0 001.7-2.5L13.7 4.4a2 2 0 00-3.4 0z" />
                          </svg>
                        </span>
                        <h4>No permitted devices found</h4>
                        <p>No allowed device groups were returned for this account.</p>
                      </div>
                    </td>
                  </tr>

                  <tr
                    v-for="device in paginatedDevices"
                    :key="device.deviceId"
                    class="device-row"
                    @click="navigateToDevice(device.deviceId, device.serialNumber)"
                  >
                    <td class="serial-cell" data-label="Serial Number">
                      <div class="flex items-center gap-3">
                        <span class="device-avatar">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-5 w-5">
                            <rect x="5" y="3" width="14" height="18" rx="2" stroke-width="1.8" />
                            <path stroke-linecap="round" stroke-width="1.8" d="M9 8h6M9 12h6M10 17h4" />
                          </svg>
                        </span>
                        <div class="min-w-0">
                          <p class="device-name font-bold text-slate-800">{{ device.serialNumber }}</p>
                        </div>
                      </div>
                    </td>
                    <td class="device-id-cell" data-label="Device ID">
                      <span class="device-id-text">{{ device.deviceId }}</span>
                    </td>
                    <td class="timestamp-cell" data-label="Timestamp">
                      <div class="flex items-center gap-2 text-slate-600">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-4 w-4 shrink-0 text-slate-400">
                          <circle cx="12" cy="12" r="9" stroke-width="1.8" />
                          <path stroke-linecap="round" stroke-width="1.8" d="M12 7v5l3 2" />
                        </svg>
                        {{ device.timestamp }}
                      </div>
                    </td>
                    <td class="metric-cell text-right" data-label="Flowrate"><span class="measurement measurement-blue">{{ device.latestData.flowrate }}</span></td>
                    <td class="metric-cell text-right" data-label="Totaliser"><span class="measurement measurement-cyan">{{ device.latestData.totaliser }}</span></td>
                    <td class="metric-cell text-right" data-label="Pressure"><span class="measurement measurement-violet">{{ device.latestData.pressure || "N/A" }}</span></td>
                    <td class="open-cell">
                      <span class="row-arrow">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-4 w-4">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                      </span>
                    </td>
                  </tr>

                  <tr v-if="deviceList.length > 0 && paginatedDevices.length === 0">
                    <td colspan="7" class="empty-state-cell">
                      <div class="empty-state py-10">
                        <h4>No matching serial number</h4>
                        <p>Try a different search term.</p>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Pagination -->
            <div class="flex flex-col gap-4 border-t border-slate-100 bg-slate-50/70 px-5 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6">
              <div class="flex items-center gap-3 text-sm text-slate-500">
                <label for="rows-per-page" class="font-medium">Rows per page</label>
                <select id="rows-per-page" v-model.number="rowsPerPage" class="page-size-select">
                  <option :value="10">10</option>
                  <option :value="25">25</option>
                  <option :value="50">50</option>
                  <option :value="100">100</option>
                </select>
              </div>

              <div class="flex items-center justify-between gap-3 sm:justify-end">
                <p class="hidden text-sm text-slate-500 sm:block">
                  Page <span class="font-bold text-slate-800">{{ currentPage }}</span> of
                  <span class="font-bold text-slate-800">{{ totalPages }}</span>
                </p>

                <div class="flex items-center gap-2">
                  <button type="button" class="page-button" :disabled="currentPage === 1" @click="prevPage">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-4 w-4">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                    <span>Previous</span>
                  </button>

                  <span class="flex h-9 min-w-9 items-center justify-center rounded-lg bg-slate-800 px-3 text-sm font-bold text-white sm:hidden">{{ currentPage }}</span>

                  <button type="button" class="page-button" :disabled="currentPage >= totalPages" @click="nextPage">
                    <span>Next</span>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-4 w-4">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          
         <p class="copyright mt-4 text-center text-xs text-slate-400">
  © {{ new Date().getFullYear() }} Happy IoT Solutions. All rights reserved.
</p>
        </div>
      </section>
    </main>

    <!-- Change password modal -->
    <transition name="modal">
      <div v-if="showModal" class="fixed inset-0 z-[70] flex items-center justify-center bg-slate-950/60 p-4 backdrop-blur-sm">
        <div class="modal-card w-full max-w-md overflow-hidden rounded-3xl bg-white shadow-2xl">
          <div class="modal-header px-6 py-6">
            <div class="flex items-start justify-between gap-4">
              <div class="flex items-center gap-3">
                <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-white/15 text-white">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-6 w-6">
                    <rect x="5" y="10" width="14" height="10" rx="2" stroke-width="1.8" />
                    <path stroke-linecap="round" stroke-width="1.8" d="M8 10V7a4 4 0 018 0v3" />
                  </svg>
                </span>
                <div>
                  <h2 class="text-xl font-extrabold text-white">Change Password</h2>
                  <p class="mt-0.5 text-xs text-cyan-100">Update your account security</p>
                </div>
              </div>
              <button type="button" class="rounded-lg p-2 text-white/70 transition hover:bg-white/10 hover:text-white" aria-label="Close modal" @click="showModal = false">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-5 w-5">
                  <path stroke-linecap="round" stroke-width="2" d="M6 6l12 12M18 6L6 18" />
                </svg>
              </button>
            </div>
          </div>

          <div class="space-y-4 p-6">
            <label class="form-field">
              <span>Current password</span>
              <input v-model="currentPassword" type="password" placeholder="Enter current password" />
            </label>

            <label class="form-field">
              <span>New password</span>
              <input v-model="newPassword" type="password" placeholder="Enter new password" />
            </label>

            <label class="form-field">
              <span>Confirm new password</span>
              <input v-model="confirmPassword" type="password" placeholder="Re-enter new password" />
            </label>

            <div v-if="errorMessage" class="alert-message alert-error">{{ errorMessage }}</div>
            <div v-if="successMessage" class="alert-message alert-success">{{ successMessage }}</div>

            <div class="flex gap-3 pt-2">
              <button type="button" class="secondary-button flex-1" @click="showModal = false">Cancel</button>
              <button type="button" class="primary-button flex-1" @click="changePassword">Update Password</button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { session } from "../data/session";
import { createResource } from "frappe-ui";
import * as XLSX from "xlsx";

const router = useRouter();

const userImage = ref("/User.png");
const deviceList = ref([]);
const searchQuery = ref("");
const rowsPerPage = ref(10);
const currentPage = ref(1);
const selectedTab = ref(2);
const isSidebarOpen = ref(
  typeof window !== "undefined" && window.innerWidth >= 1024
);
const isDropdownOpen = ref(false);

const showModal = ref(false);
const successMessage = ref("");
const errorMessage = ref("");
const currentPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");

const currentUser = ref(session.user || "Guest");

/**
 * Check whether an API value is valid.
 * Numeric zero is considered valid.
 */
const hasValue = (value) => {
  return value !== null && value !== undefined && value !== "" && value !== "null";
};

/** Convert a value for table display. */
const displayValue = (value) => {
  return hasValue(value) ? String(value) : "N/A";
};

/** Read a cookie value. */
const getCookie = (name) => {
  const cookies = document.cookie.split("; ");
  const cookie = cookies.find((row) => row.startsWith(`${name}=`));
  return cookie ? decodeURIComponent(cookie.split("=")[1]) : null;
};

const getUserImageFromCookie = () => {
  return getCookie("user_image");
};

/** Fetch the logged-in user's information. */
const fetchUserImage = async (username) => {
  try {
    const response = await fetch(`/api/resource/User/${encodeURIComponent(username)}`);

    if (!response.ok) {
      return null;
    }

    const result = await response.json();
    return result?.data || result;
  } catch (error) {
    console.error("Error fetching user image:", error);
    return null;
  }
};

/** Fetch the logged-in user automatically. */
createResource({
  url: "/api/method/frappe.auth.get_logged_user",
  auto: true,

  onSuccess: async (response) => {
    const username = response?.message || response;

    if (!username) {
      return;
    }

    currentUser.value = username;
    const userDetails = await fetchUserImage(username);
    const imagePath = userDetails?.user_image || getUserImageFromCookie() || "/User.png";

    userImage.value = imagePath;
    window.user_image_path = imagePath;
  }
});

/** Sidebar methods. */
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

const setDashboardTab = () => {
  selectedTab.value = 2;
};

/** Dropdown methods. */
const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

/** Change password modal. */
const openPasswordModal = () => {
  showModal.value = true;
  errorMessage.value = "";
  successMessage.value = "";
};

/** Change password API. */
const changePassword = async () => {
  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = "Passwords do not match.";
    return;
  }

  try {
    const response = await axios.post(
      "/api/method/beetwin_iot.beetwin_iot.api.changedpassword.admin_change_password",
      {
        user: currentUser.value,
        old_password: currentPassword.value,
        new_password: newPassword.value
      }
    );

    if (response.data.message === "Password Updated") {
      successMessage.value = "Password changed successfully.";

      setTimeout(() => {
        showModal.value = false;
      }, 1500);
    } else {
      errorMessage.value = response.data.message || "Unexpected error.";
    }
  } catch (error) {
    console.error("Password API error:", error.response?.data || error);
    errorMessage.value = error.response?.data?.message || "Failed to update password.";
  }
};

/** Logout. */
const logout = () => {
  session.logout.submit();
  isDropdownOpen.value = false;
};

/** Fetch telemetry devices. */
const fetchDevices = async () => {
  try {
    const response = await axios.get(
      "/api/method/beetwin_iot.beetwin_iot.api.get_latest_device_data.get_filtered_device_data"
    );

    console.log("API Response from Cloud:", response.data);
    const apiMessage = response.data?.message;

    if (apiMessage?.status !== "success") {
      console.error("Invalid API response:", apiMessage?.message || response.data);
      deviceList.value = [];
      return;
    }

    const apiDevices = Array.isArray(apiMessage.data) ? apiMessage.data : [];

    deviceList.value = apiDevices
      .filter((device) => {
        if (!device) {
          return false;
        }

        return (
          hasValue(device["Serial Number"]) ||
          hasValue(device["Flowrate"]) ||
          hasValue(device["Totaliser"])
        );
      })
      .map((device) => {
        /* Backend keys are case-sensitive: Flowrate and Totaliser. */
        const flowrate = device["Flowrate"];
        const totaliser = device["Totaliser"];

        return {
          deviceId: displayValue(device["Device ID"]),
          serialNumber: displayValue(device["Serial Number"]),
          timestamp: hasValue(device["Timestamp"])
            ? String(device["Timestamp"]).slice(0, 16)
            : "N/A",
          latestData: {
            flowrate: displayValue(flowrate),
            totaliser: displayValue(totaliser),
            ht: hasValue(device["Sensor Health"])
              ? String(device["Sensor Health"])
              : null,
            rssi: displayValue(device["RSSI Value"])
          }
        };
      });

    currentPage.value = 1;
    console.log("Final mapped device list:", deviceList.value);
  } catch (error) {
    deviceList.value = [];
    console.error("Error fetching devices:", error.response?.data || error);
  }
};

/** Search and sorting. */
const sortedDeviceList = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();

  return deviceList.value
    .filter((device) =>
      String(device.serialNumber).toLowerCase().includes(query)
    )
    .sort((a, b) =>
      String(a.serialNumber).localeCompare(String(b.serialNumber), undefined, {
        numeric: true
      })
    );
});

/** Pagination total uses filtered device list. */
const totalPages = computed(() => {
  return Math.max(1, Math.ceil(sortedDeviceList.value.length / rowsPerPage.value));
});

/** Devices displayed on the current page. */
const paginatedDevices = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage.value;
  return sortedDeviceList.value.slice(start, start + rowsPerPage.value);
});

/** Reset pagination after search or rows-per-page changes. */
watch([searchQuery, rowsPerPage], () => {
  currentPage.value = 1;
});

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

/** Excel download. */
const downloadReport = () => {
  if (deviceList.value.length === 0) {
    alert("No data to export.");
    return;
  }

  const sortedData = [...deviceList.value].sort((a, b) =>
    String(a.serialNumber).localeCompare(String(b.serialNumber), undefined, {
      numeric: true
    })
  );

  const reportData = sortedData.map((device) => ({
    "Serial Number": device.serialNumber,
    "Device ID": device.deviceId,
    Timestamp: device.timestamp,
    Flowrate: device.latestData.flowrate,
    Totaliser: device.latestData.totaliser,
    Pressure: device.latestData.pressure
  }));

  const worksheet = XLSX.utils.json_to_sheet(reportData);
  const workbook = XLSX.utils.book_new();

  XLSX.utils.book_append_sheet(workbook, worksheet, "MIDC TTC Data");
  XLSX.writeFile(workbook, "MIDC TTC Data.xlsx");
};

/** Device report API. */
const fetchDeviceReport = async (deviceData, fromDate, toDate) => {
  try {
    const csrfToken = window.frappe?.csrf_token;

    const response = await fetch(
      "/api/method/beetwin_iot.beetwin_iot.report.btx_pp_timeseries_data_table.btx_pp_timeseries_data_table.generate_device_report",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Frappe-CSRF-Token": csrfToken
        },
        credentials: "include",
        body: JSON.stringify({
          device_data: deviceData,
          from_date: fromDate,
          to_date: toDate
        })
      }
    );

    const report = await response.json();
    console.log(report);
  } catch (error) {
    console.error("Error fetching device report:", error);
  }
};

/** Open device details. */
const navigateToDevice = (deviceId, serialNumber) => {
  router.push({
    name: "DeviceDetails",
    params: { deviceId },
    query: { serialNumber }
  });
};

/** Page initialization. */
onMounted(() => {
  if (window.user_image_path) {
    userImage.value = window.user_image_path;
  } else {
    const imagePath = getCookie("user_image");

    if (imagePath) {
      userImage.value = imagePath;
    }
  }

  fetchDevices();
});
</script>

<style scoped>
.dashboard-shell {
  color: #1f3344;
  background:
    radial-gradient(circle at 100% 0%, rgba(21, 164, 183, 0.09), transparent 30rem),
    linear-gradient(180deg, #f7fafc 0%, #edf4f7 100%);
}

.app-header {
  border-bottom: 1px solid #d9e5ea;
  background: rgba(255, 255, 255, 0.97);
  box-shadow: 0 8px 30px rgba(27, 67, 82, 0.09);
  backdrop-filter: blur(18px);
}

.app-header::after {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  height: 3px;
  content: "";
  background: linear-gradient(90deg, #087f9a 0%, #18a8bd 52%, #25b79b 100%);
}

.header-eyebrow {
  color: #168da4;
}

.header-title {
  color: #173447;
  text-shadow: none;
}

.brand-logo-wrap {
  display: flex;
  min-width: 4.5rem;
  height: 4rem;
  align-items: center;
  justify-content: center;
  border-radius: 0.75rem;
  padding: 0.2rem;
  background: #ffffff;
}

.icon-button {
  display: inline-flex;
  width: 2.75rem;
  height: 2.75rem;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  border: 1px solid #cfe0e7;
  border-radius: 0.8rem;
  color: #176c80;
  background: #f7fbfc;
  box-shadow: 0 3px 10px rgba(31, 78, 94, 0.08);
  transition: border-color 0.2s ease, color 0.2s ease, background 0.2s ease, transform 0.2s ease;
}

.icon-button:hover {
  transform: translateY(-1px);
  border-color: #75c6d2;
  color: #08687d;
  background: #eaf8fa;
}

.status-pulse {
  width: 0.45rem;
  height: 0.45rem;
  border-radius: 9999px;
  background: #10b981;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.12);
}

.system-status {
  align-items: center;
  gap: 0.4rem;
  min-height: 2.65rem;
  padding: 0 0.9rem;
  border: 1px solid #d3e3e8;
  border-radius: 9999px;
  white-space: nowrap;
  background: #f7fbfc;
  box-shadow: 0 4px 14px rgba(28, 75, 91, 0.07);
}

.system-status-label {
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #536b79;
}

.system-status-value {
  font-size: 0.76rem;
  font-weight: 700;
  color: #087f68;
}

.midc-logo {
  filter: drop-shadow(0 3px 6px rgba(94, 31, 38, 0.1));
}

.user-button {
  position: relative;
  width: 2.8rem;
  height: 2.8rem;
  padding: 0.15rem;
  border: 2px solid #ffffff;
  border-radius: 9999px;
  background: #e2e8f0;
  box-shadow: 0 0 0 1px #cfe0e7, 0 5px 16px rgba(28, 75, 91, 0.13);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.user-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 0 2px rgba(8, 145, 178, 0.25), 0 8px 20px rgba(15, 23, 42, 0.15);
}

.user-menu {
  border: 1px solid rgba(226, 232, 240, 0.9);
}

.menu-item {
  display: flex;
  width: 100%;
  align-items: center;
  gap: 0.75rem;
  border-radius: 0.75rem;
  padding: 0.7rem 0.8rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  transition: background 0.18s ease, color 0.18s ease;
}

.menu-item:hover { background: #f1f5f9; color: #0f172a; }
.menu-item-danger:hover { background: #fff1f2; color: #e11d48; }

.sidebar {
  overflow-y: auto;
  background:
    radial-gradient(circle at 10% 0%, rgba(75, 211, 218, 0.15), transparent 17rem),
    linear-gradient(175deg, #0c5264 0%, #083e50 52%, #062f3d 100%);
  box-shadow: 12px 0 30px rgba(15, 23, 42, 0.08);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border: 1px solid transparent;
  border-radius: 0.9rem;
  padding: 0.75rem;
  font-size: 0.875rem;
  font-weight: 700;
  color: #cbd5e1;
  transition: all 0.2s ease;
}

.nav-item-active {
  border-color: rgba(139, 230, 235, 0.25);
  color: #fff;
  background: linear-gradient(90deg, rgba(37, 183, 155, 0.28), rgba(24, 168, 189, 0.14));
  box-shadow: inset 3px 0 0 #5eead4;
}

.nav-icon {
  display: flex;
  width: 2.25rem;
  height: 2.25rem;
  align-items: center;
  justify-content: center;
  border-radius: 0.7rem;
  color: #99f6e4;
  background: rgba(94, 234, 212, 0.13);
}

.dashboard-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  margin-bottom: 1.25rem;
  padding: 1.25rem 1.35rem;
  border: 1px solid #dbe4ec;
  border-radius: 1.15rem;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
}

.toolbar-title {
  min-width: 17rem;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
}

.search-box {
  display: flex;
  width: 19rem;
  height: 3rem;
  align-items: center;
  gap: 0.65rem;
  border: 1px solid #dbe4ec;
  border-radius: 0.8rem;
  padding: 0 0.9rem;
  background: #fff;
  box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.search-box input {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  border: 0 !important;
  border-radius: 0;
  outline: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
  appearance: none;
}

.search-box:focus-within {
  border-color: #0891b2;
  box-shadow: 0 0 0 3px rgba(8, 145, 178, 0.1);
}

.export-button {
  display: inline-flex;
  min-width: 10.2rem;
  height: 3rem;
  align-items: center;
  justify-content: center;
  gap: 0.55rem;
  border: 1px solid #087f9a;
  border-radius: 0.8rem;
  padding: 0 1rem;
  font-size: 0.8rem;
  font-weight: 800;
  color: #fff;
  white-space: nowrap;
  background: linear-gradient(135deg, #087f9a, #159fb2);
  box-shadow: 0 7px 16px rgba(8, 127, 154, 0.2);
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.export-button:hover {
  transform: translateY(-1px);
  background: linear-gradient(135deg, #07697f, #087f9a);
  box-shadow: 0 10px 22px rgba(8, 127, 154, 0.27);
}

.primary-button {
  display: inline-flex;
  height: 2.8rem;
  align-items: center;
  justify-content: center;
  border-radius: 0.85rem;
  padding: 0 1rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: #fff;
  background: linear-gradient(135deg, #0e7490, #0891b2);
  box-shadow: 0 8px 18px rgba(8, 145, 178, 0.2);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.primary-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 11px 24px rgba(8, 145, 178, 0.27);
}

.data-panel {
  border: 1px solid #dbe4ec;
  border-radius: 1.2rem;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 12px 35px rgba(15, 23, 42, 0.07);
}

.device-table-wrap {
  overflow-x: auto;
}

.device-table {
  min-width: 55rem;
  border-collapse: separate;
  border-spacing: 0;
}

.device-table th {
  padding: 0.9rem 1.15rem;
  border-bottom: 1px solid #0a6071;
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-align: left;
  text-transform: uppercase;
  white-space: nowrap;
  color: #fff;
  background: #0d6677;
}

.device-table th + th { border-left: 1px solid rgba(255, 255, 255, 0.1); }
.device-table th.text-right { text-align: right; }

.device-table td {
  padding: 0.95rem 1.15rem;
  border-bottom: 1px solid #e5ebf1;
  font-size: 0.84rem;
  vertical-align: middle;
  white-space: nowrap;
  color: #475569;
}

.device-table td + td { border-left: 1px solid #f0f4f7; }
.device-table td.text-right { text-align: right; }
.device-table tbody .device-row:nth-child(even) { background: #f8fbfc; }

.device-table tbody tr:last-child td { border-bottom: 0; }

.device-row {
  cursor: pointer;
  transition: background 0.18s ease, box-shadow 0.18s ease;
}

.device-row:hover {
  background: #ecfeff !important;
  box-shadow: inset 3px 0 0 #06b6d4;
}

.row-number {
  display: inline-flex;
  min-width: 1.8rem;
  height: 1.8rem;
  align-items: center;
  justify-content: center;
  border-radius: 0.55rem;
  font-size: 0.7rem;
  font-weight: 800;
  color: #94a3b8;
  background: #f1f5f9;
}

.device-avatar {
  display: flex;
  width: 2.4rem;
  height: 2.4rem;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  border: 1px solid #bae6fd;
  border-radius: 0.75rem;
  color: #0284c7;
  background: linear-gradient(135deg, #f0f9ff, #ecfeff);
}

.device-id-text {
  display: inline-block;
  max-width: 14rem;
  overflow: hidden;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.76rem;
  font-weight: 600;
  text-overflow: ellipsis;
  color: #334155;
}

.measurement {
  display: inline-block;
  min-width: 4.5rem;
  border: 1px solid transparent;
  border-radius: 0.55rem;
  padding: 0.35rem 0.65rem;
  font-size: 0.78rem;
  font-weight: 800;
  text-align: center;
}

.measurement-blue { border-color: #bfdbfe; color: #1d4ed8; background: #eff6ff; }
.measurement-cyan { border-color: #a5f3fc; color: #0e7490; background: #ecfeff; }
.measurement-violet { border-color: #ddd6fe; color: #6d28d9; background: #f5f3ff; }

.row-arrow {
  display: flex;
  width: 2rem;
  height: 2rem;
  align-items: center;
  justify-content: center;
  border-radius: 0.6rem;
  color: #94a3b8;
  transition: transform 0.2s ease, color 0.2s ease, background 0.2s ease;
}

.device-row:hover .row-arrow {
  transform: translateX(2px);
  color: #0891b2;
  background: #cffafe;
}

.empty-state-cell { white-space: normal !important; }
.empty-state { display: flex; flex-direction: column; align-items: center; padding: 4rem 1rem; text-align: center; }
.empty-state-icon { display: flex; width: 4rem; height: 4rem; align-items: center; justify-content: center; border-radius: 1rem; color: #f43f5e; background: #fff1f2; }
.empty-state h4 { margin-top: 1rem; font-size: 0.95rem; font-weight: 800; color: #334155; }
.empty-state p { margin-top: 0.3rem; font-size: 0.8rem; color: #94a3b8; }

.page-size-select {
  height: 2.3rem;
  border: 1px solid #dbe4ec;
  border-radius: 0.65rem;
  padding: 0 2rem 0 0.7rem;
  font-size: 0.8rem;
  font-weight: 700;
  color: #334155;
  background-color: #fff;
  outline: none;
}

.page-button {
  display: inline-flex;
  height: 2.3rem;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  border: 1px solid #dbe4ec;
  border-radius: 0.65rem;
  padding: 0 0.8rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: #475569;
  background: #fff;
  transition: all 0.18s ease;
}

.page-button:not(:disabled):hover { border-color: #0891b2; color: #0e7490; background: #ecfeff; }
.page-button:disabled { cursor: not-allowed; opacity: 0.42; }

.modal-card { border: 1px solid rgba(255, 255, 255, 0.6); }
.modal-header { background: linear-gradient(135deg, #164e63, #0891b2); }

.form-field { display: block; }
.form-field span { display: block; margin-bottom: 0.4rem; font-size: 0.72rem; font-weight: 800; color: #475569; }
.form-field input { width: 100%; height: 2.75rem; border: 1px solid #dbe4ec; border-radius: 0.75rem; padding: 0 0.9rem; font-size: 0.85rem; color: #1e293b; outline: none; transition: all 0.2s ease; }
.form-field input:focus { border-color: #0891b2; box-shadow: 0 0 0 3px rgba(8, 145, 178, 0.1); }

.secondary-button {
  height: 2.8rem;
  border: 1px solid #dbe4ec;
  border-radius: 0.85rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: #475569;
  background: #fff;
}

.alert-message { border-radius: 0.75rem; padding: 0.7rem 0.85rem; font-size: 0.78rem; font-weight: 600; }
.alert-error { border: 1px solid #fecdd3; color: #be123c; background: #fff1f2; }
.alert-success { border: 1px solid #a7f3d0; color: #047857; background: #ecfdf5; }

.dropdown-enter-active,
.dropdown-leave-active,
.modal-enter-active,
.modal-leave-active { transition: all 0.2s ease; }
.dropdown-enter-from,
.dropdown-leave-to { transform: translateY(-6px) scale(0.98); opacity: 0; }
.modal-enter-from,
.modal-leave-to { opacity: 0; }
.modal-enter-from .modal-card,
.modal-leave-to .modal-card { transform: translateY(10px) scale(0.98); }

@media (max-width: 1279px) {
  .dashboard-toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .toolbar-title {
    min-width: 0;
  }

  .toolbar-actions {
    justify-content: flex-start;
  }

  .search-box {
    width: auto;
    flex: 1;
  }
}

@media (max-width: 767px) {
  .app-header > div {
    gap: 0.35rem;
    padding-right: 0.55rem;
    padding-left: 0.55rem;
  }

  .app-header .lg\:w-\[22rem\] {
    width: auto;
  }

  .app-header > div > div:first-child {
    flex: 0 0 auto;
    gap: 0.3rem;
  }

  .brand-logo-wrap {
    display: flex !important;
    width: 3.35rem;
    min-width: 3.35rem;
    height: 2.45rem;
    padding: 0.1rem;
    border: 1px solid #d9e6eb;
    border-radius: 0.65rem;
    box-shadow: 0 3px 10px rgba(31, 78, 94, 0.07);
  }

  .brand-logo-wrap img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  .app-header > div > div:last-child {
    flex: 0 0 auto;
    gap: 0.3rem;
  }

  .midc-logo {
    display: block !important;
    width: 2.15rem;
    min-width: 2.15rem;
    height: 2.45rem;
    object-fit: contain;
  }

  .icon-button {
    width: 2.35rem;
    height: 2.35rem;
    border-radius: 0.7rem;
  }

  .user-button {
    width: 2.3rem;
    height: 2.3rem;
  }

  .header-title {
    overflow: visible;
    font-size: 0.68rem;
    line-height: 1.15;
    white-space: normal;
  }

  .sidebar {
    width: min(18rem, 86vw);
  }

  .user-menu {
    right: -0.25rem;
    width: min(18rem, calc(100vw - 1.5rem));
  }

  .dashboard-toolbar {
    gap: 1rem;
    margin-bottom: 0.9rem;
    padding: 1rem;
    border-radius: 1rem;
  }

  .toolbar-title h2 {
    font-size: 1.35rem;
  }

  .data-panel {
    overflow: visible;
    border-radius: 1rem;
  }

  .device-table-wrap {
    overflow: visible;
    padding: 0.75rem;
    background: #f3f8fa;
  }

  .device-table {
    min-width: 0;
  }

  .device-table thead {
    display: none;
  }

  .device-table tbody,
  .device-table tr,
  .device-table td {
    display: block;
    width: 100%;
  }

  .device-table tbody .device-row {
    position: relative;
    margin-bottom: 0.75rem;
    overflow: hidden;
    border: 1px solid #d9e6eb;
    border-radius: 1rem;
    background: #ffffff !important;
    box-shadow: 0 5px 16px rgba(31, 78, 94, 0.07);
  }

  .device-table tbody .device-row:last-child {
    margin-bottom: 0;
  }

  .device-table tbody .device-row:hover {
    background: #ffffff !important;
    box-shadow: 0 7px 20px rgba(8, 127, 154, 0.12);
  }

  .device-table .device-row td {
    display: flex;
    min-height: 3rem;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.68rem 1rem;
    border: 0 !important;
    border-bottom: 1px solid #edf2f5 !important;
    font-size: 0.8rem;
    text-align: right !important;
    white-space: normal;
  }

  .device-table .device-row td::before {
    flex: 0 0 5.5rem;
    content: attr(data-label);
    font-size: 0.62rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-align: left;
    text-transform: uppercase;
    color: #8294a0;
  }

  .device-table .device-row .serial-cell {
    min-height: 4.3rem;
    justify-content: flex-start;
    padding: 0.9rem 3.2rem 0.9rem 1rem;
    background: linear-gradient(135deg, #f7fcfd, #effbfc);
  }

  .device-table .device-row .serial-cell::before,
  .device-table .device-row .open-cell::before {
    display: none;
  }

  .device-name {
    overflow-wrap: anywhere;
    text-align: left;
  }

  .device-id-text {
    max-width: calc(100vw - 9rem);
    overflow-wrap: anywhere;
    text-align: right;
    white-space: normal;
  }

  .timestamp-cell > div {
    justify-content: flex-end;
  }

  .device-table .device-row .open-cell {
    position: absolute;
    top: 1.05rem;
    right: 0.75rem;
    width: 2rem;
    min-height: 2rem;
    padding: 0;
    border: 0 !important;
  }

  .device-table .device-row td:nth-last-child(2) {
    border-bottom: 0 !important;
  }

  .device-table .empty-state-cell {
    display: block !important;
    border: 0 !important;
    text-align: center !important;
  }

  .device-table .empty-state-cell::before {
    display: none;
  }

  .empty-state {
    padding: 2.5rem 1rem;
  }
}

@media (max-width: 639px) {
  .dashboard-toolbar {
    padding: 1rem;
  }

  .toolbar-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box,
  .export-button {
    width: 100%;
  }

  .search-box { min-width: 100%; }
  .export-button { width: 100%; }
  .page-button span { display: none; }
  .page-button { width: 2.3rem; padding: 0; }
}
</style>
