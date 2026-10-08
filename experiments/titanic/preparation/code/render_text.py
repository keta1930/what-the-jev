"""Render the passenger records of data/dataset.json as text into dataset.text.json."""

import json
from pathlib import Path
from typing import Any

PREPARATION = Path(__file__).resolve().parents[1]
SOURCE_PATH = PREPARATION.parent / 'data/dataset.json'
TARGET_PATH = PREPARATION.parent / 'data/dataset.text.json'

TEMPLATE = (
    'The passenger is {NAME}, {AGE_SEX} travelling in {CLASS} class with {COMPANIONS}. '
    'The ticket number is {TICKET}, and the fare paid is {FARE}. {CABIN} {BOARDING}'
)


def create_mapping_rules() -> dict[str, dict[Any, str]]:
    """Return the field-value to wording table."""
    return {
        'PCLASS': {1: 'first', 2: 'second', 3: 'third'},
        'EMBARKED': {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'},
    }


def format_number(value: float) -> str:
    """Write the number as given, without a trailing .0."""
    return repr(value).removesuffix('.0')


def format_age_sex(age: float | None, sex: str) -> str:
    """Return the age and sex phrase, or "of unrecorded age" when the age is missing."""
    if age is None:
        return f'a {sex} of unrecorded age'
    return f'a {format_number(age)}-year-old {sex}'


def format_companions(sibsp: int, parch: int) -> str:
    """Return the siblings or spouses and parents or children phrase."""
    return f'{_format_sibling(sibsp)} and {_format_child(parch)}'


def _format_sibling(count: int) -> str:
    """Return the siblings or spouses phrase."""
    if count == 0:
        return 'no siblings or spouses'
    return f'{count} sibling or spouse' if count == 1 else f'{count} siblings or spouses'


def _format_child(count: int) -> str:
    """Return the parents or children phrase."""
    if count == 0:
        return 'no parents or children'
    return f'{count} parent or child' if count == 1 else f'{count} parents or children'


def format_cabin(cabin: str | None) -> str:
    """Return the cabin phrase, or a note that it is unrecorded."""
    if cabin is None:
        return 'No cabin number is recorded.'
    numbers = cabin.split()
    if len(numbers) == 1:
        return f'The cabin number is {numbers[0]}.'
    return f'The cabin numbers are {cabin}.'


def build_values(passenger: dict[str, Any], mappings: dict[str, dict[Any, str]]) -> dict[str, str]:
    """Return the template placeholder values for one passenger record."""
    fare = passenger['Fare']
    return {
        'NAME': passenger['Name'],
        'AGE_SEX': format_age_sex(passenger['Age'], passenger['Sex']),
        'CLASS': mappings['PCLASS'][passenger['Pclass']],
        'COMPANIONS': format_companions(passenger['SibSp'], passenger['Parch']),
        'TICKET': passenger['Ticket'],
        'FARE': format_number(fare),
        'CABIN': format_cabin(passenger['Cabin']),
        'BOARDING': (
            f"The passenger boarded the ship at {mappings['EMBARKED'][passenger['Embarked']]}."
            if passenger['Embarked'] is not None
            else 'The port of embarkation is not recorded.'
        ),
    }


def render_passenger(passenger: dict[str, Any]) -> str:
    """Return one passenger record as a text description."""
    return TEMPLATE.format(**build_values(passenger, create_mapping_rules()))


def render_sample(sample: dict[str, Any]) -> dict[str, Any]:
    """Return the sample with its state replaced by the text description."""
    return {
        **sample,
        'input': {
            **sample['input'],
            'state': render_passenger(sample['input']['state']['passenger']),
        },
    }


def load_dataset(path: Path) -> dict[str, Any]:
    """Read the dataset file."""
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, value: Any) -> None:
    """Write JSON preserving non-ASCII characters and key order."""
    with path.open('w', encoding='utf-8') as file:
        json.dump(value, file, ensure_ascii=False, indent=2, allow_nan=False)
        file.write('\n')


def main() -> None:
    """Rewrite the state as text and write the text dataset."""
    dataset = load_dataset(SOURCE_PATH)
    samples = [render_sample(sample) for sample in dataset['samples']]
    write_json(TARGET_PATH, {'schema_version': dataset['schema_version'], 'samples': samples})
    print(f'input {SOURCE_PATH}: {len(dataset["samples"])} samples')
    print(f'output {TARGET_PATH}: {len(samples)} samples')
    print(f'\n{samples[0]["input"]["state"]}')


if __name__ == '__main__':
    main()
