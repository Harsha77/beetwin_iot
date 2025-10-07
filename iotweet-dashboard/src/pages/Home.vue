<template>
  <div class="min-h-screen flex flex-col">
    <header
      class="fixed top-0 left-0 w-full flex items-center justify-between py-4 border-b bg-[#08444c] shadow px-5 z-50">
      <img src="/IOtweet Logo_2.0 white.png" alt="IoTweet Logo" class="w-28" />
      <div class="text-white flex-1 text-center font-bold text-xl">BEETWIN-HS DASHBOARD</div>
      <button @click="toggleSidebar" class="lg:hidden text-white ml-auto">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      <!-- User Info Dropdown -->
      <div class="relative ml-4" @click="toggleDropdown">
        <button class="bg-gray-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold">
          <!-- Dynamically set the user's image -->

          <!-- <img src="/User.png" alt="IoTweet Logo" class="w-full h-full object-cover rounded-full" /> -->
          <img :src="userImage" alt="User Image" class="w-full h-full object-cover rounded-full" />


        </button>
        <!-- Dropdown Menu -->
        <div v-if="isDropdownOpen" class="absolute right-0 mt-2 w-64 bg-white rounded-md shadow-lg z-20">
          <!-- Display User Info -->
          <p class="block px-4 py-2 text-gray-700 font-semibold break-all">
            {{ currentUser }}
          </p>
          <a href="#" @click="showAccountInfo" class="block px-4 py-2 text-gray-700 hover:bg-gray-100">Account Info</a>
          <!-- <a href="#" @click="openPasswordModal" class="block px-4 py-2 text-gray-700 hover:bg-gray-100">Change Password</a>  -->
          <a href="#" @click="logout" class="block px-4 py-2 text-gray-700 hover:bg-gray-100">Logout</a>
        </div>
        <!-- Change Password Modal -->
        <div v-if="showModal" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
          <div class="bg-white p-6 rounded-md w-96">
            <h2 class="text-xl font-bold mb-4">Change Password</h2>

            <input v-model="currentPassword" type="password" placeholder="Current Password"
              class="w-full p-2 border rounded-md mb-2">
            <input v-model="newPassword" type="password" placeholder="New Password"
              class="w-full p-2 border rounded-md mb-2">
            <input v-model="confirmPassword" type="password" placeholder="Confirm New Password"
              class="w-full p-2 border rounded-md mb-4">

            <button @click="changePassword" class="w-full bg-blue-500 text-white p-2 rounded-md">Update
              Password</button>
            <button @click="showModal = false" class="w-full mt-2 text-gray-600">Cancel</button>

            <p v-if="errorMessage" class="text-red-500 mt-2">{{ errorMessage }}</p>
            <p v-if="successMessage" class="text-green-500 mt-2">{{ successMessage }}</p>
          </div>
        </div>
      </div>
    </header>

    <main class="flex-grow flex flex-col md:flex-row">
      <aside
        :class="{ 'hidden': !isSidebarOpen, 'lg:block': true, 'bg-[#08444c] text-white p-5 border-r transition-all duration-300': true }"
        class="mt-16">
        <nav>
          <ul class="space-y-4 text-lg font-semibold">
            <li>
              <a href="#" @click="setDashboardTab" class="flex items-center space-x-2 hover:text-gray-300">
                <img src="/Dashboard_Icon.png" alt="Download" class="w-7 h-7" />
                <span>Dashboard</span>
              </a>
            </li>

            <li>
              <a href="#" @click="setDiagnosticTab" class="flex items-center space-x-2 hover:text-gray-300">
                <img src="/Diagnostic.png" alt="Diagnostic Icon" class="w-7 h-7" />
                <span>Diagnostic</span>
              </a>
            </li>
            <!-- Add more sidebar items here -->
          </ul>

        </nav>
      </aside>
      <div class="flex-grow p-6 pt-16" v-if="selectedTab === 2">
        <!-- <h1 class="text-center text-2xl font-bold leading-[3.15] flex-1">BTX-PP</h1> -->
        <!-- <h1 class="text-2xl font-bold leading-[3.15] ml-[583px]">BTX-PP</h1> -->
        <div class="flex justify-between items-center p-4">
          <h2 class="text-lg font-semibold leading-[3.15] ml-[583px]">BTX-PP</h2>
          <div class="flex items-center gap-2">
            <input type="text" v-model="searchQuery" placeholder="Search Serial Number"
              class="border p-2 rounded-md w-64" />
            <button @click="downloadReport" class="ml-4"><img src="/Download.png" alt="Download"
                class="w-10 h-10" /></button>
          </div>
        </div>
        <div class="mt-4">
          <div class="flex justify-end mb-2">

          </div>


          <table class="table-auto w-full border-collapse border border-gray-300">
            <!-- <thead class="bg-gray-200"> -->
            <thead class="bg-[#08444c] text-white">
              <tr>
                <th class="border border-gray-300 px-4 py-2 text-center">Serial Number</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Device ID</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Timestamp</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Pressure (bar)</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Battery (%)</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Sensor Health</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Latitude</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Longitude</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Signal Strength</th>
              </tr>
            </thead>
            <tbody>

              <tr v-if="deviceList.length === 0">
                <td colspan="9" class="text-center text-red-500 font-bold py-4">No allowed device groups found.</td>
              </tr>

              <tr v-for="device in paginatedDevices" :key="device.deviceId"
                @click="navigateToDevice(device.deviceId, device.serialNumber)"
                class="cursor-pointer hover:bg-gray-100 transition-all text-center">

                <td class="border border-gray-300 px-4 py-2">{{ device.serialNumber }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ device.deviceId }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ device.timestamp }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ device.latestData.pv }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ device.latestData.bt }}</td>
                <td class="border border-gray-300 px-4 py-2">
                  {{ device.latestData.ht === "0" ? "Open" : "Healthy" }}
                </td>
                <td class="border border-gray-300 px-4 py-2">{{ device.latestData.lat }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ device.latestData.long }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ device.latestData.rssi }}</td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination Controls -->
          <div class="flex justify-between items-center mt-4">
            <div>
              <label class="mr-2 ">Items per page:</label>
              <select v-model="rowsPerPage" class="border p-2 rounded-md w-15">
                <option value="10">10</option>
                <option value="25">25</option>
                <option value="50">50</option>
                <option value="100">100</option>
              </select>
            </div>
            <div>
              <button @click="prevPage" :disabled="currentPage === 1"
                class="px-4 py-2 border rounded-md bg-gray-200 mr-2">Prev</button>
              <span>Page {{ currentPage }} of {{ totalPages }}</span>
              <button @click="nextPage" :disabled="currentPage === totalPages"
                class="px-4 py-2 border rounded-md bg-gray-200 ml-2">Next</button>
            </div>
          </div>
        </div>
      </div>

      <div class="flex-grow p-6 pt-16" v-if="selectedTab === 1">
        <!-- <h1 class="text-center text-2xl font-bold leading-[3.15] flex-1">BTX-PP</h1> -->
        <!-- <h1 class="text-2xl font-bold leading-[3.15] ml-[583px]">BTX-PP</h1> -->
        <div class="flex justify-between items-center p-4">
          <h2 class="text-lg font-semibold leading-[3.15] ml-[583px]">DIAGNOSTIC</h2>
          <div class="flex items-center gap-2">
            <input type="text" v-model="searchQuery" placeholder="Search Serial Number"
              class="border p-2 rounded-md w-64" />
            <button @click="downloaddiagnosticReport" class="ml-4"><img src="/Download.png" alt="Download"
                class="w-10 h-10" /></button>
          </div>
        </div>
        <div class="mt-4">
          <div class="flex justify-end mb-2">
            <!-- <h1 class="text-center text-2xl font-bold flex items-center justify-center ml-4">BTX-PP</h1> -->

            <!-- <button @click="downloadReport" class="bg-red-500 text-white w-40 h-10 text-lg rounded flex items-center justify-center ml-4">
                Export
              </button> -->

          </div>


          <table class="table-auto w-full border-collapse border border-gray-300">
            <!-- <thead class="bg-gray-200"> -->
            <thead class="bg-[#08444c] text-white">
              <tr>
                <th class="border border-gray-300 px-4 py-2 text-center">Serial Number</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Device ID</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Timestamp</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Retry Count</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Device Reset Status</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Sensor Health</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Mqtt Server Status</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Device Software Version</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Signal Strength</th>
              </tr>
            </thead>
            <tbody>

              <tr v-if="deviceListfordiagnostic.length === 0">
                <td colspan="9" class="text-center text-red-500 font-bold py-4">No allowed device groups found.</td>
              </tr>
              <!-- <tr 
                v-for="device in paginatedDevices" 
                :key="device.deviceId" 
                @click="navigateToDevice(device.deviceId)" 
                class="cursor-pointer hover:bg-gray-100 transition-all text-center"
              > -->
              <tr v-for="deviceforDiagnostic in paginatedDiagnosticDevices" :key="deviceforDiagnostic.deviceId"
                @click="navigateToDiagnosticDevice(deviceforDiagnostic.deviceId, deviceforDiagnostic.serialNumber)"
                class="cursor-pointer hover:bg-gray-100 transition-all text-center">

                <td class="border border-gray-300 px-4 py-2">{{ deviceforDiagnostic.serialNumber }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ deviceforDiagnostic.deviceId }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ deviceforDiagnostic.timestamp }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ deviceforDiagnostic.latestDiagnosticData.rc }}</td>
                <td class="border border-gray-300 px-4 py-2">
                  {{ deviceforDiagnostic.latestDiagnosticData.rst === "1" ? "Reset" : "Not Reset" }}</td>
                <td class="border border-gray-300 px-4 py-2">
                  {{ deviceforDiagnostic.latestDiagnosticData.ht === "0" ? "Open" : "Healthy" }}
                </td>
                <td class="border border-gray-300 px-4 py-2">
                  {{ deviceforDiagnostic.latestDiagnosticData.ms === "0" ? "Data Not Sent" : "Data Sent" }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ deviceforDiagnostic.latestDiagnosticData.sv }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ deviceforDiagnostic.latestDiagnosticData.rssi }}</td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination Controls -->
          <div class="flex justify-between items-center mt-4">
            <div>
              <label class="mr-2 ">Items per page:</label>
              <select v-model="rowsPerPage" class="border p-2 rounded-md w-15">
                <option value="10">10</option>
                <option value="25">25</option>
                <option value="50">50</option>
                <option value="100">100</option>
              </select>
            </div>
            <div>
              <button @click="prevPage" :disabled="currentPage === 1"
                class="px-4 py-2 border rounded-md bg-gray-200 mr-2">Prev</button>
              <span>Page {{ currentPage }} of {{ totalPages }}</span>
              <button @click="nextPage" :disabled="currentPage === totalPages"
                class="px-4 py-2 border rounded-md bg-gray-200 ml-2">Next</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>



<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { session } from '../data/session';  // Import session management

import { createResource } from "frappe-ui";

import * as XLSX from "xlsx";


const userImage = ref("/User.png"); // Default image


const { data } = createResource({
  url: "/api/method/frappe.auth.get_logged_user",
  auto: true,
  onSuccess: async (user) => {
    if (user) {
      const userDetails = await fetchUserImage(user.message);
      const imagePath = userDetails?.user_image || getUserImageFromCookie() || "/User.png";
      userImage.value = imagePath;
      window.user_image_path = imagePath; // Store in window for reference
      console.log("Image Path:", imagePath);
    }
  },
});

const fetchUserImage = async (username) => {

};

// Function to extract user_image from cookies
const getUserImageFromCookie = () => {
  const match = document.cookie.match(/user_image=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : null;
};

// Ensure the image updates if already stored in window
onMounted(() => {
  if (window.user_image_path) {
    userImage.value = window.user_image_path;
  }
});


// Function to get cookie value
const getCookie = (name) => {
  const cookies = document.cookie.split("; ");
  const cookie = cookies.find((row) => row.startsWith(name + "="));
  return cookie ? decodeURIComponent(cookie.split("=")[1]) : null;
};

// Fetch user image from cookies
onMounted(() => {
  const imagePath = getCookie("user_image");
  if (imagePath) {
    userImage.value = `/api/method/frappe.utils.print_format.download_pdf?file_url=${imagePath}`;
  }
});



const router = useRouter();
const deviceList = ref([]);
const deviceListfordiagnostic = ref([]);
const searchQuery = ref("");
const rowsPerPage = ref(10);
const currentPage = ref(1);



const downloadReport = () => {
  if (deviceList.value.length === 0) {
    alert("No data to export.");
    return;
  }

  // Sort data by Serial Number (ascending order)
  const sortedData = [...deviceList.value].sort((a, b) =>
    a.serialNumber.localeCompare(b.serialNumber)
  );

  // Convert sorted data to worksheet format
  const data = sortedData.map(device => ({
    "Serial Number": device.serialNumber,
    "Device ID": device.deviceId,
    "Timestamp": device.timestamp,
    "Pressure (bar)": device.latestData.pv,
    "Battery (%)": device.latestData.bt,
    "Sensor Health": device.latestData.ht === "0" ? "Open" : "Healthy",
    "Latitude": device.latestData.lat,
    "Longitude": device.latestData.long,
    "Signal Strength": device.latestData.rssi,
  }));

  const worksheet = XLSX.utils.json_to_sheet(data);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "BTX-PP Data");

  // Create an Excel file and trigger download
  XLSX.writeFile(workbook, "BTX-PP Data.xlsx");
};



const downloaddiagnosticReport = () => {
  if (deviceList.value.length === 0) {
    alert("No data to export.");
    return;
  }

  // Sort data by Serial Number (ascending order)
  const sortedData = [...deviceListfordiagnostic.value].sort((a, b) =>
    a.serialNumber.localeCompare(b.serialNumber)
  );

  // Convert sorted data to worksheet format
  const data = sortedData.map(deviceforDiagnostic => ({
    "Serial Number": deviceforDiagnostic.serialNumber,
    "Device ID": deviceforDiagnostic.deviceId,
    "Timestamp": deviceforDiagnostic.timestamp,
    "Retry Count": deviceforDiagnostic.latestDiagnosticData.rc,
    "Device Reset Status": deviceforDiagnostic.latestDiagnosticData.rst === "1" ? "Reset" : "Not Reset",
    "Sensor Health": deviceforDiagnostic.latestDiagnosticData.ht === "0" ? "Open" : "Healthy",
    "Mqtt Server Status": deviceforDiagnostic.latestDiagnosticData.ms === "0" ? "Data Not Sent" : "Data Sent",
    "Device Software Version": deviceforDiagnostic.latestDiagnosticData.sv,
    "Signal Strength": deviceforDiagnostic.latestDiagnosticData.rssi,
  }));

  const worksheet = XLSX.utils.json_to_sheet(data);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "BTX-PP Diagnostic Data");

  // Create an Excel file and trigger download
  XLSX.writeFile(workbook, "BTX-PP Diagnostic Data.xlsx");
};





// Add this line at the top along with other refs
const selectedTab = ref(2); // Set default to 2 so DASHBOARD loads by default

// Function to set tab to 2 (DASHBOARD)
const setDashboardTab = () => {
  selectedTab.value = 2;
};

// Dropdown state logic
const isDropdownOpen = ref(false);
const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
}


// Logout functionality
function logout() {
  // Call the logout function from session.js
  session.logout.submit();
  isDropdownOpen.value = false; // Close the dropdown after logging out
}

// Optional: you can show user information, e.g. user's name or ID from session
const currentUser = ref(session.user || 'Guest'); // Default to 'Guest' if no user is logged in


// Computed property for filtering and sorting
const sortedDeviceList = computed(() => {
  return deviceList.value
    .filter(device =>
      device.serialNumber.toString().includes(searchQuery.value.trim())
    )
    .sort((a, b) => a.serialNumber.localeCompare(b.serialNumber));
});


// Computed property for filtering and sorting
const sortedDeviceListforDiagnostic = computed(() => {
  return deviceListfordiagnostic.value
    .filter(device =>
      device.serialNumber.toString().includes(searchQuery.value.trim())
    )
    .sort((a, b) => a.serialNumber.localeCompare(b.serialNumber));
});

// Paginated Devices
const paginatedDevices = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage.value;
  return sortedDeviceList.value.slice(start, start + rowsPerPage.value);
});


// Paginated Devices
const paginatedDiagnosticDevices = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage.value;
  return sortedDeviceListforDiagnostic.value.slice(start, start + rowsPerPage.value);
});

// Total pages
const totalPages = computed(() => Math.ceil(deviceList.value.length / rowsPerPage.value));

// Fetch devices
const fetchDevices = async () => {
  try {
    const response = await axios.get("/api/method/beetwin_iot.beetwin_iot.api.get_latest_device_data_for_Production.get_filtered_device_data_for_production");
    if (response.data.message.status === "success") {
      deviceList.value = response.data.message.data.map((device) => ({
        deviceId: device["Device ID"],
        serialNumber: device["Serial Number"],
        timestamp: device["Timestamp"].slice(0, 16),
        latestData: {
          pv: device["Pressure (bar)"],
          bt: device["Battery (%)"],
          ht: device["Sensor Health"],
          lat: device["Latitude"],
          long: device["Longitude"],
          rssi: device["RSSI Value"],
        },
      }));
    }
  } catch (error) {
    console.error("Error fetching devices:", error);
  }
};

const fetchDiagnosticDevices = async () => {
  try {
    const response1 = await axios.get("/api/method/beetwin_iot.beetwin_iot.api.device_diagnostic_data.get_device_diagnostic_data");

    console.log("API Response from Cloud:", response1.data); // Debugging output

    if (response1.data.message.status === "success") {
      deviceListfordiagnostic.value = response1.data.message.data.map((deviceforDiagnostic) => ({
        deviceId: deviceforDiagnostic["Device ID"],
        serialNumber: deviceforDiagnostic["Serial Number"],
        timestamp: deviceforDiagnostic["Timestamp"].slice(0, 16),
        latestDiagnosticData: {
          rc: deviceforDiagnostic["Retry Count"],
          rst: deviceforDiagnostic["Device Reset Status"],
          ht: deviceforDiagnostic["Sensor Health"],
          ms: deviceforDiagnostic["Mqtt Server Data Status"],
          sv: deviceforDiagnostic["Device Software Version"],
          rssi: deviceforDiagnostic["RSSI Value"],
        },
      }));
      console.log("DeviceList for Diagnostic:", deviceListfordiagnostic.value); // Debugging output

    }
  } catch (error) {
    console.error("Error fetching devices:", error);
  }
};


// // Navigate to Device Details page
// const navigateToDevice = (deviceId) => {
//   router.push({ name: 'DeviceDetails', params: { deviceId } });
// };

const navigateToDevice = (deviceId, serialNumber) => {
  router.push({
    name: 'DeviceDetails',
    params: { deviceId },
    query: { serialNumber }
  });
};


const navigateToDiagnosticDevice = (deviceId, serialNumber) => {
  router.push({
    name: 'DeviceDetails',
    params: { deviceId },
    query: { serialNumber }
  });
};



// Pagination navigation functions
const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};
const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

// onMounted(fetchDevices);

onMounted(() => {
  fetchDevices();
  fetchDiagnosticDevices();
});

function handleDashboardTab() {
  diagnosticState.value.scrollTop = window.scrollY;
  diagnosticState.value.searchQuery = searchQuery.value;
  diagnosticState.value.currentPage = currentPage.value;

  selectedTab.value = 2;
  searchQuery.value = dashboardState.value.searchQuery;
  currentPage.value = dashboardState.value.currentPage;

  nextTick(() => {
    window.scrollTo(0, dashboardState.value.scrollTop);
  });

  setDashboardTab(); // Call the original function if needed (but in your code it's just selectedTab.value = 2)
}

function handleDiagnosticTab() {
  dashboardState.value.scrollTop = window.scrollY;
  dashboardState.value.searchQuery = searchQuery.value;
  dashboardState.value.currentPage = currentPage.value;

  selectedTab.value = 1;
  searchQuery.value = diagnosticState.value.searchQuery;
  currentPage.value = diagnosticState.value.currentPage;

  nextTick(() => {
    window.scrollTo(0, diagnosticState.value.scrollTop);
  });

  setDiagnosticTab(); // Same here
}


// 👇 Expose shared reactive refs to Options API
window.__homeState = {
  selectedTab,
  searchQuery,
  currentPage,
  fetchDevices,
  fetchDiagnosticDevices,
  downloadReport,
  downloaddiagnosticReport,
  navigateToDevice,
  navigateToDiagnosticDevice,
  logout
};


</script>



<script>
export default {
  data() {
    return {
      // UI states
      selectedTab: 2,
      isSidebarOpen: true,
      isDropdownOpen: false,
      showModal: false,

      // Pagination & Search
      searchQuery: '',
      rowsPerPage: 10,
      currentPage: 1,
      totalPages: 1,

      // User Info
      currentUser: '',
      userImage: '/User.png',

      // Data Lists
      deviceList: [],
      diagnosticDeviceList: [],

      // Password Modal
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
      errorMessage: '',
      successMessage: ''
    };
  },
  computed: {
    paginatedDevices() {
      let filtered = this.deviceList.filter(device =>
        device.serialNumber?.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
      this.totalPages = Math.ceil(filtered.length / this.rowsPerPage);
      const start = (this.currentPage - 1) * this.rowsPerPage;
      return filtered.slice(start, start + this.rowsPerPage);
    },
    paginatedDiagnosticDevices() {
      let filtered = this.diagnosticDeviceList.filter(device =>
        device.serialNumber?.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
      this.totalPages = Math.ceil(filtered.length / this.rowsPerPage);
      const start = (this.currentPage - 1) * this.rowsPerPage;
      return filtered.slice(start, start + this.rowsPerPage);
    }
  },
  methods: {
    toggleSidebar() {
      this.isSidebarOpen = !this.isSidebarOpen;
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    setDashboardTab() {
      window.__homeState.selectedTab.value = 2;
      window.__homeState.fetchDevices(); // sync Dashboard data
    },
    setDiagnosticTab() {
      window.__homeState.selectedTab.value = 1;
      window.__homeState.fetchDiagnosticDevices(); // sync Diagnostic data
    },
    fetchDashboardData() {
      // This can be tied with logic in the setup block if needed
    },
    fetchDiagnosticData() {
      // This can be tied with logic in the setup block if needed
    },
    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    },
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    downloaddiagnosticReport() {
      window.__homeState.downloaddiagnosticReport();
    },
    downloadReport() {
      window.__homeState.downloadReport(); // call setup block method
    },
    navigateToDevice(deviceId, serialNumber) {
      window.__homeState.navigateToDevice(deviceId, serialNumber);
    },
    navigateToDiagnosticDevice(deviceId, serialNumber) {
      window.__homeState.navigateToDiagnosticDevice(deviceId, serialNumber);
    },
    logout() {
      window.__homeState.logout();
    },
    showAccountInfo() {
      this.showModal = true;
    },
    changePassword() {
      // Password change logic here
    }
  },
  mounted() {
    this.fetchDashboardData();
  }
};
</script>
