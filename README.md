# Alrededor del mundo de las HD

Este proyecto está inspirado en  [Around DH 2020](https://arounddh.org/), que a su vez retomó el proyecto [Around DH in 80 Days](http://arounddh.elotroalex.com/).

## Proponer nuevos proyectos

* Cree un issue con la etiqueta 'Nuevo proyecto'. Este debe contener por lo menos los siguientes campos: 
  * Nombre del proyecto
  * Descripción del proyecto
  * URL del proyecto
  * Lugar de origen del proyecto
* También puede editar el archivo `data/propuesta_proyectos.csv` y hacer un pull request con los cambios. Debido a que el archivo `data/proyectos.geojson` se genera de manera automatizada, es recomendable no editarlo directamente.

Un log con los proyectos añadidos se puede consultar en `logs/log.txt`.

## Origen de los datos

La fuente original de datos proviene de ["A1 AroundDH ( Digital Humanities ) | Global List"](https://docs.google.com/spreadsheets/d/1_PNv9Jlw_QlUh6SeYJrGYFucoRzlZAfLf7OouWu-qe4/edit?usp=sharing), creada por @elotroalex .

Los datos fueron depurados con el script `around_HD/adh_depurador.py` para validar que los enlaces fueran válidos y se seleccionó un origen único de los proyectos. Por esta razón, proyectos multinacionales carecen de representación adecuada en el mapa.

Un archivo de los enlaces que no pudieron ser validados se encuentra en el archivo `around_HD/broken_links.txt`.

## Licencia

Este proyecto está licenciado bajo la [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
El código se pone a disposición del público bajo la licencia [MIT](https://opensource.org/licenses/MIT).
