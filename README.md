
---

# Equipo [Team ValGrind]: WRO 2025

[![SAVE-20250527-193558.jpg](https://i.postimg.cc/VvXNFbns/SAVE-20250527-193558.jpg)](https://postimg.cc/fSTZzy81)

---

## Índice

1. [Nuestro Equipo](#nuestro-equipo)
    - [Integrantes](#integrantes)
    - [Origenes](#origenes)
    - [Nuestro Objetivo](#nuestro-objetivo)
2. [El Robot](#el-robot)
    - [Apartado Mecanico](#apartado-mecanico)
        - [Impresion 3D](#impresion-3d)
        - [Movilidad](#movilidad)
    - [Apartado Electronico](#apartado-electronico)
        - [Baterias](#baterias)
        - [Sensores](#sensores)
        - [Conexiones y Circuitos](#conexiones-y-circuitos)
        - [Microcontroladores](#microcontroladores)
    - [Apartado Programatico](#apartado-programatico)
        - [Codigo por Componente](#codigo-por-componente)
        - [Diagramas de Flujo](#diagramas-de-flujo)
4. [Recursos para Hacer el Robot](#recursos-para-hacer-el-robot)
    - [Mecanica](#mecanica)
    - [Electronica](#electronica)
    - [Programacion](#programacion)

---

## Nuestro Equipo

<img src="https://github.com/damuec/ValRepo1/assets/foto-equipo.jpg" alt="Foto del equipo" width="400"/>

Somos **[Team ValGrind]**, entusiastas de la robótica y la innovación. Representamos a nuestra institución en la fase regional de la **WRO 2025**.

---

### Integrantes

- **Samuel Burgos**  
  17 años, 09/01/2008  
<foto>

- **Sebastián Salina**  
  17 años, 22/08/2008 
<foto>

- **Cristobal Mogollón**
  14 años, 14/07/2010
 <foto>

- **Institución:** [Colegio Salto Ángel](https://www.instagram.com/colegiosaltoangel)
- **Instagram Oficial:** [@team_valgrind](https://instagram.com/team_valgrind)
- **Contáctanos:** [valgrind2025@gmail.com](mailto:valgrind2025@gmail.com)

---

### Origenes

El nombre de nuestro equipo fue decidido por los tres integrantes a partir de un clásico compilador de C++ llamado de la misma forma, el cual es representado por un logotipo de un dragón hecho con origami. El nombre "ValGrind" también hace referencia a la mitología nórdica debido a las legendarias Valquirias que habitan en este.

 [![images-18.jpg](https://i.postimg.cc/dQp02CyM/images-18.jpg)](https://postimg.cc/gryddns4)


> ### ¿Por qué nuestro robot se llama Heimdall?

Este nombre no solo es un guiño a la mitología mencionada, sino que además corresponde al dios conocido como el guardián de las puertas de Asgard y del puente Bifröst, que conecta los Nueve Mundos. Al ser un personaje imponente, consideramos que es un nombre apropiado para representar a nuestro robot en la WRO.


## Nuestro Objetivo

[![Logo-wro.png](https://i.postimg.cc/85CCHB4G/Logo-wro.png)](https://postimg.cc/t1LyR68v)

"Diseñar, Construir y Programar"

- Un robot autónomo capaz de superar los desafíos de la WRO 2025, utilizando innovación y trabajo en equipo para lograr un desempeño sobresaliente en la etapa regional y avanzar a la nacional. Para llegar a esto, hemos pasado los últimos meses diseñando, construyendo, armando y programando nuestro más nuevo proyecto "Heimdall"

La World Robot Olympiad (WRO) es una competencia internacional de robótica educativa que se desarrolla en varias fases, y nuestro equipo lógicamente tiene que comenzar por la fase regional, mediante la cual al ganarla se accede a la Fase Nacional. Cada país organiza su propio torneo clasificatorio, donde equipos de jóvenes compiten en distintas categorías, aplicando conocimientos de robótica y STEAM. Por último, la fase a la cual nuestro equipo quiere llegar es la Final Internacional. Los equipos ganadores de cada país participan en la competencia global, donde enfrentan desafíos más complejos y compiten con representantes de más de 95 países 

Aún así, nuestro único objetivo no es solamente ganar, como un equipo unido también tenemos la convicción de poder crear un robot no solo funcional, sino que llene nuestras expectativas; A pesar de ser intangible nuestro deseo de poder culminar nuestro proyecto como un equipo unido y verlo brillar, también es una meta importante para nosotros.

---

## El Robot

### Apartado Mecanico

#### Impresion 3D

Antes de hablar de la movilidad o funcionalidad de nuestro robot, primero hay que explicar nuestros métodos de Diseño e Impresión 3D, los cuales se llevaron a cabo mediante ```Fusion 360```

- Fusion 360 es una plataforma de software de modelado 3D, CAD, CAM, CAE y PCB basada en la nube, destinada al diseño y la fabricación de productos. Nos permite diseñar y crear productos de acuerdo a sus especificaciones particulares, garantizando que cada pieza cumpla con los más exigentes criterios de estética, forma, ajuste y funcionalidad. Además, incorpora un conjunto integral de herramientas avanzadas para el diseño de placas de circuito impreso y componentes electrónicos, lo que facilita la conceptualización y materialización de cualquier idea, incluso las más complejas. Al implementar estas funciones, la plataforma optimiza significativamente tanto el tiempo como los costos asociados, asegurando que el proceso de producción se realice de manera eficiente y que las piezas obtenidas sean de la más alta calidad. Nosotros usamos esta herramienta gráfica y de diseño para realizar los diseños del chasis y las piezas personalizadas de nuestro robot.

#### Diseño STL del Chasis de Heimdall

![Chasis 3D](https://github.com/damuec/ValRepo1/assets/chasis-3d.png)

#### Movilidad

Ahora bien, ya habiendo dilucidado las piezas que confirmarán nuestro robot, hay que asegurarnos de que este cuente con las herramientas necesarias para moverse y evadir los obstáculos de la pista.

Nuestro robot emplea un sistema de tracción diferencial, ofreciendo maniobrabilidad precisa para enfrentar los retos del campo de competencia. El sistema de cruces se realiza mediante un servo que ajusta la dirección del robot en intersecciones críticas.

El núcleo de la movilidad de nuestro robot reside en su **subsistema mecánico de transmisión y tracción**, cuidadosamente seleccionado con componentes específicos de alta calidad. Vamos a desglosar cómo cada pieza encaja en este rompecabezas de ingeniería en miniatura, usando la escala **1/18** como referencia clave para tamaño e integración:

1.  **Diferenciales (1/18)**
    *  Los ubicamos en el eje motriz , permiten que las ruedas izquierda y derecha giren a velocidades diferentes al tomar curvas. Esto es *crucial* para evitar que el robot "patine" o forcejee en giros cerrados, manteniendo la estabilidad incluso durante maniobras agresivas. Su escala 1/18 garantiza que sean compactos, ligeros y proporcionales al resto del chasis y ruedas del robot de competición.

2.  **Los Conductores de la Fuerza: Ejes de Transmisión (1/18)**
    *   Estos robustos ejes son las **arterias mecánicas**. Conectan directamente la salida de los diferenciales (1/18) a las ruedas motrices. Transfieren el par motor generado hacia las ruedas, haciendo girar los neumáticos. Su diseño a escala 1/18 asegura la longitud y resistencia adecuadas para soportar las fuerzas de torsión y tracción sin añadir peso excesivo ni desbalancear el robot.

3.  **El Corazón que Late: Motor Brushed Injora 180° 48T**
    *   Este motor de escobillas (brushed) es la **fuente de potencia controlada**. Sus características lo hacen ideal para WRO:
        *   **180°**: Indica que su cuerpo es más corto que un motor estándar (que suele ser ~360°), ahorrando espacio vital en un robot compacto.
        *   **48T (48 Vueltas)**: Se refiere al número de vueltas del devanado del inducido. Un motor de "mayor T" (como 48T) proporciona **más par (fuerza de torsión)** a velocidades más bajas, en comparación con motores de menor T (ej: 20T) que son más rápidos pero con menos fuerza. Este alto par es *esencial* para iniciar derrapes controlados, superar pequeñas irregularidades y proporcionar aceleración contundente, incluso con las ruedas de drift que ofrecen menos tracción.

4.  **El Contacto con el Suelo: Ruedas de Drift**
    *   Estas ruedas son el **elemento transformador clave para el derrape**. Están fabricadas típicamente con un compuesto plástico duro y liso (como ABS o PU). A diferencia de las ruedas de goma adherentes, estas **minimizan deliberadamente la fricción** con superficies como linóleo o parquet (comunes en pistas WRO). Esta baja tracción permite que las ruedas motrices (traseras) pierdan agarre de manera controlada cuando se aplica potencia y dirección, iniciando y manteniendo el derrape deseado. Su diámetro y ancho se eligen para complementar la escala 1/18 y el comportamiento dinámico del robot.

5.  **La Estructura Articulada: Nudillos de Cruce (y Portanudillos)**
    *   Estos componentes (a menudo incluyendo el "portanudillo" o "knuckle") son las **articulaciones sofisticadas** que conectan las ruedas al chasis. Permiten:
        *   **Dirección**: Giran las ruedas delanteras para cambiar la trayectoria.
        *   **Suspensión Básica**: Absorben pequeñas irregularidades y mantienen las ruedas en contacto con el suelo.
        *   **Ángulo de Derrape**: Un buen diseño permite ajustar el ángulo de giro máximo, crucial para lograr derrapes pronunciados y estables. Son el punto de anclaje crítico para los terminales de los ejes de transmisión y los tirantes de dirección.

6.  **La Suavidad del Giro: Rolineras (Rodamientos)**
    *   Estos pequeños anillos con bolas son **héroes silenciosos de la eficiencia**. Se instalan en:
        *   **Ruedas**: Para que giren libremente con mínima fricción.
        *   **Nudillos/Portanudillos**: Donde pivota el eje de dirección.
        *   **Ejes de Transmisión/Diferenciales**: Para soportar la rotación del eje dentro de su alojamiento.
    *   Reemplazar buches (bushings) de plástico o bronce por rolineras **reduce drásticamente la fricción**, permitiendo que más potencia del motor llegue a las ruedas, mejorando la aceleración, la velocidad máxima y la duración de la batería.

7.  **El Esqueleto Atornillado: Tornillos M3, Tuercas de Seguridad M2, Insertos Roscados M2**
    *   Estos son los **elementos de unión esenciales** que mantienen todo el sistema mecánico integrado y robusto:
        *   **Tornillos M3**: El "estándar" para ensamblar partes estructurales principales del chasis, motores, diferenciales y soportes. Su tamaño ofrece un buen equilibrio entre resistencia y peso.
        *   **Tuercas de Seguridad M2**: Diseñadas con un anillo de nylon que "aprieta" contra el tornillo al roscarse. Ideales para **fijar componentes sujetos a vibración intensa** (como el motor, las ruedas o electrónica), evitando que se aflojen durante maniobras bruscas o derrapes prolongados.
        *   **Insertos Roscados M2**: Pequeñas piezas metálicas que se presionan o atornillan en plástico. **Refuerzan los puntos de rosca** en piezas impresas en 3D o de plástico moldeado, permitiendo atornillar y desatornillar repetidamente (tornillos M2) sin dañar el agujero. Vital para uniones fiables en materiales más blandos.

8.  **La Fuente de Energía: Batería Urgenex Li-Ion 3000mAh**
    *   Esta batería de iones de litio es el **depósito de combustible compacto**. Sus características la hacen ideal para WRO:
        *   **Li-Ion**: Tecnología que ofrece una excelente relación capacidad/peso y densidad energética, sin el efecto memoria de las NiMH.
        *   **3000mAh**: Una capacidad alta para su tamaño (típico de escala 1/18), proporcionando **largos tiempos de operación** entre cargas, crucial para prácticas extensas y rondas de competición.
        *   **Voltaje (implícito)**: Generalmente 7.4V (2S) o 11.1V (3S), proporcionando el voltaje necesario para alimentar motores brushed como el Injora 48T y la electrónica de control con suficiente potencia.

---

### Apartado Electronico

#### Baterias

Para el proyecto, decidimos usar dos baterías:

- La primera es un paquete de 2 baterías recargables de 12 V con una capacidad nominal de 2000 mAh cada una. Utilizan tecnología de níquel-metal hidruro (NiMH), lo que elimina el efecto memoria y garantiza que, a pesar de repetidos ciclos de carga y descarga, la capacidad de energía se conserve de forma óptima. Con dimensiones aproximadas de 50 x 29 x 72 mm y cableado con cables desnudos, la batería permite una integración versátil y directa, lo cual facilita su integración dentro de nuestro proyecto sin afectar el rendimiento de otros componentes o el diseño.

<foto>

- La segunda es un kit de baterías recargables Tenergy, también de tecnología NiMH, diseñado para ofrecer una salida estable de 12 V y una capacidad de 2000 mAh por unidad en un formato compacto y robusto, que facilita su integración en proyectos de electrónica y robótica gracias a sus cables desnudos para conexiones directas. Garantizando una carga rápida y un suministro energético continuo y fiable, este kit nos resulta ideal para aplicaciones exigentes como las competencias de robótica en nuestra categoría, donde es imperativo optimizar tanto el rendimiento del sistema como los tiempos de montaje y costos operativos.

<fotos>

#### Sensores 

El robot cuenta con múltiples sensores ultrasónicos (HC-SR04) ubicados estratégicamente para la detección de obstáculos y el cálculo de distancias, permitiendo navegación autónoma y segura. El sensor HC-SR04 es un sensor de distancia de bajo costo, por lo que su uso es muy frecuente en la robótica. Incorpora un par de transductores de ultrasonido que se utilizan de manera conjunta para determinar la distancia del sensor con un objeto colocado frente a este. Un transductor emite una ráfaga de ultrasonido y el otro capta el rebote de dicha onda.

El tiempo que tarda la onda sonora en ir y regresar a un objeto puede utilizarse para conocer la distancia entre el origen del sonido y el objeto. La interfaz del sensor HC-SR04 y Arduino se logra mediante 2 pines digitales: el pin de disparo (trigger) y el pin de eco (echo). La función de cada uno de estos pines es la siguiente:

- El pin trigger recibe un pulso de habilitación del microcontrolador, mediante el cual se le indica al módulo que comience a realizar la medición de distancia.
- En el pin echo el sensor devuelve al microcontrolador un pulso cuyo ancho es proporcional al tiempo que tarda el sonido en viajar del transductor al obstáculo y luego de vuelta al módulo.

#### Conexiones y Circuitos

Todos los módulos están conectados en un circuito organizado, minimizando interferencias y facilitando el mantenimiento.  

[Ver diagrama del circuito](./docs/diagrama-electronico.png)

#### Microcontroladores

Utilizamos ESP32.

---

### Apartado Programatico

#### Codigo por Componente

En cuanto al código utilizado para manejar el robot, consiste en una parte en la que se definen los pines del BNO085, del ESC y de los ultrasónicos. Dentro del código se arma el ESC, se inicializan los sensores y se inicializa una función llamada "doceVueltas", la cual se encarga de hacer una lectura constante de los sensores ultrasónicos para decidir en qué momento girar, así como de registrar los giros para que el robot se detenga al completar exitosamente 3 vueltas.

En este apartado se inicializan los pines:
```cpp
void setup() {
  Wire.begin(SDA_PIN, SCL_PIN);  // Inicializar I2C con pines específicos
  esc.attach(PIN_ESC, 1000, 2000);
  myservo.attach(PIN_SERVO);
  Serial.begin(115200);

  // Inicializar BNO085
  if (!bno08x.begin_I2C(0x4B, &Wire)) {
    Serial.println("¡No se pudo iniciar el BNO08x!");
    while(1);
  }
  bno08x.enableReport(SH2_GYROSCOPE_CALIBRATED, 10000);

  // Armar el ESC al iniciar
  esc.write(90);
  delay(3000);

  tiempoAnterior = millis();
}
```

En este apartado, se llama a la función `doceVueltas`, se hace una lectura de los sensores y se calibra el giroscopio:

```cpp
void loop() {
  doceVueltas();
}

void doceVueltas() {
  if (robotDetenido) {
    // Robot detenido, no hacer nada más
    return;
  }

  int frontal = USFront.read();
  int izquierda = USLeft.read();
  int derecha = USRight.read();

  // Leer datos del giroscopio del BNO085 y acumular el ángulo girado en el eje Z
  unsigned long tiempoActual = millis();
  float deltaTime = (tiempoActual - tiempoAnterior) / 1000.0; // segundos
  tiempoAnterior = tiempoActual;

  if (bno08x.getSensorEvent(&sensorValue)) {
    if (sensorValue.sensorId == SH2_GYROSCOPE_CALIBRATED) {
      float gyroZ = sensorValue.un.gyroscope.z * 57.3; // Convertir a dps
      anguloAcumuladoZ += gyroZ * deltaTime; // Acumula el ángulo en el eje Z (con signo)
    }
  }
}
```

Dentro de `Open.ino` está el resto de funciones descritas, y la lógica de programación mediante la cual el robot completa el desafío abierto.

#### Diagramas de Flujo

En este diagrama de flujo se halla una representación gráfica del funcionamiento lógico de nuestra programación, así como de lo que se espera sea el desempeño del robot al inicializar el programa.

[![IMG-20250523-WA0008.jpg](https://i.postimg.cc/QxYhNwBT/IMG-20250523-WA0008.jpg)](https://postimg.cc/YhFJbXzr)

#### Compiladores y Comunicacion

- **Lenguaje principal:** C++ (Arduino IDE)
- **Compilador:** [Arduino IDE](https://www.arduino.cc/en/software)
- **Comunicación entre módulos:** Bus I2C y SPI

---

## Recursos para Hacer el Robot

### Mecánico
- Diferenciales 1/28
- Ejes de Transmisión 1/18
- Motor Brushed Injora 180° 48T
- Ruedas de Drift 1/18
- Tuercas de Seguridad M2
- Tornillos M3
- Incertos Roscados M2
- Nudillos de Cruce
- Rolineras
- Urgenex Li-Ion 3000mAh
### Electrónico 
- ESP-32
- BNO085
- Ultrasónicos HSR04
### Programación 
- Abierta.ino
- Cerrada.ino
- Pixytest.ino



- [Lista de materiales detallada](./docs/lista-componentes.md)
- [Archivos STL para impresión 3D](./3d/)

---

> _¿Quieres contribuir o seguir nuestro avance? Síguenos en nuestras redes oficiales y revisa este repositorio para novedades y recursos._

---
