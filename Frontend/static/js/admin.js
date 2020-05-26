fetchData = () => {
  const urls = ["/corona_file_data", "/twitter_file_data"];

  const allRequests = urls.map((url) =>
    fetch(url).then((response) => response.json())
  );

  return Promise.all(allRequests);
};

fetchData().then(([coronaFile, twitterFile]) => {
  updateCoronaStats(coronaFile);
  updateTwitterStats(twitterFile);
});

updateCoronaStats = (coronaFile) => {
  document.getElementById("corona-file-name").innerText = coronaFile.file_name;
  document.getElementById("corona-file-size").innerText = `${(
    +coronaFile.file_size / 1e6
  ).toFixed(2)} MB`;
  document.getElementById("corona-start-date").innerText =
    coronaFile.start_date;
  document.getElementById("corona-end-date").innerText = coronaFile.end_date;
};

updateTwitterStats = (twitterFile) => {
  document.getElementById("twitter-file-name").innerText =
    twitterFile.file_name;
  document.getElementById("twitter-file-size").innerText = `${(
    twitterFile.file_size / 1e3
  ).toFixed(2)} kB`;
  document.getElementById("twitter-end-date").innerText = twitterFile.end_date;
  document.getElementById("twitter-start-date").innerText =
    twitterFile.start_date;
};

updateTweetData = () => {
  fetch("/update_twitter_data")
    .then((data) => data.json())
    .then((twitterFile) => {
      updateTwitterStats(twitterFile);
      alert("Twitter Data updated");
    });
};

updateCoronaData = () => {
  fetch("/update_corona_data")
    .then((data) => data.json())
    .then((coronaFile) => {
      updateCoronaStats(coronaFile);
      alert("Corona Data updated");
    });
};
