
//const form = document.getElementById("analyse");
//form.addEventListener("submit", analyseHandler);
var bar = $('#progressbar>div')

function analyseHandler() {
    $("div.loader").css("display", "block");
    $('#progress_shower').css("display", "block");
    $.ajax({
        type: 'POST',
        url: '/do_analysis/',
        dataType: 'json',

        data: {
            path: $("#pth").val(),

        },
        success : function(data) {
            console.log(data['pro']);  

            check_progress();
         }
    });

}



function updateBar(val)
{
 bar.css('width',val+'% ');
 bar.text(val+"%"); 
}

function check_progress(){


    $.ajax({
        type : 'GET',
        url : '/do_analysis/',
        dataType: 'json',

        success : function(data) {

          updateBar(data['pro'])
          if(data['pro']<100)
          {
            setTimeout(function () {
                check_progress();
                }, 5000);       

          }
          else
          {
            setTimeout(function(){
            $.get('/analysis',async=false,function(data){
                location.reload()
            });
            // Simulate an HTTP redirect:
            //window.location.replace("http://127");    
            
            }, 1000);       
          }
    }
    
});
}