function update_patient(id, url){
    $(document).ready(function () {
        $.ajax({
            type: "GET",
            // url: "/app/api/patients/"+id+"/?format=json",
            url: url,
            dataType: "json",
            success: function (data) {
                console.log(data)
                $("#id_first_name").val(data[0].first_name)
                $("#id_last_name").val(data[0].last_name)
                $("#id_dni").val(data[0].dni)
                $("#id_gender").val(data[0].gender)
                $("#id_phone").val(data[0].phone)
                $("#id_job").val(data[0].job)
            }, //End of AJAX Success function
        });
    });
}
