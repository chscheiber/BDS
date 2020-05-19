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

  var today = new Date();
  today.setDate(today.getDate() - 1);
  error_msg = `Please enter a date between 2020-02-01 and ${today.getFullYear()}-${
    today.getMonth() + 1
  }- ${today.getDate()}`;

  var re = /(\d{4})-(\d{2})-(\d{2})/;
  if (tmpDate.match(re) == null || tmpDate.length != 10) {
    alert(error_msg);
    return;
  }

  var match = re.exec(tmpDate);
  tmp_year = match[1];
  tmp_month = match[2];
  tmp_day = match[3];
  tmpDate = new Date(tmp_year, tmp_month - 1, tmp_day);
  if (!(tmpDate >= startDate && tmpDate < today)) {
    alert(error_msg);
    return;
  }
  resetVisualization(tmpDate);
}
form.addEventListener("submit", handleForm);
