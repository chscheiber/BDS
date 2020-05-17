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
  
}

getCoronaData();
kpi1();
