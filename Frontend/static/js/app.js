updateViz = async (date) => {
  kpiPromises = [d3.json(`/corona_date/${date}`), d3.json(`/kpis/${date}`)];

  Promise.all(kpiPromises).then(([d, kpi]) => {
    updateMap(date, d);
    updateSentimentChart();
    document.getElementById("kpi-date-text").innerText = date;
    cases.push(+kpi.cases);
    deaths.push(+kpi.deaths);
    sentiment = kpi.sentiment;
    document.getElementById("kpi-cases-text").innerText = kpi.cases;
    document.getElementById("kpi-deaths-text").innerText = kpi.deaths;
    document.getElementById("kpi-sentiment-text").innerText =
      kpi.sentiment[kpi.sentiment.length - 1];
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
