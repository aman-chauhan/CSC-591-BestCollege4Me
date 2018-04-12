Survey.StylesManager.applyTheme('default');

var json = {
  title: 'Best College for Me',
  showProgressBar: 'bottom',
  firstPageIsStarted: true,
  startSurveyText: 'Start Survey',
  pages: [
    {
      questions: [
        {
          type: 'html',
          html: '** copy here to introduce the survey and its purpose **',
        },
      ],
    },
    {
      questions: [
        {
          type: 'radiogroup',
          name: 'civilwar',
          title: 'When was the Civil War?',
          choices: [
            '1750-1800',
            '1800-1850',
            '1850-1900',
            '1900-1950',
            'after 1950',
          ],
          correctAnswer: '1850-1900',
        },
      ],
    },
    {
      questions: [
        {
          type: 'radiogroup',
          name: 'libertyordeath',
          title: "Who said 'Give me liberty or give me death?'",
          choicesOrder: 'random',
          choices: [
            'John Hancock',
            'James Madison',
            'Patrick Henry',
            'Samuel Adams',
          ],
          correctAnswer: 'Patrick Henry',
        },
      ],
    },
    {
      maxTimeToFinish: 15,
      questions: [
        {
          type: 'radiogroup',
          name: 'magnacarta',
          title: 'What is the Magna Carta?',
          choicesOrder: 'random',
          choices: [
            'The foundation of the British parliamentary system',
            'The Great Seal of the monarchs of England',
            'The French Declaration of the Rights of Man',
            'The charter signed by the Pilgrims on the Mayflower',
          ],
          correctAnswer: 'The foundation of the British parliamentary system',
        },
      ],
    },
  ],
  completedHtml:
    '<h4>You have answered correctly <b>{correctedAnswers}</b> questions from <b>{questionCount}</b>.</h4>',
};
window.survey = new Survey.Model(json);

survey.onComplete.add(function(result) {
  document.querySelector('#surveyResult').innerHTML =
    'result: ' + JSON.stringify(result.data);
  console.log(result.data);

  $.post('/bestcollege/submit_survey', JSON.stringify(result.data), function(
    raw_data
  ) {
    var uni_ids = JSON.parse(raw_data);
    console.log(uni_ids);
    var url_params = '';
    for (var i = 0; i < uni_ids.length; i++) {
      url_params += uni_ids[i] + ',';
    }

    url_params = url_params.substring(0, url_params.length - 1);
    window.location.replace('results/?ids=' + url_params);
  });
});

$('#surveyElement').Survey({ model: survey });
