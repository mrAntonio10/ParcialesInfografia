Nombre: Marco Antonio Roca Montenegro  
	Codigo: 55995
Universidad Privada Boliviana
Docente: Jose Eduardo Laruta Espejo

	Materia: Infografia 2023
	Fecha: 15/04/2023


El presente proyecto utiliza el lenguaje de programacion Python:
	Version utilizada: 3.11.1

En un comienzo queria avanzar con un proyecto al estilo Contra; en dicho videojuego
se utiliza una mecanica de disparos tomando en cuenta un angulo del pixel de la "pistola".
	Mis limitantes: Realizar el cambio de imagen para mostrar en pantalla el angulo
		donde la pistola estaba apuntando.
		
		Tener un mapa que responda a una pantalla que se mueva conforme al personaje.



Sin embargo, gracias al docente pude hacer uso de una ESCENA que se mueva junto con el personaje
	utilizando los "resources maps" de Python.

				//EL JUEGO//

Nombre: Dwolf -> Tematica pensada en un juego retro donde aparecen Demonios.
	Wolf, por uno de mis videojuegos favoritos: Wolfenstein.

El juego se basa en un mapa, el cual va generando enemigos:
	* Normales
	* Fuertes
Cada uno con sus respectivas vidas o "aguante".

Tenemos nuestro personaje principal "Storm" el cual, con su habilidad de disparar
"Ojos" tiene que eliminar a todos los enemigos.

	OJO: Cuando un enemigo logra pasar de un extremo a otro, comienza a reducir
	la vitalidad de nuestro personaje.

Utilice: Un repositorio de arcade en el cual se definen:	
	* Sprites
	* Escenas
	* PhysicsEnginePlatformer

Limitantes: 
	* Queria tener una pantalla que muestre "Game Over" y despues de 5 segundos se cierre el juego
	* Que la implementacion de detectar al personaje para que no se pierda en pantalla funcione todo el tiempo.

Futuras implementaciones:
	Que la vitalidad del personaje y de los enemigos sea una barra que se actualice en la Scena SOBRE nuestros objetos.
--Hice uso de un codigo que toma en cuenta una barra de vitalidad, pero esta al dibujarse en pantalla era estatico...
	(No se movia junto con nuestros objetos).

