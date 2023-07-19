function setInputStatus(name, helpText, status){
    let target = document.querySelector(`[name="${name}"]`);
    let classStatus = `form-control is-${status}`;
    target.className = classStatus;
    target
        .parentNode
        .querySelector(`.${status}-feedback`)
        .textContent = helpText;
}

function setInputValid(name, helpText){
    setInputStatus(name, helpText, 'valid');
}

function setInputInvalid(name, helpText){
    setInputStatus(name, helpText, 'invalid');
}

function getInputStatus(name){
    let target = document.querySelector(`[name="${name}"]`);
    let targetClass = target.className;
    if(!target.className.includes('is')){
        return 'plain';
    }else{
        return targetClass.replace(/form-control is-/g, '');
    }
}

function getInputFeedback(name, status){
    return document
            .querySelector(`[name="${name}"]`)
            .parentNode
            .querySelector(`.${status}-feedback`)
            .textContent;
}

function getInputValidFeedback(name){
    return getInputFeedback(name, 'valid');
}

function getInputInvalidFeedback(name){
    return getInputFeedback(name, 'invalid');
}

function allInputsValid(names){
    // names 长度为0时仍然返回true

    for(let name of names){
        if(getInputStatus(name) === 'invalid'){
            return false;
        }
        
        // 防止没有任何输入就返回
        if(getInputStatus(name) === 'plain'){
            return false;
        }
    }

    return true;
}

function validateInputByRegularExpression(name, re, successText, failText){
    let ele = document.querySelector(`[name="${name}"]`);
    let regex = new RegExp(re);

    if(regex.test(ele.value)){
        setInputValid(name, successText);
    }else{
        if(ele.value.trim()!==''){
            setInputInvalid(name, failText);
        }
    }

    ele.addEventListener('input', event=>{
        if(regex.test(event.target.value)){
            setInputValid(name, successText);
        }else{
            setInputInvalid(name, failText);
            event.preventDefault();
        }
    });
}

function validateValue(name, value, re, successText, failText){
    let regex = new RegExp(re);
    
    if(regex.test(value)){
        setInputValid(name, successText);
        return true;
    } else {
        setInputInvalid(name, failText);
        return false;
    }
}

function disableSubmitButton(){
    let button = document.querySelector('#input-container [type="submit"]');
    button.setAttribute('disabled', '');
}

function enableSubmitButton(){
    let button = document.querySelector('#input-container [type="submit"]');
    button.removeAttribute('disabled');
}

function validateFormInput(name, value, re, successText, failText){
    if(validateValue(name, value, re, successText, failText)){
        enableSubmitButton();
    }else{
        disableSubmitButton();
    }
}

function validateInputGroup(data){
    /*
        data = [
            {name: "", value: "", pattern: "", successText: "", failText: ""}
        ]
    */

    for(let item of data){
        let regex = new RegExp(item.pattern);
        
        if(regex.test(item.pattern)){
            setInputValid(item.name, item.successText);
        } else {
            setInputInvalid(item.name, item.failText);
        }
    }

    let names = data.map(x=>x.name);
    if(allInputsValid(names)){
        enableSubmitButton();
    } else {
        disableSubmitButton();
    }
}

