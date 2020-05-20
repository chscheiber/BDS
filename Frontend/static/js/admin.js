fetchData = () => {
  const urls = [
    "/start_date",
    "/end_date",
    "/corona_file_data",
    "/twitter_file_data",
  ];

  const allRequests = urls.map((url) =>
    fetch(url).then((response) => response.json())
  );

  return Promise.all(allRequests);
};

fetchData().then(([startDate, endDate, coronaFile, twitterFile]) => {
  document.getElementById("corona-file-name").innerText = coronaFile.file_name;
  document.getElementById("corona-file-size").innerText = coronaFile.file_size;
  document.getElementById("twitter-file-name").innerText =
    twitterFile.file_name;
  document.getElementById("twitter-file-size").innerText =
    twitterFile.file_size;
  document.getElementById("corona-start-date").innerText = startDate.date;
  document.getElementById("corona-end-date").innerText = endDate.date;
  document.getElementById("twitter-end-date").innerText = endDate.date;
  document.getElementById("twitter-start-date").innerText = startDate.date;
});
