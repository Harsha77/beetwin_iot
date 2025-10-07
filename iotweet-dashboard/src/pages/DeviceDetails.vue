<template>
  <div class="min-h-screen p-6">
    <div class="flex justify-between items-center mb-4">
      
      <button @click="$router.push('/')" class="ml-4">
                <img src="/BackButton.png" alt="Download" class="w-10 h-10" />
              </button>

      <h2 class="text-xl font-bold text-center w-full">
        Sr.No: {{ $route.query.serialNumber || 'N/A' }} | ID: {{ deviceId }}
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
      <button @click="filterData" class="bg-[#08444c] text-white px-4 py-2 rounded">Generete Report</button>
    </div>

    <!-- Loader (Show when data is loading) -->
    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <svg class="animate-spin h-10 w-10 text-blue-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="4">
        <circle cx="12" cy="12" r="10" stroke-opacity="0.2"/>
        <path d="M22 12a10 10 0 1 1-10-10" stroke-linecap="round"/>
      </svg>
    </div>

    <!-- Table (Show when data is loaded) -->
    <div v-if="!isLoading && paginatedReportData.length > 0" class="overflow-x-auto">
      <div class="max-h-[400px] overflow-y-auto border border-gray-300 rounded">
        <table class="sticky-header w-full border">
          <thead class="bg-gray-200">
            <tr>
              <th class="border border-gray-300 px-4 py-2">Timestamp</th>
              <th class="border border-gray-300 px-4 py-2">Pressure (bar)</th>
              <th class="border border-gray-300 px-4 py-2">Battery (%)</th>
              <th class="border border-gray-300 px-4 py-2">Sensor Health</th>
              <th class="border border-gray-300 px-4 py-2">Signal Strength</th>
            </tr>
          </thead>
         
          <tbody>
            <tr v-for="data in paginatedReportData" :key="data.timestamp" class="text-center">
              <td class="border border-gray-300 px-4 py-2">{{ data.timestamp.slice(0, 16) }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ data.pv }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ data.bt }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ data.ht }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ data.rssi }}</td>
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
    Pressure Graph - <span class="text-gray-600">{{ $route.query.serialNumber || 'N/A' }}</span>
  </h3>
  <button @click="downloadGraph" class="ml-auto w-8 h-8 md:w-10 md:h-10">
    <img src="/Download.png" alt="Download" class="w-full h-full" />
  </button>
</div>

  <v-chart id="pressureChart" class="w-full h-80" :option="chartOptions" />
</div>


<!-- Space between Graph and Map (adjust height if needed) -->
<div class="h-6"></div>

<!-- Map Container -->
<div class="relative w-full border border-gray-300 rounded-lg shadow-md bg-white p-4">
    <!-- Centered Title -->
    <h3 class="text-lg font-bold text-center mb-2">
      Latitude & Longitude - 
        <span class="text-gray-600">
          {{ latestLatLong ? latestLatLong.lat + ', ' + latestLatLong.long : 'N/A' }}
        </span>
    </h3>
    
    <!-- Map Section -->
    <div id="device-map" class="border border-gray-300 rounded-md" style="height: 400px;"></div>
</div>

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
    background-color: #08444c; /* Match your theme */
    color: white;
    z-index: 10;
    padding: 12px;
    border-bottom: 2px solid #ddd; /* Add border for better visibility */
    text-align: center; /* Center align header text */
    font-weight: bold;
    vertical-align: middle; /* Ensure vertical centering */
}

.sticky-header th, .sticky-header td {
    padding: 12px;
    border: 1px solid #ddd;
    text-align: center; /* Center align all cell values */
    vertical-align: middle; /* Ensure vertical centering */
}

.sticky-header tbody tr:hover {
    background-color: #f1f1f1; /* Highlight on hover */
}


.graph-container {
  width: 100%;
  max-width: 100%;
  overflow-x: auto; /* Allow horizontal scrolling if needed */
}

#pressureChart {
  width: 100% !important;
  height: 300px !important; /* Adjust height to fit mobile screens */
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
    link.download = `Pressure_Graph_${route.query.serialNumber || 'N/A'}.jpg`;
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
  [`Time Series Table For (Sr.No: ${serialNumber} |ID: ${deviceId.value})`]
];


  // Define Table Headers
  const tableHeaders = [
    ["Timestamp",  "Pressure (bar)","Battery (%)", "Sensor Health", "Latitude", "Longitude", "Signal Strength"]
  ];

  // Convert Report Data to Array Format
  const tableData = reportData.value.map(data => [
    data.timestamp.slice(0, 16),
    data.pv,
    data.bt,
    data.ht,
    data.lat,
    data.long,
    data.rssi
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
// Fetch Report Data
const fetchReportData = async () => {
  isLoading.value = true;

  let payload = { device_data: deviceId.value };
  if (fromDate.value && toDate.value) {
    payload.from_date = fromDate.value;
    payload.to_date = toDate.value;
  }

  try {
    const response = await axios.post(
      "/api/method/beetwin_iot.beetwin_iot.report.btx_pp_timeseries_data_table.btx_pp_timeseries_data_table.generate_device_report",
      payload,
      { headers: { "Content-Type": "application/json" } }
    );

    console.log("API Response Data:", response.data.message.data);
    
    if (response.data.message && response.data.message.data) {
      reportData.value = [...response.data.message.data]; // 🔥 Force reactivity
    } else {
      reportData.value = [];
    }
  } catch (error) {
    console.error("Error fetching report data:", error);
    reportData.value = [];
  } finally {
    isLoading.value = false;
    console.log("Loading Finished. Report Data Size:", reportData.value.length);
  }
};

// Handle Filter Data
const filterData = async () => {
  await fetchReportData();
};
const chartOptions = computed(() => {
  const sortedData = [...reportData.value].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  
  return {
    tooltip: { trigger: "axis" },
    grid: {
      left: "10%", // Adjust left padding
      right: "5%", // Adjust right padding to prevent cutoff
      bottom: "20%", // Increase bottom margin to prevent label cutoff
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: sortedData.map((d) => {
        const date = new Date(d.timestamp);
        return `${String(date.getDate()).padStart(2, "0")}/${String(date.getMonth() + 1).padStart(2, "0")}\n${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;
      }),
      axisLabel: {
        fontSize: window.innerWidth < 768 ? 10 : 12, // Reduce font size for mobile
        rotate: 30, // Rotate for better readability on small screens
        interval: "auto",
      },
    },
    yAxis: {
      type: "value",
      name: "Pressure (bar)",
      min: function (value) {
        return Math.floor(value.min * 0.9);
      },
      max: function (value) {
        return Math.ceil(value.max * 1.1);
      },
      axisLabel: {
        formatter: "{value} bar",
        fontSize: window.innerWidth < 768 ? 10 : 12, // Adjust font size for mobile
      },
    },
    series: [
      {
        name: "Pressure",
        type: "line",
        data: sortedData.map((d) => d.pv),
        smooth: 0.2,
        lineStyle: { width: 2, color: "#FFA500" },
        symbolSize: window.innerWidth < 768 ? 4 : 6, // Adjust point size for mobile
      },
    ],
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

const updateMap = () => {
  if (!map) {
    console.warn("Map is not initialized yet.");
    return;
  }

  console.log("Updating Map...");

  // Clear existing markers
  markers.forEach(marker => map.removeLayer(marker));
  markers = [];

  // Find the latest valid entry with latitude and longitude
  let latestEntry = reportData.value
    .filter(entry => entry.lat && entry.long)
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))[0];

  // Find the latest valid Pressure & Battery values (including 0)
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
  }).replace(",", ""); // Remove comma from locale formatting

  // Define custom marker icon
  const customIcon = L.icon({
    iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
    shadowSize: [41, 41]
  });

  // Create and add the latest marker
  let marker = L.marker([latestLat, latestLong], { icon: customIcon }).addTo(map);
  markers.push(marker);

  // Customize popup content
  let popupContent = `
    <strong>Device ID:</strong> ${deviceId.value} <br>
    <strong>Serial Number:</strong> ${route.query.serialNumber || "N/A"} <br>
    <strong>Pressure:</strong> ${latestPressure} bar<br>
    <strong>Battery:</strong> ${latestBattery}% <br>
    <strong>Timestamp:</strong> ${latestTimestamp}
  `;

  marker.bindPopup(popupContent);
  marker.on("mouseover", function () {
    this.openPopup();
  });
  marker.on("mouseout", function () {
    this.closePopup();
  });

  console.log("Latest Marker Plotted at:", latestLat, latestLong);

  // Adjust map view to the latest marker
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

watch(reportData, () => {
  resetMap();  // 🔥 Reset the map when data changes
  updateMap();
  chartOptions.value = { ...chartOptions.value }; // Trigger chart update
}, { deep: true });

onMounted(async () => {
  await fetchReportData(); // Ensure data is fetched first
  initializeMap();
  updateMap(); // Force update after initializing map
});

// Fetch data and initialize map on mount
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
