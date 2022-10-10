const chartProperties = {
  width: 1500,
  height: 600,
  timeScale: {
    timeVisible: true,
    secondsVisible: false,
  }
}

const domElement = document.getElementById('stock');
const chart = LightweightCharts.createChart(domElement, chartProperties);
const candleSeries = chart.addCandlestickSeries();
const currentLocale = window.navigator.languages[0];

chart.applyOptions({
  crosshair: {
    // Change mode from default 'magnet' to 'normal'.
    // Allows the crosshair to move freely without snapping to datapoints
    mode: LightweightCharts.CrosshairMode.Normal,

    // Vertical crosshair line (showing Date in Label)
    vertLine: {
      width: 8,
      color: '#C3BCDB44',
      style: LightweightCharts.LineStyle.Solid,
      labelBackgroundColor: '#9B7DFF',
    },

    // Horizontal crosshair line (showing Price in Label)
    horzLine: {
      color: '#9B7DFF',
      labelBackgroundColor: '#9B7DFF',
    },
  },
});
const myPriceFormatter = Intl.NumberFormat(currentLocale, {
  style: 'currency',
  currency: 'USD', // Currency for data points
}).format;

chart.timeScale().applyOptions({
  borderColor: '#71649C',
  barSpacing: 10,
});
chart.applyOptions({
  localization: {
    priceFormatter: myPriceFormatter,
  },
});

fetch('https://api.binance.com/api/v3/klines?symbol=ADAUSDT&interval=1d&limit=1000')
  .then(res => res.json())
  .then(data => {
    const cdata = data.map(d => {
      return { time: d[0] / 1000, open: parseFloat(d[1]), high: parseFloat(d[2]), low: parseFloat(d[3]), close: parseFloat(d[4]) }
    });
    candleSeries.setData(cdata);
    // const lineData = cdata.map(datapoint => ({
    //   time: datapoint.time,
    //   value: (datapoint.close + datapoint.open) / 2,
    // }));

    // // graph color need implementation 
    // const areaSeries = chart.addAreaSeries({
    //   lastValueVisible: false, // hide the last value marker for this series
    //   crosshairMarkerVisible: false, // hide the crosshair marker for this series
    //   lineColor: 'transparent', // hide the line
    //   topColor: 'rgba(56, 33, 110,0.6)',
    //   bottomColor: 'rgba(56, 33, 110, 0.1)',
    // });
    // Set the data for the Area Series
    areaSeries.setData(lineData);
    candleSeries.priceScale().applyOptions({
      autoScale: false, // disables auto scaling based on visible content
      scaleMargins: {
        top: 0.1,
        bottom: 0.2,
      },
    });
    // Setting the border color for the horizontal axis
  })
  .catch(err => log(err))