myChart=null
tipo='line'
function graficar(labels,data){
    var canvas = document.getElementById('prescripciones').getContext('2d');
    const config = {
        type: tipo,
        data: {
            labels: labels,
            datasets: [{
                label: 'Prescripciones',
                data: data,
                backgroundColor: 'rgba(0, 123, 255, .5)',
                borderColor: 'rgba(0, 123, 255, .5)',
                // rgba(0, 123, 255, .1)
                borderWidth: 3,
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

const SEMANAS=['lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'];
const MESES=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre','Octubre','Noviembre','Diciembre']

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
            // response_data.data.forEach(function(item,index){
               
            //     if (response_data.options.label=='Semana'){
            //         labels.push( SEMANAS[item.dato-1])
            //         data.push(item.total)
            //     }else{
            //         labels.push(item.dato)
            //         data.push(item.total)
            //     }
            // });

            contador=0;
            for (let i=1;i<=response_data.options.size;++i){
                if (response_data.data[contador] != undefined && response_data.data[contador].dato==i){
                    data.push(response_data.data[contador].total)
                    contador++;
                }else{
                    data.push(0)
                }
                    
                if (response_data.options.label=='Semana'){
                    labels.push( SEMANAS[i-1]);  
                }else if(response_data.options.label=='Mes'){
                    if(i<10){
                        labels.push('0'+i);  
                    } else{
                        labels.push(i);  
                    }
                }else if(response_data.options.label=='Año'){
                    labels.push( MESES[i-1]); 
                }else if (response_data.options.label=='Dia'){
                    labels.push(i+"h");
                }
                
            }
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

