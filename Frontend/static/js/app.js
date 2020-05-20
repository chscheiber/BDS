updateViz = async (date) => {
  kpiPromises = [
    d3.json(`/corona_date/${date}`),
    d3.json(`/aggregated/${date}`),
    d3.json(`/corona_tweets/${date}`),
    d3.json(`/all_tweets/${date}`),
  ];

  Promise.all(kpiPromises).then(([d, agg, coronaTweets, allTweets]) => {
    document.getElementById("kpi-date-text").innerText = date;
    cases = +agg.cases;
    deaths = +agg.deaths;
    polarity_corona = coronaTweets.polarity;
    polarity_all = allTweets.polarity;
    document.getElementById("kpi-cases-text").innerText = +agg.cases;
    document.getElementById("kpi-deaths-text").innerText = +agg.deaths;
    tmp_popularity =
      coronaTweets.polarity.length >= 1
        ? +coronaTweets.polarity[coronaTweets.polarity.length - 1].toFixed(4)
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
