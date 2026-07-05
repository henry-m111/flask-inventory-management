from unittest.mock import patch, Mock
import cli


def test_view_items_displays_items(capsys):
    """view_items should print each item's details."""
    fake_items = [
        {"id": 1, "name": "Nutella", "brand": "Ferrero", "price": 4.99, "quantity": 10}
    ]
    mock_response = Mock()
    mock_response.json.return_value = fake_items

    with patch("cli.requests.get", return_value=mock_response):
        cli.view_items()

    captured = capsys.readouterr()
    assert "Nutella" in captured.out
    assert "Ferrero" in captured.out


def test_view_items_empty(capsys):
    """view_items should print a message when inventory is empty."""
    mock_response = Mock()
    mock_response.json.return_value = []

    with patch("cli.requests.get", return_value=mock_response):
        cli.view_items()

    captured = capsys.readouterr()
    assert "No items in inventory." in captured.out


def test_add_item_success(capsys):
    """add_item should print a success message when the API call succeeds."""
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": 1, "name": "Nutella", "brand": "Ferrero", "price": 4.99, "quantity": 10
    }

    with patch("cli.requests.post", return_value=mock_response), \
         patch("builtins.input", side_effect=["Nutella", "Ferrero", "4.99", "10"]):
        cli.add_item()

    captured = capsys.readouterr()
    assert "Item added successfully" in captured.out

def test_update_item_success(capsys):
    """update_item should print a success message when the API call succeeds."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1, "name": "Nutella", "brand": "Ferrero", "price": 3.99, "quantity": 5
    }

    with patch("cli.requests.patch", return_value=mock_response), \
         patch("builtins.input", side_effect=["1", "", "", "3.99", "5"]):
        cli.update_item()

    captured = capsys.readouterr()
    assert "Item updated successfully" in captured.out


def test_delete_item_success(capsys):
    """delete_item should print a success message when the API call succeeds."""
    mock_response = Mock()
    mock_response.status_code = 200

    with patch("cli.requests.delete", return_value=mock_response), \
         patch("builtins.input", side_effect=["1"]):
        cli.delete_item()

    captured = capsys.readouterr()
    assert "Item deleted successfully" in captured.out