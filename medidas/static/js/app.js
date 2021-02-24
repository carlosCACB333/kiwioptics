
function get_patient( url){
// obtiene los datos de una persona con la api rest-framewowrk
    $.ajax({
        type: "GET",
        // url: "/app/api/patients/"+id+"/?format=json",
        url: url,
        dataType: "json",
        success: function (data) {
            console.log(data)
             dato=data
            $("#id_patient").val(data.id)
            $("#id_full_name").val(data.full_name)
            $("#id_dni").val(data.dni)
            $("#id_gender").val(data.gender)
            $("#id_phone").val(data.phone)
            $("#id_job").val(data.job)
        }, //End of AJAX Success function
    });
}



function update_patient(){
    id_patient=$("#id_patient").val()
    datos=$("#prescription_form").serialize()
    console.log(datos)
     url="/app/api/patientUpdate/"+$("#id_patient").val()+"/"

    $.ajax({
        type: "PUT",
        // url: "/app/api/patients/"+id+"/?format=json",
        url: url,
        data:datos,
        dataType: "json",
        success: function (data) {
        location.reload()
        }, //End of AJAX Success function
    }).fail(function(e){
    console.log(e.message)
    });

}

function delete_patient(){
  url="/app/api/patientDelete/"+$("#id_patient").val()+"/"
 $.ajax({
        type: "DELETE",
        // url: "/app/api/patients/"+id+"/?format=json",
        url: url,
        dataType: "json",
        success: function (data) {
        location.reload()
            console.log(data)

        }, //End of AJAX Success function
    }).fail(function(e){
    console.log(e.message)
    });
}
