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

FUNCIONAMIENTO PARA DETERMINAR LOS MEDIOS DE TRASNPORTE POR NODO
Solicitud de parámetros:  Primeramente al usuario se le solicitan 3 parámetros necesarios para determinar el tipo de transporte a elegir: 
a.	Nodo-origen
b.	Nodo-destino 
c.	Tipo-transporte

A su vez, el sistema determina los nodos vecinos de los nodos que están ingresando por parámetros, esto para determinar si en los nodos vecinos al Nodo-Destino final, existe un medio de transporte más rápido (avión o tren) con el fin de buscar el viaje más corto y rápido. Si este fuera el escenario se enviaría a la persona hasta ese nodo-vecino en cualquiera de esos dos medios de transporte, y luego al nodo del Nodo-Destino final en bus o en taxi. 

Posibles casos:
•	AVIONES Y TRENES: 
DIRECTO
Si el tipo de transporte es avión o tren y tanto en el nodo-origen como en el nodo-destino seleccionado por el usuario hay presentes alguno de estos dos tipos de transporte, el viaje será directo de un punto a otro, en caso del tren esta consulta las estaciones por las cuales pasa el tren hasta el nodo-destino.  

INDIRECTO
Nodo-Origen tiene tipo de transporte, pero nodo-destino no: 
Para este caso, ya que el nodo-destino no tiene el tipo de transporte avión o tren igual que el nodo-origen, este busca entre los vecinos del nodo-destino para así poder ver cual tiene estos tipos de transporte y si esto es verdadero el sistema hace que el usuario viaje del nodo-origen al nodo-vecino en avión o tren y posteriormente se dirija a el nodo-destino en bus o taxi. 
Nodo-destino tiene tipo transporte, pero nodo-origen no: 
Para este caso, ya que el nodo-origen no posee el tipo de transporte avión o tren igual que el nodo-destino, el sistema busca entre los vecinos del nodo-origen para así poder ver cual tiene estos tipos de transporte y si esto es verdadero el sistema hace que el usuario viaje del nodo-origen al nodo-vecino en taxi o bus y posteriormente se dirija a el nodo-vecino al nodo-destino en avión o tren. 
Nodo-origen no tiene tipo de transporte ni nodo-destino:  
Para esta posible situación, el sistema es capaz de buscar los nodos-vecinos de cada nodo (origen y destino), dirigiéndose de la siguiente manera: de nodo-origen a nodo-vecino en bus y taxi, de nodo-vecino de nodo-origen a nodo-vecino de nodo-destino en avión o tren, y por último de nodo-vecino de destino a nodo-destino en bus o taxi nuevamente. 
Si ninguna de las anteriores opciones se pudiera realizar, el sistema brinda un mensaje al usuario especificando que es imposible ir en Avión o Tren, verifique en Bus o Taxi. 

•	TAXIS y BUSES GENERAL
Primeramente, se toman los parámetros el nodo-origen y nodo-destino para determinar la ruta más corta mediante el algoritmo de Dijkstra.  Posteriormente, se obtiene la zona desde donde se requiere el servicio (nodo-origen) para ofrecer un taxi que opere en dicha zona. 

•	TAXIS
Para el caso de los taxis, el grafo se divide en tres zonas A, B y C, donde en cada zona se encuentran los taxis cercanos al nodo-origen y al nodo-destino. 

•	BUSES
El sistema busca los buses del nodo-origen y el nodo-destino. Al usuario reservar un espacio en el bus este debe asignarle el número de campo y reservarlo quitando la disponibilidad de este a otro usuario. 
