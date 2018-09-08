var staff_id = null;
//
$(document).ready(function(){
    $("#score-selector").hide();

    $("#staff-selector").submit(function (e){
        e.preventDefault();
        alert("Starting Session For: " +$("#staff-id-input").val());
        staff_id = $("#staff-id-input").val();
        console.log(staff_id);
        $(this).hide()
        $("#score-selector").show();
    })

    $(".rating-button").click(function() {
        alert("Thank you for feedback");
    })

})