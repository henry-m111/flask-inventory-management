"""
Unit tests for the CLI frontend.
Mocks both user input (input()) and API calls (requests) so tests run
in isolation without a live server or real user interaction.
"""

from unittest.mock import patch, MagicMock
import cli


def test_view_all_items_displays_data(capsys):
    """Should print a formatted table when items are returned from the API."""
    mock_items = [
        {"id": 1, "product_name": "Almond Milk", "brand": "Silk",
         "quantity_in_stock": 50, "price": 3.99},
    ]

    with patch("cli.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_items
        mock_get.return_value = mock_response

        cli.view_all_items()

    captured = capsys.readouterr()
    assert "Almond Milk" in captured.out
    assert "Silk" in captured.out


def test_view_all_items_empty(capsys):
    """Should print a friendly message when inventory is empty."""
    with patch("cli.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        cli.view_all_items()

    captured = capsys.readouterr()
    assert "Inventory is empty." in captured.out


def test_view_all_items_connection_error(capsys):
    """Should print a friendly error message when the API is unreachable."""
    with patch("cli.requests.get") as mock_get:
        mock_get.side_effect = cli.requests.exceptions.ConnectionError("refused")

        cli.view_all_items()

    captured = capsys.readouterr()
    assert "Error: could not reach the API." in captured.out


def test_view_single_item_invalid_id(capsys):
    """Should reject non-numeric IDs before making any API call."""
    with patch("builtins.input", return_value="abc"):
        cli.view_single_item()

    captured = capsys.readouterr()
    assert "valid numeric ID" in captured.out


def test_add_item_manual_success(capsys):
    """Should POST the entered data and confirm success."""
    user_inputs = iter([
        "Peanut Butter",  # product_name
        "Jif",            # brand
        "0051500255516",  # barcode
        "Spreads",        # category
        "20",             # quantity
        "4.29",           # price
    ])

    with patch("builtins.input", lambda _: next(user_inputs)):
        with patch("cli.requests.post") as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.json.return_value = {"id": 3, "product_name": "Peanut Butter"}
            mock_post.return_value = mock_response

            cli.add_item_manual()

    captured = capsys.readouterr()
    assert "Item added successfully with ID 3." in captured.out


def test_add_item_manual_missing_name(capsys):
    """Should cancel if product name is left blank."""
    user_inputs = iter(["", "Jif", "123", "Spreads", "20", "4.29"])

    with patch("builtins.input", lambda _: next(user_inputs)):
        cli.add_item_manual()

    captured = capsys.readouterr()
    assert "Product name is required" in captured.out


def test_delete_item_confirmed(capsys):
    """Should call DELETE when the user confirms."""
    user_inputs = iter(["1", "y"])

    with patch("builtins.input", lambda _: next(user_inputs)):
        with patch("cli.requests.delete") as mock_delete:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_delete.return_value = mock_response

            cli.delete_item()

    captured = capsys.readouterr()
    assert "Item deleted successfully." in captured.out


def test_delete_item_cancelled(capsys):
    """Should NOT call DELETE when the user does not confirm."""
    user_inputs = iter(["1", "n"])

    with patch("builtins.input", lambda _: next(user_inputs)):
        with patch("cli.requests.delete") as mock_delete:
            cli.delete_item()
            mock_delete.assert_not_called()

    captured = capsys.readouterr()
    assert "Cancelled." in captured.out


def test_find_item_on_api_not_found(capsys):
    """Should print a friendly message when the barcode isn't found."""
    with patch("builtins.input", return_value="0000000000000"):
        with patch("cli.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response

            cli.find_item_on_api()

    captured = capsys.readouterr()
    assert "No product found for barcode" in captured.out