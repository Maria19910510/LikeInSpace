from src.transaction_helpers import process_bank_search, process_bank_operations



def test_process_bank_search_found():
    data = [
        {'id': 1, 'description': 'Payment to electricity bill'},
        {'id': 2, 'description': 'Grocery shopping at supermarket'},
        {'id': 3, 'description': 'Salary for August'},
        {'id': 4, 'description': 'Payment to water bill'},
        {'id': 5, 'description': None},
        {'id': 6}
    ]
    result = process_bank_search(data, 'payment')
    result_ids = {item['id'] for item in result}
    assert result_ids == {1, 4}


def test_process_bank_search_not_found():
    data = [
        {'id': 1, 'description': 'Payment to electricity bill'},
        {'id': 2, 'description': 'Grocery shopping at supermarket'}
    ]
    result = process_bank_search(data, 'rent')
    assert result == []

def test_process_bank_search_handles_missing_description():
    data = [
        {'id': 1, 'description': 'Payment to electricity bill'},
        {'id': 2},
        {'id': 3, 'description': None}
    ]
    result = process_bank_search(data, 'payment')
    # Должны быть только транзакции, содержащие 'payment'
    assert len(result) == 1
    assert result[0]['id'] == 1

def test_process_bank_operations_counts():
    data = [
        {'description': 'Electricity bill'},
        {'description': 'electricity'},
        {'description': 'Water bill'},
        {'description': 'GROCERY shopping'},
        {'description': 'Salary'}
    ]
    categories = ['electricity', 'water', 'grocery']
    counts = process_bank_operations(data, categories)
    assert counts['electricity'] == 2
    assert counts['water'] == 1
    assert counts['grocery'] == 1

def test_process_bank_operations_no_matches():
    data = [
        {'description': 'Rent payment'},
        {'description': 'Insurance premium'}
    ]
    categories = ['electricity']
    counts = process_bank_operations(data, categories)
    assert counts['electricity'] == 0

def test_case_insensitivity():
    data = [{'description': 'GROCERY store'}]
    categories = ['grocery']
    counts = process_bank_operations(data, categories)
    assert counts['grocery'] == 1
