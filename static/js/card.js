function setScopeAsCardHeader(scope, header){
    let target = document.querySelector(`#pywebio-scope-${scope}`);
    target.className = 'card-header'
    let headerElement = document.createElement('h3');
    headerElement.textContent = header;
    target.appendChild(headerElement);
}

function setScopeAsCardBody(scope){
    let target = document.querySelector(`#pywebio-scope-${scope}`);
    target.className = 'card-body'
}

function setScopeAsCardRoot(scope){
    let target = document.querySelector(`#pywebio-scope-${scope}`);
    target.className = 'card'
}