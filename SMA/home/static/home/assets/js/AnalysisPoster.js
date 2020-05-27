
const form = document.getElementById("analyse");
form.addEventListener("submit", analyseHandler);

function analyseHandler(e) {
    $("div.loader").css("display", "block");
    $.ajax({
        type: 'POST',
        url: "{% url 'analysis' %}",
        dataType: 'json',

        data: {
            path: $("#pth").val(),

        },
        success: function(data) {
            alert("Success");
        }
    });

}