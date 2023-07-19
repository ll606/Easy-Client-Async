from pywebio.session import run_js, eval_js
from typing import Sequence, Literal, List


def validate_input(name: str, pattern: str, success: str, fail: str) -> None:
    run_js(
        'validateInputByRegularExpression(name, pattern, success, fail)',
        name=name, pattern=pattern, success=success, fail=fail
    )


async def get_input_status(name: str) -> Literal['valid', 'invalid']:
    return await eval_js('getInputStatus(name)', name=name)

    
async def all_inputs_valid(names: Sequence) -> bool:
    return await eval_js('allInputsValid(names)', names=names)


def validate_form_input(value: str, pattern: str, success: str, fail: str) -> None:
    run_js(
        'validateFormInput("data", value, pattern, success, fail)',
        value=value, pattern=pattern, success=success, fail=fail
    )
    
def set_input_valid(name: str, text: str):
    run_js('setInputValid(name, text)', name=name, text=text)

def set_input_invalid(name: str, text: str):
    run_js('setInputInvalid(name, text)', name=name, text=text)
    
def validate_input_group(
    values: dict[str, str], patterns: dict[str, str], 
    successes: dict[str, str], fails: dict[str, str]
) -> None:
    # data {"name": "value"}
    data: List[dict[str, str]] = []
    
    names: List[str] = [each for each in values.keys()]
    
    for name in names:
        data.append({
            'name': name, 
            'pattern': patterns[name],
            'successText': successes[name], 
            'failText': fails[name]
        })
    
    run_js('validateInputGroup(data)', data=data)