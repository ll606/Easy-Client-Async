function getAllScopes(){
    return [
        ...document
            .querySelectorAll('[id^="pywebio-scope-"]')
    ].map(x=>x.id.replace(/pywebio-scope-/g,''));
}

function getSubScope(scope){
    let target = document.querySelectorAll(`#pywebio-scope-${scope}`);
    
    if(target===null){
        return null;
    }

    let scopes = [
        ...target.querySelectorAll('[id^="pywebio-scope-"]')
    ].map(x=>x.id.replace(/pywebio-scope-/g, ''))
    return scopes
}

function getParentScope(selector){
    let target = document.querySelectorAll(selector);
    if(target===null){
        return null;
    }

    let root = document.querySelector('#pywebio-scope-ROOT');
    while(target !== root){
        target = target.parentNode;
        if((target.hasAttribute('id')) && (target.id.startsWith('pywebio-scope-'))){
            return target.id.replace(/pywebio-scope-/g, '');
        }
    }
}

function getParentScopeByScope(scope){
    return getParentScope(`#pywebio-scope-${scope}`);
}

function getParentScopeByName(name){
    return getParentScope(`[name="${name}"]`);
}


function getAllParentScopes(scope){
    let target = document.querySelector(`#pywebio-scope-${scope}`);

    if(target===null){
        return null;
    }

    let root = document.querySelector('#pywebio-scope-ROOT');

    let scopes = []; 
    while(target!==root){
        target = target.parentNode;
        if(target.hasAttribute('id') && target.id.startsWith('pywebio-scope-')){
            scopes.push(target.id.replace(/pywebio-scope-/g, ''));
        }
    }
    return scopes;
}

function getInputs(scope){
    let target = document.querySelector(`#pywebio-scope-${scope}`);
    let inputs = [...target.querySelectorAll('.form-group input[name]')].map(x=>x.name);
    let selects = [...target.querySelectorAll('.form-group select[name]')].map(x=>x.name);
    return inputs.concat(selects);
}