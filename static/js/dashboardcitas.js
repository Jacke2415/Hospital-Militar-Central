function validaciondashboardcitas() {
  var idcita = document.dashboardcitas.idcita.value;
  var idpaciente=document.dashboardcitas.idPaciente.value;
  var idmedico=document.dashboardcitas.idMedico.value;
  
  if (idcita.length==0 &&  idpaciente.length==0 && idmedico.length==0){
    alert("Debes Ingresar algun parametro de busqueda")
    
  }else{
    if (idcita.length>0  &&  !(/^\d{0,10}$/.test(idcita) || /^\s+$/.test(idcita))) {
      alert("Debes ingresar un id de cita Valido")
      return false;
    }
  
    if (idpaciente.length>0  && !(/^\d{8,10}$/.test(idpaciente) || /^\s+$/.test(idpaciente))) {
      alert("Debes ingresar una identificacion del Paciente Valida")
      return false;
    }
  
    if (idmedico.length>0  && !(/^\d{8,10}$/.test(idmedico) || /^\s+$/.test(idmedico))) {
      alert("Debes ingresar una identificacion del Medico Valida");
      return false;
    }

  }

}  

function validaciondashboardmedico(){
  var cedula = document.dasboardMedico.cedula.value;
  var nombre=document.dasboardMedico.nombre.value;
  var especialidad=document.dasboardMedico.especialidad.value;
  
  if (cedula.length==0 &&  nombre.length==0 && especialidad.length==0){
    alert("Debes Ingresar algun parametro de busqueda")
    
  }else{
    if (cedula.length>0  && !(/^\d{8,10}$/.test(cedula) || /^\s+$/.test(cedula))) {
      alert("Debes ingresar una identificacion del Medico Valida")
      return false;
    }
    
    if (nombre.length>0  && !(/^[a-zA-Z ]+$/.test(nombre) || /^\s+$/.test(nombre))) {
      alert("Debes ingresar un Nombre Valido")
      return false;
    }
    
    if (especialidad.length>0  && !(/^[a-zA-Z]+$/.test(especialidad) || /^\s+$/.test(especialidad))) {
      alert("Debes ingresar una Especialidad Valida: Cardiologia,General,Pediatria...");
      return false;
    }

  }


} 
    