updateViz = async (date) => {
  kpiPromises = [
    d3.json(`/corona_date/${date}`),
    d3.json(`/aggregated/${date}`),
    d3.json(`/corona_tweets/${date}`),
  ];

  Promise.all(kpiPromises).then(([d, agg, tweet]) => {
    document.getElementById("kpi-date-text").innerText = date;
    cases = +agg.cases;
    deaths = +agg.deaths;
    polarity = tweet.polarity;
    document.getElementById("kpi-cases-text").innerText = +agg.cases;
    document.getElementById("kpi-deaths-text").innerText = +agg.deaths;
    tmp_popularity =
      tweet.polarity.length >= 1
        ? +tweet.polarity[tweet.polarity.length - 1].toFixed(4)
        : 0;
    document.getElementById("kpi-sentiment-text").innerText = tmp_popularity;
    updateMap(date, d);
    updateSentimentChart();
  });
};

startDate = new Date(2020, 1, 1);
latestDate = new Date();
datePromises = [d3.json("/start_date"), d3.json("/end_date")];

Promise.all(datePromises).then(([sDate, eDate]) => {
  startDate = stringToDate(sDate.date);
  latestDate = stringToDate(eDate.date);
});

date = new Date(startDate);
//updateKPIs(getDateString(startDate));

var isLoading = true;
drawMap(getDateString(date));
updateViz(getDateString(date));
