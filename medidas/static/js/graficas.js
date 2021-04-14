myChart=null
function graficar(labels,data){
    var canvas = document.getElementById('prescripciones').getContext('2d');
    const config = {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Reporte prescripciones',
                data: data,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgb(75, 192, 192)',
                borderWidth: 3,
                borderColor: 'rgb(75, 192, 192)',
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true
        }
    };
    if (myChart!=null){
        myChart.destroy();
    }
    myChart = new Chart(canvas,config);
}



// ajax y obteer datos
$("#radio-calendar input").on("click", function(){
    // alert("Value is " + this.value);
    // alert($('input:radio[name=calendar]:checked').val());
    let calendar=this.value;
    let url=$("#url_rest_patient_list").val()+'?calendar='+calendar;
    get_data(url)

});

function get_data(url) {
    // obtener datos  con la api rest-framewowrk
    $.ajax({
        type: "GET",
        // url: "/app/api/patients/"+id+"/?format=json",
        url: url,
        dataType: "json",
        success: function(response_data) {
            console.log(response_data)
            ra=response_data
            let labels=[]
            let data=[]
            response_data.data.forEach(function(item,index){
                labels.push(item.dato+'° ' +response_data.options.label)
                data.push(item.total)
            });
            graficar(labels,data)
            $("#id_current").val(response_data.options.current)
            $("#id_current_year").val(response_data.options.current_year)
            $("#id_current_month").val(response_data.options.current_month)
            
            if($("#id_current_year").val().length==0){
                $("#id_current_year").hide()
            }else{
                $("#id_current_year").show()
            }
            if($("#id_current_month").val().length==0){
                $("#id_current_month").hide()
            }else{
                $("#id_current_month").show()
            }
        }, //End of AJAX Success function
    });


}

$(document).ready(function(){
    let calendar=$('input:radio[name=calendar]:checked').val();
    let url=$("#url_rest_patient_list").val()+'?calendar='+calendar;
    get_data(url);
});

$("#id_previus").click(function(){
    let calendar=$('input:radio[name=calendar]:checked').val();
    let current= $("#id_current").val();
    let current_year= $("#id_current_year").val();
    let url=$("#url_rest_patient_list").val()+'?calendar='+calendar+'&option=previus&current='+current+'&current_year='+current_year+'&current_month='+$("#id_current_month").val();
    get_data(url);
})
$("#id_next").click(function(){
    let calendar=$('input:radio[name=calendar]:checked').val();
    let current= $("#id_current").val();
    let current_year= $("#id_current_year").val();
    let url=$("#url_rest_patient_list").val()+'?calendar='+calendar+'&option=next&current='+current+'&current_year='+current_year+'&current_month='+$("#id_current_month").val();
    get_data(url);
})

