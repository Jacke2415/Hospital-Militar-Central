function validarfecha() {
    var fechainicial = document.getElementById("fechai").value;
    var fechafinal=document.getElementById("fechaf").value;
    
 
    
    if (fechainicial>fechafinal){
      alert("Ingresar una Fecha Inicial Valida, La Fecha Inicial no Puede ser Mayor a la Fecha Final")
    } 
   
}  
  
function habilitarinputs(){
  document.getElementById('fecha').disabled=false
  document.getElementById('hora').disabled=false
  
 
} 