import 'dart:html';
import 'dart:convert';

//void main() {
//  loadData();
//}
//
//void loadData() {
//  var url = "http://127.0.0.1:5000/update";
//  var request = HttpRequest.getString(url).then(onDataLoaded);
//}
//
//void onDataLoaded(String responseText) {
//  Map parsedResponse = JSON.decode(responseText);
//  parsedResponse.forEach((String milestone, Map user_issues) {
//      var milestoneElement = new DivElement();
//      milestoneElement.classes.add("milestone");
//      milestoneElement.appendHtml("<h2>" + milestone + "</h2>");
//    user_issues.forEach((user, issues) {
//      var userElement = new DivElement();
//      userElement.appendHtml("<h3>" + user + "</h3>");
//      userElement.classes.add("user");
//      for (var issue in issues) {
//        var issueElement = new DivElement();
//        var issueTitleElement = new DivElement();
//        issueTitleElement.text = issue["title"];
//        issueElement.append(issueTitleElement);
//        var issueScoreElement = new DivElement();
//        issueScoreElement.text = issue["score"].toString();
//        issueElement.append(issueScoreElement);
//        userElement.append(issueElement);
//      }
//      milestoneElement.append(userElement);
//    });
//    var mainContainer = querySelector("#main_container");
//    mainContainer.append(milestoneElement);
//  });
//}
//
