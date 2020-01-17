# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    ('Inicio', False, URL('default', 'index'), []),
    ('Casos de Drogas', False, URL('drogas', 'casos_drogas'), []),
    ('Mapa', False, URL('drogas', 'mapa'), []),
]