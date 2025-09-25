#include <Wire.h>
#include <ESP32Servo.h>
#include <SPI.h>
#include <Pixy2SPI_SS.h>
#include <NewPing.h>
#include <MPU6050_light.h>
#include <SD.h>

// ========== CONFIGURACIÓN DE PINES ==========
// Pines de motor y servo
#define IN1 16
#define IN2 17
#define MOTOR_PWM_CHANNEL 6
#define MOTOR_PWM_PIN IN1
#define PIN_SERVO 2
#define PIN_BOTON 15

// Pines de sensores ultrasónicos
#define USTLEFT 14
#define USELEFT 27
#define USTRIGHT 25
#define USERIGHT 26
#define USTFRONT 12
#define USEFRONT 13
#define MAX_DISTANCE 357

// Pines CS para SPI
#define SD_CS   4   // GPIO4
#define PIXY_CS 5   // GPIO5

// Pines SPI
#define VSPI_MISO 19  // GPIO19 - MISO
#define VSPI_MOSI 23  // GPIO23 - MOSI  
#define VSPI_SCK  18  // GPIO18 - SCK
#define HSPI_MISO 39  // GPIO39- MISO
#define HSPI_MOSI 32  // GPIO32 - MOSI  
#define HSPI_SCK  33  // GPIO33 - SCK

// ========== OBJETOS ==========
NewPing sensorFront(USTFRONT, USEFRONT, MAX_DISTANCE);
NewPing sensorIzq(USTLEFT, USELEFT, MAX_DISTANCE);
NewPing sensorDer(USTRIGHT, USERIGHT, MAX_DISTANCE);
MPU6050 mpu(Wire);
Servo myservo;
Pixy2SPI_SS pixy;

// Segundo bus SPI para SD
SPIClass hspi(HSPI);

// ========== PARÁMETROS PID GIROSCOPIO ==========
const int CORRECCION_MAX = 15; 
const float kP = 1.3;
const float kI = 0.01;
const float kD = 0.11;
const int DEAD_BAND_CORRECCION = 3;

// ========== VELOCIDADES ==========
int velocidadNormal = 150;
int velocidadReversa = 100;
int velocidadGiro = 150;

// ========== PARÁMETROS DE CONTROL ==========
const int ANGULO_CENTRO = 98;
const int ANGULO_MAX = 128;
const int ANGULO_MIN = 68;

// ========== PARÁMETROS DE ESQUIVA ==========
const int ANGULO_ESQUIVA_PRIMARIO = 25;
const int ANGULO_ESQUIVA_SECUNDARIO = 20;
const unsigned long TIEMPO_RECTA_ENTRE_GIROS = 100;

// ========== TIEMPOS DE ESQUIVA DIFERENTES PARA VERDE Y ROJO ==========
// ESQUIVA VERDE (más larga/más pronunciada)
const unsigned long TIEMPO_ESQUIVA_PRIMARIA_VERDE = 570; 
const unsigned long TIEMPO_ESQUIVA_SECUNDARIA_VERDE = 580; 

// ESQUIVA ROJO (mantenemos los originales o ajustamos)
const unsigned long TIEMPO_ESQUIVA_PRIMARIA_ROJO = 650;  
const unsigned long TIEMPO_ESQUIVA_SECUNDARIA_ROJO = 580; 

// ========== NUEVOS PARÁMETROS PARA ESQUIVAS PREVENTIVAS ==========
const unsigned long TIEMPO_ESQUIVA_PREVENTIVA = 400;
const int ANGULO_ESQUIVA_PREVENTIVA = 20;  

// ========== TIEMPOS DE MANIOBRAS ==========
const unsigned long TIEMPO_ESQUIVA_VERDE = TIEMPO_ESQUIVA_PRIMARIA_VERDE + TIEMPO_RECTA_ENTRE_GIROS + TIEMPO_ESQUIVA_SECUNDARIA_VERDE;
const unsigned long TIEMPO_ESQUIVA_ROJO = TIEMPO_ESQUIVA_PRIMARIA_ROJO + TIEMPO_RECTA_ENTRE_GIROS + TIEMPO_ESQUIVA_SECUNDARIA_ROJO;
const unsigned long TIEMPO_POST_ESQUIVA_VERDE = 100;
const unsigned long TIEMPO_POST_ESQUIVA_ROJO = 150;
const unsigned long TIEMPO_GIRO_DERECHA_VERDE = 800;
const unsigned long TIEMPO_GIRO_IZQUIERDA_VERDE = 500;
const unsigned long TIEMPO_GIRO_IZQUIERDA_ROJO = 650;
const unsigned long TIEMPO_GIRO_DERECHA_ROJO = 500;
const unsigned long TIEMPO_RETROCESO = 1100;
const unsigned long TIEMPO_RETROCESO_FINAL = 1300;

// ========== UMBRALES DE DETECCIÓN ==========
const int UMBRAL_TAMANO_BLOQUE_VERDE = 920;
const int UMBRAL_TAMANO_BLOQUE_ROJO = 820;
const int OBSTACULO_FRONTAL = 25;
const int UMBRAL_CENTRO_PIXY = 15;

// ========== ESTADOS DEL ROBOT ==========
enum Estado {
  DETENIDO,
  AVANZAR,
  ESQUIVAR_VERDE_IZQ,
  ESQUIVAR_ROJO_DER,
  ESQUIVA_PREVENTIVA_VERDE_DER,
  ESQUIVA_PREVENTIVA_ROJO_IZQ,
  POST_ESQUIVA_VERDE,
  POST_ESQUIVA_ROJO,
  GIRO_SERVO,
  RETROCEDER_CON_GIRO,
  RETROCEDER_FINAL,
  REAJUSTAR_POSICION,
  CALIBRAR_GIROSCOPIO
};

// ========== VARIABLES GLOBALES ==========
Estado estadoActual = DETENIDO;
bool bloqueVerdeDetectado = false;
bool bloqueRojoDetectado = false;
bool bloqueVerdeCercano = false;
bool bloqueRojoCercano = false;
int posicionBloqueX = 0;
int ladoMasLibre = 0;
int ultimoGiro = 0;

// Variables giroscopio
float offsetAngleZ = 0;
bool calibrado = false;
bool usarCorreccionGiroscopio = false;
unsigned long tiempoCalibracionInicio = 0;
const unsigned long DURACION_CALIBRACION = 10000;

// Variables PID
float integralError = 0;
float prevError = 0;
unsigned long prevTime = 0;

// Variables para el control de movimiento por tiempo
unsigned long tiempoInicioManiobra = 0;
unsigned long tiempoFaseActual = 0;

// Variables para dispositivos
bool sdInicializada = false;
bool pixyInicializada = false;

// ========== FUNCIONES AUXILIARES ==========
void avanzar();
void retroceder();
void detenerRobot();
void leerPixy();
void aplicarCorreccionGiroscopio();
bool guardarCalibracion(float offset);
bool cargarCalibracion(float &offset);
void reiniciarGiroscopio();
void resetearAcumuladorAngulo();
void emergencyStop();
void borrarCalibracionCorrupta();

void setup() {
  Serial.begin(115200);
  Serial.println("=== INICIANDO SISTEMA ===");
  
  // 1. Configurar pines
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(PIN_BOTON, INPUT_PULLUP);
  pinMode(SD_CS, OUTPUT);
  pinMode(PIXY_CS, OUTPUT);
  
  // Asegurar CS en HIGH inicialmente
  digitalWrite(SD_CS, HIGH);
  digitalWrite(PIXY_CS, HIGH);
  
  // Configurar servo y motor
  myservo.attach(PIN_SERVO);
  myservo.write(ANGULO_CENTRO);
  ledcSetup(MOTOR_PWM_CHANNEL, 5000, 8);
  ledcAttachPin(MOTOR_PWM_PIN, MOTOR_PWM_CHANNEL);
  detenerRobot();
  
  // 2. Inicializar MPU6050
  Wire.begin();
  byte status = mpu.begin();
  Serial.print("MPU6050: ");
  if (status == 0) {
    mpu.calcOffsets();
    Serial.println("OK");
  } else {
    Serial.println("ERROR");
  }

  // 3. INICIALIZAR PIXY CON VSPI
  Serial.print("Iniciando Pixy...");
  
  // Configurar VSPI para Pixy
  SPI.begin(VSPI_SCK, VSPI_MISO, VSPI_MOSI, PIXY_CS);
  SPI.setFrequency(1000000);
  
  digitalWrite(SD_CS, HIGH);
  digitalWrite(PIXY_CS, LOW);
  delay(100);
  
  int pixyResult = pixy.init();
  if (pixyResult == 0) {
    pixy.setLamp(1, 1);
    pixyInicializada = true;
    Serial.println(" OK");
    Serial.print("Pixy firmware: ");
    Serial.print(pixy.version->firmwareMajor);
    Serial.print(".");
    Serial.print(pixy.version->firmwareMinor);
    Serial.print(".");
    Serial.println(pixy.version->firmwareBuild);
  } else {
    Serial.print(" ERROR: ");
    Serial.println(pixyResult);
  }
  digitalWrite(PIXY_CS, HIGH);
  
  // 4. INICIALIZAR SD CON HSPI
  Serial.print("Iniciando SD...");
  
  // Configurar HSPI para SD
  hspi.begin(HSPI_SCK, HSPI_MISO, HSPI_MOSI, SD_CS);
  hspi.setFrequency(1000000); // 1MHz
  
  // Intentar inicializar SD
  if (!SD.begin(SD_CS, hspi)) {
    Serial.println(" ERROR en primera prueba");
    
    // Intentar con frecuencia más baja
    hspi.setFrequency(500000);
    if (SD.begin(SD_CS, hspi)) {
      sdInicializada = true;
      Serial.println(" OK con 500kHz");
    } else {
      Serial.println(" ERROR definitivo");
      sdInicializada = false;
    }
  } else {
    sdInicializada = true;
    Serial.println(" OK con 1MHz");
  }

  // Borrar calibración corrupta si existe
  if (sdInicializada) {
    borrarCalibracionCorrupta();
  }

  // Verificar escritura en SD
  if (sdInicializada) {
    File testFile = SD.open("/test.txt", FILE_WRITE);
    if (testFile) {
      testFile.println("Sistema iniciado correctamente");
      testFile.close();
      Serial.println("Escritura SD: OK");
    } else {
      Serial.println("Escritura SD: ERROR");
      sdInicializada = false;
    }
  }
  
  prevTime = millis();
  Serial.println("=== SISTEMA INICIALIZADO ===");
  Serial.println("Pixy: " + String(pixyInicializada ? "OK" : "NO"));
  Serial.println("SD: " + String(sdInicializada ? "OK" : "NO"));
  Serial.println("Presione botón para comenzar...");
}

void loop() {
  // Leer estado del botón
  if (digitalRead(PIN_BOTON) == LOW && estadoActual == DETENIDO) {
    // Intentar cargar calibración previa solo si SD está OK
    if (sdInicializada) {
      if (cargarCalibracion(offsetAngleZ)) {
        calibrado = true;
        usarCorreccionGiroscopio = true;
        estadoActual = AVANZAR;
        Serial.println("Calibración cargada desde SD, iniciando movimiento");
      } else {
        // No había calibración previa o estaba corrupta, necesitamos calibrar
        estadoActual = CALIBRAR_GIROSCOPIO;
        tiempoCalibracionInicio = millis();
        Serial.println("Iniciando calibración giroscopio...");
      }
    } else {
      // SD no disponible, necesitamos calibrar
      estadoActual = CALIBRAR_GIROSCOPIO;
      tiempoCalibracionInicio = millis();
      Serial.println("SD no disponible, iniciando calibración giroscopio...");
    }
    delay(300); // Debounce del botón
  }
  
  // Actualizar MPU
  mpu.update();
  
  // Leer sensores ultrasónicos
  int distanciaFrontal = sensorFront.ping_cm();
  int distanciaIzquierda = sensorIzq.ping_cm();
  int distanciaDerecha = sensorDer.ping_cm();
  
  // Leer datos de Pixy (solo si está inicializada)
  if (pixyInicializada && estadoActual != ESQUIVAR_VERDE_IZQ && estadoActual != ESQUIVAR_ROJO_DER && 
      estadoActual != ESQUIVA_PREVENTIVA_VERDE_DER && estadoActual != ESQUIVA_PREVENTIVA_ROJO_IZQ &&
      estadoActual != POST_ESQUIVA_VERDE && estadoActual != POST_ESQUIVA_ROJO &&
      estadoActual != CALIBRAR_GIROSCOPIO) {
    leerPixy();
  }
  
  // Mostrar información de depuración
  if (millis() % 1000 < 50) {
    Serial.print("Estado: ");
    Serial.print(estadoActual);
    Serial.print(" | Frontal: ");
    Serial.print(distanciaFrontal);
    Serial.print("cm | Izq: ");
    Serial.print(distanciaIzquierda);
    Serial.print("cm | Der: ");
    Serial.print(distanciaDerecha);
    Serial.print("cm | Verde: ");
    Serial.print(bloqueVerdeDetectado);
    Serial.print(" | Rojo: ");
    Serial.print(bloqueRojoDetectado);
    Serial.print(" | PosX: ");
    Serial.print(posicionBloqueX);
    Serial.print(" | Giroscopio: ");
    Serial.print(calibrado ? "Calibrado" : "NoCalibrado");
    Serial.print(" | Correccion: ");
    Serial.print(usarCorreccionGiroscopio ? "ON" : "OFF");
    Serial.print(" | ÚltimoGiro: ");
    Serial.print(ultimoGiro);
    Serial.print(" | SD: ");
    Serial.print(sdInicializada ? "OK" : "ERROR");
    Serial.print(" | Pixy: ");
    Serial.println(pixyInicializada ? "OK" : "ERROR");
  }
  
  // Máquina de estados del robot
  switch (estadoActual) {
    case DETENIDO:
      detenerRobot();
      break;
      
    case CALIBRAR_GIROSCOPIO:
      tiempoFaseActual = millis() - tiempoCalibracionInicio;
      detenerRobot();
      
      if (tiempoFaseActual < DURACION_CALIBRACION) {
        if (millis() % 1000 < 50) {
          Serial.print("Calibrando... ");
          Serial.print(int(tiempoFaseActual / 1000));
          Serial.println(" seg");
        }
      } else {
        if (sdInicializada) {
          if (guardarCalibracion(0)) {
            if (cargarCalibracion(offsetAngleZ)) {
              calibrado = true;
              usarCorreccionGiroscopio = true;
              reiniciarGiroscopio();
              estadoActual = AVANZAR;
              Serial.println("✓ Calibración precisa completada y giroscopio reiniciado");
            }
          }
        } else {
          // Fallback sin SD
          mpu.update();
          offsetAngleZ = mpu.getAngleZ();
          calibrado = true;
          usarCorreccionGiroscopio = true;
          reiniciarGiroscopio();
          estadoActual = AVANZAR;
        }
      }
      break;
      
    case AVANZAR:
      // Aplicar corrección de giroscopio solo si está calibrado and activado
      if (calibrado && usarCorreccionGiroscopio) {
        aplicarCorreccionGiroscopio();
      } else {
        // Sin corrección, avanzar recto
        myservo.write(ANGULO_CENTRO);
        avanzar();
      }
      
      // Verificar obstáculos y tomar decisiones
      if (distanciaFrontal > 0 && distanciaFrontal < OBSTACULO_FRONTAL) {
        if (!bloqueVerdeDetectado && !bloqueRojoDetectado) {
          // Usar el último giro como prioridad si existe
          if (ultimoGiro != 0) {
            ladoMasLibre = ultimoGiro;
            Serial.print("Usando último giro recordado: ");
            Serial.println(ultimoGiro == 1 ? "Derecha" : "Izquierda");
          } 
          // Si no hay último giro, decidir basado en distancias
          else if (distanciaIzquierda > distanciaDerecha + 5) {
            ladoMasLibre = 1;
          } else if (distanciaDerecha > distanciaIzquierda + 5) {
            ladoMasLibre = -1;
          } 
          // Si no hay diferencia clara, girar a la izquierda por defecto
          else {
            ladoMasLibre = -1;
          }
          
          // Guardar el giro actual como último giro
          ultimoGiro = ladoMasLibre;
          
          // Desactivar corrección durante giro
          usarCorreccionGiroscopio = false;
          estadoActual = GIRO_SERVO;
          tiempoInicioManiobra = millis();
          Serial.println("Obstáculo frontal detectado, girando servo");
        }
      }
      
      // Comportamiento según color detectado y posición
      if (bloqueVerdeDetectado && bloqueVerdeCercano) {
        if (posicionBloqueX == 1) {
          // NUEVO: Esquiva preventiva para verde a la derecha
          usarCorreccionGiroscopio = false;
          estadoActual = ESQUIVA_PREVENTIVA_VERDE_DER;
          tiempoInicioManiobra = millis();
          Serial.println("Verde detectado a la derecha, esquiva preventiva a izquierda");
        } else if (posicionBloqueX == -1) {
          // Desactivar corrección durante esquiva
          usarCorreccionGiroscopio = false;
          estadoActual = ESQUIVAR_VERDE_IZQ;
          tiempoInicioManiobra = millis();
          Serial.println("Verde detectado a la izquierda, iniciando esquiva");
        } else if (posicionBloqueX == 0) {
          // Bloque verde en el centro
          Serial.println("Verde detectado en centro, decidiendo dirección...");
          if (ultimoGiro != 0) {
            if (ultimoGiro == -1) {
              estadoActual = ESQUIVAR_VERDE_IZQ;
            } else {
              estadoActual = ESQUIVAR_VERDE_IZQ;
            }
          } else if (distanciaIzquierda > distanciaDerecha + 5) {
            estadoActual = ESQUIVAR_VERDE_IZQ;
          } else {
            estadoActual = ESQUIVAR_VERDE_IZQ;
          }
          usarCorreccionGiroscopio = false;
          tiempoInicioManiobra = millis();
        }
      } else if (bloqueRojoDetectado && bloqueRojoCercano) {
        if (posicionBloqueX == -1) {
          // NUEVO: Esquiva preventiva para rojo a la izquierda
          usarCorreccionGiroscopio = false;
          estadoActual = ESQUIVA_PREVENTIVA_ROJO_IZQ;
          tiempoInicioManiobra = millis();
          Serial.println("Rojo detectado a la izquierda, esquiva preventiva a derecha");
        } else if (posicionBloqueX == 1) {
          // Desactivar corrección durante esquiva
          usarCorreccionGiroscopio = false;
          estadoActual = ESQUIVAR_ROJO_DER;
          tiempoInicioManiobra = millis();
          Serial.println("Rojo detectado a la derecha, iniciando esquiva");
        } else if (posicionBloqueX == 0) {
          // Bloque rojo en el centro
          Serial.println("Rojo detectado en centro, decidiendo dirección...");
          if (ultimoGiro != 0) {
            if (ultimoGiro == 1) {
              estadoActual = ESQUIVAR_ROJO_DER;
            } else {
              estadoActual = ESQUIVAR_ROJO_DER;
            }
          } else if (distanciaDerecha > distanciaIzquierda + 5) {
            estadoActual = ESQUIVAR_ROJO_DER;
          } else {
            estadoActual = ESQUIVAR_ROJO_DER;
          }
          usarCorreccionGiroscopio = false;
          tiempoInicioManiobra = millis();
        }
      }
      break;
      
    case ESQUIVA_PREVENTIVA_VERDE_DER:
      tiempoFaseActual = millis() - tiempoInicioManiobra;
      
      if (tiempoFaseActual < TIEMPO_ESQUIVA_PREVENTIVA) {
        // Girar suavemente a la izquierda para evitar bloque verde a la derecha
        myservo.write(ANGULO_CENTRO + ANGULO_ESQUIVA_PREVENTIVA); // 98 - 15 = 83°
        avanzar();
        Serial.println("Esquiva preventiva: Girando a izquierda para evitar verde derecho");
      } else {
        // Volver a la navegación normal
        myservo.write(ANGULO_CENTRO);
        estadoActual = AVANZAR;
        usarCorreccionGiroscopio = true;
        Serial.println("Esquiva preventiva completada, volviendo a navegación normal");
      }
      break;

    case ESQUIVA_PREVENTIVA_ROJO_IZQ:
      tiempoFaseActual = millis() - tiempoInicioManiobra;
      
      if (tiempoFaseActual < TIEMPO_ESQUIVA_PREVENTIVA) {
        // Girar suavemente a la derecha para evitar bloque rojo a la izquierda
        myservo.write(ANGULO_CENTRO - ANGULO_ESQUIVA_PREVENTIVA); // 98 + 15 = 113°
        avanzar();
        Serial.println("Esquiva preventiva: Girando a derecha para evitar rojo izquierdo");
      } else {
        // Volver a la navegación normal
        myservo.write(ANGULO_CENTRO);
        estadoActual = AVANZAR;
        usarCorreccionGiroscopio = true;
        Serial.println("Esquiva preventiva completada, volviendo a navegación normal");
      }
      break;
      
    case ESQUIVAR_VERDE_IZQ:
      // Esquiva para bloque verde a la izquierda (SIN corrección de giroscopio)
      tiempoFaseActual = millis() - tiempoInicioManiobra;
      
      if (tiempoFaseActual < TIEMPO_ESQUIVA_PRIMARIA_VERDE) {
        myservo.write(ANGULO_CENTRO + ANGULO_ESQUIVA_PRIMARIO);
        avanzar();
        Serial.println("Fase 1 VERDE: Esquivando a la derecha");
      } else if (tiempoFaseActual < TIEMPO_ESQUIVA_PRIMARIA_VERDE + TIEMPO_RECTA_ENTRE_GIROS) {
        myservo.write(ANGULO_CENTRO);
        avanzar();
        Serial.println("Fase 2 VERDE: Avanzando recto");
      } else if (tiempoFaseActual < TIEMPO_ESQUIVA_VERDE) {
        myservo.write(ANGULO_CENTRO - ANGULO_ESQUIVA_SECUNDARIO);
        avanzar();
        Serial.println("Fase 3 VERDE: Re-centrando a la izquierda");
      } else {
        estadoActual = POST_ESQUIVA_VERDE;
        tiempoInicioManiobra = millis();
        Serial.println("Esquiva verde completada, iniciando secuencia post-esquiva");
      }
      break;
      
    case POST_ESQUIVA_VERDE:
      // Secuencia post-esquiva verde (SIN corrección de giroscopio)
      tiempoFaseActual = millis() - tiempoInicioManiobra;
      
      if (tiempoFaseActual < TIEMPO_POST_ESQUIVA_VERDE) {
        myservo.write(ANGULO_CENTRO);
        avanzar();
        Serial.println("Post-esquiva verde: Avanzando recto");
      } else if (tiempoFaseActual < TIEMPO_POST_ESQUIVA_VERDE + TIEMPO_GIRO_DERECHA_VERDE) {
        myservo.write(ANGULO_CENTRO - ANGULO_ESQUIVA_PRIMARIO);
        avanzar();
        Serial.println("Post-esquiva verde: Girando a la derecha");
      } else if (tiempoFaseActual < TIEMPO_POST_ESQUIVA_VERDE + TIEMPO_GIRO_DERECHA_VERDE + TIEMPO_RECTA_ENTRE_GIROS) {
        myservo.write(ANGULO_CENTRO);
        avanzar();
        Serial.println("Post-esquiva verde: Centrando servo");
      } else if (tiempoFaseActual < TIEMPO_POST_ESQUIVA_VERDE + TIEMPO_GIRO_DERECHA_VERDE + TIEMPO_RECTA_ENTRE_GIROS + TIEMPO_GIRO_IZQUIERDA_VERDE) {
        myservo.write(ANGULO_CENTRO + ANGULO_ESQUIVA_PRIMARIO);
        avanzar();
        Serial.println("Post-esquiva verde: Girando a la izquierda");
      } else {
        // Volver a avanzar normalmente SIN recalibrar
        myservo.write(ANGULO_CENTRO);
        estadoActual = AVANZAR;
        usarCorreccionGiroscopio = true; // Reactivar corrección
        Serial.println("Secuencia post-esquiva completada, avanzando normalmente");
      }
      break;
      
    case ESQUIVAR_ROJO_DER:
      // Esquiva para bloque rojo a la derecha (SIN corrección de giroscopio)
      tiempoFaseActual = millis() - tiempoInicioManiobra;
      
      if (tiempoFaseActual < TIEMPO_ESQUIVA_PRIMARIA_ROJO) {
        myservo.write(ANGULO_CENTRO - ANGULO_ESQUIVA_PRIMARIO);
        avanzar();
        Serial.println("Fase 1 ROJO: Esquivando a la izquierda");
      } else if (tiempoFaseActual < TIEMPO_ESQUIVA_PRIMARIA_ROJO + TIEMPO_RECTA_ENTRE_GIROS) {
        myservo.write(ANGULO_CENTRO);
        avanzar();
        Serial.println("Fase 2 ROJO: Avanzando recto");
      } else if (tiempoFaseActual < TIEMPO_ESQUIVA_ROJO) {
        myservo.write(ANGULO_CENTRO + ANGULO_ESQUIVA_SECUNDARIO);
        avanzar();
        Serial.println("Fase 3 ROJO: Re-centrando a la derecha");
      } else {
        estadoActual = POST_ESQUIVA_ROJO;
        tiempoInicioManiobra = millis();
        Serial.println("Esquiva rojo completada, iniciando secuencia post-esquiva");
      }
      break;
      
    case POST_ESQUIVA_ROJO:
      // Secuencia post-esquiva rojo (SIN corrección de giroscopio)
      tiempoFaseActual = millis() - tiempoInicioManiobra;
      
      if (tiempoFaseActual < TIEMPO_POST_ESQUIVA_ROJO) {
        myservo.write(ANGULO_CENTRO);
        avanzar();
        Serial.println("Post-esquiva rojo: Avanzando recto");
      } else if (tiempoFaseActual < TIEMPO_POST_ESQUIVA_ROJO + TIEMPO_GIRO_IZQUIERDA_ROJO) {
        myservo.write(ANGULO_CENTRO + ANGULO_ESQUIVA_PRIMARIO);
        avanzar();
        Serial.println("Post-esquiva rojo: Girando a la izquierda");
      } else if (tiempoFaseActual < TIEMPO_POST_ESQUIVA_ROJO + TIEMPO_GIRO_IZQUIERDA_ROJO + TIEMPO_RECTA_ENTRE_GIROS) {
        myservo.write(ANGULO_CENTRO);
        avanzar();
        Serial.println("Post-esquiva rojo: Centrando servo");
      } else if (tiempoFaseActual < TIEMPO_POST_ESQUIVA_ROJO + TIEMPO_GIRO_IZQUIERDA_ROJO + TIEMPO_RECTA_ENTRE_GIROS + TIEMPO_GIRO_DERECHA_ROJO) {
        myservo.write(ANGULO_CENTRO - ANGULO_ESQUIVA_PRIMARIO);
        avanzar();
        Serial.println("Post-esquiva rojo: Girando a la derecha");
      } else {
        // Volver a avanzar normalmente SIN recalibrar
        myservo.write(ANGULO_CENTRO);
        estadoActual = AVANZAR;
        usarCorreccionGiroscopio = true; // Reactivar corrección
        Serial.println("Secuencia post-esquiva completada, avanzando normalmente");
      }
      break;
      
    case GIRO_SERVO:
      if (ladoMasLibre == -1) {
        myservo.write(ANGULO_MAX);
        Serial.println("Servo girado a derecha (contrario a izquierda libre)");
      } else {
        myservo.write(ANGULO_MIN);
        Serial.println("Servo girado a izquierda (contrario a derecha libre)");
      }
      
      estadoActual = RETROCEDER_CON_GIRO;
      tiempoInicioManiobra = millis();
      break;
      
    case RETROCEDER_CON_GIRO:
      tiempoFaseActual = millis() - tiempoInicioManiobra;
      
      if (tiempoFaseActual < TIEMPO_RETROCESO) {
        retroceder();
        Serial.println("Retrocediendo con servo girado");
      } else {
        myservo.write(ANGULO_CENTRO);
        estadoActual = RETROCEDER_FINAL;
        tiempoInicioManiobra = millis();
        Serial.println("Centrando servo y retrocediendo más");
      }
      break;
      
    case RETROCEDER_FINAL:
      tiempoFaseActual = millis() - tiempoInicioManiobra;
      
      if (tiempoFaseActual < TIEMPO_RETROCESO_FINAL) {
        retroceder();
        Serial.println("Retrocediendo final hacia la pared");
      } else {
        detenerRobot();
        
        if (sdInicializada && cargarCalibracion(offsetAngleZ)) {
          calibrado = true;
          usarCorreccionGiroscopio = true;
          estadoActual = AVANZAR;
        } else {
          // Fallback rápido sin SD o si la calibración falla
          Serial.println("Calibración rápida de emergencia...");
          mpu.update();
          offsetAngleZ = mpu.getAngleZ();
          calibrado = true;
          usarCorreccionGiroscopio = true;
          reiniciarGiroscopio();
          estadoActual = AVANZAR;
        }
      }
      break;
      
    case REAJUSTAR_POSICION:
      estadoActual = AVANZAR;
      break;
  }
  
  delay(50);
}

// ... (el resto de las funciones se mantienen igual: aplicarCorreccionGiroscopio, leerPixy, avanzar, retroceder, detenerRobot, guardarCalibracion, cargarCalibracion, reiniciarGiroscopio, resetearAcumuladorAngulo, borrarCalibracionCorrupta, emergencyStop)

void aplicarCorreccionGiroscopio() {
  mpu.update(); // Asegurar lectura fresca
  
  float anguloRaw = mpu.getAngleZ();
  float anguloZ = anguloRaw - offsetAngleZ;
  float error = -anguloZ;
  
  // Si el error es muy grande, forzar reinicio COMPLETO
  if (abs(error) > 45.0) {
    Serial.print("ERROR CRÍTICO (");
    Serial.print(error, 1);
    Serial.println("°), reiniciando giroscopio COMPLETO...");
    
    reiniciarGiroscopio(); // Reinicio físico completo
    
    // Esperar a que se estabilice
    delay(50);
    mpu.update();
    
    // Recalcular error después del reinicio
    anguloRaw = mpu.getAngleZ();
    anguloZ = anguloRaw - offsetAngleZ;
    error = -anguloZ;
    
    Serial.print("Después del reinicio - Error: ");
    Serial.println(error, 1);
  }
  
  if (abs(error) > DEAD_BAND_CORRECCION) {
    unsigned long currentTime = millis();
    float deltaTime = (currentTime - prevTime) / 1000.0;
    if (deltaTime <= 0) deltaTime = 0.01;
    
    integralError += error * deltaTime;
    integralError = constrain(integralError, -50, 50);
    float derivative = (error - prevError) / deltaTime;
    float output = kP * error + kI * integralError + kD * derivative;
    
    prevError = error;
    prevTime = currentTime;
    
    int correccion = ANGULO_CENTRO + (int)output;
    correccion = constrain(correccion, ANGULO_MIN, ANGULO_MAX);

    Serial.print("PID | Servo: ");
    Serial.print(correccion);
    Serial.print(" | Error: ");
    Serial.print(error, 1);
    Serial.print("° | Raw: ");
    Serial.print(anguloRaw, 1);
    Serial.print("° | Corregido: ");
    Serial.print(anguloZ, 1);
    Serial.println("°");

    myservo.write(correccion);
    avanzar();
  } else {
    myservo.write(ANGULO_CENTRO);
    integralError = 0;
    prevError = 0;
    prevTime = millis();
    avanzar();
  }
}

void leerPixy() {
  static unsigned long ultimaLectura = 0;
  
  if (millis() - ultimaLectura > 100) {
    ultimaLectura = millis();
    
    // Desactivar SD primero
    digitalWrite(SD_CS, HIGH);
    delay(2);
    
    // Activar Pixy
    digitalWrite(PIXY_CS, LOW);
    delay(2);
    
    // Obtener bloques de la Pixy
    pixy.ccc.getBlocks();
    
    // Desactivar Pixy
    digitalWrite(PIXY_CS, HIGH);
    delay(2);
    
    bloqueVerdeDetectado = false;
    bloqueRojoDetectado = false;
    bloqueVerdeCercano = false;
    bloqueRojoCercano = false;
    posicionBloqueX = 0;
    
    if (pixy.ccc.numBlocks) {
      for (int i = 0; i < pixy.ccc.numBlocks; i++) {
        int centroX = pixy.ccc.blocks[i].m_x;
        int mitadPantalla = pixy.frameWidth / 2;
        
        // Determinar si el bloque está a la izquierda, derecha o centro
        if (centroX < mitadPantalla - UMBRAL_CENTRO_PIXY) {
          posicionBloqueX = -1; // Izquierda
        } else if (centroX > mitadPantalla + UMBRAL_CENTRO_PIXY) {
          posicionBloqueX = 1;  // Derecha
        } else {
          posicionBloqueX = 0;  // Centro
        }
        
        if (pixy.ccc.blocks[i].m_signature == 1) {
          bloqueVerdeDetectado = true;
          if (pixy.ccc.blocks[i].m_width * pixy.ccc.blocks[i].m_height > UMBRAL_TAMANO_BLOQUE_VERDE) {
            bloqueVerdeCercano = true;
          }
          break;
        }
        else if (pixy.ccc.blocks[i].m_signature == 2) {
          bloqueRojoDetectado = true;
          if (pixy.ccc.blocks[i].m_width * pixy.ccc.blocks[i].m_height > UMBRAL_TAMANO_BLOQUE_ROJO) {
            bloqueRojoCercano = true;
          }
          break;
        }
      }
    }
  }
}

void avanzar() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  ledcWrite(MOTOR_PWM_CHANNEL, velocidadNormal);
}

void retroceder() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  ledcWrite(MOTOR_PWM_CHANNEL, velocidadReversa);
}

void detenerRobot() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  ledcWrite(MOTOR_PWM_CHANNEL, 0);
}

bool guardarCalibracion(float offset) {
  if (!sdInicializada) {
    Serial.println("SD no disponible para guardar calibración");
    return false;
  }

  digitalWrite(PIXY_CS, HIGH);
  delay(2);
  digitalWrite(SD_CS, LOW);
  delay(2);
  
  const int numLecturas = 200;
  const float maxDesviacionPermitida = 0.3;
  float suma = 0;
  float primeraLectura = 0;
  
  Serial.println("Iniciando calibración precisa...");
  
  // Tomar primera lectura como referencia
  mpu.update();
  primeraLectura = mpu.getAngleZ();
  
  // Tomar múltiples lecturas
  for(int i = 0; i < numLecturas; i++) {
    mpu.update();
    float lecturaActual = mpu.getAngleZ();
    
    // Verificar estabilidad (que no se mueva el robot)
    if(abs(lecturaActual - primeraLectura) > maxDesviacionPermitida) {
      Serial.println("Error: Robot se movió durante calibración");
      digitalWrite(SD_CS, HIGH);
      return false;
    }
    
    suma += lecturaActual;
    
    if(i % 50 == 0) Serial.print("."); // Progreso
    delay(10);
  }
  
  // Calcular promedio preciso
  float offsetPreciso = suma / numLecturas;
  
  // Obtener ángulo inicial de referencia
  mpu.update();
  float anguloInicial = mpu.getAngleZ() - offsetPreciso;
  
  // Guardar en SD
  if (SD.exists("/calibracion.txt")) {
    SD.remove("/calibracion.txt");
  }
  
  File archivo = SD.open("/calibracion.txt", FILE_WRITE);
  if (archivo) {
    archivo.printf("offset: %.8f\n", offsetPreciso);
    archivo.printf("angulo_inicial: %.8f\n", anguloInicial);
    archivo.close();
    
    Serial.print("✓ Calibración guardada | Offset: ");
    Serial.print(offsetPreciso, 6);
    Serial.print(" | Ángulo Inicial: ");
    Serial.print(anguloInicial, 6);
    Serial.println("°");
    
    digitalWrite(SD_CS, HIGH);
    return true;
  }
  
  digitalWrite(SD_CS, HIGH);
  Serial.println("Error al abrir archivo en SD");
  return false;
}

bool cargarCalibracion(float &offset) {
  if (!sdInicializada) {
    Serial.println("SD no disponible para cargar calibración");
    return false;
  }
  
  digitalWrite(PIXY_CS, HIGH);
  delay(2);
  digitalWrite(SD_CS, LOW);
  delay(2);
  
  if (SD.exists("/calibracion.txt")) {
    File archivo = SD.open("/calibracion.txt");
    if (archivo) {
      String contenido = archivo.readString();
      archivo.close();
      
      // Buscar offset y ángulo inicial
      int posOffset = contenido.indexOf("offset: ");
      int posAngulo = contenido.indexOf("angulo_inicial: ");
      
      if (posOffset != -1 && posAngulo != -1) {
        // Extraer offset
        String strOffset = contenido.substring(posOffset + 8);
        strOffset = strOffset.substring(0, strOffset.indexOf('\n'));
        offset = strOffset.toFloat();
        
        // Extraer ángulo inicial de referencia
        String strAngulo = contenido.substring(posAngulo + 16);
        strAngulo = strAngulo.substring(0, strAngulo.indexOf('\n'));
        float anguloInicial = strAngulo.toFloat();
        
        digitalWrite(SD_CS, HIGH);
        
        // ✅ VERIFICACIÓN CRUCIAL: Comparar con ángulo actual
        mpu.update();
        float anguloActual = mpu.getAngleZ() - offset;
        float diferencia = abs(anguloActual - anguloInicial);
        
        Serial.print("✓ Calibración cargada | Offset: ");
        Serial.print(offset, 6);
        Serial.print(" | Ángulo Inicial Esperado: ");
        Serial.print(anguloInicial, 2);
        Serial.print("° | Ángulo Actual: ");
        Serial.print(anguloActual, 2);
        Serial.print("° | Diferencia: ");
        Serial.print(diferencia, 2);
        Serial.println("°");
        
        // 🔴 Si la diferencia es grande, la calibración es inválida
        if (diferencia > 15.0) {
          Serial.println("❌ Calibración inválida - Diferencia demasiado grande");
          return false;
        }
        
        // 🔄 AJUSTAR OFFSET para compensar diferencia
        if (diferencia > 5.0) {
          Serial.println("⚠️  Ajustando offset para compensar diferencia...");
          offset = offset + (anguloActual - anguloInicial);
          Serial.print("Nuevo offset: ");
          Serial.println(offset, 6);
        }
        
        reiniciarGiroscopio();
        return true;
      }
    }
    digitalWrite(SD_CS, HIGH);
    return false;
  }
  
  digitalWrite(SD_CS, HIGH);
  Serial.println("No se encontró archivo de calibración");
  return false;
}

void reiniciarGiroscopio() {
  // Reiniciar variables del PID
  integralError = 0;
  prevError = 0;
  prevTime = millis();
  
  // Forzar varias lecturas para estabilizar
  for (int i = 0; i < 10; i++) {
    mpu.update();
    delay(10);
  }
  
  if (calibrado) {
    float anguloActual = mpu.getAngleZ() - offsetAngleZ;
    Serial.print("Giroscopio reiniciado. Ángulo: ");
    Serial.print(anguloActual, 2);
    Serial.println("°");
    
    // ✅ Verificación final
    if (abs(anguloActual) > 5.0) {
      Serial.println("⚠️  Ajuste fino del ángulo...");
      // Pequeño ajuste para acercarse a 0
      offsetAngleZ += anguloActual * 0.8; // Factor de suavizado
      Serial.print("Offset ajustado a: ");
      Serial.println(offsetAngleZ, 6);
    }
  }
}

void resetearAcumuladorAngulo() {
  // Método suave primero
  for (int i = 0; i < 20; i++) {
    mpu.update();
    delay(5);
  }
  
  // Verificar si es necesario reinicio físico
  mpu.update();
  float anguloActual = mpu.getAngleZ();
  if (abs(anguloActual) > 45.0) {
    Serial.println("Reinicio físico del MPU6050...");
    Wire.beginTransmission(0x68);
    Wire.write(0x6B);
    Wire.write(0x80);
    Wire.endTransmission(true);
    delay(100);
    mpu.begin();
    mpu.calcOffsets();
  }
  
  Serial.println("Acumulador de ángulo reiniciado");
}

void borrarCalibracionCorrupta() {
  if (SD.exists("/calibracion.txt")) {
    // Verificar si el archivo está corrupto
    File archivo = SD.open("/calibracion.txt");
    if (archivo) {
      String contenido = archivo.readString();
      archivo.close();
      
      // Buscar offset y ángulo inicial
      int posOffset = contenido.indexOf("offset: ");
      int posAngulo = contenido.indexOf("angulo_inicial: ");
      
      if (posOffset == -1 || posAngulo == -1) {
        // Archivo corrupto - borrar
        SD.remove("/calibracion.txt");
        Serial.println("Calibración corrupta borrada");
      }
    }
  }
}

// Función de emergencia
void emergencyStop() {
  detenerRobot();
  estadoActual = DETENIDO;
  Serial.println("EMERGENCY STOP");
  
  if (pixyInicializada) {
    digitalWrite(PIXY_CS, LOW);
    pixy.setLamp(0, 0);
    digitalWrite(PIXY_CS, HIGH);
  }
}
