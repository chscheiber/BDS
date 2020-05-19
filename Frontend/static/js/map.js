let svg = d3
  .select("#chart-1")
  .append("svg")
  .attr("id", "map-svg")
  .attr("viewBox", "0 0 960 620")
  .attr("height", "100%");

let county_map = d3.map();
let state_map = d3.map();

let path = d3.geoPath();

let color = d3.scaleSequential(d3.interpolateBlues);

// Map based on: https://bl.ocks.org/adamjanes/6cf85a4fd79e122695ebde7d41fe327f
drawMap = (date) => {
  var promises = [
    d3.json("https://d3js.org/us-10m.v1.json"),
    d3.json(`/corona_date/${date}`),
    d3.json("/counties"),
  ];
  let cases = d3.map();

  Promise.all(promises).then(ready);

  function ready([us, d, counties]) {
    for (var key in d) {
      curr_fips = +d[key].fips >= 10000 ? d[key].fips : "0" + d[key].fips;
      cases.set(curr_fips, +d[key].cases);
    }

    for (var key in counties) {
      curr_fips =
        +counties[key].fips >= 10000
          ? counties[key].fips
          : "0" + counties[key].fips;
      county_map.set(curr_fips, counties[key].county_name);
      state_map.set(curr_fips, counties[key].state_name);
    }
    document.getElementById("map-load").remove();
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
        return (
          "County:\t" +
          county_map.get(d.id) +
          "\nState:\t" +
          state_map.get(d.id) +
          "\nCases:\t" +
          (cases.get(d.id) | 0)
        );
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
    isLoading = false;
  }
};

updateMap = (date) => {
  let svg = d3.select("#map-svg");
  let cases = d3.map();

  var promises = [d3.json(`/corona_date/${date}`)];

  Promise.all(promises).then(ready);

  function ready([d]) {
    for (var key in d) {
      curr_fips = +d[key].fips >= 10000 ? d[key].fips : "0" + d[key].fips;
      cases.set(curr_fips, +d[key].cases);
    }

    var colorScale = d3
      .scaleLog()
      .domain([1, d3.max(cases.values())])
      .range([0, 1]);

    svg.selectAll("path").attr("fill", function (d) {
      return color(colorScale(cases.get(d.id) | 1));
    });

    svg.selectAll("title").text(function (d) {
      return (
        "Date:\t" +
        date +
        "\nCounty:\t" +
        county_map.get(d.id) +
        "\nState:\t" +
        state_map.get(d.id) +
        "\nCases:\t" +
        (cases.get(d.id) | 0)
      );
    });
    document.getElementById("kpi-1-text").innerText = date;
  }
};

getDateString = (date) => {
  year = date.getFullYear();
  month = date.getMonth() + 1;
  month = month >= 10 ? month : "0" + month;
  day = date.getDate();
  day = day >= 10 ? day : "0" + day;
  return `${year}-${month}-${day}`;
};

stringToDate = (dateString) => {
  var re = /(\d{4})-(\d{2})-(\d{2})/;
  if (dateString.match(re) == null || dateString.length != 10) return undefined;

  var match = re.exec(dateString);
  tmp_year = match[1];
  tmp_month = match[2];
  tmp_day = match[3];
  return new Date(tmp_year, tmp_month - 1, tmp_day);
};

startDate = new Date(2020, 1, 1);
latestDate = new Date();
datePromises = [d3.json("/start_date"), d3.json("/end_date")];
console.log(datePromises);
Promise.all(datePromises).then(([sDate, eDate]) => {
  console.log(sDate, eDate);
  startDate = stringToDate(sDate.date);
  latestDate = stringToDate(eDate.date);
});

date = new Date(startDate);
var isLoading = true;
drawMap(getDateString(date));
document.getElementById("kpi-1-text").innerText = getDateString(date);
