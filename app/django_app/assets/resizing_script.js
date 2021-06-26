if (!window.dash_clientside) {
  window.dash_clientside = {};
}
window.dash_clientside.clientside = {
  resize: function(value) {
    console.log("resizing..."); // for testing
    setTimeout(function() {
      window.dispatchEvent(new Event("resize"));
      console.log("fired resize");
    }, 5);
    return null;
  }
};


// $(document).on('shown.bs.tab', 'a[data-toggle="tab"]', function (event) {
//   var doc = $(".tab-pane.active .plotly-graph-div");
//   for (var i = 0; i < doc.length; i++) {
//       Plotly.relayout(doc[i], {autosize: true});
//   }
// })