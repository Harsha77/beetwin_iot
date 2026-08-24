<template>
  <div class="min-h-screen flex flex-col">
    <!-- Fixed header -->
    <header
      class="fixed top-0 left-0 w-full h-28 flex items-center justify-between border-b bg-white shadow px-5 z-50"
    >
      <img
        src="/public/HS.png"
        alt="Happy Solutions Logo"
        class="h-20 w-auto object-contain"
      />

      <div
        class="midc flex-1 text-center font-bold text-xl"
      >
        MIDC Mahape- Watermain Dashboard
      </div>

      <img
        src="/public/MIDC.png"
        alt="MIDC Logo"
        class="h-20 w-auto object-contain"
      />

      <button
        @click="toggleSidebar"
        class="lg:hidden text-gray-700 ml-4"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>

      <!-- User dropdown -->
      <div class="relative ml-4">
        <button
          @click.stop="toggleDropdown"
          class="bg-gray-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold"
        >
          <img
            :src="userImage"
            alt="User Image"
            class="w-full h-full object-cover rounded-full"
          />
        </button>

        <div
          v-if="isDropdownOpen"
          class="absolute right-0 mt-2 w-64 bg-white rounded-md shadow-lg z-20"
        >
          <p
            class="block px-4 py-2 text-gray-700 font-semibold break-all"
          >
            {{ currentUser }}
          </p>

          <a
            href="#"
            @click.prevent="logout"
            class="block px-4 py-2 text-gray-700 hover:bg-gray-100"
          >
            Logout
          </a>
        </div>

        <!-- Change password modal -->
        <div
          v-if="showModal"
          class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50"
        >
          <div class="bg-white p-6 rounded-md w-96">
            <h2 class="text-xl font-bold mb-4">
              Change Password
            </h2>

            <input
              v-model="currentPassword"
              type="password"
              placeholder="Current Password"
              class="w-full p-2 border rounded-md mb-2"
            />

            <input
              v-model="newPassword"
              type="password"
              placeholder="New Password"
              class="w-full p-2 border rounded-md mb-2"
            />

            <input
              v-model="confirmPassword"
              type="password"
              placeholder="Confirm New Password"
              class="w-full p-2 border rounded-md mb-4"
            />

            <button
              @click="changePassword"
              class="w-full bg-blue-500 text-white p-2 rounded-md"
            >
              Update Password
            </button>

            <button
              @click="showModal = false"
              class="w-full mt-2 text-gray-600"
            >
              Cancel
            </button>

            <p
              v-if="errorMessage"
              class="text-red-500 mt-2"
            >
              {{ errorMessage }}
            </p>

            <p
              v-if="successMessage"
              class="text-green-500 mt-2"
            >
              {{ successMessage }}
            </p>
          </div>
        </div>
      </div>
    </header>

    <!--
      Header height is h-28.
      Therefore main uses pt-28.
      No additional 140px or pt-16 padding is required.
    -->
    <main class="flex-grow flex flex-col md:flex-row pt-28">
      <!-- Sidebar -->
      <aside
        :class="{
          hidden: !isSidebarOpen,
          'lg:block': false,
          'bg-[#08444c] text-white p-5 border-r transition-all duration-300': true
        }"
      >
        <nav>
          <ul class="space-y-4 text-lg font-semibold">
            <li>
              <a
                href="#"
                @click.prevent="setDashboardTab"
                class="flex items-center space-x-2 hover:text-gray-300"
              >
                <span>DASHBOARD</span>
              </a>
            </li>
          </ul>
        </nav>
      </aside>

      <!-- Dashboard -->
      <div
        v-if="selectedTab === 2"
        class="flex-grow px-6 pt-5 pb-6"
      >
        <!-- Search and download -->
        <div
          class="flex justify-end items-center gap-3 mb-4"
        >
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search Serial Number"
            class="border p-2 rounded-md w-64"
          />

          <button @click="downloadReport">
            <img
              src="/Download.png"
              alt="Download"
              class="w-10 h-10"
            />
          </button>
        </div>

        <!-- Device table -->
        <div class="overflow-x-auto">
          <table
            class="table-auto w-full border-collapse border border-gray-300"
          >
            <thead class="bg-[#00a3d3] text-white">
              <tr>
                <th
                  class="border border-gray-300 px-4 py-2 text-center"
                >
                  Serial Number
                </th>

                <th
                  class="border border-gray-300 px-4 py-2 text-center"
                >
                  Device ID
                </th>

                <th
                  class="border border-gray-300 px-4 py-2 text-center"
                >
                  Timestamp
                </th>

                <th
                  class="border border-gray-300 px-4 py-2 text-center"
                >
                  Flowrate
                </th>

                <th
                  class="border border-gray-300 px-4 py-2 text-center"
                >
                  Totaliser
                </th>

                <th
                  class="border border-gray-300 px-4 py-2 text-center"
                >
                  Pressure
                </th>
              </tr>
            </thead>

            <tbody>
              <tr v-if="deviceList.length === 0">
                <td
                  colspan="6"
                  class="text-center text-red-500 font-bold py-4"
                >
                  No allowed device groups found.
                </td>
              </tr>

              <tr
                v-for="device in paginatedDevices"
                :key="device.deviceId"
                @click="
                  navigateToDevice(
                    device.deviceId,
                    device.serialNumber
                  )
                "
                class="cursor-pointer hover:bg-gray-100 transition-all text-center"
              >
                <td
                  class="border border-gray-300 px-4 py-2"
                >
                  {{ device.serialNumber }}
                </td>

                <td
                  class="border border-gray-300 px-4 py-2"
                >
                  {{ device.deviceId }}
                </td>

                <td
                  class="border border-gray-300 px-4 py-2"
                >
                  {{ device.timestamp }}
                </td>

                <td
                  class="border border-gray-300 px-4 py-2"
                >
                  {{ device.latestData.flowrate }}
                </td>

                <td
                  class="border border-gray-300 px-4 py-2"
                >
                  {{ device.latestData.totaliser }}
                </td>

                <td
                  class="border border-gray-300 px-4 py-2"
                >
                  {{ device.latestData.pressure || "N/A" }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div
          class="flex justify-between items-center mt-4"
        >
          <div>
            <label class="mr-2">
              Items per page:
            </label>

            <select
              v-model.number="rowsPerPage"
              class="border p-2 rounded-md"
            >
              <option :value="10">10</option>
              <option :value="25">25</option>
              <option :value="50">50</option>
              <option :value="100">100</option>
            </select>
          </div>

          <div>
            <button
              @click="prevPage"
              :disabled="currentPage === 1"
              class="px-4 py-2 border rounded-md bg-gray-200 mr-2 disabled:opacity-50"
            >
              Prev
            </button>

            <span>
              Page {{ currentPage }} of {{ totalPages }}
            </span>

            <button
              @click="nextPage"
              :disabled="currentPage >= totalPages"
              class="px-4 py-2 border rounded-md bg-gray-200 ml-2 disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.midc {
  color: #00a3d3;
}
</style>

<script setup>
import {
  ref,
  computed,
  onMounted,
  watch
} from "vue";

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
const isSidebarOpen = ref(false);
const isDropdownOpen = ref(false);

const showModal = ref(false);
const successMessage = ref("");
const errorMessage = ref("");
const currentPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");

const currentUser = ref(
  session.user || "Guest"
);

/**
 * Check whether an API value is valid.
 *
 * Numeric zero is considered valid.
 */
const hasValue = (value) => {
  return (
    value !== null &&
    value !== undefined &&
    value !== "" &&
    value !== "null"
  );
};

/**
 * Convert a value for table display.
 */
const displayValue = (value) => {
  return hasValue(value)
    ? String(value)
    : "N/A";
};

/**
 * Read a cookie value.
 */
const getCookie = (name) => {
  const cookies = document.cookie.split("; ");

  const cookie = cookies.find((row) =>
    row.startsWith(`${name}=`)
  );

  return cookie
    ? decodeURIComponent(
        cookie.split("=")[1]
      )
    : null;
};

const getUserImageFromCookie = () => {
  return getCookie("user_image");
};

/**
 * Fetch the logged-in user's information.
 */
const fetchUserImage = async (username) => {
  try {
    const response = await fetch(
      `/api/resource/User/${encodeURIComponent(username)}`
    );

    if (!response.ok) {
      return null;
    }

    const result = await response.json();

    return result?.data || result;
  } catch (error) {
    console.error(
      "Error fetching user image:",
      error
    );

    return null;
  }
};

/**
 * Fetch the logged-in user automatically.
 */
createResource({
  url: "/api/method/frappe.auth.get_logged_user",
  auto: true,

  onSuccess: async (response) => {
    const username =
      response?.message || response;

    if (!username) {
      return;
    }

    currentUser.value = username;

    const userDetails =
      await fetchUserImage(username);

    const imagePath =
      userDetails?.user_image ||
      getUserImageFromCookie() ||
      "/User.png";

    userImage.value = imagePath;

    window.user_image_path = imagePath;
  }
});

/**
 * Sidebar methods.
 */
const toggleSidebar = () => {
  isSidebarOpen.value =
    !isSidebarOpen.value;
};

const setDashboardTab = () => {
  selectedTab.value = 2;
};

/**
 * Dropdown methods.
 */
const toggleDropdown = () => {
  isDropdownOpen.value =
    !isDropdownOpen.value;
};

/**
 * Change password modal.
 */
const openPasswordModal = () => {
  showModal.value = true;
  errorMessage.value = "";
  successMessage.value = "";
};

/**
 * Change password API.
 */
const changePassword = async () => {
  if (
    newPassword.value !==
    confirmPassword.value
  ) {
    errorMessage.value =
      "Passwords do not match.";

    return;
  }

  try {
    const response = await axios.post(
      "/api/method/beetwin_iot.beetwin_iot.api.changedpassword.admin_change_password",
      {
        user: currentUser.value,
        old_password:
          currentPassword.value,
        new_password:
          newPassword.value
      }
    );

    if (
      response.data.message ===
      "Password Updated"
    ) {
      successMessage.value =
        "Password changed successfully.";

      setTimeout(() => {
        showModal.value = false;
      }, 1500);
    } else {
      errorMessage.value =
        response.data.message ||
        "Unexpected error.";
    }
  } catch (error) {
    console.error(
      "Password API error:",
      error.response?.data || error
    );

    errorMessage.value =
      error.response?.data?.message ||
      "Failed to update password.";
  }
};

/**
 * Logout.
 */
const logout = () => {
  session.logout.submit();
  isDropdownOpen.value = false;
};

/**
 * Fetch telemetry devices.
 */
const fetchDevices = async () => {
  try {
    const response = await axios.get(
      "/api/method/beetwin_iot.beetwin_iot.api.get_latest_device_data.get_filtered_device_data"
    );

    console.log(
      "API Response from Cloud:",
      response.data
    );

    const apiMessage =
      response.data?.message;

    if (
      apiMessage?.status !== "success"
    ) {
      console.error(
        "Invalid API response:",
        apiMessage?.message ||
          response.data
      );

      deviceList.value = [];

      return;
    }

    const apiDevices =
      Array.isArray(apiMessage.data)
        ? apiMessage.data
        : [];

    deviceList.value = apiDevices
      .filter((device) => {
        if (!device) {
          return false;
        }

        return (
          hasValue(
            device["Serial Number"]
          ) ||
          hasValue(
            device["Flowrate"]
          ) ||
          hasValue(
            device["Totaliser"]
          )
        );
      })
      .map((device) => {
        /*
         * Backend keys are case-sensitive:
         *
         * Flowrate
         * Totaliser
         *
         * Do not use:
         * device["flowrate"]
         * device["totaliser"]
         */

        const flowrate =
          device["Flowrate"];

        const totaliser =
          device["Totaliser"];

        return {
          deviceId: displayValue(
            device["Device ID"]
          ),

          serialNumber: displayValue(
            device["Serial Number"]
          ),

          timestamp: hasValue(
            device["Timestamp"]
          )
            ? String(
                device["Timestamp"]
              ).slice(0, 16)
            : "N/A",

          latestData: {
            flowrate:
              displayValue(flowrate),

            totaliser:
              displayValue(totaliser),

            ht: hasValue(
              device["Sensor Health"]
            )
              ? String(
                  device["Sensor Health"]
                )
              : null,

            rssi: displayValue(
              device["RSSI Value"]
            )
          }
        };
      });

    currentPage.value = 1;

    console.log(
      "Final mapped device list:",
      deviceList.value
    );
  } catch (error) {
    deviceList.value = [];

    console.error(
      "Error fetching devices:",
      error.response?.data || error
    );
  }
};

/**
 * Search and sorting.
 */
const sortedDeviceList = computed(() => {
  const query =
    searchQuery.value
      .trim()
      .toLowerCase();

  return deviceList.value
    .filter((device) =>
      String(device.serialNumber)
        .toLowerCase()
        .includes(query)
    )
    .sort((a, b) =>
      String(a.serialNumber)
        .localeCompare(
          String(b.serialNumber),
          undefined,
          {
            numeric: true
          }
        )
    );
});

/**
 * Pagination total.
 *
 * Uses filtered device list instead
 * of the unfiltered deviceList.
 */
const totalPages = computed(() => {
  return Math.max(
    1,
    Math.ceil(
      sortedDeviceList.value.length /
        rowsPerPage.value
    )
  );
});

/**
 * Devices displayed on the current page.
 */
const paginatedDevices = computed(() => {
  const start =
    (currentPage.value - 1) *
    rowsPerPage.value;

  return sortedDeviceList.value.slice(
    start,
    start + rowsPerPage.value
  );
});

/**
 * Reset pagination after search or
 * rows-per-page changes.
 */
watch(
  [searchQuery, rowsPerPage],
  () => {
    currentPage.value = 1;
  }
);

const nextPage = () => {
  if (
    currentPage.value <
    totalPages.value
  ) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

/**
 * Excel download.
 */
const downloadReport = () => {
  if (
    deviceList.value.length === 0
  ) {
    alert("No data to export.");

    return;
  }

  const sortedData = [
    ...deviceList.value
  ].sort((a, b) =>
    String(a.serialNumber)
      .localeCompare(
        String(b.serialNumber),
        undefined,
        {
          numeric: true
        }
      )
  );

  const reportData =
    sortedData.map((device) => ({
      "Serial Number":
        device.serialNumber,

      "Device ID":
        device.deviceId,

      Timestamp:
        device.timestamp,

      Flowrate:
        device.latestData.flowrate,

      Totaliser:
        device.latestData.totaliser,
       Pressure:
        device.latestData.pressure  
    }));

  const worksheet =
    XLSX.utils.json_to_sheet(
      reportData
    );

  const workbook =
    XLSX.utils.book_new();

  XLSX.utils.book_append_sheet(
    workbook,
    worksheet,
    "MIDC TTC Data"
  );

  XLSX.writeFile(
    workbook,
    "MIDC TTC Data.xlsx"
  );
};

/**
 * Device report API.
 */
const fetchDeviceReport = async (
  deviceData,
  fromDate,
  toDate
) => {
  try {
    const csrfToken =
      window.frappe?.csrf_token;

    const response = await fetch(
      "/api/method/beetwin_iot.beetwin_iot.report.btx_pp_timeseries_data_table.btx_pp_timeseries_data_table.generate_device_report",
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json",

          "X-Frappe-CSRF-Token":
            csrfToken
        },

        credentials: "include",

        body: JSON.stringify({
          device_data:
            deviceData,

          from_date:
            fromDate,

          to_date:
            toDate
        })
      }
    );

    const report =
      await response.json();

    console.log(report);
  } catch (error) {
    console.error(
      "Error fetching device report:",
      error
    );
  }
};

/**
 * Open device details.
 */
const navigateToDevice = (
  deviceId,
  serialNumber
) => {
  router.push({
    name: "DeviceDetails",

    params: {
      deviceId
    },

    query: {
      serialNumber
    }
  });
};

/**
 * Page initialization.
 */
onMounted(() => {
  if (
    window.user_image_path
  ) {
    userImage.value =
      window.user_image_path;
  } else {
    const imagePath =
      getCookie("user_image");

    if (imagePath) {
      userImage.value =
        imagePath;
    }
  }

  fetchDevices();
});
</script>