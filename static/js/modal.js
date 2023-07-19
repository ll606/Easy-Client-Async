
function setModalSize(size){
    modal = document.querySelector('.modal-dialog');
    sizemap = {
        extra_large: 'modal-xl',
        large: 'modal-lg',
        default: '',
        small: 'modal-sm'
    };
    size = sizemap[size];
    for(let each in sizemap){
        modal.className = modal.className.replaceAll(
            sizemap[each], ''
        );
    }
    modal.className += ` ${size}`;
}

function setModalCentered(){
    modal = document.querySelector('.modal-dialog');
    if(!modal.className.includes('modal-dialog-centered')){
        modal.className += ' modal-dialog-centered';
    }
}