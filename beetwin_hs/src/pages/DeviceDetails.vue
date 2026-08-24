<template>
  <div class="min-h-screen p-6">
    <div class="flex justify-between items-center mb-4">

      <button @click="$router.push('/')" class="ml-4">
        <img src="/BackButton.png" alt="Download" class="w-10 h-10" />
      </button>

      <h2 class="text-xl font-bold text-center w-full">
        Location Name: {{ $route.query.serialNumber || 'N/A' }}
      </h2>

      <button @click="downloadReport" class="ml-4">
        <img src="/Download.png" alt="Download" class="w-10 h-10" />
      </button>

    </div>
    <!-- Date Filters -->
    <div class="flex flex-col md:flex-row items-center justify-center gap-4 mb-4">
      <div class="flex items-center gap-2">
        <label class="font-semibold">From Date:</label>
        <input type="date" v-model="fromDate" class="border rounded px-2 py-1">
      </div>
      <div class="flex items-center gap-2">
        <label class="font-semibold">To Date:</label>
        <input type="date" v-model="toDate" class="border rounded px-2 py-1">
      </div>
      <button @click="filterData" class="bg-[#00a3d3] text-white px-4 py-2 rounded">Generete Report</button>
    </div>

    <!-- Loader (Show when data is loading) -->
    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <svg class="animate-spin h-10 w-10 text-blue-500" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="4">
        <circle cx="12" cy="12" r="10" stroke-opacity="0.2" />
        <path d="M22 12a10 10 0 1 1-10-10" stroke-linecap="round" />
      </svg>
    </div>

    <!-- Table (Show when data is loaded) -->
    <div v-if="!isLoading && paginatedReportData.length > 0" class="overflow-x-auto">
      <div class="max-h-[400px] overflow-y-auto border border-gray-300 rounded">
        <table class="sticky-header w-full border">
          <thead class="bg-gray-200">
            <tr>
              <th class="border border-gray-300 px-4 py-2">Timestamp</th>
              <th class="border border-gray-300 px-4 py-2">Flowrate</th>
              <th class="border border-gray-300 px-4 py-2">Totaliser</th>
              <th class="border border-gray-300 px-4 py-2">Pressure</th>

            </tr>
          </thead>

          <tbody>
            <tr v-for="data in paginatedReportData" :key="data.timestamp" class="text-center">
              <td class="border border-gray-300 px-4 py-2">{{ data.timestamp.slice(0, 16) }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ data.pv }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ data.bt }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ data.pressure }}</td>

            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- No Data Message -->
    <p v-if="!isLoading && paginatedReportData.length === 0" class="text-center text-gray-500">
      No data available for this device.
    </p>

    <!-- Pressure vs Time Series Graph -->
    <div class="graph-container mt-6 p-4 border border-gray-300 rounded bg-white w-full overflow-x-auto">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-bold text-center w-full">
  Flowrate Graph -
  <span class="text-gray-600">
    {{ $route.query.serialNumber || "N/A" }}
  </span>
</h3>
        <button @click="downloadGraph" class="ml-auto w-8 h-8 md:w-10 md:h-10">
          <img src="/Download.png" alt="Download" class="w-full h-full" />
        </button>
      </div>

      <v-chart id="pressureChart" class="w-full h-80" :option="chartOptions" />
    </div>


    <!-- Space between Graph and Map (adjust height if needed) -->
    <div class="h-6"></div>

    
    <!-- Map Container Hide on Date 23-04-2025 as per getting instruction from client and discussed it with Chetan Sir Also... -->

    
            <!-- <div class="relative w-full border border-gray-300 rounded-lg shadow-md bg-white p-4"> -->
              <!-- Centered Title -->
              <!-- <h3 class="text-lg font-bold text-center mb-2"> -->
                <!-- Location Name: <span class="text-gray-600">{{ locationName }}</span> | Latitude & Longitude - <span
                  class="text-gray-600"> -->
                  <!-- {{ latestLatLong ? latestLatLong.lat + ', ' + latestLatLong.long : 'N/A' }}
                </span> -->
              <!-- </h3> -->

              <!-- Location Name -->
              <!-- <h3 class="text-lg font-bold text-center mb-2"> -->

              <!-- </h3> -->
              <!-- Map Section -->
              <!-- <div id="device-map" class="border border-gray-300 rounded-md" style="height: 400px;"></div> -->
            <!-- </div> -->

    <!-- Map Container -->

  </div>
</template>


<style scoped>
.sticky-header {
  border-collapse: collapse;
  width: 100%;
}

.sticky-header thead th {
  position: sticky;
  top: 0;
  background-color: #00a3d3;
  /* Match your theme */
  color: white;
  z-index: 10;
  padding: 12px;
  border-bottom: 2px solid #ddd;
  /* Add border for better visibility */
  text-align: center;
  /* Center align header text */
  font-weight: bold;
  vertical-align: middle;
  /* Ensure vertical centering */
}

.sticky-header th,
.sticky-header td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: center;
  /* Center align all cell values */
  vertical-align: middle;
  /* Ensure vertical centering */
}

.sticky-header tbody tr:hover {
  background-color: #f1f1f1;
  /* Highlight on hover */
}


.graph-container {
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
  /* Allow horizontal scrolling if needed */
}

#pressureChart {
  width: 100% !important;
  height: 300px !important;
  /* Adjust height to fit mobile screens */
}
</style>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import * as XLSX from "xlsx";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { use } from "echarts/core";
import { LineChart } from "echarts/charts";
import { CanvasRenderer } from "echarts/renderers";
import { GridComponent, TooltipComponent, LegendComponent } from "echarts/components";
import VChart from "vue-echarts";
import html2canvas from "html2canvas";



use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent]);



const route = useRoute();
const deviceId = ref(route.params.deviceId);
const reportData = ref([]);
const reportPage = ref(1);
const reportRowsPerPage = ref(10);
const isLoading = ref(true);
let map = null;
const formatTime = (timestamp) => timestamp.slice(0, 16);

let markers = [];


// Computed property to get the latest latitude and longitude
const latestLatLong = computed(() => {
  const validEntries = reportData.value.filter(entry => entry.lat && entry.long);
  return validEntries.length > 0 ? validEntries.reduce((latest, entry) => {
    return new Date(entry.timestamp) > new Date(latest.timestamp) ? entry : latest;
  }) : null;
});

const downloadGraph = async () => {
  const chartContainer = document.querySelector(".graph-container"); // Capture the entire container

  if (!chartContainer) {
    alert("Graph container not found!");
    return;
  }

  try {
    const canvas = await html2canvas(chartContainer, { scale: 2 }); // High-resolution capture
    const imgData = canvas.toDataURL("image/jpeg");

    const link = document.createElement("a");
    link.href = imgData;
    link.download = `Flowrate_Graph_${route.query.serialNumber || "N/A"}.jpg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error("Error downloading graph:", error);
  }
};


// Export to Excel
const downloadReport = () => {
  if (reportData.value.length === 0) {
    alert("No data available to download.");
    return;
  }
  // Get Serial Number or default to 'N/A'
  const serialNumber = route.query.serialNumber || "N/A";
  // Create Header Row
  const headerRow = [
    [`Location Name: ${serialNumber}`]
  ];


  // Define Table Headers
  const tableHeaders = [
    ["Timestamp", "Flowrate", "Totaliser", "Pressure"]
  ];

  // Convert Report Data to Array Format
  const tableData = reportData.value.map(data => [
    data.timestamp.slice(0, 16),
    data.pv,
    data.bt,
    data.pressure
  ]);

  // Combine Header + Table Headers + Data
  const finalData = [...headerRow, [], ...tableHeaders, ...tableData];

  // Create Worksheet
  const worksheet = XLSX.utils.aoa_to_sheet(finalData);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Device Report");

  // Save File with Serial Number Instead of Device ID
  XLSX.writeFile(workbook, `Telemetry_Report_${serialNumber}.xlsx`);

};

const fromDate = ref("");
const toDate = ref("");
// ✅ Ensure `getCsrfToken` is properly declared
const getCsrfToken = async () => {
  try {
    // ✅ First, check if token is already available in the browser
    if (window.csrf_token) {
      console.log("Using CSRF Token from window:", window.csrf_token);
      return window.csrf_token;
    }

    // ✅ Second, try fetching it manually
    const response = await axios.get("/api/method/frappe.auth.get_logged_user", {
      withCredentials: true,
    });

    // ✅ Try extracting from headers
    const csrfToken = response.headers["x-frappe-csrf-token"] || document.cookie.match(/csrftoken=([^;]+)/)?.[1];

    console.log("Fetched CSRF Token:", csrfToken);
    return csrfToken;
  } catch (error) {
    console.error("Failed to fetch CSRF Token:", error);
    return null;
  }
};


// ✅ Fetch Report Data
const fetchReportData = async () => {
  isLoading.value = true;

  // 🔹 Fetch CSRF Token
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
          "X-Frappe-CSRF-Token": csrfToken, // ✅ Correct CSRF Token
          Accept: "application/json",
        },
        withCredentials: true, // ✅ Required for authentication
      }
    );

    console.log("API Response Data:", response.data.message.data);
    reportData.value = response.data.message.data || [];
  } catch (error) {
    console.error("Error fetching report data:", error);
    reportData.value = [];
  } finally {
    isLoading.value = false;
  }
};

// ✅ Fetch CSRF Token & Check Login Status on Mount
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

// Handle Filter Data
const filterData = async () => {
  await fetchReportData();
};



const chartOptions = computed(() => {
  if (
    !Array.isArray(reportData.value) ||
    reportData.value.length === 0
  ) {
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

  /*
   * Convert the API response into clean graph data.
   * Prefer flowrate; use pv only for older records.
   */
  const validData = reportData.value
    .map((record) => {
      const rawFlowrate =
        record.flowrate ??
        record.Flowrate ??
        record.pv;

      const numericFlowrate =
        Number(rawFlowrate);

      return {
        timestamp: record.timestamp,
        flowrate: numericFlowrate
      };
    })
    .filter((record) => {
      return (
        record.timestamp &&
        Number.isFinite(record.flowrate)
      );
    })
    .sort((first, second) => {
      const firstTime = new Date(
        String(first.timestamp).replace(" ", "T")
      ).getTime();

      const secondTime = new Date(
        String(second.timestamp).replace(" ", "T")
      ).getTime();

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

  const timestamps = validData.map(
    (record) => {
      const date = new Date(
        String(record.timestamp).replace(
          " ",
          "T"
        )
      );

      const day = String(
        date.getDate()
      ).padStart(2, "0");

      const month = String(
        date.getMonth() + 1
      ).padStart(2, "0");

      const hours = String(
        date.getHours()
      ).padStart(2, "0");

      const minutes = String(
        date.getMinutes()
      ).padStart(2, "0");

      const seconds = String(
        date.getSeconds()
      ).padStart(2, "0");

      return `${day}/${month} ${hours}:${minutes}:${seconds}`;
    }
  );

  const flowrateValues = validData.map(
    (record) => record.flowrate
  );

  /*
   * Create a dynamic Y-axis around the actual values.
   *
   * Example values 244–258 will produce approximately
   * a 239–263 range instead of always showing 0–300.
   * This makes small changes clearly visible.
   */
  const minimumFlowrate =
    Math.min(...flowrateValues);

  const maximumFlowrate =
    Math.max(...flowrateValues);

  const valueDifference =
    maximumFlowrate - minimumFlowrate;

  const axisPadding = Math.max(
    valueDifference * 0.15,
    5
  );

  const yAxisMinimum = Math.max(
    0,
    Math.floor(
      minimumFlowrate - axisPadding
    )
  );

  const yAxisMaximum = Math.ceil(
    maximumFlowrate + axisPadding
  );

  /*
   * Display approximately ten timestamp labels.
   * All points remain present in the graph.
   */
  const labelInterval = Math.max(
    0,
    Math.ceil(timestamps.length / 10) - 1
  );

  return {
    animation: true,
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
          Flowrate: <strong>${Number(
            point.data
          ).toFixed(3)}</strong>
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
        fontSize:
          window.innerWidth < 768
            ? 9
            : 11,
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
        fontSize:
          window.innerWidth < 768
            ? 9
            : 11,
        formatter: (value) =>
          Number(value).toFixed(1)
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
        connectNulls: false,
        showSymbol:
          flowrateValues.length <= 30,
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
            shadowColor:
              "rgba(0, 163, 211, 0.5)"
          }
        }
      }
    ]
  };
});

// Pagination
const paginatedReportData = computed(() => reportData.value);


const totalReportPages = computed(() => Math.ceil(reportData.value.length / reportRowsPerPage.value));

const nextReportPage = () => {
  if (reportPage.value < totalReportPages.value) reportPage.value++;
};

const prevReportPage = () => {
  if (reportPage.value > 1) reportPage.value--;
};

const initializeMap = () => {
  map = L.map("device-map", {
    center: [22.3511, 78.6677], // Centered in India
    zoom: 5, // Default zoom level for India
    maxBounds: [
      [6.5, 68.0],   // Southwest corner (Lakshadweep)
      [35.0, 97.5],  // Northeast corner (Arunachal Pradesh)
    ],
    maxBoundsViscosity: 1.0, // Prevents dragging outside India
  });

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);
  updateMap();
};





const locationName = ref("Fetching..."); // Reactive variable for location name

const getLocationName = async (lat, long) => {
  try {
    const response = await axios.get(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${long}`);
    if (response.data && response.data.display_name) {
      return response.data.display_name; // Returns the readable address
    }
  } catch (error) {
    console.error("Error fetching location name:", error);
  }
  return "Unknown Location"; // Fallback if API fails
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

  locationName.value = await getLocationName(latestLat, latestLong); // Store location name in reactive variable

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



// Watch for data changes and update the map
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
  await fetchReportData(); // Ensure data is fetched first
  initializeMap();
  updateMap(); // Force update after initializing map
});





</script>

<style scoped>
#device-map {
  width: 100%;
  height: 400px;
  margin-top: 20px;
}
</style>