# WS-2
Autores: Carlos Pérez, Diana Camacho, Hillary Brenes.

Estudiantes de Ulacit de la carrera bachillerato en Ing. Informática, curso: Servicios Web.

La funcionalidad del proyecto consiste en determinar las rutas de viaje más cortas de un punto a otro para los clientes finales de este sistema, proporcionando la mejor experiencia de viaje a dichos clientes finales. 

Como parte de la realización de este proyecto se hace uso del algoritmo de Dijkstra, el cual también llamado algoritmo de caminos mínimos, es un algoritmo para la determinación del camino más corto dado un vértice origen al resto de los vértices en un grafo con pesos en cada arista. Así mismo, se hace uso de la implementación de la libreria Networkx para Python la cual es utilizada para la creación, manipulación y estudio de las estructuras, dinámicas y funciones de redes complejas.

Para el desarrollo del servidor web encargado de manejar las transacciones que el cliente va a realizar, se utiliza en primer lugar el micro-framework de Python llamado Flask, debido a lo sencillo que resulta su implementación y no requiere herramientas o bibliotecas particulares. A su vez para la realizacion del sistema se debe hacer la implementacion de una base de datos la cual sirva para guardar todos los datos necesarios para el desarrollo de dicho sistema. Esta se realiza por medio de la implementación de la base de datos Objeto-relacional PostgreSQL, el cual es un potente sistema de base de datos de código abierto.

La modalidad de uso depende de la ruta determinada, donde una vez seleccionada la ruta se le brindan al cliente distintas opciones de transporte. Las opciones de transporte son: bus, taxi, tren y avión.

Puntos o nodos establecidos:
1.    Volcán Arenal (ALAJUELA)
2.    Quepos (PUNTARENAS)
3.    Las Juntas (GUANACASTE)
4.    Cariari Pococí (LIMON)
5.    Puerto Jiménez (PUNTARENAS)
6.    Volcán Rincón de la Vieja (ALAJUELA)
7.    Volcán Poás (ALAJUELA)
8.    Upala (ALAJUELA)
9.    Puerto Viejo Sarapiquí (HEREDIA)
10.   Cahuita (LIMON)
11.   Filadelfia (GUANACASTE)
12.   Volcán Turrialba (CARTAGO)
13.   San Isidro del General (SAN JOSE)
14.   Uvita (PUNTARENAS)
15.   Volcán Irazú (CARTAGO)
16.   Volcán Tenorio (GUANACASTE)
17.   Moravia (SAN JOSE)
18.   Cerro chirripó (SAN JOSE)
19.   Casona Santa Rosa (GUANACASTE)
20.   Bribri (LIMON)
21.   Puerto Viejo Talamanca (LIMON)
22.   Los chiles (ALAJUELA)
23.   Volcán Barva (HEREDIA)
24.   Puerto Moreno Santa Cruz (GUANACASTE)
