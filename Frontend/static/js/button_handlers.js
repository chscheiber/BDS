var interval = undefined;
var isRunning = false;

startVisualization = () => {
  if (isRunning || isLoading) return;
  isRunning = true;
  console.log("Run");
  interval = setInterval(update_interval, 1000);
  function update_interval() {
    if (date >= latestDate) {
      clearInterval(interval);
      isRunning = false;
    } else {
      updateMap(getDateString(date));
      date.setDate(date.getDate() + 1);
    }
  }
};

pauseVisualization = () => {
  if (!isRunning || isLoading) return;
  console.log("Pause");
  clearInterval(interval);
  isRunning = false;
};

resetVisualization = (resetDate = new Date(startDate)) => {
  if (isLoading) return;
  console.log("Reset");
  clearInterval(interval);
  updateMap(getDateString(resetDate));
  date = new Date(resetDate);
  isRunning = false;
};

// Form
var form = document.getElementById("date-form");
function handleForm(event) {
  event.preventDefault();
  tmpDate = document.getElementById("dateSetter").value;

  error_msg = `Please enter a date between 2020-02-01 and ${latestDate.getFullYear()}-${
    latestDate.getMonth() + 1
  }- ${latestDate.getDate()}`;

  tmpDate = stringToDate(tmpDate);
  if (tmpDate == undefined || !(tmpDate >= startDate && tmpDate < today)) {
    alert(error_msg);
    return;
  }
  resetVisualization(tmpDate);
}
form.addEventListener("submit", handleForm);
