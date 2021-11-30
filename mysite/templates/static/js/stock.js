//Pseudo code
//Step 1: Define chart properties.
//Step 2: Create the chart with defined properties and bind it to the DOM element.
//Step 3: Add the CandleStick Series.
//Step 4: Set the data and render.


//Code
const log = console.log;

const chartProperties = {
  width:1200,
  height:600,
  layout: {
    backgroundColor: '#000000',
    textColor: 'rgba(255, 255, 255, 0.9)',
    },
  timeScale:{
    timeVisible:true,
    secondsVisible:false,

  },
  rightPriceScale: {
    borderColor: 'rgba(197, 203, 206, 0.8)',
  },
  timeScale: {
    borderColor: 'rgba(197, 203, 206, 0.8)',
  },
  crosshair: {
    mode: LightweightCharts.CrosshairMode.Normal,
  },
}

const domElement = document.getElementById('tvchart');
const chart = LightweightCharts.createChart(domElement,chartProperties);
const candleSeries = chart.addCandlestickSeries({
    upColor: 'rgba(255, 144, 0, 1)',
    downColor: '#000',
    borderDownColor: 'rgba(255, 144, 0, 1)',
    borderUpColor: 'rgba(255, 144, 0, 1)',
    wickDownColor: 'rgba(255, 144, 0, 1)',
    wickUpColor: 'rgba(255, 144, 0, 1)',
  });

/*fetch(`https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=1d&limit=1000`)
  .then(res => res.json())
  .then(data => {
    const cdata = data.map(d => {
      return {time:d[0]/1000,open:parseFloat(d[1]),high:parseFloat(d[2]),low:parseFloat(d[3]),close:parseFloat(d[4])}
    });
    candleSeries.setData(cdata);
  })
  .catch(err => log(err))*/
//stockinfo
const mydata = JSON.parse(document.getElementById('stockinfo').textContent);

var iterator = mydata.values();
for (let elements of iterator) {
    console.log(elements[0]);
}
console.log(mydata);
candleSeries.setData(mydata);