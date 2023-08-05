**Nombre de la librería**
doit-monitoring-api

Descripción
La librería doit-monitoring-api es una API que se encarga de monitorear otros sistemas de tipo ETL. Esta librería ha sido desarrollada por DoIteasy.

Instalación
Para instalar esta librería, puedes clonar el repositorio desde GitHub:

Uso
La API está compuesta por varios endpoints que permiten la monitorización de sistemas ETL. A continuación se presentan los endpoints disponibles:

/health: endpoint para verificar el estado de la API.
/jobs: endpoint para listar los trabajos monitoreados por la API.
/jobs/{job_id}: endpoint para obtener detalles sobre un trabajo específico.
/jobs/{job_id}/runs: endpoint para listar las ejecuciones de un trabajo específico.
/jobs/{job_id}/runs/{run_id}: endpoint para obtener detalles sobre una ejecución específica.
Contributing
Si deseas contribuir a esta librería, por favor, sigue estos pasos:

Haz un fork del repositorio.
Crea una rama para tu contribución (git checkout -b feature/your-feature).
Haz tus cambios y haz commit de los mismos (git commit -am 'Add some feature').
Empuja tus cambios a la rama (git push origin feature/your-feature).
Abre un pull request.
Licencia
Esta librería se distribuye bajo la licencia MIT. Ver el archivo LICENSE para más detalles.