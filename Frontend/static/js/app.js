getCoronaData = async () => {
  coronaData = {};
  fetch("/infections", { headers: { "Content-Type": "application/json" } })
    .then((data) => data.json())
    .then((data) => (coronaData = data));
  console.log(coronaData);
};

kpi1 = () => {
  document.getElementById("kpi-1").innerText = "Test";
};


// Map based on: https://bl.ocks.org/adamjanes/6cf85a4fd79e122695ebde7d41fe327f
drawMap = () => {
  var svg = d3
    .select("#chart-1")
    .append("svg")
    .attr("width", 960)
    .attr("height", 600);
  
  var cases = d3.map();
  var county_map = d3.map();
  var state_map = d3.map();

  var path = d3.geoPath();

  var color = d3
    .scaleSequential(d3.interpolateBlues) 

  var promises = [
    d3.json("https://d3js.org/us-10m.v1.json"),
    d3.csv(
      "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv",
      function (d) {
        cases.set(d.fips, +d.cases);
        county_map.set(d.fips, d.county)
        state_map.set(d.fips, d.state)
      }
    ),
  ];

  Promise.all(promises).then(ready);
  function ready([us]) {
     var colorScale = d3
       .scaleLog()
       .domain([1, d3.max(cases.values())])
       .range([0, 1]);
    svg
      .append("g")
      .attr("class", "counties county-borders")
      .selectAll("path")
      .data(topojson.feature(us, us.objects.counties).features)
      .enter()
      .append("path")
      .attr("fill", function (d) {
        return color(colorScale(cases.get(d.id) | 1));
      })
      .attr("d", path)
      .append("title")
      .text(function (d) {
        return ("County:\t" + county_map.get(d.id) +
          "\nState:\t" + state_map.get(d.id) +
          "\nCases:\t" + (cases.get(d.id) | 0));
      });
    svg
      .append("path")
      .datum(
        topojson.mesh(us, us.objects.states, function (a, b) {
          return a !== b;
        })
      )
      .attr("class", "states")
      .attr("d", path);
  }

};

drawMap();
