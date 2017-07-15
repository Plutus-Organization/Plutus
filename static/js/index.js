val heroku_app_url = '';

function get_article_for_name(name) {
  var requestUrl = heroku_app_url + '?name=' + name;
  var responseTxt = httpGet(requestUrl);
  var responseJson = JSON.parse(responseTxt);
  var summaryTxt = responseJson['summary'];
  var url = responseJson['url'];
  var urlHyper = '<a href=' + url + '>Link to Article</a>';
  $('#news_result').text(summaryTxt);
  $('#news_url').html(urlHyper);
}

function httpGet(url) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", url, false ); // false for synchronous request
  xmlHttp.send( null );
  return xmlHttp.responseText;
}