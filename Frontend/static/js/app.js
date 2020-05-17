//document.getElementById("chart-1").offsetWidth
//document.getElementById("chart-1").clientWidth -> without borders width

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

drawMap = () => {
  // https://bl.ocks.org/adamjanes/6cf85a4fd79e122695ebde7d41fe327f#unemployment.tsv
  var chart = d3.select("#chart-1");
  var width = document.getElementById("chart-1").clientWidth;
  var height = document.getElementById("chart-1").clientHeight;

  var svg = chart.append("svg").attr("width", width).attr("height", height);

  var path = d3.geoPath();

  var x = d3.scaleLinear().domain([1, 10]).rangeRound([height, width]);

  var color = d3
    .scaleThreshold()
    .domain(d3.range(2, 10))
    .range(d3.schemeBlues[9]);

  var g = svg
    .append("g")
    .attr("class", "key")
    .attr("transform", "translate(0,40)");

  g.selectAll("rect")
    .data(
      color.range().map(function (d) {
        d = color.invertExtent(d);
        if (d[0] == null) d[0] = x.domain()[0];
        if (d[1] == null) d[1] = x.domain()[1];
        return d;
      })
    )
    .enter()
    .append("rect")
    .attr("height", 8)
    .attr("x", function (d) {
      return x(d[0]);
    })
    .attr("width", function (d) {
      return x(d[1]) - x(d[0]);
    })

  g.call(
    d3
      .axisBottom(x)
      .tickSize(13)
      .tickFormat(function (x, i) {
        return i ? x : x + "%";
      })
      .tickValues(color.domain())
  )
    .select(".domain")
    .remove();

  var promises = [
    d3.json("https://d3js.org/us-10m.v1.json"),
  ];

  Promise.all(promises).then(ready);

  function ready([us]) {
    svg
      .append("g")
      .attr("class", "counties")
      .selectAll("path")
      .data(topojson.feature(us, us.objects.counties).features)
      .enter()
      .append("path")
      .attr("d", path);

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

drawMap()