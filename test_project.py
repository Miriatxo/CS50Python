from project import get_type, get_date, get_keyword, clean_html
from unittest.mock import patch


def test_get_type():
    with patch("builtins.input", return_value="1. music"):
        result = get_type()
        assert result == "music"


def test_get_date():
    with patch("builtins.input", return_value="jul 24"):
        result = get_date()
        assert result == "2024-07-24"


def test_get_keyword():
    with patch("builtins.input", return_value="jazzaldi"):
        result = get_keyword()
        assert result == "jazzaldi"


def test_clean_html():
    input_html = '<p>Dentro del programa del <a href="https://www.kulturklik.euskadi.eus/evento/2024/07/15/programa-festival-de-jazz-de-vitoria-gasteiz-2024/webkklik00-detalle/es/" target="_blank"><strong> Festival de Jazz de Vitoria-Gasteiz 2024</strong></a>.'
    expected_output = 'Dentro del programa del Festival de Jazz de Vitoria-Gasteiz 2024.'
    assert clean_html(input_html) == expected_output


