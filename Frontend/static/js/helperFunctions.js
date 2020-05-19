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
