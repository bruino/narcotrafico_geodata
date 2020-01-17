# -*- coding: utf-8 -*-
from gluon.html import DIV, SCRIPT
from gluon.sqlhtml import SQLFORM

# New widget geocoder
def latlng_widget(field, value):
    wrapper = DIV()
    input_latlng = SQLFORM.widgets.string.widget(field, value, _type="hidden")
    point = str(value).split(',')
    javascript = SCRIPT("""
        var map = L.map('map').setView([-26.83077, -65.21644], 8);
        map.addControl(new L.Control.Fullscreen());

        L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYnJ1aW5vIiwiYSI6ImNqeTBiam9zMTAxZ2czZ3E4aGE2ZHQ0bGIifQ.SbLskdmBG33M34jXkrSSOA', {
            attribution: '© <a href="https://www.mapbox.com/feedback/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        var marker;
        
        function onMapClick(e) {
            if (marker) map.removeLayer(marker);
            marker = new L.Marker(e.latlng, { draggable: false });
            map.addLayer(marker);
            $("#%s").val(e.latlng.lat + "," + e.latlng.lng);
            // marker.bindPopup("<b>Hello world!</b><br />I am a popup.").openPopup();
        }
        map.on('click', onMapClick);
        
        L.Control.geocoder({
            defaultMarkGeocode: false,
            collapsed: false,
            placeholder: 'Buscar',
            errorMessage: 'No encontrado.',
            // geocoder: L.Control.Geocoder.google("AIzaSyBoaA9X9yKIpEfAcleKRXf78DKm51AYLjw")
            })
            .on('markgeocode', function (e) {
                if (marker) map.removeLayer(marker);
                marker = new L.Marker(e.geocode.center, { draggable: true });
                map.addLayer(marker);
                map.setView(e.geocode.center, 15);
                $("#%s").val(e.geocode.center.lat + "," + e.geocode.center.lng);
            })
            .addTo(map);

            latlng = %s;
            if(latlng != ['None']) {
                marker = new L.Marker(latlng, { draggable: true });
                map.addLayer(marker);
                map.setView(latlng, 13);
            }
    """ %(input_latlng['_id'],  input_latlng['_id'], point), _type='text/javascript')
    wrapper.components.extend([input_latlng, DIV(_id='map', _style='width: 100%; height: 500px'), javascript])
    return wrapper

# New widget date
def date_widget(field, value):
    wrapper = DIV()
    input_date = SQLFORM.widgets.date.widget(field, value)
    javascript = SCRIPT("""
        jQuery.datetimepicker.setLocale('es');
            $(function () {
                $("#%s").datetimepicker({
                    format: 'Y-m-d',
                    inline: true,
                    timepicker:false,
                });
            });
    """ % input_date['_id'], _type='text/javascript')
    wrapper.components.extend([input_date,javascript])
    return wrapper