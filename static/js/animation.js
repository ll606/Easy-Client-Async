function hideElement(selector, ms){
    let target = document.querySelector(selector);
    let unit = ms / 100;

    for(let i=0;i<=100;i++){
        setTimeout(()=>{
            target.style.opacity = 1 - 0.01 * i;
        }, unit*i);
    }

    setTimeout(()=>{
        target.style.display = 'none';
    }, ms);

}

function showElement(selector, ms){
    let target = document.querySelector(selector);
    let unit = ms / 100;
    target.style.opacity = 0;
    target.style.display = 'block';
    
    for(let i=0;i<=100;i++){
        setTimeout(()=>{
            target.style.opacity = 0.01 * i;
        }, unit*i)
    }
}