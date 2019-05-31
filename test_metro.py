from metro import build_graph
from metro import get_alphabetical_shortest_path


def test_build_graph():
    g = build_graph([
        {'stations': [
            {
                "name": "A",
                "time": 0
            },
            {
                "name": "B",
                "time": 5
            },
            {
                "name": "C",
                "time": 7
            },
        ]},
        {'stations': [
            {
                "name": "B",
                "time": 0
            },
            {
                "name": "D",
                "time": 10
            },
        ]},
    ])
    assert len(g.nodes) == 4
    assert len(g.edges) == 3
    assert g['B']['C']['weight'] == 2


def test_get_alphabetical_shortest_path_one():
    result = get_alphabetical_shortest_path([['A', 'B', 'C']])
    assert result == ['A', 'B', 'C']


def test_get_alphabetical_shortest_path_various():
    result = get_alphabetical_shortest_path([['A', 'D', 'E', 'C'], ['A', 'B', 'E', 'C'], ['A', 'Z', 'C']])
    assert result == ['A', 'B', 'E', 'C']


def test_get_alphabetical_shortest_path_caps_accent():
    result = get_alphabetical_shortest_path([['A', 'b', 'É', 'C'], ['A', 'B', 'I', 'C']])
    assert result == ['A', 'b', 'É', 'C']


def test_get_alphabetical_shortest_path_real():
    result = get_alphabetical_shortest_path([
        ['Pacífico', 'Sainz de Baranda', 'Príncipe de Vergara', 'Núñez de Balboa', 'Alonso Martínez', 'Tribunal'],
        ['Pacífico', 'Sainz de Baranda', 'Manuel Becerra', 'Diego de León', 'Núñez de Balboa', 'Alonso Martínez', 'Tribunal'],
        ['Pacífico', 'Sol', 'Gran Vía', 'Tribunal'],
        ['Pacífico', 'Sainz de Baranda', 'Príncipe de Vergara', 'Núñez de Balboa', 'Alonso Martínez', 'Bilbao', 'Tribunal'],
        ['Pacífico', 'Sainz de Baranda', 'Manuel Becerra', 'Diego de León', 'Núñez de Balboa', 'Alonso Martínez', 'Bilbao', 'Tribunal'],
        ['Pacífico', 'Sol', 'Callao', 'Plaza de España', 'Tribunal']
    ])
    assert result == ['Pacífico', 'Sainz de Baranda', 'Manuel Becerra', 'Diego de León', 'Núñez de Balboa', 'Alonso Martínez', 'Bilbao', 'Tribunal']


def test_get_alphabetical_shortest_path_one_with_multiple_letters():
    path = ['Ópera', 'Sol', 'Príncipe de Vergara', 'Núñez de Balboa', 'Avenida de América', 'Mar de Cristal', 'Pinar de Chamartín']
    result = get_alphabetical_shortest_path([path])
    assert result == path
