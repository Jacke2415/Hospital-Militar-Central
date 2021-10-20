// Para hacer la busqueda
let noticia1 = "El programa de cardiologia del Hospital X entre los mejores del Pais" + "Doctor Hernando Pulido y Sonia Fonseca" + "Segun el Ministerio de Salud, los diez mejores programas de cardiologia de Colombia, en lo corrido del trimestre ya habrian sido escogidos.Luego de muchos informes se mostro que la atencion al Usuario, la respuesta a emergencia, entre otros factores sirvieron para ordenar el ranking.Segun el Ministerio de Salud, los diez mejores programas de cardiologia de Colombia, en lo corrido del trimestre ya habrian sido escogidos.Luego de muchos informes se mostro que la atencion al Usuario, la respuesta a emergencia, entre otros factores sirvieron para ordenar el ranking."

let noticia2 = "Curso de Buenas Prácticas Clínicas 2021" + "Doctor Pedro Maestre y Sonia Mercado" +  "Entre los temas que se tratarán en este espacio académico están: Ética de la investigación en seres humanos, Fundamento legal BPC, ¿Existen los biobancos? ¿Qué hay en ellos?, Bioética en modelos animales, consentimiento informado, manejo ético en bases de datos, ¿Qué es la necroética en investigación? e investigación en Pediatría, entre otros."

let noticia3 = "Clínicas HOMIL" + "Doctor Pedro Maestre y Sonia Mercado" +  "Las clínicas son grupos de varios profesionales que trabajan articuladamente para mejorar la calidad de vida, disminuir las complicaciones y optimizar los recursos de atención para los pacientes adultos usuarios del Subsistema de Salud de las Fuerzas Militares con diagnóstico de enfermedades crónicas.Los pacientes para el ingreso a las clínicas deben ser remitidos de su sitio de atención primaria (Dispensarios), algunos serán valorados y retornarán a su dispensario y otros permanecerán en las clínicas hasta la estabilización y control de su patología. En las clínicas se cuenta con la atención de un médico especialista y/o supra especialista, una enfermera jefa y una nutricionista. Es posible contar con otros profesionales como terapistas, psicólogos según las necesidades de los pacientes."
// vector de noticias
let noticias = [noticia1,noticia2,noticia3];


//Noticias en forma de html sha

let noticia1HTML = `<div class="result">
<div class="result-text">
    <h1> El programa de cardiologia del Hospital X entre los mejores del Pais
    </h1>
    <p>Segun el Ministerio de Salud, los diez mejores programas de cardiologia de Colombia, en lo
        corrido del trimestre ya habrian sido escogidos. Luego de muchos informes se mostro que la
        atencion al Usuario, la respuesta a emergencia, entre otros factores sirvieron para ordenar
        el ranking. Segun el Ministerio de Salud, los diez mejores programas de cardiologia de
        Colombia, en lo corrido del trimestre ya habrian sido escogidos. Luego de muchos informes se
        mostro que la atencion al Usuario, la respuesta a emergencia, entre otros factores sirvieron
        para ordenar el ranking.<a href="notiica.html">[Ver mas]</a></p>
</div>
<div class="result-img">
    <img src="{{url_for('static', filename = 'galeria.jpeg')}}" alt="Prueba">
</div>
</div>`;

let noticia2HTML = `<div class="result">
<div class="result-text">
    <h1> Curso de Buenas Prácticas Clínicas 2021
    </h1>
    <p>Entre los temas que se tratarán en este espacio académico están: Ética de la investigación en seres humanos, Fundamento legal BPC, ¿Existen los biobancos? ¿Qué hay en ellos?, Bioética en modelos animales, consentimiento informado, manejo ético en bases de datos, ¿Qué es la necroética en investigación? e investigación en Pediatría, entre otros.<a href="notiica.html">[Ver mas]</a></p>
</div>
<div class="result-img">
    <img src="{{url_for('static', filename = '/img/noticia2.jpg')}}" alt="Image">
</div>
</div>`;

let noticia3HTML = `<div class="result">
<div class="result-text">
    <h1> Clínicas HOMIL
    </h1>
    <p>Las clínicas son grupos de varios profesionales que trabajan articuladamente para mejorar la calidad de vida, disminuir las complicaciones y optimizar los recursos de atención para los pacientes adultos usuarios del Subsistema de Salud de las Fuerzas Militares con diagnóstico de enfermedades crónicas.Los pacientes para el ingreso a las clínicas deben ser remitidos de su sitio de atención primaria (Dispensarios), algunos serán valorados y retornarán a su dispensario y otros permanecerán en las clínicas hasta la estabilización y control de su patología. En las clínicas se cuenta con la atención de un médico especialista y/o supra especialista, una enfermera jefa y una nutricionista. Es posible contar con otros profesionales como terapistas, psicólogos según las necesidades de los pacientes.<a href="notiica.html">[Ver mas]</a></p>
</div>
<div class="result-img">
    <img src="{{url_for('static', filename = '/img/noticia3.jpg')}}" alt="Image">
</div>
</div>`;
let noticiasHTML = [noticia1HTML,noticia2HTML,noticia3HTML];

let noResultsFound = `<div class="noMatches">
<h1>Lo sentimos, no encotramos un coincidencia a tu busqueda.</h1>
<img src="./img/noResults.png" alt="Sin resultados">
</div>`

function resaltarPalabra(entradaHTML,entrada){
    let salidaHTML = ""
    let caracteres = entradaHTML.split(" ");
    for (let i = 0; i < caracteres.length;i++) {
        if(entrada == caracteres[i]){
            salidaHTML = salidaHTML + "<span class='resaltado'>"+ caracteres[i] + "</span>" + " ";
        }else{
            salidaHTML = salidaHTML +  caracteres[i] + " ";
        }
    }
    return salidaHTML;
}


function agregarNoticia(contenido) {
    document.getElementById("respuesta").innerHTML = contenido;
}
// Pendiente agregar enter para poder realizar la busqueda
// var input = document.getElementById("busqueda");
// input.addEventListener("keyup", function(event) {
//   if (KeyboardEvent.keyCode === 13) {
//    event.preventDefault();
//    document.getElementById("search-b").click();
//   }
// });
function realizarBusqueda(){
    //document.getElementById("respuesta").innerHTML = "";
    let matches = 0;
    let entrada = document.getElementById("busqueda").value;
    for(let i=0;i<noticias.length;i++){
        if(noticias[i].includes(entrada)){
            agregarNoticia(resaltarPalabra(noticiasHTML[i],entrada));
            matches++;
        }
    }
    if (matches==0){
        agregarNoticia(noResultsFound);
    }
}