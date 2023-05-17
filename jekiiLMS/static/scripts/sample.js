var analyticOvData = {
  labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"],
  dataUnit: 'Ksh',
  lineTension: .1,
  datasets: [{
    label: "Current Month",
    color: "#e85347",
    dash: [5],
    background: "transparent",
    data: [3910, 4420, 4110, 5180, 4400, 5170, 6460, 8830, 5290, 5430, 4690, 4350]
  }, {
    label: "Current Month",
    color: "#798bff",
    dash: 0,
    background: NioApp.hexRGB('#798bff', .15),
    data: [4110, 4220, 4810, 5480, 4600, 5670, 6660, 4830, 5590, 5730, 4790, 4950]
  }]
};

function analyticsLineLarge(selector, set_data) {
  var $selector = selector ? $(selector) : $('.analytics-line-large');
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
        borderDash: _get_data.datasets[i].dash,
        borderColor: _get_data.datasets[i].color,
        pointBorderColor: 'transparent',
        pointBackgroundColor: 'transparent',
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: _get_data.datasets[i].color,
        pointBorderWidth: 2,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 2,
        pointRadius: 4,
        pointHitRadius: 4,
        data: _get_data.datasets[i].data
      });
    }

    var chart = new Chart(selectCanvas, {
      type: 'line',
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
              return data['labels'][tooltipItem[0]['index']];
            },
            label: function label(tooltipItem, data) {
              return data.datasets[tooltipItem.datasetIndex]['data'][tooltipItem['index']];
            }
          },
          backgroundColor: '#fff',
          borderColor: '#eff6ff',
          borderWidth: 2,
          titleFontSize: 13,
          titleFontColor: '#6783b8',
          titleMarginBottom: 6,
          bodyFontColor: '#9eaecf',
          bodyFontSize: 12,
          bodySpacing: 4,
          yPadding: 10,
          xPadding: 10,
          footerMarginTop: 0,
          displayColors: false
        },
        scales: {
          yAxes: [{
            display: true,
            position: NioApp.State.isRTL ? "right" : "left",
            ticks: {
              beginAtZero: true,
              fontSize: 12,
              fontColor: '#9eaecf',
              padding: 8,
              stepSize: 2400
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
  analyticsLineLarge();
});


//income vs expense starts
var incomExpensData = {
  labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"],
  dataUnit: 'Ksh',
  lineTension: .1,
  datasets: []
};

function fetchExpensIncomData() {
  var companyId = $('#incomExpensData').data('company-id');
  // Make a GET request to your API endpoint
  $.ajax({
    url: 'http://127.0.0.1:8000/api/loans-repayment/'+ companyId +'/', 
    type: 'GET',
    success: function(response) {
      // Process the response and update the incomExpensData object
      incomExpensData.datasets = [{
        label: "Current Month",
        color: "#e85347",
        dash: [5],
        background: "transparent",
        data: [3910, 4420, 4110, 5180, 4400, 5170, 6460, 8830, 5290, 5430, 4690, 4350]
      }, {
        label: "Current Month",
        color: "#798bff",
        dash: 0,
        background: NioApp.hexRGB('#798bff', .15),
        data: [4110, 4220, 4810, 5480, 4600, 5670, 6660, 4830, 5590, 5730, 4790, 4950]
      }];

      // Call the chart initialization function
      analyticsLineLarge();
    },
    error: function(error) {
      console.log(error);
    }
  });
}

function analyticsLineLarge(selector, set_data) {
  var $selector = selector ? $(selector) : $('.analytics-line-large');
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
        borderDash: _get_data.datasets[i].dash,
        borderColor: _get_data.datasets[i].color,
        pointBorderColor: 'transparent',
        pointBackgroundColor: 'transparent',
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: _get_data.datasets[i].color,
        pointBorderWidth: 2,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 2,
        pointRadius: 4,
        pointHitRadius: 4,
        data: _get_data.datasets[i].data
      });
    }

    var chart = new Chart(selectCanvas, {
      type: 'line',
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
              return data['labels'][tooltipItem[0]['index']];
            },
            label: function label(tooltipItem, data) {
              return data.datasets[tooltipItem.datasetIndex]['data'][tooltipItem['index']];
            }
          },
          backgroundColor: '#fff',
          borderColor: '#eff6ff',
          borderWidth: 2,
          titleFontSize: 13,
          titleFontColor: '#6783b8',
          titleMarginBottom: 6,
          bodyFontColor: '#9eaecf',
          bodyFontSize: 12,
          bodySpacing: 4,
          yPadding: 10,
          xPadding: 10,
          footerMarginTop: 0,
          displayColors: false
        },
        scales: {
          yAxes: [{
            display: true,
            position: NioApp.State.isRTL ? "right" : "left",
            ticks: {
              beginAtZero: true,
              fontSize: 12,
              fontColor: '#9eaecf',
              padding: 8,
              stepSize: 2400
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

// Init chart after the API data is fetched
NioApp.coms.docReady.push(function () {
  fetchExpensIncomData();
});
//ends