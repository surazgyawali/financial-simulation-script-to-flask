function gameStart(){
    alert("The game is going to start!")

$('#next').click(function(){
    $('#welcome').addClass("d-none")
    $('#intro').removeClass("d-none")
})

$('#gameStart').click(function () {
    ajax_fetch()
})

function ajax_fetch() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var response = this.responseText;
            $('html').html(response);
        }
    };
    xhttp.open(
        method = "POST",
        url = "/game",
        true
    );
    xhttp.send();
}