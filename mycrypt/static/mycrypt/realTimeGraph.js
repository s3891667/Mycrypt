const log2 = console.log;
const chartProperties2 = {
    width: 750,
    height: 300,
    timeScale: {
        timeVisible: true,
        secondsVisible: false,
    }
}
const dom2 = document.getElementById('stock2');
const chart2 = LightweightCharts.createChart(dom2, chartProperties2);
const candleSeries2 = chart2.addCandlestickSeries();
const currentLocale2 = window.navigator.languages[0];
var value = window.localStorage.getItem("coin");
var value2 = value.toUpperCase();
var url = `https://api.binance.com/api/v3/klines?symbol=${value2}USDT&interval=1m&limit=1000`;
fetch(url)
    .then(res => res.json())
    .then(data => {
        const cdata2 = data.map(d => {
            return { time: d[0] / 1000, open: parseFloat(d[1]), high: parseFloat(d[2]), low: parseFloat(d[3]), close: parseFloat(d[4]) }
        });
        candleSeries2.setData(cdata2);

    })
    .catch(err => log(err))

const binanceSocket = new WebSocket(
    `wss://stream.binance.com:9443/ws/` + value + `usdt@kline_1m`);
binanceSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    const cdata2 = {
        time: (data["k"]["t"]) /1000,
        open: data["k"]["o"],
        high: data["k"]["h"],
        low: data["k"]["l"],
        close: data["k"]["c"],
    };
    candleSeries2.update(cdata2);
};