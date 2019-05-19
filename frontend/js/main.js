var pos = [];
var neg = [];
$.ajax({
    type: "GET",
    url: "http://localhost:5000/positive_tweets",
    cache: false,
    crossDomain: true,
    success: function(data){
      //$("#results").append(html);
        console.log(data);
        pos = data;
        fillPositives(data);
    }
});

$.ajax({
    type: "GET",
    url: "http://localhost:5000/negative_tweets",
    cache: false,
    crossDomain: true,
    success: function(data){
      //$("#results").append(html);
        console.log(data);
        neg = data;
        fillNegatives(data);
        drawChart();
    }
});
 
function fillPositives(data) {
   // data.slice(Math.max(data.length - 5, 1))
    var items = [];
    data.forEach(element => {
              
        items.push('<li class="list-group-item list-group-item-success">' + element + '</li>');0
    });
    $('#positives').append(items.join(''));
}

function fillNegatives(data) {
  //  data.slice(Math.max(data.length - 5, 1))
    var items = [];
    data.forEach(element => {
              
        items.push('<li class="list-group-item list-group-item-danger">' + element + '</li>');0
    });
    $('#negatives').append(items.join(''));
}

function drawChart() {
         
    var ctx = $('#myChart');

    data = {
        datasets: [{
            data: [pos.length, neg.length],
            backgroundColor: ["#2ECC40","#FF4136"]
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
            'Positive tweets',
            'Negative tweets',
        ]
    };

    var options = Chart.defaults.doughnut;
    options.responsive = true;
    options.maintainAspectRatio = false;
    var myDoughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: options
    });
}