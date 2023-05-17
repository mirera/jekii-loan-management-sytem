var disbursementData = {
  labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"],
  dataUnit: 'Loans',
  lineTension: .1,
  datasets: [{
    label: "Loans",
    color: "#9cabff",
    background: "#9cabff",
    data: []
  }]
};

function fetchDisbursementData() {
  var companyId = $('#disbursementData').data('company-id');
  // Make a GET request to your API endpoint
  $.ajax({
    url: 'http://127.0.0.1:8000/api/disbursement-data/' + companyId + '/', 
    type: 'GET',
    success: function(response) {
      // Process the response and update the incomExpensData object
      disbursementData.datasets = [{
        label: "Current Month",
        color: "#e85347",
        dash: [5],
        background: "transparent",
        data: response
      }];

      // Call the chart initialization function
      analyticsAu();
    },
    error: function(error) {
      console.log(error);
    }
  });
}
function analyticsAu(selector, set_data) {
  var $selector = selector ? $(selector) : $('.analytics-au-chart');
  $selector.each(function () {
    var $self = $(this),
        _self_id = $self.attr('id'),
        _get_data = typeof set_data === 'undefined' ? eval(_self_id) : set_data;

    var selectCanvas = document.getElementById(_self_id).getContext("2d");
    var chart_data = [];

    for (var i = 0; i < _get_data.datasets.length; i++) {
      chart_data.push({
        label: _get_data.datasets[i].label,
        tension: _get_data.lineTension,
        backgroundColor: _get_data.datasets[i].background,
        borderWidth: 2,
        borderColor: _get_data.datasets[i].color,
        data: _get_data.datasets[i].data,
        barPercentage: .7,
        categoryPercentage: .7
      });
    }

    var chart = new Chart(selectCanvas, {
      type: 'bar',
      data: {
        labels: _get_data.labels,
        datasets: chart_data
      },
      options: {
        legend: {
          display: _get_data.legend ? _get_data.legend : false,
          labels: {
            boxWidth: 12,
            padding: 20,
            fontColor: '#6783b8'
          }
        },
        maintainAspectRatio: false,
        tooltips: {
          enabled: true,
          rtl: NioApp.State.isRTL,
          callbacks: {
            title: function title(tooltipItem, data) {
              return false; //data['labels'][tooltipItem[0]['index']];
            },
            label: function label(tooltipItem, data) {
              return data.datasets[tooltipItem.datasetIndex]['data'][tooltipItem['index']];
            }
          },
          backgroundColor: '#eff6ff',
          titleFontSize: 9,
          titleFontColor: '#6783b8',
          titleMarginBottom: 6,
          bodyFontColor: '#9eaecf',
          bodyFontSize: 9,
          bodySpacing: 4,
          yPadding: 6,
          xPadding: 6,
          footerMarginTop: 0,
          displayColors: false
        },
        scales: {
          yAxes: [{
            display: true,
            position: NioApp.State.isRTL ? "right" : "left",
            ticks: {
              beginAtZero: false,
              fontSize: 12,
              fontColor: '#9eaecf',
              padding: 0,
              display: false,
              stepSize: 300
            },
            gridLines: {
              color: NioApp.hexRGB("#526484", .2),
              tickMarkLength: 0,
              zeroLineColor: NioApp.hexRGB("#526484", .2)
            }
          }],
          xAxes: [{
            display: false,
            ticks: {
              fontSize: 12,
              fontColor: '#9eaecf',
              source: 'auto',
              padding: 0,
              reverse: NioApp.State.isRTL
            },
            gridLines: {
              color: "transparent",
              tickMarkLength: 0,
              zeroLineColor: 'transparent',
              offsetGridLines: true
            }
          }]
        }
      }
    });
  });
} // init chart

NioApp.coms.docReady.push(function () {
  analyticsAu();
});