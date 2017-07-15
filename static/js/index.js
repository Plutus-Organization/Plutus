

function get_article_for_name() {
  var name = $('#news').val();
  console.log(name);
  //var requestUrl = 'https://plutus-backend.herokuapp.com/get_article_from_name?name=' + name;
  var requestUrl = 'http://localhost:5000/get_article_from_name?name=' + name;
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
