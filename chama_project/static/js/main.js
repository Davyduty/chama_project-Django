import { Chart } from "@/components/ui/chart"
// Enable Bootstrap tooltips
document.addEventListener("DOMContentLoaded", () => {
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl))

  // Auto-hide alerts after 5 seconds
  setTimeout(() => {
    var alerts = document.querySelectorAll(".alert")
    alerts.forEach((alert) => {
      var bsAlert = new bootstrap.Alert(alert)
      bsAlert.close()
    })
  }, 5000)

  // Confirm delete actions
  const confirmDeleteButtons = document.querySelectorAll(".confirm-delete")
  confirmDeleteButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      if (!confirm("Are you sure you want to delete this item? This action cannot be undone.")) {
        e.preventDefault()
      }
    })
  })

  // Form validation
  const forms = document.querySelectorAll(".needs-validation")
  Array.from(forms).forEach((form) => {
    form.addEventListener(
      "submit",
      (event) => {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
        form.classList.add("was-validated")
      },
      false,
    )
  })
})

// Chart.js integration for dashboard (if Chart.js is included)
if (typeof Chart !== "undefined") {
  // Sample data (replace with your actual data)
  const contributionLabels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
  const contributionData = [10, 20, 15, 25, 30, 22, 28, 35, 40, 38, 45, 50]
  const loanStatusData = [30, 40, 10, 20]

  // Sample contribution chart
  const contributionChartEl = document.getElementById("contributionChart")
  if (contributionChartEl) {
    const contributionChart = new Chart(contributionChartEl, {
      type: "line",
      data: {
        labels: contributionLabels,
        datasets: [
          {
            label: "Contributions",
            data: contributionData,
            backgroundColor: "rgba(13, 110, 253, 0.2)",
            borderColor: "rgba(13, 110, 253, 1)",
            borderWidth: 2,
            tension: 0.3,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: "Contribution History",
          },
        },
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    })
  }

  // Sample loan chart
  const loanChartEl = document.getElementById("loanChart")
  if (loanChartEl) {
    const loanChart = new Chart(loanChartEl, {
      type: "doughnut",
      data: {
        labels: ["Pending", "Approved", "Rejected", "Paid"],
        datasets: [
          {
            data: loanStatusData,
            backgroundColor: [
              "rgba(255, 193, 7, 0.8)",
              "rgba(40, 167, 69, 0.8)",
              "rgba(220, 53, 69, 0.8)",
              "rgba(32, 201, 151, 0.8)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "right",
          },
          title: {
            display: true,
            text: "Loan Status",
          },
        },
      },
    })
  }
}

