function validarRegistro() {
    
    var nombre = document.formularioRegistro.nombre.value;
    var apellido = document.formularioRegistro.apellido.value;
    var fechaN = document.formularioRegistro.fechaN;
    var cedula = document.formularioRegistro.cedula;
    var password = document.formularioRegistro.password.value;
    var password1 = document.formularioRegistro.passwordC.value;
    var opcionr = document.formularioRegistro.condicionesr;
    var opcionesRadio = document.formularioRegistro.tipoId;
    var lista = document.formularioRegistro.sexo;
    var dir = document.formularioRegistro.direccion.value;
    var tel = document.formularioRegistro.telefono.value;
    var email = document.formularioRegistro.correo;
    
    if(nombre == null || nombre.length < 2 || /^\s+$/.test(nombre)){
        swal.fire({
            title:"ERROR",
            text:"Se debe ingresar un nombre valido",
            icon:"error",
            confirmButtonText:"continuar",
        });
        return false;
    }

    if(apellido == null || apellido.length < 2 || /^\s+$/.test(apellido)){
        swal.fire({
            title:"ERROR",
            text:"Se debe ingresar un apellido valido",
            icon:"error",
            confirmButtonText:"continuar",
        });
        return false;
    }

    if(fechaN == null){
        swal.fire({
            title:"ERROR",
            text:"Se debe seleccionar una fecha valido",
            icon:"error",
            confirmButtonText:"continuar",
        });
        return false;
    }

    if(lista.selectedIndex == null || lista.selectedIndex == 0){
        swal.fire({
            title:"ERROR",
            text:"Debes seleccionar tu sexo",
            icon:"error",
            confirmButtonText:"continuar",
        });
        return false;
    }
        
    var pulsado = false;
    var elegido = -1;
    for(i = 0; i < opcionesRadio.length; i++){
        if(opcionesRadio[i].checked == true){
            pulsado = true;
            elegido = i;
        }
    }
    if (pulsado == true){
        miOpcion = opcionesRadio[elegido].value
        /*alert("has elegido la opción: " + miOpcion + 
        "\n es correcto?")*/
    }
    else{
        swal.fire({
            title:"ERROR",
            text:"No has elegido ninguna opción de tipo de documento",
            icon:"error",
            confirmButtonText:"continuar",
        });
        return false
    }

    var cedula_len = cedula.value.length;
    if(cedula_len < 8 || cedula_len > 10 || isNaN(cedula.value)){
        swal.fire({
            title:"ERROR",
            text:"Se debe ingresar un número de identificación valido",
            icon:"error",
            confirmButtonText:"continuar",
        });
        return false;
    }

    if(dir == null || dir.length < 2 || /^\s+$/.test(dir)){
        swal.fire({
            title:"ERROR",
            text:"Se debe ingresar una dirección valida",
            icon:"error",
            confirmButtonText:"continuar",
        });
        return false;
    }

    if(!(/^\d{10}$/.test(tel)) && !(/^\d{1}\s\d{7}$/.test(tel))){
        swal.fire({
            title:"ERROR",
            text:"Se debe ingresar un número de teléfono valido",
            icon:"error",
            confirmButtonText:"continuar",
        });
        return false;
    }

    var formato_email = /^[-\w.%+]{1,64}@(?:[A-Z0-9-]{1,63}\.){1,125}[A-Z]{2,63}$/i;
    if (!email.value.match(formato_email)){
        swal.fire({
            title:"ERROR",
            text:"Se debe ingresar un email con formato válido",
            icon:"error",
            confirmButtonText:"continuar",
        });
        return false;
    }

    if(password.length < 8){
        swal.fire({
            title:"ERROR",
            text:"Se debe ingresar un password con mas de 8 carateres",
            icon:"error",
            confirmButtonText:"continuar",
        });
        return false;
    }
    if (password != password1){
        swal.fire({
            title:"ERROR",
            text:"Las contraseñas deben coincidir",
            icon:"error",
            confirmButtonText:"continuar",
        });
        return false
    }
    
    if (opcionr.checked == true){
        swal.fire({
            text:"tu registro ha sido exitoso",
            icon:"success",
            confirmButtonText:"continuar",
        });
    }
    else{
        swal.fire({
            title:"ERROR",
            text:"Debes aceptar nuestras politicas de privacidad",
            icon:"error",
            confirmButtonText:"continuar",
        });
        return false
    }
    
}

function validarLogin(){

    var cedula = document.formularioLogin.cedula.value;
    var password = document.formularioLogin.password.value;
    var opcion = document.formularioLogin.condiciones;

    if(cedula.length < 8 || cedula.length > 10 || isNaN(cedula)){
        alert('Se debe ingresar un número de identificación valido')
        /*swal.fire({
            title:"ERROR",
            text:"Se debe ingresar un número de identificación valido",
            icon:"error",
            confirmButtonText:"continuar",
        });*/        
        return false;
    }

    if(password.length < 8){
        /*swal.fire({
            title:"ERROR",
            text:"Se debe ingresar un password con mas de 8 carateres",
            icon:"error",
            confirmButtonText:"continuar",
        });*/
        alert('Se debe ingresar un password con mas de 8 carateres')
        return false
    }

    if (opcion.checked == false){
        /*swal.fire({
            title:"ERROR",
            text:"Debes aceptar nuestras politicas de privacidad",
            icon:"error",
            confirmButtonText:"continuar",
        });*/
        alert('Debes aceptar nuestras politicas de privacidad')
        return false;        
    }
}