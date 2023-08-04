"use strict";

!function (NioApp, $) { 
  "use strict"; //////// for developer - User Balance //////// 
  // Avilable options to pass from outside 
  // labels: array,
  // legend: false - boolean,
  // dataUnit: string, (Used in tooltip or other section for display) 
  // datasets: [{label : string, color: string (color code with # or other format), data: array}]

//disbursement bar chart
var disbursementData = {
  labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"],
  dataUnit: 'Loans',
  lineTension: .1,
  datasets: []
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
        label: "Loans",
        color: "#9cabff",
        background: "#9cabff",
        data: response.disbursementData
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
  fetchDisbursementData();
});
// ends

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
    url: 'http://127.0.0.1:8000/api/income-expense/' + companyId + '/', 
    type: 'GET',
    success: function(response) {
      // Process the response and update the incomExpensData object
      incomExpensData.datasets = [{
        label: "Current Month",
        color: "#e85347",
        dash: [5],
        background: "transparent",
        data: response.expenseData
      }, {
        label: "Current Month",
        color: "#798bff",
        dash: 0,
        background: NioApp.hexRGB('#798bff', .15),
        data: response.incomeData
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

// dynamic loans repayment data 
var LoansData = {
  labels: ["Mature", "Cleared", "Defaulted", "Immature"],
  dataUnit: 'Ksh',
  legend: false,
  datasets: []
};

function fetchLoansData() {
  var companyId = $('#LoansData').data('company-id');
  // Make a GET request to your API endpoint
  $.ajax({
    url: 'http://127.0.0.1:8000/api/loans-repayment/'+ companyId +'/', 
    type: 'GET',
    success: function(response) {
      // Process the response and update the LoansData object
      LoansData.datasets = [{
        borderColor: "#fff",
        background: ["#798bff", "#1ee0ac", "#E45550", "#8294AC"],
        data: response //response data already in required format
      }];

      // Call the chart initialization function
      analyticsDoughnut();
    },
    error: function(error) {
      console.log(error);
    }
  });
}

function analyticsDoughnut(selector, set_data) {
  var $selector = selector ? $(selector) : $('.analytics-doughnut');
  $selector.each(function () {
    var $self = $(this),
        _self_id = $self.attr('id'),
        _get_data = typeof set_data === 'undefined' ? eval(_self_id) : set_data;

    var selectCanvas = document.getElementById(_self_id).getContext("2d");
    var chart_data = [];

    for (var i = 0; i < _get_data.datasets.length; i++) {
      chart_data.push({
        backgroundColor: _get_data.datasets[i].background,
        borderWidth: 2,
        borderColor: _get_data.datasets[i].borderColor,
        hoverBorderColor: _get_data.datasets[i].borderColor,
        data: _get_data.datasets[i].data
      });
    }

    var chart = new Chart(selectCanvas, {
      type: 'doughnut',
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
        rotation: -1.5,
        cutoutPercentage: 70,
        maintainAspectRatio: false,
        tooltips: {
          enabled: true,
          rtl: NioApp.State.isRTL,
          callbacks: {
            title: function title(tooltipItem, data) {
              return data['labels'][tooltipItem[0]['index']];
            },
            label: function label(tooltipItem, data) {
              return data.datasets[tooltipItem.datasetIndex]['data'][tooltipItem['index']] + ' ' + _get_data.dataUnit;
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
        }
      }
    });
  });
} // init chart

// Init chart after the API data is fetched
NioApp.coms.docReady.push(function () {
  fetchLoansData();
});
// ends

  var totalRoom = {
    labels: ["01 Jan", "02 Jan", "03 Jan", "04 Jan", "05 Jan", "06 Jan", "07 Jan"],
    dataUnit: 'Room',
    stacked: true,
    datasets: [{
      label: "User",
      color: [NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), NioApp.hexRGB("#6576ff", .2), "#6576ff"],
      // @v2.0
      data: [12, 15, 6, 5, 15, 7, 8]
    }]
  };
  var totalBooking = {
    labels: ["01 Jan", "02 Jan", "03 Jan", "04 Jan", "05 Jan", "06 Jan", "07 Jan"],
    dataUnit: 'Room',
    stacked: true,
    datasets: [{
      label: "User",
      color: [NioApp.hexRGB("#816bff", .2), NioApp.hexRGB("#816bff", .2), NioApp.hexRGB("#816bff", .2), NioApp.hexRGB("#816bff", .2), NioApp.hexRGB("#816bff", .2), NioApp.hexRGB("#816bff", .2), "#816bff"],
      // @v2.0
      data: [120, 150, 80, 69, 50, 105, 75]
    }]
  };
  var totalExpenses = {
    labels: ["01 Jan", "02 Jan", "03 Jan", "04 Jan", "05 Jan", "06 Jan", "07 Jan"],
    dataUnit: 'USD',
    stacked: true,
    datasets: [{
      label: "Expenses",
      color: [NioApp.hexRGB("#559bfb", .2), NioApp.hexRGB("#559bfb", .2), NioApp.hexRGB("#559bfb", .2), NioApp.hexRGB("#559bfb", .2), NioApp.hexRGB("#559bfb", .2), NioApp.hexRGB("#559bfb", .2), "#559bfb"],
      // @v2.0
      data: [600, 700, 800, 500, 600, 500, 1200]
    }]
  };

  function ivDataChart(selector, set_data) {
    var $selector = selector ? $(selector) : $('.iv-data-chart');
    $selector.each(function () {
      var $self = $(this),
          _self_id = $self.attr('id'),
          _get_data = typeof set_data === 'undefined' ? eval(_self_id) : set_data,
          _d_legend = typeof _get_data.legend === 'undefined' ? false : _get_data.legend;

      var selectCanvas = document.getElementById(_self_id).getContext("2d");
      var chart_data = [];

      for (var i = 0; i < _get_data.datasets.length; i++) {
        chart_data.push({
          label: _get_data.datasets[i].label,
          data: _get_data.datasets[i].data,
          // Styles
          backgroundColor: _get_data.datasets[i].color,
          borderWidth: 2,
          borderColor: 'transparent',
          hoverBorderColor: 'transparent',
          borderSkipped: 'bottom',
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
              boxWidth: 30,
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
                return false;
              },
              label: function label(tooltipItem, data) {
                return data['labels'][tooltipItem['index']] + ' ' + data.datasets[tooltipItem.datasetIndex]['data'][tooltipItem['index']];
              }
            },
            backgroundColor: '#eff6ff',
            titleFontSize: 11,
            titleFontColor: '#6783b8',
            titleMarginBottom: 4,
            bodyFontColor: '#9eaecf',
            bodyFontSize: 10,
            bodySpacing: 3,
            yPadding: 8,
            xPadding: 8,
            footerMarginTop: 0,
            displayColors: false
          },
          scales: {
            yAxes: [{
              display: false,
              stacked: _get_data.stacked ? _get_data.stacked : false,
              ticks: {
                beginAtZero: true
              }
            }],
            xAxes: [{
              display: false,
              stacked: _get_data.stacked ? _get_data.stacked : false,
              ticks: {
                reverse: NioApp.State.isRTL
              }
            }]
          }
        }
      });
    });
  } // init chart

  NioApp.coms.docReady.push(function () {
    ivDataChart();
  });

  //reports and analytics scirpts starts here

  
}(NioApp, jQuery);