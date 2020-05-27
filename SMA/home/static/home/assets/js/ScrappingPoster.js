
const form = document.getElementById("scraper");
form.addEventListener("submit", scrapHandler);

function scrapHandler() {
    //var formData = new FormData(document.querySelector('scraper'))
    $('div.loader').css('display', 'block');
    $.ajax({
        type: 'POST',
        url: "{% url 'scrapping' %}",
        dataType: 'json',

        

        success: function(data) {
            alert("Success");
        }
    });

}