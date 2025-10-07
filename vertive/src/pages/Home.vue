<template>
  <div class="min-h-screen flex flex-col">
    <header
      class="fixed top-0 left-0 w-full flex items-center justify-between py-4 border-b bg-[#08444c] shadow px-5 z-50">
      <img src="/IOtweet Logo_2.0 white.png" alt="IoTweet Logo" class="w-28" />
      <div class="text-white flex-1 text-center font-bold text-xl">VERTIV ENERGY DASHBOARD</div>

      <button @click="toggleSidebar" class="lg:hidden text-white ml-auto">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      <!-- User Info Dropdown -->
      <div class="relative ml-4" @click="toggleDropdown">
        <button class="bg-gray-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold">
          <img :src="userImage" alt="User Image" class="w-full h-full object-cover rounded-full" />
        </button>
        <!-- Dropdown Menu -->
        <div v-if="isDropdownOpen" class="absolute right-0 mt-2 w-64 bg-white rounded-md shadow-lg z-20">
          <!-- Display User Info -->
          <p class="block px-4 py-2 text-gray-700 font-semibold break-all">
            {{ currentUser }}
          </p>
          <!-- <a href="#" @click="showAccountInfo" class="block px-4 py-2 text-gray-700 hover:bg-gray-100">Account Info</a> -->
          <!-- <a href="#" @click="openPasswordModal" class="block px-4 py-2 text-gray-700 hover:bg-gray-100">Change
            Password</a> -->
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

      <div class="flex-grow p-6 pt-16" v-if="selectedTab === 2">

        <div class="mt-4">
          <div class="flex justify-end mb-2">
            <!-- <div class="marquee-wrapper w-full mt-6" @mouseenter="pauseMarquee" @mouseleave="resumeMarquee">
              <div class="marquee flex items-center space-x-2 whitespace-nowrap" :class="{ paused: isPaused }">
                <span>Welcome to</span>
                <img src="/IOtweet Logo_2.0 Teal .png" alt="IoTweet Logo" class="h-5 w-auto inline-block" />
                <span>| The best platform for your needs. |</span>
                <a href="#" target="_blank" class="marquee-link text-blue-500 underline">Join us today!</a>
              </div>
            </div> -->
          </div>

          <div class="bg-[#08444c] min-h-screen p-4 text-white font-sans ">
            <!-- Top Timestamp Bar -->
            <div class="bg-[#08444c] rounded-md p-2 text-center text-sm mb-4">
              <span class="text-white flex-1 text-center font-bold text-xl ">Updated: {{ deviceList[0]?.timestamp || 'N/A' }}</span>

            </div>

            <!-- Main White Card -->
            <div class="bg-white text-black rounded-md p-6 shadow-md">
              <div class="grid grid-cols-3 items-start">
                <!-- Input Section -->
                <div class="text-center">
                  <img src="/gauge.png" alt="Input Gauge" class="w-24 h-16 mb-2 mx-auto" />
                  <p class="font-bold mb-2">Input</p>

                  <div class="overflow-x-auto inline-block">
                    <table class="table-auto border border-green-600">
                      <tbody v-if="deviceList.length > 0">
                        <tr class="border border-green-600">
                          <td class="border border-green-600 px-4 py-2 font-bold">L-N</td>
                          <td class="border border-green-600 px-4 py-2">{{ deviceList[0].latestData.INPV }}</td>
                          <td class="border border-green-600 px-4 py-2">VAC</td>
                        </tr>

                        <tr class="border border-green-600">
                          <td class="border border-green-600 px-4 py-2 font-bold">Amps</td>
                          <td class="border border-green-600 px-4 py-2">{{ deviceList[0].latestData.INPI }}</td>
                          <td class="border border-green-600 px-4 py-2">A</td>
                        </tr>

                        <tr class="border border-green-600">
                          <td class="border border-green-600 px-4 py-2 font-bold">Freq</td>
                          <td class="border border-green-600 px-4 py-2">{{ deviceList[0].latestData.INF }}</td>
                          <td class="border border-green-600 px-4 py-2">Hz</td>
                        </tr>
                      </tbody>

                    </table>
                  </div>
                </div>


                <!-- Middle Section with Flow -->
                <div class="text-center">
                  <img src="/Battery-1.png" alt="Input Gauge" class="w-24 h-16 mb-2 mx-auto" />
                  <p class="font-bold mb-2">Battery</p>

                  <div class="overflow-x-auto inline-block">
                    <table class="table-auto border border-green-600">
                      <tbody v-if="deviceList.length > 0">

                        <tr class="border border-green-600">
                          <td class="border border-green-600 px-4 py-2 font-bold">Voltage</td>
                          <td class="border border-green-600 px-4 py-2">{{ deviceList[0].latestData.BTV }}</td>
                          <td class="border border-green-600 px-4 py-2">VDC</td>
                        </tr>
                        <tr class="border border-green-600">
                          <td class="border border-green-600 px-4 py-2 font-bold">Charge</td>
                          <td class="border border-green-600 px-4 py-2">{{ deviceList[0].latestData.BTC }}</td>
                          <td class="border border-green-600 px-4 py-2">%</td>
                        </tr>
                        
                      </tbody>
                    </table>
                  </div>
                </div>

                <!-- Output Section -->
                <div class="text-center">
                  <img src="/gauge.png" alt="Input Gauge" class="w-24 h-16 mb-2 mx-auto" />
                  <p class="font-bold mb-2">Output</p>

                  <div class="overflow-x-auto inline-block">
                    <table class="table-auto border border-green-600">
                      <tbody v-if="deviceList.length > 0">
                        <tr class="border border-green-600">
                          <td class="border border-green-600 px-4 py-2 font-bold">L-N</td>
                          <td class="border border-green-600 px-4 py-2">{{ deviceList[0].latestData.OPV }}</td>
                          <td class="border border-green-600 px-4 py-2">VAC</td>
                        </tr>
                        <tr class="border border-green-600">
                          <td class="border border-green-600 px-4 py-2 font-bold">Amps</td>
                          <td class="border border-green-600 px-4 py-2">{{ deviceList[0].latestData.OPI }}</td>
                          <td class="border border-green-600 px-4 py-2">A</td>
                        </tr>
                        <tr class="border border-green-600">
                          <td class="border border-green-600 px-4 py-2 font-bold">Load</td>
                          <td class="border border-green-600 px-4 py-2">{{ deviceList[0].latestData.OPL }}</td>
                          <td class="border border-green-600 px-4 py-2">%</td>
                        </tr>
                        
                        <tr class="border border-green-600">
                          <td class="border border-green-600 px-4 py-2 font-bold">Freq</td>
                          <td class="border border-green-600 px-4 py-2">{{ deviceList[0].latestData.OPF }}</td>
                          <td class="border border-green-600 px-4 py-2">Hz</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              <!-- Active Events Table -->
              <div class="bg-white text-black rounded-md p-4 mt-6 shadow-md">
                <div class="flex justify-between mb-2 text-sm">
                  <span class="font-semibold">Alert Events Updated: {{ deviceList[0]?.timestamp || 'N/A' }}</span>
                  <span class="text-gray-500"></span>
                </div>
                <table class="w-full text-sm border border-gray-200">
                  <thead class="bg-gray-100">
                    <tr>
                      <!-- <th class="p-2 text-left">Alert</th> -->
                      <!-- <th class="p-2 text-left">Ack</th> -->
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="deviceList.length > 0 &&
                      (deviceList[0].latestData?.ALINPVHI === '1' || deviceList[0].latestData?.ALINPVLOW === '1')"
                      class="border-t">
                      <td class="p-2 flex items-center gap-2">
                        <span class="w-3 h-3 bg-yellow-400 rounded-full inline-block"></span>
                        <div class="border border-green-600 px-4 py-2 alert-blink">
                          <div v-if="deviceList[0].latestData?.ALINPVHI === '1'">High Input Voltage Alert</div>
                          <div v-if="deviceList[0].latestData?.ALINPVLOW === '1'">Low Input Voltage Alert</div>
                        </div>
                      </td>
                      <!-- <td class="p-2">Active</td> -->
                    </tr>


                    <!-- <td class="p-2">Active</td> -->
                    

                  </tbody>
                </table>
              </div>
            </div>






            <!-- Pagination Controls -->

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
  const response = await fetch(`/api/resource/User/${username}`);
  if (!response.ok) return null;
  return await response.json();
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


const router = useRouter();
const deviceList = ref([]);
const searchQuery = ref("");
const rowsPerPage = ref(10);
const currentPage = ref(1);
const showModal = ref(false);
const successMessage = ref("");
const errorMessage = ref("");
const currentPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");


// Open Change Password Modal
const openPasswordModal = () => {
  showModal.value = true;
  errorMessage.value = "";
  successMessage.value = "";
};

// Change Password API Call
const changePassword = async () => {
  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = "Passwords do not match.";
    return;
  }

  try {
    const response = await axios.post("/api/method/beetwin_iot.beetwin_iot.api.changedpassword.admin_change_password", {
      user: currentUser.value,
      old_password: currentPassword.value,
      new_password: newPassword.value,
    });

    if (response.data.message === "Password Updated") {
      successMessage.value = "Password changed successfully.";
      setTimeout(() => {
        console.log("Closing modal..."); // This should appear after 1.5s
        showModal.value = false;
      }, 1500);

    } else {
      errorMessage.value = response.data.message || "Unexpected error.";
    }
  } catch (error) {
    console.error("API Error:", error.response?.data);
    errorMessage.value = error.response?.data?.message || "Failed to update password.";
  }
};


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

// Paginated Devices
const paginatedDevices = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage.value;
  return sortedDeviceList.value.slice(start, start + rowsPerPage.value);
});

// Total pages
const totalPages = computed(() => Math.ceil(deviceList.value.length / rowsPerPage.value));

const fetchDevices = async () => {
  try {
    const response = await axios.get("/api/method/beetwin_iot.beetwin_iot.api.get_latest_device_data_vertiv.get_filtered_device_data");

    console.log("API Response from Cloud:", response.data); // Debugging output

    if (response.data && response.data.message && response.data.message.status === "success") {
      deviceList.value = response.data.message.data
        .filter(device =>
          device && (
            device["Serial Number"] ||
            device["Input Voltage"] ||
            device["Input Current"] ||
            device["Input Freq"] ||
            device["Output Voltage"] ||
            device["Output Current"] ||
            device["Output Load"] ||
            device["Output Freq"] ||
            device["Output VA"] ||
            device["Output Watts"] ||
            device["Output Load"] ||
            device["Output VA"] ||
            device["Watts"] ||
            device["Output Freq"] ||
            device["Battry Volatge"] ||
            device["Battery Charge"] ||
            device["Time Remaining"] ||
            device["Input Volatge High"] ||
            device["Input Volatge Low"]
          )
        )
        .map((device) => ({
          deviceId: device["Device ID"] || "N/A",
          serialNumber: device["Serial Number"] ? device["Serial Number"].toString() : "N/A",
          timestamp: device["Timestamp"] ? device["Timestamp"].slice(0, 19) : "N/A",
          latestData: {
            INPV: device["Input Voltage"] ? device["Input Voltage"].toString() : "N/A",
            INPI: device["Input Current"] ? device["Input Current"].toString() : "N/A",
            INF: device["Input Freq"] ? device["Input Freq"].toString() : "N/A",
            OPV: device["Output Voltage"] ? device["Output Voltage"].toString() : "N/A",
            OPI: device["Output Current"] ? device["Output Current"].toString() : "N/A",
            OPL: device["Output Load"] ? device["Output Load"].toString() : "N/A",
            OPVA: device["Output VA"] ? device["Output VA"].toString() : "N/A",
            OPW: device["Watts"] ? device["Watts"].toString() : "N/A",
            OPF: device["Output Freq"] ? device["Output Freq"].toString() : "N/A",
            BTV: device["Battry Volatge"] ? device["Battry Volatge"].toString() : "N/A",
            BTC: device["Battery Charge"] ? device["Battery Charge"].toString() : "N/A",
            BT: device["Time Remaining"] ? device["Time Remaining"].toString() : "N/A",
            ALINPVHI: device["Input Volatge High"] ? device["Input Volatge High"].toString() : "N/A",
            ALINPVLOW: device["Input Volatge Low"] ? device["Input Volatge Low"].toString() : "N/A",
          },
        }));
    } else {
      console.error("Invalid API response:", response.data);
    }
  } catch (error) {
    console.error("Error fetching devices:", error);
  }
};

const fetchDeviceReport = async (deviceData, fromDate, toDate) => {
  try {
    const csrfToken = frappe.csrf_token; // Fetch CSRF token
    const response = await fetch('/api/method/beetwin_iot.beetwin_iot.report.btx_pp_timeseries_data_table.btx_pp_timeseries_data_table.generate_device_report', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': csrfToken // Include CSRF token
      },
      credentials: 'include', // Ensure cookies are sent
      body: JSON.stringify({ device_data: deviceData, from_date: fromDate, to_date: toDate })
    });
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Error fetching device report:', error);
  }
};

const navigateToDevice = (deviceId, serialNumber) => {
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
  // Already existing logic
  fetchDevices();

  // Add this new logic for auto-refresh every 10 seconds
  setInterval(() => {
    fetchDevices();
  }, 10000); // 10000ms = 10 seconds
});


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
  position: relative;
  width: 100%;
  height: 2rem;
  /* or whatever suits your layout */

}

.marquee {
  display: inline-block;
  white-space: nowrap;
  min-width: 100%;
  /* this ensures it's at least as wide as the container */
  animation: marquee 30s linear infinite;
  will-change: transform;
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
    /* start fully offscreen to the right */
  }

  100% {
    transform: translateX(-100%);
    /* move fully offscreen to the left */
  }
}

.alert-blink {
  background-color: red;
  color: white;
  animation: blink-bg 1s infinite;
}

@keyframes blink-bg {
  0% {
    background-color: red;
  }

  50% {
    background-color: darkred;
  }

  100% {
    background-color: red;
  }
}
</style>
