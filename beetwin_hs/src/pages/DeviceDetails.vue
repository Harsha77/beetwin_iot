<template>
  <div class="details-shell min-h-screen">
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

    <div
      v-if="isSidebarOpen"
      class="fixed inset-0 z-30 bg-slate-950/40 backdrop-blur-sm lg:hidden"
      @click="toggleSidebar"
    ></div>

    <main class="flex min-h-screen pt-24">
      <!-- Matching navigation sidebar -->
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
                <a href="#" class="nav-item nav-item-active" @click.prevent="openDashboard">
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

      <!-- Device report content -->
      <section
        :class="[
          'min-w-0 flex-1 px-4 py-6 transition-[margin] duration-300 sm:px-6 lg:px-8 lg:py-8',
          isSidebarOpen ? 'lg:ml-72' : 'lg:ml-0'
        ]"
      >
        <div class="mx-auto max-w-[1600px]">
          <div class="report-workspace">
          <!-- Page heading and report actions -->
          <div class="page-toolbar">
            <div class="flex min-w-0 items-center gap-4">
              <button
                type="button"
                class="content-back-button"
                aria-label="Back to dashboard"
                title="Back to dashboard"
                @click="$router.push('/')"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-5 w-5">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 18l-6-6 6-6" />
                </svg>
              </button>

              <div class="flex min-w-0 items-center gap-3">
                <span class="location-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-6 w-6">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1116 0z" />
                    <circle cx="12" cy="10" r="2.5" stroke-width="1.8" />
                  </svg>
                </span>
                <div class="min-w-0">
                  <h2 class="truncate text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">
                    {{ $route.query.serialNumber || "N/A" }}
                  </h2>
                </div>
              </div>
            </div>

            <button type="button" class="export-button" title="Download Excel report" @click="downloadReport">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-5 w-5">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M6 3h9l4 4v14H6V3zM14 3v5h5" />
                <path stroke-linecap="round" stroke-width="1.8" d="M9 12l6 6m0-6l-6 6" />
              </svg>
              <span>Export Excel</span>
            </button>
          </div>

          <!-- Date filter card -->
          <div class="filter-card">
            <div class="filter-heading">
              <span class="filter-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-5 w-5">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M7 3v3m10-3v3M4 9h16M5 5h14a1 1 0 011 1v14H4V6a1 1 0 011-1z" />
                </svg>
              </span>
              <div>
                <h3 class="text-sm font-extrabold text-slate-800">Report period</h3>
                <p class="text-xs text-slate-400">Choose a date range to generate the telemetry report</p>
              </div>
            </div>

            <div class="filter-controls">
              <label class="date-field">
                <span>From date</span>
                <input v-model="fromDate" type="date" />
              </label>

              <span class="date-divider hidden xl:flex">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-4 w-4">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14m-4-4l4 4-4 4" />
                </svg>
              </span>

              <label class="date-field">
                <span>To date</span>
                <input v-model="toDate" type="date" />
              </label>

              <button type="button" class="generate-button" @click="filterData">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-5 w-5">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4 5h16M7 12h10m-7 7h4" />
                </svg>
                Generate Report
              </button>
            </div>
          </div>

          <!-- Loading state -->
          <div v-if="isLoading" class="state-card">
            <span class="loading-ring"></span>
            <h3>Loading telemetry data</h3>
            <p>Please wait while the device report is prepared.</p>
          </div>

          <!-- Report table -->
          <div v-if="!isLoading && paginatedReportData.length > 0" class="data-panel overflow-hidden">
            <div class="panel-heading">
              <div class="flex items-center gap-3">
                <span class="panel-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-5 w-5">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4 5h16v14H4V5zm0 5h16M9 5v14" />
                  </svg>
                </span>
                <div>
                  <h3 class="text-sm font-extrabold text-slate-800">Telemetry readings</h3>
                  <p class="text-xs text-slate-400">Historical measurements for the selected device</p>
                </div>
              </div>

              <div class="record-count">
                <span></span>
                {{ reportData.length }} record{{ reportData.length === 1 ? "" : "s" }}
              </div>
            </div>

            <div class="table-scroll-area">
              <table class="report-table w-full">
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th class="text-right">Flowrate</th>
                    <th class="text-right">Totaliser</th>
                    <th class="text-right">Pressure</th>
                  </tr>
                </thead>

                <tbody>
                  <tr v-for="data in paginatedReportData" :key="data.timestamp">
                    <td class="report-timestamp" data-label="Timestamp">
                      <div class="timestamp-cell">
                        <span class="clock-icon">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-4 w-4">
                            <circle cx="12" cy="12" r="8" stroke-width="1.8" />
                            <path stroke-linecap="round" stroke-width="1.8" d="M12 8v5l3 2" />
                          </svg>
                        </span>
                        {{ data.timestamp.slice(0, 16) }}
                      </div>
                    </td>
                    <td class="text-right" data-label="Flowrate"><span class="metric metric-blue">{{ data.pv }}</span></td>
                    <td class="text-right" data-label="Totaliser"><span class="metric metric-cyan">{{ data.bt }}</span></td>
                    <td class="text-right" data-label="Pressure"><span class="metric metric-violet">{{ data.pressure }}</span></td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="pagination-bar">
              <div class="pagination-size">
                <span>Rows per page</span>
                <select v-model.number="reportRowsPerPage" class="page-size-select">
                  <option :value="10">10</option>
                  <option :value="25">25</option>
                  <option :value="50">50</option>
                  <option :value="100">100</option>
                </select>
                <span class="hidden sm:inline">
                  Showing {{ firstReportRow }}{{ lastReportRow }} of {{ reportData.length }}
                </span>
              </div>

              <div class="pagination-actions">
                <button
                  type="button"
                  class="page-button"
                  :disabled="reportPage === 1"
                  @click="prevReportPage"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-4 w-4">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 18l-6-6 6-6" />
                  </svg>
                  <span>Previous</span>
                </button>

                <span class="page-indicator">Page {{ reportPage }} of {{ totalReportPages }}</span>

                <button
                  type="button"
                  class="page-button"
                  :disabled="reportPage >= totalReportPages"
                  @click="nextReportPage"
                >
                  <span>Next</span>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-4 w-4">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 6l6 6-6 6" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Empty state -->
          <div v-if="!isLoading && reportData.length === 0" class="state-card">
            <span class="empty-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-8 w-8">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.6" d="M4 5h16v14H4V5zm0 5h16M9 5v14" />
              </svg>
            </span>
            <h3>No telemetry data available</h3>
            <p>No records were found for this device and selected date range.</p>
          </div>
          </div>

          <!-- Flowrate chart -->
          <div class="graph-container chart-panel">
            <div class="panel-heading">
              <div class="flex items-center gap-3">
                <span class="panel-icon panel-icon-orange">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-5 w-5">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4 18l5-6 4 3 7-9M4 20h16" />
                  </svg>
                </span>
                <div>
                  <h3 class="text-sm font-extrabold text-slate-800">Flowrate trend</h3>
                  <p class="text-xs text-slate-400">
                    {{ $route.query.serialNumber || "N/A" }}   Flowrate over time
                  </p>
                </div>
              </div>

              <button
                type="button"
                class="download-graph-button"
                title="Download graph"
                :disabled="isGraphDownloading"
                @click="downloadGraph"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-5 w-5">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 3v12m0 0l-4-4m4 4l4-4M5 19h14" />
                </svg>
                <span class="hidden sm:inline">
                  {{ isGraphDownloading ? "Preparing..." : "Download graph" }}
                </span>
              </button>
            </div>

            <div class="chart-body">
              <v-chart
                id="pressureChart"
                ref="flowrateChart"
                class="h-80 w-full"
                :option="chartOptions"
              />
            </div>
          </div>
           <p class="copyright mt-4 text-center text-xs text-slate-400">
  © {{ new Date().getFullYear() }} Happy IoT Solutions. All rights reserved.
</p>

          <!-- Keep the map target available while the client-facing map remains hidden. -->
          <div id="device-map" class="hidden-map" aria-hidden="true"></div>
        </div>
      </section>
    </main>

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
import { ref, computed, onMounted, watch, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import { session } from "../data/session";
import { createResource } from "frappe-ui";
import * as XLSX from "xlsx";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { use } from "echarts/core";
import { LineChart } from "echarts/charts";
import { CanvasRenderer } from "echarts/renderers";
import { GridComponent, TooltipComponent, LegendComponent } from "echarts/components";
import VChart from "vue-echarts";

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent]);

const route = useRoute();
const router = useRouter();
const deviceId = ref(route.params.deviceId);
const reportData = ref([]);
const reportPage = ref(1);
const reportRowsPerPage = ref(10);
const isLoading = ref(true);
const flowrateChart = ref(null);
const isGraphDownloading = ref(false);
const userImage = ref("/User.png");
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
let map = null;
const formatTime = (timestamp) => timestamp.slice(0, 16);
let markers = [];

const getCookie = (name) => {
  const cookies = document.cookie.split("; ");
  const cookie = cookies.find((row) => row.startsWith(`${name}=`));
  return cookie ? decodeURIComponent(cookie.split("=")[1]) : null;
};

const getUserImageFromCookie = () => getCookie("user_image");

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

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

const openDashboard = () => {
  router.push("/");
};

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

const openPasswordModal = () => {
  showModal.value = true;
  errorMessage.value = "";
  successMessage.value = "";
};

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

const logout = () => {
  session.logout.submit();
  isDropdownOpen.value = false;
};

const latestLatLong = computed(() => {
  const validEntries = reportData.value.filter(entry => entry.lat && entry.long);
  return validEntries.length > 0 ? validEntries.reduce((latest, entry) => {
    return new Date(entry.timestamp) > new Date(latest.timestamp) ? entry : latest;
  }) : null;
});

const downloadGraph = async () => {
  if (!flowrateChart.value) {
    alert("Graph is not ready yet. Please try again.");
    return;
  }

  isGraphDownloading.value = true;

  try {
    await nextTick();
    await new Promise((resolve) => requestAnimationFrame(resolve));

    let imgData = null;

    if (typeof flowrateChart.value.getDataURL === "function") {
      imgData = flowrateChart.value.getDataURL({
        type: "png",
        pixelRatio: 2,
        backgroundColor: "#ffffff"
      });
    }

    if (!imgData && typeof flowrateChart.value.chart?.getDataURL === "function") {
      imgData = flowrateChart.value.chart.getDataURL({
        type: "png",
        pixelRatio: 2,
        backgroundColor: "#ffffff"
      });
    }

    if (!imgData) {
      const chartCanvas = document.querySelector("#pressureChart canvas");
      imgData = chartCanvas?.toDataURL("image/png");
    }

    if (!imgData) {
      throw new Error("Unable to create the graph image.");
    }

    const link = document.createElement("a");
    link.href = imgData;
    link.download = `Flowrate_Graph_${route.query.serialNumber || "N/A"}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error("Error downloading graph:", error);
    alert("Unable to download the graph. Please try again.");
  } finally {
    isGraphDownloading.value = false;
  }
};

const downloadReport = () => {
  if (reportData.value.length === 0) {
    alert("No data available to download.");
    return;
  }

  const serialNumber = route.query.serialNumber || "N/A";
  const headerRow = [[`Location Name: ${serialNumber}`]];
  const tableHeaders = [["Timestamp", "Flowrate", "Totaliser", "Pressure"]];
  const tableData = reportData.value.map(data => [
    data.timestamp.slice(0, 16),
    data.pv,
    data.bt,
    data.pressure
  ]);

  const finalData = [...headerRow, [], ...tableHeaders, ...tableData];
  const worksheet = XLSX.utils.aoa_to_sheet(finalData);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Device Report");
  XLSX.writeFile(workbook, `Telemetry_Report_${serialNumber}.xlsx`);
};

const fromDate = ref("");
const toDate = ref("");

const getCsrfToken = async () => {
  try {
    if (window.csrf_token) {
      console.log("Using CSRF Token from window:", window.csrf_token);
      return window.csrf_token;
    }

    const response = await axios.get("/api/method/frappe.auth.get_logged_user", {
      withCredentials: true,
    });

    const csrfToken = response.headers["x-frappe-csrf-token"] || document.cookie.match(/csrftoken=([^;]+)/)?.[1];
    console.log("Fetched CSRF Token:", csrfToken);
    return csrfToken;
  } catch (error) {
    console.error("Failed to fetch CSRF Token:", error);
    return null;
  }
};

const fetchReportData = async () => {
  isLoading.value = true;

  const csrfToken = await getCsrfToken();
  if (!csrfToken) {
    console.error("CSRF Token is missing. Aborting request.");
    isLoading.value = false;
    return;
  }

  let payload = { device_data: deviceId.value };
  if (fromDate.value && toDate.value) {
    payload.from_date = fromDate.value;
    payload.to_date = toDate.value;
  }

  try {
    const response = await axios.post(
      "/api/method/beetwin_iot.beetwin_iot.report.btx_pp_timeseries_data_table.btx_pp_timeseries_data_table.generate_device_report",
      payload,
      {
        headers: {
          "Content-Type": "application/json",
          "X-Frappe-CSRF-Token": csrfToken,
          Accept: "application/json",
        },
        withCredentials: true,
      }
    );

    console.log("API Response Data:", response.data.message.data);
    reportData.value = response.data.message.data || [];
    reportPage.value = 1;
  } catch (error) {
    console.error("Error fetching report data:", error);
    reportData.value = [];
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  try {
    const loggedUser = await axios.get("/api/method/frappe.auth.get_logged_user", {
      withCredentials: true,
    });

    console.log("Logged-in User:", loggedUser.data.message);
    if (loggedUser.data.message === "Guest") {
      console.error("User is not logged in. Please log in first.");
    }
  } catch (error) {
    console.error("Error checking logged-in user:", error);
  }
});

const filterData = async () => {
  await fetchReportData();
};

const chartOptions = computed(() => {
  if (!Array.isArray(reportData.value) || reportData.value.length === 0) {
    return {
      title: {
        text: "No Flowrate Data Available",
        left: "center",
        top: "center",
        textStyle: {
          color: "#6b7280",
          fontSize: 16
        }
      }
    };
  }

  const validData = reportData.value
    .map((record) => {
      const rawFlowrate = record.flowrate ?? record.Flowrate ?? record.pv;
      const numericFlowrate = Number(rawFlowrate);

      return {
        timestamp: record.timestamp,
        flowrate: numericFlowrate
      };
    })
    .filter((record) => {
      return record.timestamp && Number.isFinite(record.flowrate);
    })
    .sort((first, second) => {
      const firstTime = new Date(String(first.timestamp).replace(" ", "T")).getTime();
      const secondTime = new Date(String(second.timestamp).replace(" ", "T")).getTime();
      return firstTime - secondTime;
    });

  if (validData.length === 0) {
    return {
      title: {
        text: "No Valid Flowrate Data Available",
        left: "center",
        top: "center",
        textStyle: {
          color: "#6b7280",
          fontSize: 16
        }
      }
    };
  }

  const timestamps = validData.map((record) => {
    const date = new Date(String(record.timestamp).replace(" ", "T"));
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const seconds = String(date.getSeconds()).padStart(2, "0");
    return `${day}/${month} ${hours}:${minutes}:${seconds}`;
  });

  const flowrateValues = validData.map((record) => record.flowrate);
  const minimumFlowrate = Math.min(...flowrateValues);
  const maximumFlowrate = Math.max(...flowrateValues);
  const valueDifference = maximumFlowrate - minimumFlowrate;
  const axisPadding = Math.max(valueDifference * 0.15, 5);
  const yAxisMinimum = Math.max(0, Math.floor(minimumFlowrate - axisPadding));
  const yAxisMaximum = Math.ceil(maximumFlowrate + axisPadding);
  const labelInterval = Math.max(0, Math.ceil(timestamps.length / 10) - 1);

  return {
    animation: validData.length <= 2000,
    animationDuration: 500,
    color: ["#00a3d3"],

    tooltip: {
      trigger: "axis",
      backgroundColor: "rgba(8, 68, 76, 0.95)",
      borderColor: "#00a3d3",
      borderWidth: 1,
      textStyle: {
        color: "#ffffff"
      },
      formatter: (parameters) => {
        const point = parameters?.[0];

        if (!point) {
          return "";
        }

        return `
          <strong>${point.axisValue}</strong><br/>
          Flowrate: <strong>${Number(point.data).toFixed(3)}</strong>
        `;
      }
    },

    grid: {
      left: "4%",
      right: "4%",
      top: "15%",
      bottom: "22%",
      containLabel: true
    },

    xAxis: {
      type: "category",
      boundaryGap: false,
      data: timestamps,
      name: "Timestamp",
      nameLocation: "middle",
      nameGap: 58,
      axisLine: {
        lineStyle: {
          color: "#9ca3af"
        }
      },
      axisTick: {
        alignWithLabel: true
      },
      axisLabel: {
        fontSize: window.innerWidth < 768 ? 9 : 11,
        rotate: 35,
        interval: labelInterval,
        color: "#374151"
      }
    },

    yAxis: {
      type: "value",
      name: "Flowrate",
      nameLocation: "middle",
      nameGap: 50,
      min: yAxisMinimum,
      max: yAxisMaximum,
      splitNumber: 6,
      scale: true,
      axisLabel: {
        color: "#374151",
        fontSize: window.innerWidth < 768 ? 9 : 11,
        formatter: (value) => Number(value).toFixed(1)
      },
      axisLine: {
        show: true,
        lineStyle: {
          color: "#9ca3af"
        }
      },
      splitLine: {
        show: true,
        lineStyle: {
          type: "dashed",
          color: "#d1d5db"
        }
      }
    },

    series: [
      {
        name: "Flowrate",
        type: "line",
        data: flowrateValues,
        smooth: true,
        sampling: "lttb",
        progressive: 2000,
        progressiveThreshold: 3000,
        connectNulls: false,
        showSymbol: flowrateValues.length <= 30,
        symbol: "circle",
        symbolSize: 6,
        lineStyle: {
          width: 3,
          color: "#FFA500"
        },
        itemStyle: {
          color: "#FFA500",
          borderColor: "#ffffff",
          borderWidth: 2
        },
        areaStyle: {
          color: "rgba(0, 163, 211, 0.15)"
        },
        emphasis: {
          focus: "series",
          itemStyle: {
            borderWidth: 3,
            shadowBlur: 10,
            shadowColor: "rgba(0, 163, 211, 0.5)"
          }
        }
      }
    ]
  };
});

const paginatedReportData = computed(() => {
  const start = (reportPage.value - 1) * reportRowsPerPage.value;
  return reportData.value.slice(start, start + reportRowsPerPage.value);
});

const totalReportPages = computed(() => {
  return Math.max(1, Math.ceil(reportData.value.length / reportRowsPerPage.value));
});

const firstReportRow = computed(() => {
  if (reportData.value.length === 0) return 0;
  return (reportPage.value - 1) * reportRowsPerPage.value + 1;
});

const lastReportRow = computed(() => {
  return Math.min(reportPage.value * reportRowsPerPage.value, reportData.value.length);
});

watch(reportRowsPerPage, () => {
  reportPage.value = 1;
});

const nextReportPage = () => {
  if (reportPage.value < totalReportPages.value) reportPage.value++;
};

const prevReportPage = () => {
  if (reportPage.value > 1) reportPage.value--;
};

const initializeMap = () => {
  if (map) {
    return;
  }

  map = L.map("device-map", {
    center: [22.3511, 78.6677],
    zoom: 5,
    maxBounds: [
      [6.5, 68.0],
      [35.0, 97.5],
    ],
    maxBoundsViscosity: 1.0,
  });

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);
  updateMap();
};

const locationName = ref("Fetching...");

const getLocationName = async (lat, long) => {
  try {
    const response = await axios.get(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${long}`);
    if (response.data && response.data.display_name) {
      return response.data.display_name;
    }
  } catch (error) {
    console.error("Error fetching location name:", error);
  }
  return "Unknown Location";
};

const updateMap = async () => {
  if (!map) {
    console.warn("Map is not initialized yet.");
    return;
  }

  console.log("Updating Map...");
  markers.forEach(marker => map.removeLayer(marker));
  markers = [];

  let latestEntry = reportData.value
    .filter(entry => entry.lat && entry.long)
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))[0];

  let latestDataEntry = reportData.value
    .filter(entry => entry.pv !== null && entry.pv !== undefined && entry.bt !== null && entry.bt !== undefined)
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))[0];

  if (!latestEntry || !latestDataEntry) {
    console.warn("No valid latitude/longitude or PV/BT found.");
    return;
  }

  let latestLat = Number(latestEntry.lat);
  let latestLong = Number(latestEntry.long);
  let latestPressure = latestDataEntry.pv ?? "N/A";
  let latestBattery = latestDataEntry.bt ?? "N/A";
  let latestTimestamp = new Date(latestEntry.timestamp).toLocaleString("en-GB", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false
  }).replace(",", "");

  locationName.value = await getLocationName(latestLat, latestLong);

  const customIcon = L.icon({
    iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
    shadowSize: [41, 41]
  });

  let marker = L.marker([latestLat, latestLong], { icon: customIcon }).addTo(map);
  markers.push(marker);

  let popupContent = `
    <strong>Device ID:</strong> ${deviceId.value} <br>
    <strong>Serial Number:</strong> ${route.query.serialNumber || "N/A"} <br>
    <strong>Pressure:</strong> ${latestPressure} bar<br>
    <strong>Battery:</strong> ${latestBattery}% <br>
    <strong>Timestamp:</strong> ${latestTimestamp} <br>
  `;

  marker.bindPopup(popupContent);
  marker.on("mouseover", function () {
    this.openPopup();
  });
  marker.on("mouseout", function () {
    this.closePopup();
  });

  console.log("Latest Marker Plotted at:", latestLat, latestLong, "Location:", locationName.value);
  map.setView([latestLat, latestLong], 12);
};

watch(paginatedReportData, updateMap, { deep: true });

const resetMap = () => {
  if (map) {
    map.remove();
    map = null;
  }
  initializeMap();
};

watch(
  reportData,
  () => {
    resetMap();
    updateMap();
  },
  { deep: true }
);

onMounted(async () => {
  if (window.user_image_path) {
    userImage.value = window.user_image_path;
  } else {
    const imagePath = getCookie("user_image");

    if (imagePath) {
      userImage.value = imagePath;
    }
  }

  await fetchReportData();
  initializeMap();
  updateMap();
});
</script>

<style scoped>
.details-shell {
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

.header-eyebrow { color: #168da4; }
.header-title { color: #173447; }

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
  transition: all 0.2s ease;
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

.midc-logo { filter: drop-shadow(0 3px 6px rgba(94, 31, 38, 0.1)); }

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

.user-menu { border: 1px solid rgba(226, 232, 240, 0.9); }

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
  text-align: left;
  color: #cbd5e1;
  transition: all 0.2s ease;
}

button.nav-item:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.07);
}

.nav-item-active {
  border-color: rgba(139, 230, 235, 0.25);
  color: #ffffff;
  background: linear-gradient(90deg, rgba(37, 183, 155, 0.28), rgba(24, 168, 189, 0.14));
  box-shadow: inset 3px 0 0 #5eead4;
}

.nav-icon {
  display: flex;
  width: 2.25rem;
  height: 2.25rem;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  border-radius: 0.7rem;
  color: #99f6e4;
  background: rgba(94, 234, 212, 0.13);
}

.report-workspace,
.chart-panel {
  border: 1px solid #dbe5ea;
  background: rgba(255, 255, 255, 0.97);
  box-shadow: 0 11px 30px rgba(24, 63, 78, 0.065);
}

.report-workspace {
  margin-bottom: 1.15rem;
  overflow: hidden;
  border-radius: 1.2rem;
}

.page-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  margin: 0;
  border: 0;
  border-radius: 0;
  padding: 1.3rem 1.4rem;
  background: #ffffff;
  box-shadow: none;
}

.breadcrumb-link { transition: color 0.18s ease; }
.breadcrumb-link:hover { color: #087f9a; }

.location-icon {
  display: flex;
  width: 3rem;
  height: 3rem;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  border: 1px solid #c8edf1;
  border-radius: 0.9rem;
  color: #087f9a;
  background: linear-gradient(135deg, #effcfd, #e9f8fa);
}

.content-back-button {
  display: inline-flex;
  width: 2.7rem;
  height: 2.7rem;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  border: 1px solid #cfe0e7;
  border-radius: 0.8rem;
  color: #176c80;
  background: #f7fbfc;
  box-shadow: 0 3px 10px rgba(31, 78, 94, 0.08);
  transition: all 0.2s ease;
}

.content-back-button:hover {
  transform: translateX(-2px);
  border-color: #75c6d2;
  color: #08687d;
  background: #eaf8fa;
}

.export-button,
.generate-button,
.download-graph-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.export-button {
  min-width: 10.3rem;
  height: 3rem;
  gap: 0.55rem;
  border: 1px solid #087f9a;
  border-radius: 0.8rem;
  padding: 0 1rem;
  font-size: 0.8rem;
  font-weight: 800;
  color: #ffffff;
  background: linear-gradient(135deg, #087f9a, #159fb2);
  box-shadow: 0 7px 16px rgba(8, 127, 154, 0.2);
}

.export-button:hover,
.generate-button:hover,
.download-graph-button:hover {
  transform: translateY(-1px);
}

.export-button:hover {
  background: linear-gradient(135deg, #07697f, #087f9a);
  box-shadow: 0 10px 22px rgba(8, 127, 154, 0.27);
}

.filter-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  margin: 0;
  border: 0;
  border-top: 1px solid #e4edf1;
  border-radius: 0;
  padding: 1rem 1.25rem;
  background: linear-gradient(90deg, #f8fbfc, #f3fafb);
  box-shadow: none;
}

.filter-heading,
.filter-controls {
  display: flex;
  align-items: center;
}

.filter-heading { gap: 0.75rem; }
.filter-controls { gap: 0.7rem; }

.filter-icon,
.panel-icon {
  display: flex;
  width: 2.6rem;
  height: 2.6rem;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  border-radius: 0.8rem;
  color: #087f9a;
  background: #ecfbfc;
}

.date-field span {
  display: block;
  margin-bottom: 0.35rem;
  font-size: 0.65rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #718394;
}

.date-field input {
  width: 10.6rem;
  height: 2.7rem;
  border: 1px solid #d5e2e8;
  border-radius: 0.72rem;
  padding: 0 0.75rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: #334155;
  background: #ffffff;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.date-field input:focus {
  border-color: #159fb2;
  box-shadow: 0 0 0 3px rgba(21, 159, 178, 0.11);
}

.date-divider {
  width: 1.8rem;
  height: 1.8rem;
  align-items: center;
  justify-content: center;
  margin-top: 1.15rem;
  border-radius: 9999px;
  color: #94a3b8;
  background: #f1f5f9;
}

.generate-button {
  height: 2.7rem;
  align-self: flex-end;
  gap: 0.5rem;
  border: 1px solid #12856f;
  border-radius: 0.72rem;
  padding: 0 1rem;
  font-size: 0.78rem;
  font-weight: 800;
  color: #ffffff;
  background: linear-gradient(135deg, #12856f, #20a58c);
  box-shadow: 0 6px 14px rgba(18, 133, 111, 0.19);
}

.generate-button:hover {
  background: linear-gradient(135deg, #0d725f, #12856f);
  box-shadow: 0 9px 20px rgba(18, 133, 111, 0.25);
}

.data-panel,
.chart-panel { border-radius: 1.2rem; }

.report-workspace .data-panel {
  margin: 0;
  border: 0;
  border-top: 1px solid #e4edf1;
  border-radius: 0;
  background: #ffffff;
  box-shadow: none;
}

.panel-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  border-bottom: 1px solid #e7eef2;
  padding: 1rem 1.35rem;
}

.record-count {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: #5a7180;
}

.record-count span {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 9999px;
  background: #18a8bd;
}

.table-scroll-area {
  max-height: 29rem;
  overflow: auto;
}

.report-table {
  min-width: 47.5rem;
  border-collapse: separate;
  border-spacing: 0;
}

.report-table th {
  position: sticky;
  top: 0;
  z-index: 5;
  padding: 0.95rem 1.25rem;
  border-bottom: 1px solid #0a6071;
  font-size: 0.7rem;
  font-weight: 800;
  text-align: left;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #ffffff;
  background: #0d6677;
}

.report-table th + th { border-left: 1px solid rgba(255, 255, 255, 0.1); }
.report-table th.text-right { text-align: right; }

.report-table td {
  padding: 0.9rem 1.25rem;
  border-bottom: 1px solid #e7eef2;
  font-size: 0.82rem;
  vertical-align: middle;
  white-space: nowrap;
  color: #465d6c;
}

.report-table td + td { border-left: 1px solid #f0f4f6; }
.report-table td.text-right { text-align: right; }
.report-table tbody tr:nth-child(even) { background: #f8fbfc; }
.report-table tbody tr:hover { background: #edfbfc; }
.report-table tbody tr:last-child td { border-bottom: 0; }

.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  border-top: 1px solid #e4edf1;
  padding: 0.85rem 1.25rem;
  background: #f8fbfc;
}

.pagination-size,
.pagination-actions {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 0.74rem;
  font-weight: 700;
  color: #647887;
}

.page-size-select {
  height: 2.25rem;
  border: 1px solid #d5e2e8;
  border-radius: 0.62rem;
  padding: 0 1.8rem 0 0.65rem;
  font-size: 0.75rem;
  font-weight: 800;
  color: #334e60;
  background: #ffffff;
  outline: none;
}

.page-button {
  display: inline-flex;
  height: 2.25rem;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  border: 1px solid #d5e2e8;
  border-radius: 0.62rem;
  padding: 0 0.75rem;
  font-size: 0.73rem;
  font-weight: 800;
  color: #496473;
  background: #ffffff;
  transition: all 0.18s ease;
}

.page-button:not(:disabled):hover {
  border-color: #80cbd5;
  color: #087f9a;
  background: #ecfbfc;
}

.page-button:disabled {
  cursor: not-allowed;
  opacity: 0.42;
}

.page-indicator {
  min-width: 7rem;
  text-align: center;
}

.timestamp-cell {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-weight: 650;
  color: #334e60;
}

.clock-icon {
  display: flex;
  width: 1.8rem;
  height: 1.8rem;
  align-items: center;
  justify-content: center;
  border-radius: 0.55rem;
  color: #5f7484;
  background: #f1f5f7;
}

.metric {
  display: inline-block;
  min-width: 5.2rem;
  border: 1px solid transparent;
  border-radius: 0.58rem;
  padding: 0.36rem 0.65rem;
  font-size: 0.78rem;
  font-weight: 800;
  text-align: center;
}

.metric-blue { border-color: #bfdbfe; color: #1d4ed8; background: #eff6ff; }
.metric-cyan { border-color: #a5f3fc; color: #0e7490; background: #ecfeff; }
.metric-violet { border-color: #ddd6fe; color: #6d28d9; background: #f5f3ff; }

.state-card {
  display: flex;
  min-height: 17rem;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0;
  border: 0;
  border-top: 1px solid #e4edf1;
  border-radius: 0;
  padding: 2rem;
  text-align: center;
  background: #ffffff;
  box-shadow: none;
}

.state-card h3 {
  margin-top: 1rem;
  font-size: 0.95rem;
  font-weight: 800;
  color: #334155;
}

.state-card p {
  margin-top: 0.3rem;
  font-size: 0.8rem;
  color: #94a3b8;
}

.loading-ring {
  width: 2.8rem;
  height: 2.8rem;
  border: 3px solid #d9f2f5;
  border-top-color: #159fb2;
  border-radius: 9999px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.empty-icon {
  display: flex;
  width: 4rem;
  height: 4rem;
  align-items: center;
  justify-content: center;
  border-radius: 1rem;
  color: #087f9a;
  background: #ecfbfc;
}

.chart-panel {
  width: 100%;
  max-width: 100%;
  overflow: hidden;
}

.panel-icon-orange { color: #c96a05; background: #fff7ed; }

.download-graph-button {
  height: 2.55rem;
  gap: 0.45rem;
  border: 1px solid #d5e2e8;
  border-radius: 0.72rem;
  padding: 0 0.8rem;
  font-size: 0.74rem;
  font-weight: 800;
  color: #496473;
  background: #ffffff;
  box-shadow: 0 3px 10px rgba(31, 78, 94, 0.06);
}

.download-graph-button:hover {
  border-color: #80cbd5;
  color: #087f9a;
  background: #f1fbfc;
  box-shadow: 0 7px 16px rgba(8, 127, 154, 0.12);
}

.download-graph-button:disabled {
  cursor: wait;
  transform: none;
  opacity: 0.68;
}

.chart-body {
  min-width: 42rem;
  padding: 0.8rem 1rem 0.2rem;
  overflow-x: auto;
}

#pressureChart {
  width: 100% !important;
  height: 340px !important;
}

.hidden-map {
  position: fixed;
  right: -10000px;
  bottom: -10000px;
  width: 400px;
  height: 400px;
  visibility: hidden;
  pointer-events: none;
}

.modal-card { border: 1px solid rgba(255, 255, 255, 0.6); }
.modal-header { background: linear-gradient(135deg, #164e63, #0891b2); }

.form-field { display: block; }
.form-field span { display: block; margin-bottom: 0.4rem; font-size: 0.72rem; font-weight: 800; color: #475569; }
.form-field input { width: 100%; height: 2.75rem; border: 1px solid #dbe4ec; border-radius: 0.75rem; padding: 0 0.9rem; font-size: 0.85rem; color: #1e293b; outline: none; transition: all 0.2s ease; }
.form-field input:focus { border-color: #0891b2; box-shadow: 0 0 0 3px rgba(8, 145, 178, 0.1); }

.primary-button {
  display: inline-flex;
  height: 2.8rem;
  align-items: center;
  justify-content: center;
  border-radius: 0.85rem;
  padding: 0 1rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: #ffffff;
  background: linear-gradient(135deg, #0e7490, #0891b2);
  box-shadow: 0 8px 18px rgba(8, 145, 178, 0.2);
}

.secondary-button {
  height: 2.8rem;
  border: 1px solid #dbe4ec;
  border-radius: 0.85rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: #475569;
  background: #ffffff;
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
  .filter-card {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-controls { justify-content: flex-start; }
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

  .report-workspace,
  .chart-panel {
    border-radius: 1rem;
  }

  .page-toolbar {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .page-toolbar > div:first-child {
    gap: 0.75rem;
  }

  .content-back-button {
    width: 2.5rem;
    height: 2.5rem;
  }

  .location-icon {
    width: 2.65rem;
    height: 2.65rem;
  }

  .page-toolbar h2 {
    overflow-wrap: anywhere;
    font-size: 1.35rem;
    white-space: normal;
  }

  .export-button { width: 100%; }

  .filter-card {
    gap: 1rem;
  }

  .filter-controls {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }

  .date-field input { width: 100%; }
  .generate-button { grid-column: 1 / -1; width: 100%; }
  .pagination-bar { align-items: stretch; flex-direction: column; }
  .pagination-actions { justify-content: space-between; }

  .table-scroll-area {
    max-height: 34rem;
    padding: 0.75rem;
    overflow-x: hidden;
    overflow-y: auto;
    background: #f3f8fa;
  }

  .report-table {
    min-width: 0;
  }

  .report-table thead {
    display: none;
  }

  .report-table tbody,
  .report-table tr,
  .report-table td {
    display: block;
    width: 100%;
  }

  .report-table tbody tr {
    margin-bottom: 0.75rem;
    overflow: hidden;
    border: 1px solid #d9e6eb;
    border-radius: 0.9rem;
    background: #ffffff !important;
    box-shadow: 0 5px 16px rgba(31, 78, 94, 0.07);
  }

  .report-table tbody tr:last-child {
    margin-bottom: 0;
  }

  .report-table tbody tr:hover {
    background: #ffffff !important;
    box-shadow: 0 7px 20px rgba(8, 127, 154, 0.12);
  }

  .report-table td {
    display: flex;
    min-height: 3rem;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.68rem 0.9rem;
    border: 0 !important;
    border-bottom: 1px solid #edf2f5 !important;
    font-size: 0.8rem;
    text-align: right !important;
    white-space: normal;
  }

  .report-table td::before {
    flex: 0 0 5.25rem;
    content: attr(data-label);
    font-size: 0.62rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-align: left;
    text-transform: uppercase;
    color: #8294a0;
  }

  .report-table .report-timestamp {
    min-height: 3.65rem;
    background: linear-gradient(135deg, #f7fcfd, #effbfc);
  }

  .report-table .timestamp-cell {
    justify-content: flex-end;
    text-align: right;
  }

  .report-table td:last-child {
    border-bottom: 0 !important;
  }

  .metric {
    min-width: 5.25rem;
  }

  .chart-body {
    min-width: 0;
    padding: 0.5rem 0.25rem 0;
    overflow: hidden;
  }

  #pressureChart {
    height: 300px !important;
  }
}

@media (max-width: 639px) {
  .page-toolbar,
  .filter-card { padding: 1rem; }
  .filter-controls { grid-template-columns: 1fr; }
  .generate-button { grid-column: auto; }
  .panel-heading {
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.9rem 1rem;
  }
  .record-count { display: none; }
  .page-button span { display: none; }
  .page-button { width: 2.25rem; padding: 0; }

  .filter-heading {
    align-items: flex-start;
  }

  .pagination-size {
    justify-content: space-between;
  }

  .page-indicator {
    font-size: 0.7rem;
  }

  .download-graph-button {
    width: 2.55rem;
    flex: 0 0 auto;
    padding: 0;
  }
}
</style>
