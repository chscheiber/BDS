polarity_corona = [];
polarity_all = [];

var margin = { top: 10, right: 30, bottom: 30, left: 60 },
  width =
    document.getElementById("sentiment-timeline").offsetWidth -
    margin.left -
    margin.right,
  height =
    document.getElementById("sentiment-timeline").clientHeight -
    margin.top -
    margin.bottom;
console.log(width);

var sentimentSVG = d3
  .select("#sentiment-timeline")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var xScaleCoronaTweets = d3.scaleLinear().range([0, width]); // output
var xScaleAllTweets = d3.scaleLinear().range([0, width]); // output

var yScale = d3
  .scaleLinear()
  .domain([-1, 1]) // input
  .range([height, 0]); // output

var lineCoronaTweets = d3
  .line()
  .x((d, i) => xScaleCoronaTweets(i))
  .y((d) => yScale(d))
  .curve(d3.curveMonotoneX); // apply smoothing to the line

var lineAllTweets = d3
  .line()
  .x((d, i) => xScaleAllTweets(i))
  .y((d) => yScale(d))
  .curve(d3.curveMonotoneX); // apply smoothing to the line
var xAxis = d3.axisBottom(xScaleAllTweets).ticks(0);

var yAxis = d3.axisLeft(yScale).ticks(5);

sentimentSVG
  .append("g")
  .attr("class", "x axis")
  .attr("transform", "translate(0," + yScale(0) + ")")
  .call(xAxis); // Create an axis component with d3.axisBottom

sentimentSVG.append("g").attr("class", "y axis").call(yAxis); // Create an axis component with d3.axisLeft

sentimentSVG
  .append("path")
  .attr("class", "line corona-tweets")
  .attr("d", lineCoronaTweets(polarity_corona));
sentimentSVG
  .append("path")
  .attr("class", "line all-tweets")
  .attr("d", lineAllTweets(polarity_all));

function updateSentimentChart() {
  xScaleCoronaTweets.domain([0, polarity_corona.length - 1]);
  xScaleAllTweets.domain([0, polarity_all.length - 1]);
  var svg = d3.select("#sentiment-timeline");

  svg
    .select(".line.corona-tweets")
    .attr("d", lineCoronaTweets(polarity_corona));
  svg.select(".line.all-tweets").attr("d", lineAllTweets(polarity_all));

  svg
    .select(".x.axis") // change the x axis
    .call(xAxis);
}