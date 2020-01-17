@auth.requires_login()
def casos_drogas():
    if request.args(1) and request.args(1) == 'new':
        redirect(URL('nuevo'))

    db.CasoDeDroga.id.readable=False
    db.CasoDeDroga.id.writable=False
    db.CasoDeDroga.latlng.represent = lambda id, row: latlng_view(row.latlng)

    fields = [
        db.CasoDeDroga.lugar,
        db.CasoDeDroga.fecha,
        db.CasoDeDroga.tipo_procedimiento,
        db.CasoDeDroga.resultado,
        db.Denunciado.nombre_y_apellido,
        db.Denunciado.domicilio,
        db.Denunciado.edad,
        db.Arma.calibre,
        db.Arma.descripcion,
        db.Vehiculo.modelo,
        db.Vehiculo.tipo,
        db.Vehiculo.patente,
        ]

    form = SQLFORM.smartgrid(
        db.CasoDeDroga,
        breadcrumbs_class='breadcrumb',
        showbuttontext=False,
        fields=fields,
        csv=False,
        orderby=dict(CasoDeDroga=~db.CasoDeDroga.id),
        advanced_search=False,
        deletable=auth.has_membership("admin"),
        )
    return dict(form=form)

@auth.requires_login()
def nuevo():
    form = SQLFORM.factory(db.CasoDeDroga)
    if form.accepts(request.vars):
        id_caso_de_droga = db.CasoDeDroga.insert(**db.CasoDeDroga._filter_fields(form.vars))
        redirect(URL(
            'casos_drogas',
            args= ['CasoDeDroga', 'view', 'CasoDeDroga', id_caso_de_droga],
            user_signature=True)
            )
    return dict(form=form)

def vehiculo_droga():
    db.CasoDeDroga.id.readable=False
    db.CasoDeDroga.id.writable=False
    db.Vehiculo.id.readable=False
    db.Vehiculo.id.writable=False
    db.Vehiculo.id_caso_de_droga.readable=False
    db.Vehiculo.id_caso_de_droga.writable=False
    form = SQLFORM.smartgrid(
        db.CasoDeDroga,
        searchable=False,
        showbuttontext=False,
        csv=False,
        user_signature=False,
        formname='vehiculo')
    return dict(form=form)

def denunciado_droga():
    db.CasoDeDroga.id.readable=False
    db.CasoDeDroga.id.writable=False
    db.Denunciado.id.readable=False
    db.Denunciado.id.writable=False
    db.Denunciado.id_caso_de_droga.readable=False
    db.Denunciado.id_caso_de_droga.writable=False
    form = SQLFORM.smartgrid(
        db.CasoDeDroga,
        searchable=False,
        showbuttontext=False,
        csv=False,
        user_signature=False,
        formname='denunciado')
    return dict(form=form)

def arma_droga():
    db.CasoDeDroga.id.readable=False
    db.CasoDeDroga.id.writable=False
    db.Arma.id.readable=False
    db.Arma.id.writable=False
    db.Arma.id_caso_de_droga.readable=False
    db.Arma.id_caso_de_droga.writable=False
    form = SQLFORM.smartgrid(
        db.CasoDeDroga,
        searchable=False,
        showbuttontext=False,
        csv=False,
        user_signature=False,
        formname='arma')
    return dict(form=form)

@auth.requires_login()
def mapa():
    # desde = request.args(0) if request.args(0) else None
    # hasta = request.args(1) if request.args(1) else None

    # form = SQLFORM.factory(
    #     Field('desde', 'date', widget=date_widget),
    #     Field('hasta', 'date', widget=date_widget),
    # )

    # if form.process().accepted:
    #     desde = form.vars.desde
    #     hasta = form.vars.hasta
    #     redirect(URL('mapa', args=[desde, hasta]))

    points_a = []
    points_b = []

    
    # query_desde = (db.CasoDeDroga.fecha >= desde)
    # query_hasta = (db.CasoDeDroga.fecha >= hasta)

    query_flagrancia = (db.CasoDeDroga.tipo_procedimiento == 'Flagrancia') & (db.CasoDeDroga.latlng != None)
    query_investigacion = (db.CasoDeDroga.tipo_procedimiento == 'Investigacion') & (db.CasoDeDroga.latlng != None)

    # if desde:
    #     query_flagrancia = query_flagrancia & query_desde
    #     query_investigacion = query_investigacion & query_desde
    # if hasta:
    #     query_flagrancia = query_flagrancia & query_hasta
    #     query_investigacion = query_investigacion & query_hasta
    
    for row in db(query_flagrancia).select(db.CasoDeDroga.latlng, db.CasoDeDroga.lugar):
        points_a.append([return_point(row.latlng), row.lugar or '-'])
    
    for row in db(query_investigacion).select(db.CasoDeDroga.latlng, db.CasoDeDroga.lugar):
        points_b.append([return_point(row.latlng), row.lugar or '-'])
    
    return dict(
        flagrancia=points_a,
        investigaciones=points_b,
        capital=db(db.CasoDeDroga.digedrop == 'CAPITAL').count(),
        talitas=db(db.CasoDeDroga.digedrop == 'TALITAS').count(),
        sur=db(db.CasoDeDroga.digedrop == 'SUR').count(),
        oeste=db(db.CasoDeDroga.digedrop == 'OESTE').count(),
        este=db(db.CasoDeDroga.digedrop == 'ESTE').count(),
    )

def return_point(latlng):
    lista = latlng.split(',')
    return [float(lista[0]), float(lista[1])]

def latlng_view(value):
    wrapper = DIV()
    point = str(value).split(',')
    javascript = SCRIPT("""
        var map = L.map('map').setView([-26.83077, -65.21644], 8);
        map.addControl(new L.Control.Fullscreen());

        L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYnJ1aW5vIiwiYSI6ImNqeTBiam9zMTAxZ2czZ3E4aGE2ZHQ0bGIifQ.SbLskdmBG33M34jXkrSSOA', {
            attribution: '© <a href="https://www.mapbox.com/feedback/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        var marker = new L.Marker(%s, { draggable: false });
        map.addLayer(marker);
    """ %(point), _type='text/javascript')
    wrapper.components.extend([DIV(_id='map', _style='width: 100%; height: 500px'), javascript])
    return wrapper
