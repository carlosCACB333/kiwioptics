myChart=null;
charSucursal=null;
tipo='line'
charSucursalType='bar';
function graficar(labels,datasets,canvas,type){
    const config = {
        type: type,
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
            responsive: true,
        
        }
    };
    let grafica = new Chart(canvas,config);
    return grafica;
}





const SEMANAS=['lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'];
const MESES=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Set','Oct','Nov','Dic']

// GRAFICA DE REPORTE DE PRESCRIPCIONES POR FECHAS
function char_prescriptions(url){
  
    $.ajax({
        type: "GET",        
        url: url,
        dataType: "json",
        success: function(response_data) {
        // console.log(response_data)
        let labels=[]
        let data=[]
        let contador=0;
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
        let gradientStroke=gradient_color(canva,"#448AFF","#00BCD4","#1DE9B6","#8EEEEE");
        let datasets=[{
            label: 'PRescripciones',
            data: data,
            backgroundColor: gradientStroke,
            borderColor: gradientStroke,
            pointBorderColor: gradientStroke,
            pointBackgroundColor: gradientStroke,
            pointHoverBackgroundColor: gradientStroke,
            pointHoverBorderColor: gradientStroke,
            borderWidth: 3,
            
        }];
        myChart= graficar(labels,datasets,canva,tipo)                
        
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

function gradient_color(ctx,firstColour,secondColour,thirdColour,fourthColour){
    let width = window.innerWidth || document.body.clientWidth;
    let  gradientStroke = ctx.createLinearGradient(0, 0, width, 0);
    gradientStroke.addColorStop(0, firstColour);
    gradientStroke.addColorStop(0.3, secondColour);
    gradientStroke.addColorStop(0.6, thirdColour);
    gradientStroke.addColorStop(1, fourthColour);
    return gradientStroke;
    }



$(document).ready(function(){
    let calendar=$('#radio-calendar input:radio[name=calendar]:checked').val();
    let url=$("#url_rest_patient_list").val()+'?calendar='+calendar;
    char_prescriptions(url);


    //sucursales
    let calendar2=$('#subsidiary_radio_calendar input:radio[name=calendar2]:checked').val();
    let url2=$("#url_rest_subsidiary_prescription").val()+'?calendar='+calendar2;
    char_subsidiary_prescriptions(url2);

    
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
function char_subsidiary_prescriptions(url){
  
    $.ajax({
        type: "GET",        
        url: url,
        dataType: "json",
        success: function(response_data) {

            console.log(response_data)
            let labels=[]
            let sucursales=[];
            let grupo_data=[];
            $.each(response_data.options.subsididiary, function( index, value ) {
                if(value.subsidiary__subsidiary_name!=null){
                    sucursales.push(value.subsidiary__subsidiary_name)
                }else{
                    sucursales.push('Desconocido')
                }
                grupo_data.push([])
            });

            $.each(grupo_data, function( index, value ) {
                value.length=response_data.options.size   
                value.fill(0,0,response_data.options.size)
            });

            console.log(sucursales)


            for (let i=1;i<=response_data.options.size;++i){
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

       
      

        
        $.each(response_data.data, function( index, value ) {
            console.log(value)
            mi_indice=sucursales.indexOf(value.subsidiary.subsidiary_name);
            console.log(value.total)
            grupo_data[mi_indice][value.dato-1]=value.total
        });

        console.log(grupo_data)

       
        let datsets=[]
        $.each(grupo_data, function( index, value ) {
            let color=colorRGB();
            let datos={
                label: sucursales[index],
                data: value,
                backgroundColor: color,// Color de fondo
                borderColor:color,// Color del borde
                borderWidth: .5,// Ancho del borde
            }
            datsets.push(datos);
        });

        console.log(datsets)
        console.log(labels)

        let canva=document.getElementById('subsidiary').getContext('2d');
        if (charSucursal!=null){
            charSucursal.destroy();
        }

        charSucursal= graficar(labels,datsets,canva,charSucursalType)                
        
        $("#subsidiary_current").val(response_data.options.current)
        $("#subsidiary_current_year").val(response_data.options.current_year)
        $("#subsidiary_current_month").val(response_data.options.current_month)
        
        if($("#subsidiary_current_year").val().length==0){
            $("#subsidiary_current_year").hide()
        }else{
            $("#subsidiary_current_year").show()
        }
        if($("#subsidiary_current_month").val().length==0){
            $("#subsidiary_current_month").hide()
        }else{
            $("#subsidiary_current_month").show()
        }
        }, //End of AJAX Success function
    });
    
}

$("#subsidiary_radio_calendar input").on("click", function(){

    let calendar=this.value;
    let url=$("#url_rest_subsidiary_prescription").val()+'?calendar='+calendar;
    char_subsidiary_prescriptions(url);
});

$("#subsidiary_previus").click(function(){
    let calendar=$('input:radio[name=calendar2]:checked').val();
    let current= $("#subsidiary_current").val();
    let current_year= $("#subsidiary_current_year").val();
    let url=$("#url_rest_subsidiary_prescription").val()+'?calendar='+calendar+'&option=previus&current='+current+'&current_year='+current_year+'&current_month='+$("#subsidiary_current_month").val();
    char_subsidiary_prescriptions(url);
})
$("#subsidiary_next").click(function(){
    let calendar=$('input:radio[name=calendar2]:checked').val();
    let current= $("#subsidiary_current").val();
    let current_year= $("#subsidiary_current_year").val();
    let url=$("#url_rest_subsidiary_prescription").val()+'?calendar='+calendar+'&option=next&current='+current+'&current_year='+current_year+'&current_month='+$("#subsidiary_current_month").val();
    char_subsidiary_prescriptions(url);
})


// ra

function generarNumero(numero){
	return (Math.random()*numero).toFixed(0);
}

function colorRGB(){
	var coolor = "("+generarNumero(255)+"," + generarNumero(255) + "," + generarNumero(255) +")";
	return "rgb" + coolor;
}