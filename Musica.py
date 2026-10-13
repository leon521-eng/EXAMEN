class Cancion:
    _contador_id = 1

    def __init__(self, titulo, artista, duracion):
        self.id = Cancion._contador_id
        Cancion._contador_id += 1
        self.titulo = titulo
        self.artista = artista
        self.duracion = duracion

    def __str__(self):
        return f"[{self.id}]{self.titulo} - {self.artista} ({self.duracion})"

class Nodo:
    def __init__(self, cancion):
        self.cancion = cancion
        self.siguiente = None
        self.anterior = None
            
class ListaDeReproduccion:
    def __init__(self):
        self.cabeza = None
        self.cola = None         
        self.actual = None
        self.cantidad = 0

    def obtener_cantidad(self):
        return self.cantidad

    def agregar_inicio(self, cancion):
        nuevo = Nodo(cancion)
        if self.cantidad == 0:
            self.cabeza = self.cola = self.actual = nuevo
            nuevo.siguiente = nuevo.anterior = nuevo
        else:
            nuevo.siguiente = self.cabeza
            nuevo.anterior = self.cola
            self.cabeza.anterior = nuevo
            self.cola.siguiente = nuevo
            self.cabeza = nuevo
        self.cantidad += 1

    def agregar_final(self, cancion):
        nuevo = Nodo(cancion)
        if self.cantidad == 0:
            self.cabeza = self.cola = self.actual = nuevo
            nuevo.siguiente = nuevo.anterior = nuevo

        else:
            nuevo.siguiente = self.cabeza
            nuevo.anterior = self.cola
            self.cola.anterior = nuevo
            self.cabeza.siguiente = nuevo
            self.cola = nuevo
        self.cantidad += 1

    def consultar_actual(self):
        return self.actual.cancion if self.actual else None
    
    def avanzar(self):
        if self.actual:
            self.actual = self.actual.siguiente
        return self.consultar_actual()

    def retroceder(self):
        if self.actual:
            self.actual = self.actual.anterior
        return self.consultar_actual()

    def _buscar_nodo(self, id_cancion):
        if self.cantidad == 0:
            return None
        temp = self.cabeza
        for _ in range(self.cantidad):
            if temp.cancion.id == id_cancion:
                return temp
            temp = temp.siguiente
        return None

    def seleccionar_actual(self, id_cancion):
        nodo = self._buscar_nodo(id_cancion)
        if nodo:
            self.actual = nodo
            return True
        return False

    def buscar_por_id(self, id_cancion):
        nodo = self._buscar_nodo(id_cancion)
        if nodo:
            self.actual = nodo
            return True
        return False

    def _eliminar_nodo(self, nodo):
        if self.cantidad == 1:
            self.cabeza = self.cola = self.actual = None
        else:
            nodo.anterior.siguiente = nodo.siguiente
            nodo.siguiente.anterior = nodo.anterior

            if self.cabeza == nodo:
                self.cabeza = nodo.siguiente
            if self.cola == nodo:
                self.cola = nodo.anterior
            if self.actual == nodo:
                self.actual = nodo.siguiente

        self.cantidad -= 1
        return True

    def eliminar_actual(self):
        if self.actual:
            return self._eliminar_nodo(self.actual)
        return False

    def eliminar_por_id(self, id_cancion):
        nodo = self._buscar_nodo(id_cancion)
        if nodo:
            return self._eliminar_nodo(nodo)
        return False

    def mostrar_adelante(self):
        if self.cantidad == 0:
            return []
        resultado = []
        temp = self.cabeza
        for _ in range(self.cantidad):
            resultado.append(temp.cancion)
            temp = temp.siguiente
        return resultado

    def mostrar_atras(self):
        if self.cantidad == 0:
            return []
        resultado = []
        temp = self.cola
        for _ in range(self.cantidad):
            resultado.append(temp.cancion)
            temp = temp.anterior
        return resultado

    def simular_reproduccion(self, k):
        if not self.actual or k <= 0:
            return []
        historial = []
        for _ in range(k):
            historial.append(self.actual.cancion)
            self.actual = self.actual.siguiente
        return historial

#salidas

def ejecutar_pruebas():
    print("INICIANDO PRUEBAS DE FUNCIONAMIENTO\n")
    lista = ListaDeReproduccion()
    
    def estado():
        print(f"   -> Tamaño: {lista.obtener_cantidad()}, Actual: {lista.consultar_actual()}")

    print("1. Operaciones sobre una lista vacía")
    print("   Esperado: Manejo seguro sin errores. Retroceder y avanzar retornan None.")
    lista.avanzar()
    lista.eliminar_actual()
    estado()

    print("\n2. Inserción de la primera canción")
    lista.agregar_inicio(Cancion("Bohemian Rhapsody", "Queen", 354))
    print("   Esperado: Tamaño 1, Actual: Bohemian Rhapsody. Enlaces circulares sobre sí mismo.")
    estado()

    print("\n3. Navegación en ambos sentidos con un solo nodo")
    print("   Avanzando:", lista.avanzar())
    print("   Retrocediendo:", lista.retroceder())
    print("   Esperado: Siempre retorna la misma canción.")

    print("\n4. Inserciones al inicio y al final")
    lista.agregar_final(Cancion("Hotel California", "Eagles", 390))
    lista.agregar_inicio(Cancion("Imagine", "John Lennon", 183))
    print("   Esperado: Tamaño 3, Actual sigue siendo Bohemian (ID 1).")
    estado()
    

    print("\n5. Recorridos con al menos cinco canciones")
    lista.agregar_final(Cancion("Hey Jude", "The Beatles", 431))
    lista.agregar_final(Cancion("Smells Like Teen Spirit", "Nirvana", 301))
    print("   Sentido Adelante:")
    for c in lista.mostrar_adelante(): print(f"     {c}")
    print("   Sentido Atrás:")
    for c in lista.mostrar_atras(): print(f"     {c}")

    print("\n6. Avance desde la última canción hacia la primera")
    lista.seleccionar_actual(5) # Nirvana
    print("   Actual:", lista.consultar_actual())
    print("   Avanzando...", lista.avanzar())
    print("   Esperado: Imagine (ID 3, la primera de la lista).")

    print("\n7. Retroceso desde la primera canción hacia la última")
    print("   Actual:", lista.consultar_actual())
    print("   Retrocediendo...", lista.retroceder())
    print("   Esperado: Nirvana (ID 5, la última).")

    print("\n8. Eliminación del primer nodo, del último y de uno intermedio")
    lista.eliminar_por_id(3) # Imagine (Primero)
    lista.eliminar_por_id(5) # Nirvana (Último)
    lista.eliminar_por_id(2) # Hotel California (Intermedio)
    print("   Esperado: Tamaño 2 (Quedan Queen y Beatles).")
    estado()

    print("\n9. Búsqueda y eliminación de un identificador inexistente")
    print("   Eliminando ID 99:", lista.eliminar_por_id(99))
    print("   Buscando ID 99:", lista.buscar_por_id(99))

    print("\n10. Reproducción simulada con k mayor que la cantidad de canciones")
    lista.seleccionar_actual(1) # Queen
    print("   Simulando k=5 sobre 2 canciones:")
    repro = lista.simular_reproduccion(5)
    for c in repro: print(f"     {c}")
    print("   Actual quedó en:", lista.consultar_actual())

    print("\n11. Eliminación de la canción actual y de la única canción")
    print("   Eliminando actual (Beatles)...")
    lista.eliminar_actual()
    estado()
    print("   Eliminando única restante (Queen)...")
    lista.eliminar_actual()
    estado()
    print("   Esperado: Lista vacía limpia.")

if __name__ == "__main__":
    ejecutar_pruebas()
        