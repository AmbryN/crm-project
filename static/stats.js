// When the page is entirely loaded
window.addEventListener("load", function() {
    var canvas = document.getElementById("mychart").getContext("2d");
    var offers = Number(document.getElementById("offers").textContent);
    var orders = Number(document.getElementById("orders").textContent);
    
    if (offers > 0){
        // Create a pie chart with Chart.js
        var myChart = new Chart(canvas, {
            type: 'pie',
            data: {
                labels: ["Offers", "Orders"],
                datasets: [{
                    label: "Number",
                    data: [offers, orders],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255,99,132,1)',
                        'rgba(54, 162, 235, 1)',
                    ],
                    borderWidth: 1
                }]
            }
        });
    }
});
