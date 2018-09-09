let staff_id = null;
//
$(document).ready(function(){
    $("#score-selector").hide();

    $("#staff-selector").submit(function (e){
        e.preventDefault();
        alert("Starting Session For: " +$("#staff-id-input").val());
        staff_id = $("#staff-id-input").val();
        $(this).hide()
        $("#score-selector").show();
    })

    $(".rating-button").click(function() {
        alert("Thank you for feedback");
        let selected_score_button = $(this).attr("id");
        let score = selected_score_button[4];
        let time = new Date();
        let hour = time.getHours();

        let xhr = new XMLHttpRequest();
        xhr.open("POST", "http://127.0.0.1:7643/staffscore", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify(
            {"report":{ "name": staff_id, "score":score, "time":hour}}
        ));
    })

})