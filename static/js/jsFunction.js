let eyeiconPasswd = document.getElementById('eye-password');
let password = document.getElementById('passwd');
let eyeiconCpasswd = document.getElementById('eye-cpass');
let cpassword = document.getElementById('Cpasswd');

eyeiconPasswd.onclick = function(){
    if(password.value.length){
        if(password.type == "password"){
            password.setAttribute("type","text");
            eyeiconPasswd.classList.remove("fa-eye-slash"); 
            eyeiconPasswd.classList.add("fa-eye")
        }else{
            password.setAttribute("type","password");
            eyeiconPasswd.classList.remove("fa-eye"); 
            eyeiconPasswd.classList.add("fa-eye-slash")
        }
    }
}

try {
eyeiconCpasswd.onclick = function(){
    if(cpassword.value.length){
        if(cpassword.type == "password"){
            cpassword.setAttribute("type","text");
            eyeiconCpasswd.classList.remove("fa-eye-slash"); 
            eyeiconCpasswd.classList.add("fa-eye")
        }else{
            cpassword.setAttribute("type","password");
            eyeiconCpasswd.classList.remove("fa-eye"); 
            eyeiconCpasswd.classList.add("fa-eye-slash")
        }
    }
}


password.onfocusin = function () {
    document.getElementById('ListPopOn').style.display = 'block';
    let lowercase = document.querySelector('.lower-case i');
    let uppercase = document.querySelector('.upper-case i');
    let number = document.querySelector('.number-digits i');
    let special = document.querySelector('.special-characters i');
    let atleast = document.querySelector('.AtLeast-Eight i');

    let lower = document.querySelector('.list-group-item .lower-case');
    let upper = document.querySelector('.list-group-item .upper-case');
    let digit = document.querySelector('.list-group-item .number-digits');
    let char = document.querySelector('.list-group-item .special-characters');
    let len = document.querySelector('.list-group-item .AtLeast-Eight');
    var checker = false;
    password.oninput = function () {
        
        if (password.value.match(/[a-z]/g)) {
            lowercase.classList.remove('fa-times-circle');
            lower.classList.remove('invalid');
            lowercase.classList.add('fa-check-circle');
            lower.classList.add('valid');
        }
        else {
            lowercase.classList.remove('fa-check-circle');
            lower.classList.remove('valid');
            lowercase.classList.add('fa-times-circle');
            lower.classList.add('invalid');
        }
        if (password.value.match(/[A-Z]/g)) {
            uppercase.classList.remove('fa-times-circle');
            upper.classList.remove('invalid');
            uppercase.classList.add('fa-check-circle');
            upper.classList.add('valid');
        }
        else {
            uppercase.classList.remove('fa-check-circle');
            upper.classList.remove('valid');
            uppercase.classList.add('fa-times-circle');
            upper.classList.add('invalid');
        }
        if (password.value.match(/[0-9]/g)) {
            number.classList.remove('fa-times-circle');
            digit.classList.remove('invalid');
            number.classList.add('fa-check-circle');
            digit.classList.add('valid');
        }
        else {
            number.classList.remove('fa-check-circle');
            digit.classList.remove('valid');
            number.classList.add('fa-times-circle');
            digit.classList.add('invalid');
        }
        if (password.value.match(/[!@#$%^&*]/g)) {
            special.classList.remove('fa-times-circle');
            char.classList.remove('invalid');
            special.classList.add('fa-check-circle');
            char.classList.add('valid');
        }
        else {
            special.classList.remove('fa-check-circle');
            char.classList.remove('valid');
            special.classList.add('fa-times-circle');
            char.classList.add('invalid');
        }
        if (password.value.length >=8 ) {
            atleast.classList.remove('fa-times-circle');
            len.classList.remove('invalid');
            atleast.classList.add('fa-check-circle');
            len.classList.add('valid');
        }
        else {
            atleast.classList.remove('fa-check-circle');
            len.classList.remove('valid');
            atleast.classList.add('fa-times-circle');
            len.classList.add('invalid');
        }
    }
}

password.onfocusout = function () {
    document.getElementById('ListPopOn').style.display = 'none';
}


} catch (error) {
    console.log(error);
}

try{
    let setpassword = document.getElementById('SetPassword');
      let passfield  = document.getElementById('form-password');
      if(setpassword.value == 'True'){
        passfield.style.display = "block";
      }else{
        passfield.style.display = "none";
      }
      setpassword.addEventListener("mouseout",()=>{
        console.log(setpassword.value);
        if(setpassword.value == 'True'){
          passfield.style.display = "block";
          document.getElementById("passwd").setAttribute("required","true");
        }else{
          passfield.style.display = "none";
          document.getElementById("passwd").removeAttribute("required");
        }
      });
}catch(error){
    console.log(error)
}