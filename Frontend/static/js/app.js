updateViz = async (date) => {
  kpiPromises = [
    d3.json(`/corona_date/${date}`),
    d3.json(`/kpis/${date}`),
    d3.json(`/corona_tweets/${date}`),
  ];

  Promise.all(kpiPromises).then(([d, kpi, tweet]) => {
    document.getElementById("kpi-date-text").innerText = date;
    cases.push(+kpi.cases);
    deaths.push(+kpi.deaths);
    console.log(tweet);
    polarity = tweet.polarity;
    document.getElementById("kpi-cases-text").innerText = kpi.cases;
    document.getElementById("kpi-deaths-text").innerText = kpi.deaths;
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
