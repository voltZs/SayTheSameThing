function poll() {

queryString = "state="+JSON.stringify(currentState);

$.ajax({
    url:"/poll",
    data: queryString,
    timeout: 60000,
    success: function(data) {
        console.log(data);
        if(currentState == null) {
            currentState = JSON.parse(data);
        }
        else {
            console.log("A change has occurred");
        }

        poll();

    },
    error: function(jqXHR, textStatus, errorThrown) {

        console.log(jqXHR.status + "," + textStatus + ", " + errorThrown);

        poll();

    }
});

}
