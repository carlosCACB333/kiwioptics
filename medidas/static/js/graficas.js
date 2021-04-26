myChart=null;
charSucursal=null;
tipo='line'
charSucursalType='line';
function graficar(labels,datasets,canvas){
    const config = {
        type: tipo,
        data: {
            labels: labels,
            datasets: datasets
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
    let grafica = new Chart(canvas,config);
    return grafica;
}





const SEMANAS=['lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'];
const MESES=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre','Octubre','Noviembre','Diciembre']

// GRAFICA DE REPORTE DE PRESCRIPCIONES POR FECHAS
function char_prescriptions(url){
  
    $.ajax({
        type: "GET",        
        url: url,
        dataType: "json",
        success: function(response_data) {
        console.log(response_data)
        let labels=[]
        let data=[]
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
        let canva=document.getElementById('prescripciones').getContext('2d');
        if (myChart!=null){
            myChart.destroy();
        }

        let datasets=[{
            label: 'PRescripciones',
            data: data,
            backgroundColor: 'rgba(0, 123, 255, .5)',
            borderColor: 'rgba(0, 123, 255, .5)',
            borderWidth: 3,
        }];
        myChart= graficar(labels,datasets,canva)                
        
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
    char_prescriptions(url);


    //sucursales
    const etiquetas = ["Enero", "Febrero", "Marzo", "Abril"]
    const const1 = {
        label: "sucursal norte",
        data: [5000, 1500, 8000, 5102], // La data es un arreglo que debe tener la misma cantidad de valores que la cantidad de etiquetas
        backgroundColor: 'rgba(54, 162, 235, 0.2)', // Color de fondo
        borderColor: 'rgba(54, 162, 235, 1)', // Color del borde
        borderWidth: 1,// Ancho del borde
    };
    const const2 = {
        label: "sucursal gozu",
        data: [10000, 1700, 5000, 5989], // La data es un arreglo que debe tener la misma cantidad de valores que la cantidad de etiquetas
        backgroundColor: 'rgba(255, 159, 64, 0.2)',// Color de fondo
        borderColor: 'rgba(255, 159, 64, 1)',// Color del borde
        borderWidth: 1,// Ancho del borde
    };
    const const3 = {
        label: "sucursal sur",
        data: [3000, 2500, 9000, 10582], // La data es un arreglo que debe tener la misma cantidad de valores que la cantidad de etiquetas
        backgroundColor: 'rgba(255, 159, 64, 0.2)',// Color de fondo
        borderColor: 'rgba(25, 19, 64, 1)',// Color del borde
        borderWidth: 1,// Ancho del borde
    };
    const const4= {
        label: "sucursal ra",
        data: [2563, 5281, 9635, 4526], // La data es un arreglo que debe tener la misma cantidad de valores que la cantidad de etiquetas
        backgroundColor: 'rgba(54, 162, 235, 0.2)', // Color de fondo
        borderColor: 'rgba(54, 162, 235, 1)', // Color del borde
        borderWidth: 1,// Ancho del borde
    };
   
    let canva=document.getElementById('subsidiary').getContext('2d');
    graficar(etiquetas,[const1,const2,const3,const4],canva    )
});

$("#radio-calendar input").on("click", function(){
    // alert("Value is " + this.value);
    // alert($('input:radio[name=calendar]:checked').val());
    let calendar=this.value;
    let url=$("#url_rest_patient_list").val()+'?calendar='+calendar;
    char_prescriptions(url);

});

$("#id_previus").click(function(){
    let calendar=$('input:radio[name=calendar]:checked').val();
    let current= $("#id_current").val();
    let current_year= $("#id_current_year").val();
    let url=$("#url_rest_patient_list").val()+'?calendar='+calendar+'&option=previus&current='+current+'&current_year='+current_year+'&current_month='+$("#id_current_month").val();
    char_prescriptions(url);
})
$("#id_next").click(function(){
    let calendar=$('input:radio[name=calendar]:checked').val();
    let current= $("#id_current").val();
    let current_year= $("#id_current_year").val();
    let url=$("#url_rest_patient_list").val()+'?calendar='+calendar+'&option=next&current='+current+'&current_year='+current_year+'&current_month='+$("#id_current_month").val();
    char_prescriptions(url);
})

// GRAFICA DE SUCURSALES Y LA CANTIDAD DE PRESCRIPCIONES POR FECHAS

$("#subsidiary_radio_calendar input").on("click", function(){
    alert("Value is " + this.value);
    // alert($('input:radio[name=calendar]:checked').val());
    // let calendar=this.value;
    // let url=$("#url_rest_patient_list").val()+'?calendar='+calendar;
    // char_prescriptions(url);

});