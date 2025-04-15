document.addEventListener("DOMContentLoaded", () => {
    const ctx = document.getElementById('overviewChart').getContext('2d');
  
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Students', 'Subjects', 'Exams'],
        datasets: [{
          label: 'Statistics',
          data: [50, 12, 5], // Replace with dynamic values via AJAX
          backgroundColor: ['#1abc9c', '#3498db', '#9b59b6'],
          borderRadius: 10
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: { enabled: true }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  });
  











  const ctx = document.getElementById('overviewChart').getContext('2d');

const overviewChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Students', 'Subjects', 'Exams'],
        datasets: [{
            label: 'Count Overview',
            data: [120, 25, 10], // Replace with values from Flask later via templating or AJAX
            backgroundColor: ['#007bff', '#28a745', '#ffc107'],
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false },
        }
    }
});
