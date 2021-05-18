var data;
var papa_csv = Papa.parse('static/sensor2.csv', {
    download: false,
    header: true,
    complete: function(results) {
        console.log("Parse results: ", results.data);
        data = results.data;
        
        let i = 0;
        results.data.map((data, index)=> {
            if (i === 0) {
                let table = document.getElementById('tbl-data');
                generateTableHead(table, data);
            } else {
                let table = document.getElementById('tbl-data');
                generateTableRows(table, data);
            }
            i++;
        });
        
    }
});
/*
console.log(data);
var options = {
  series: [{
      data: data
  }],
  chart: {
      id: 'chart2',
      type: 'line',
      height: 230,
      toolbar: {
          autoSelected: 'pan',
          show: false
      }
  },
  colors: ['#546E7A'],
  stroke: {
      width: 3
  },
  dataLabels: {
      enabled: false
  },
  fill: {
      opacity: 1,
  },
  markers: {
      size: 0
  },
  xaxis: {
      type: 'datetime'
  }
};

var chart = new ApexCharts(document.querySelector("#chart-line"), options);
chart.render();

var optionsLine = {
  series: [{
      data: data
  }],
  chart: {
      id: 'chart1',
      height: 130,
      type: 'area',
      brush: {
          target: 'chart2',
          enabled: true
      },
      selection: {
          enabled: true,
          xaxis: {
              min: new Date('10 Feb 2017').getTime(),
              max: new Date('15 Feb 2017').getTime()
          }
      },
  },
  colors: ['#008FFB'],
  fill: {
      type: 'gradient',
      gradient: {
          opacityFrom: 0.91,
          opacityTo: 0.1,
      }
  },
  xaxis: {
      type: 'datetime',
      tooltip: {
          enabled: false
      }
  },
  yaxis: {
      tickAmount: 2
  }
};

var chartLine = new ApexCharts(document.querySelector("#chart-line2"), optionsLine);
chartLine.render();
*/
