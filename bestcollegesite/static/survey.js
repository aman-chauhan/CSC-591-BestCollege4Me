Survey.StylesManager.applyTheme('default');

var surveyJSON;
// window.survey = new Survey.Model();
function on_page_load() {
  $.get(
    'https://raw.githubusercontent.com/aman-chauhan/CSC-591-BestCollege4Me/master/bestcollegesite/static/survey.json',
    function(raw_data) {
      surveyJSON = raw_data;
      // console.log(raw_data);
      window.survey = new Survey.Model(surveyJSON);
      survey.onComplete.add(function(result) {
        document.querySelector('#surveyResult').innerHTML =
          'result: ' + JSON.stringify(result.data);
        // console.log(result.data);

        $.post(
          '/bestcollege/submit_survey',
          JSON.stringify(result.data),
          function(raw_data) {
            var uni_ids = JSON.parse(raw_data).ids;
            console.log(uni_ids);
            var url_params = '';
            for (var i = 0; i < uni_ids.length; i++) {
              url_params += uni_ids[i] + ',';
            }

            var zip = JSON.parse(raw_data).zip;

            url_params = url_params.substring(0, url_params.length - 1);
            console.log('results/?ids=' + url_params + '&zip=' + zip);
            window.location.replace(
              'results/?ids=' + url_params + '&zip=' + zip
            );
          }
        );
      });
      $('#surveyElement').Survey({ model: survey });
    }
  );
}

if (!window.isLoaded) {
  window.addEventListener(
    'load',
    function() {
      on_page_load();
    },
    false
  );
} else {
  on_page_load();
}
