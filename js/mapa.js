window.onload = function () {
    var basemap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        minZoom: 2,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });

    function refresh() {
        map.setView([lat, lng], 3);
    }

    $.getJSON("data/proyectos.geojson", function (data) {
        var markers = L.markerClusterGroup();

        var geojson = L.geoJson(data, {
            onEachFeature: function (feature, layer) {
                if (feature.properties.nombre == "") {
                    layer.bindPopup(
                        "<a href=" + feature.properties.url + " target=\"_blank\" class=\"link-primary\">" + feature.properties.url + "</a>" +
                        "<p><b>Ubicación:</b> " + feature.properties.origen + "<br \\>" +
                        "<b>Equipo:</b> " + feature.properties.equipo + "<br \\>" +
                        "<b>Tema:</b> " + feature.properties.tema + "<br \\>" +
                        "<b>Tipo de proyecto:</b> " + feature.properties.tipo_proyecto + "</p>"
                    );
                } else {
                    layer.bindPopup(
                        "<h3>" + "<a href=" + feature.properties.url + " target=\"_blank\" class=\"link-primary\">" + feature.properties.nombre + "</a></h3>" +
                        "<p><b>Ubicación:</b> " + feature.properties.origen + "<br \\>" +
                        "<b>Equipo:</b> " + feature.properties.equipo + "<br \\>" +
                        "<b>Tema:</b> " + feature.properties.tema + "<br \\>" +
                        "<b>Tipo de proyecto:</b> " + feature.properties.tipo_proyecto + "</p>")
                }
            }
        });

        var map = L.map('map', {
            center: [40.4167, -3.7033],
            zoom: 12,
            layers: [basemap, geojson]
        }).fitBounds(geojson.getBounds()).setView([19.6594, -36.9521], 3);

        geojson.eachLayer(function (layer) {
            markers.addLayer(layer);
        });

        map.addLayer(markers);

        var baseMaps = {
            "OpenStreetMap": basemap
        };

        var overlayMaps = {
            "Proyectos": geojson
        };

        L.control.layers(baseMaps, overlayMaps).addTo(map);

        /* custom button to flyTo center of map */
        var centerButton = L.Control.extend({
            options: {
                position: 'topright'
            },
            onAdd: function (map) {
                var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
                container.style.backgroundColor = 'white';
                container.style.backgroundSize = 'contain';
                container.style.backgroundRepeat = 'no-repeat';
                container.style.backgroundPosition = 'center';
                container.style.width = '45px';
                container.style.height = '45px';
                container.style.cursor = 'pointer';
                container.style.fontfamily = 'FontAwesome';
                container.style.textAlign = 'center';
                container.style.fontSize = '30px';
                container.style.paddingTop = '.4rem';
                container.style.color = 'rgba(0,0,0,0.6)';
                container.innerHTML = '<i class="fa-solid fa-expand"></i>';
                container.addEventListener('mouseover', function () {
                    container.title = 'Centrar mapa';
                    container.style.backgroundColor = '#f5f5f5';
                    container.style.fontSize = '35px';
                    container.style.color = 'rgba(0,0,0,0.8)';
                    container.style.paddingTop = '.15rem';
                });
                container.addEventListener('mouseout', function () {
                    container.style.backgroundColor = 'white';
                    container.style.fontSize = '30px';
                    container.style.paddingTop = '.4rem';
                    container.style.color = 'rgba(0,0,0,0.6)';
                });
                container.onclick = function () {
                    map.flyTo([19.6594, -36.9521], 3);
                };
                
                return container;
            }

        });
        map.addControl(new centerButton());
    });

};