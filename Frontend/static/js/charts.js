deaths = [];
cases = [];
sentiment = [];

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

var xScale = d3.scaleLinear().range([0, width]); // output

var yScale = d3
  .scaleLinear()
  .domain([-1, 1]) // input
  .range([height, 0]); // output

var line = d3
  .line()
  .x((d, i) => xScale(i))
  .y((d) => yScale(d));
//.curve(d3.curveMonotoneX); // apply smoothing to the line
var xAxis = d3.axisBottom(xScale).ticks(0);

var yAxis = d3.axisLeft(yScale).ticks(5);

sentimentSVG
  .append("g")
  .attr("class", "x axis")
  .attr("transform", "translate(0," + yScale(0) + ")")
  .call(xAxis); // Create an axis component with d3.axisBottom

sentimentSVG.append("g").attr("class", "y axis").call(yAxis); // Create an axis component with d3.axisLeft

sentimentSVG.append("path").attr("class", "line").attr("d", line(sentiment));

function updateSentimentChart() {
  xScale.domain([0, sentiment.length]);
  var svg = d3.select("#sentiment-timeline");

  svg.select(".line").attr("d", line(sentiment));

  svg
    .select(".x.axis") // change the x axis
    .call(xAxis);
}

//-------------------------------------
/*
var coronaDevSVG;

drawCoronaDevelopment = () => {
  var margin = { top: 10, right: 30, bottom: 30, left: 60 },
    width =
      document.getElementById("corona-dev-chart").offsetWidth -
      margin.left -
      margin.right,
    height =
      document.getElementById("corona-dev-chart").clientHeight -
      margin.top -
      margin.bottom;

  var svg = d3
    .select("#corona-dev-chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  coronaDevSVG = svg;
  updateCoronaDevelopment();
};

updateCoronaDevelopment = () => {
  console.log(cases);
  var margin = { top: 10, right: 30, bottom: 30, left: 60 },
    width =
      document.getElementById("corona-dev-chart").offsetWidth -
      margin.left -
      margin.right,
    height =
      document.getElementById("corona-dev-chart").clientHeight -
      margin.top -
      margin.bottom;
  var svg = coronaDevSVG;
  var n = cases.length;
  var xScale = d3
    .scaleLinear()
    .domain([0, n - 1]) // input
    .range([0, width]); // output

  var yScale = d3
    .scaleLinear()
    .domain([0, d3.max(cases)]) // input
    .range([height, 0]); // output

  var line = d3
    .line()
    .x(function (d, i) {
      return xScale(i);
    }) // set the x values for the line generator
    .y(function (d) {
      return yScale(d);
    }) // set the y values for the line generator
    .curve(d3.curveMonotoneX); // apply smoothing to the line

  svg
    .append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom

  svg.append("g").attr("class", "y axis").call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft
  svg
    .append("path")
    .datum(cases) // 10. Binds data to the line
    .attr("class", "line") // Assign a class for styling
    .attr("d", line); // 11. Calls the line generator

  svg
    .selectAll(".dot")
    .data(cases)
    .enter()
    .append("circle") // Uses the enter().append() method
    .attr("class", "dot") // Assign a class for styling
    .attr("cx", function (d, i) {
      return xScale(i);
    })
    .attr("cy", function (d) {
      return yScale(d);
    })
    .attr("r", 4)
    .append("title")
    .text(function (d) {
      return d;
    })
    .on("mouseover", function (a, b, c) {
      console.log(a);
    })
    .on("mouseout", function () {});
};
*/
