function pin(name){
    let parse = document.querySelector(`[name="${name}"]`).value;
    
    if((parse.length <= 1) || (parse.length === undefined)){
        return parse;
    }

    if(parse[0] === '"'){
        parse = parse.substr(1, parse.length - 2);
    }
    
    return parse;

}

function validateVariableContent(){
    let var_type = pin('var_type');
    let var_content = pin('var_content');

    if(var_type === '数字'){
        if(var_content.trim() === ""){
            setInputInvalid('var_content', '输入的数字无效！');
            return;
        }

        let testNumber = Number(var_content);
        if(!isNaN(testNumber)){
            setInputValid('var_content', '该输入有效');
        } else {
            setInputInvalid('var_content', '输入的数字无效！');
        }
    } else if(var_type === '文本'){
        setInputValid('var_content', '该输入有效');
    } else {
        let data;
        
        try{
            data = JSON.parse(var_content);
        }catch(e){
            setInputInvalid('var_content', '输入错误！');
            return;
        }

        if((var_type==='列表')&&(data instanceof Array)){
            setInputValid('var_content', '该输入有效！')
            return;
        } else if((var_type==='字典')&&(data instanceof Object)){
            setInputValid('var_content', '该输入有效！')
            return;
        } else {
            setInputInvalid('var_content', '输入错误！');
            return;
        }
    }
}