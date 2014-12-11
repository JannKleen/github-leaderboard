import 'package:polymer/polymer.dart';
import 'dart:html';
import 'dart:convert';
import 'dart:async';

@CustomTag('milestone-list')
class MilestoneList extends PolymerElement {
  @observable List milestones = toObservable([]);
  @observable int selected = 0;
  @observable List<Map> issue_groups = toObservable([]);
  @observable List<Map> score_groups_lookup = toObservable([]);
  @observable List<List<Map>> score_groups_ordered = toObservable([]);

  Map responseData = {};

  MilestoneList.created() : super.created();

  @override
  void attached() {
    super.attached();

    // Start refresh loop
    this.refresh();
  }

  void refresh() {
    // Activate spinner
    var spinner = shadowRoot.querySelector('paper-spinner');
    spinner.active = true;

    // Fetch updated data
    String url = "/update";
    var request = HttpRequest.getString(url).then(onDataLoaded);

    // Schedule next refresh
    new Future.delayed(const Duration(seconds:60), () {
      this.refresh();
    });

  }

  void onDataLoaded(String responseText) {
    this.responseData = JSON.decode(responseText);
    this.milestones = toObservable(this.responseData['issues'].keys);
    for (var milestone in this.milestones) {
      this.issue_groups.add(responseData['issues'][milestone]);
    }
    for (var milestone in this.milestones) {
      List<Map> scores = [];
      responseData['scores'][milestone].forEach((key, value) {
        scores.add({'username': key,
                    'score': value});
      });
      scores.sort((x, y) => y['score'].compareTo(x['score']));
      this.score_groups_ordered.add(scores);
      this.score_groups_lookup.add(responseData['scores'][milestone]);
    }

    // de-activate spinner
    var spinner = shadowRoot.querySelector('paper-spinner');
    spinner.active = false;
  }

  void select_milestone(Event e, var detail, Node target) {

  }
}
