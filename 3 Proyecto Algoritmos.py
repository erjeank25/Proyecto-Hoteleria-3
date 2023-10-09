import pickle #serializar y deserializar
from datetime import datetime #manejo de fechas

class NodoEmpleado: #Representa un empleado en un arbol binario
    def __init__(self, empleado):
        self.empleado = empleado
        self.izquierda = None
        self.derecha = None

class Empleado: #Representa los datos de cada empleado
    def __init__(self, nombre, posicion, salario, fecha_contratacion):
        self.nombre = nombre
        self.posicion = posicion
        self.salario = salario
        self.fecha_contratacion = fecha_contratacion
        self.izquierda = None
        self.derecha = None

#CRUDL
class ArbolEmpleados: #Metodos a implementar en 1er modulo
    def __init__(self):
        self.raiz = None

    def serializar(self, archivo): #serializar empleados
        empleados = []
        try:
            with open(archivo, 'r') as f:
                f.readline()
                for linea in f:
                    nombre, posicion, salario, fecha_contratacion = linea.strip().split(';')
                    salario = salario
                    fecha_contratacion = datetime.strptime(fecha_contratacion, "%d/%m/%Y")
                    empleado = Empleado(nombre, posicion, float(salario), fecha_contratacion)
                    self.agregar(empleado)
        except FileNotFoundError:
            print("No se encontro un archivo")

        with open(f"{archivo}.pickle", 'wb') as f:
            pickle.dump(self.raiz, f)

    def deserializar(self, archivo): #deserializar empleados
        try:
            with open(f"{archivo}.pickle", 'rb') as f:
                self.raiz = pickle.load(f)
        except FileNotFoundError:
            print("No se encontro ningun archivo")

    def actualizar_txt(self, archivo): #actualizar .txt al finalizar el modulo
        empleados = self.listar()
        with open(archivo, 'w') as f:
            f.write("Nombre;Posicion;Salario;FechaContratacion\n")
            for empleado in empleados:
                f.write(f"{empleado.nombre};{empleado.posicion};{empleado.salario};{empleado.fecha_contratacion}\n")                 

    #CREATE
    def agregar(self, empleado): #agrega un empleado al arbol
        self.raiz = self._agregar_empleado(self.raiz, empleado)

    def _agregar_empleado(self, nodo, empleado): #Recursion usada para recorrer los empleados desde la raiz del arbol
        if nodo is None:
            return NodoEmpleado(empleado)

        if empleado.nombre < nodo.empleado.nombre:
                nodo.izquierda = self._agregar_empleado(nodo.izquierda, empleado)
        elif empleado.nombre > nodo.empleado.nombre:
                nodo.derecha = self._agregar_empleado(nodo.derecha, empleado)
        return nodo        

    #READ
    def leer(self, nombre): #lee un empleado a partir de su nombre
        return self._leer_empleado(self.raiz, nombre)
        
    def _leer_empleado(self, nodo, nombre): #Recursion usada para recorrer los nombres de los empleados desde la raiz del arbol
        if nodo is None:
            return None
        elif nodo.empleado.nombre == nombre:
            return nodo.empleado
        elif nombre < nodo.empleado.nombre:
            return self._leer_empleado(nodo.izquierda, nombre)
        else:
            return self._leer_empleado(nodo.derecha, nombre)

    #UPDATE
    def modificar(self, nombre, nueva_posicion, nuevo_salario, nueva_fecha_contratacion): #modifica la informacion de un empleado
        self.raiz = self._modificar_empleado(self.raiz, nombre, nueva_posicion, nuevo_salario, nueva_fecha_contratacion)

    def _modificar_empleado(self, nodo, nombre, nueva_posicion, nuevo_salario, nueva_fecha_contratracion): #Recursion usada para recorrer los nombres de los empleados desde la raiz del arbol y asi modificar sus datos
        if nodo is None:
            return None

        if nodo.empleado.nombre == nombre:
            nodo.empleado.posicion = nueva_posicion
            nodo.empleado.salario = nuevo_salario
            nodo.empleado.fecha_contratacion = nueva_fecha_contratracion
        elif nombre < nodo.empleado.nombre:
            nodo.izquierda = self._modificar_empleado(nodo.izquierda, nombre, nueva_posicion, nuevo_salario, nueva_fecha_contratracion)
        else:
            nodo.derecha = self._modificar_empleado(nodo.derecha, nombre, nueva_posicion, nuevo_salario, nueva_fecha_contratracion)

        return nodo

    #DELETE
    def eliminar(self, nombre): #usada para eliminar a un empleado
        self.raiz = self._eliminar_empleado(self.raiz, nombre)

    #en caso de haber 2 hijos, se busca al sucesor del padre 
    def _encontrar_sucesor(self, nodo):
        while nodo.izquierda:
            nodo = nodo.izquierda
        return nodo        

    def _eliminar_empleado(self, nodo, nombre): #recorre el arbol desde la raiz para encontrar el nombre a eliminar
        if nodo is None:
            return None

        if nombre == nodo.empleado.nombre:
            # Caso 1: No tiene hijos (Nodo Hoja)
            if nodo.izquierda is None:
                return nodo.derecha
            # Caso 2: tiene un hijo
            elif nodo.derecha is None:
                return nodo.izquierda

            #Caso 3: tiene dos hijos
            sucesor = self._encontrar_sucesor(nodo.derecha)
            nodo.empleado = sucesor.empleado
            nodo.derecha = self._eliminar_empleado(nodo.derecha, sucesor.empleado.nombre)
        elif nombre < nodo.empleado.nombre:
            nodo.izquierda = self._eliminar_empleado(nodo.izquierda, nombre)
        else:
            nodo.derecha = self._eliminar_empleado(nodo.derecha, nombre)

        return nodo
        
    #LIST
    def listar(self):
        empleados = []
        self._listar_empleados(self.raiz, empleados)
        return empleados
        
    def _listar_empleados(self, nodo, empleados):
        if nodo:
            self._listar_empleados(nodo.izquierda, empleados)
            empleados.append(nodo.empleado)
            self._listar_empleados(nodo.derecha, empleados)

    def cinco_empleados(self):
        empleados = self.listar()
        empleados.sort(key=lambda emp: emp.fecha_contratacion) #se ordenan por orden ascendente (mas antiguo a menos antiguo)
        return empleados[:5] #se retornan los primeros 5 empleados mas antiguos

    def listar_fechas(self):
        empleados = self.listar()
        empleados.sort(key=lambda emp: emp.fecha_contratacion) #se ordenan por orden ascendente (mas antiguo a menos antiguo)
        return empleados

    def altura_arbol_inorden(self): #recorrido inorden
        elementos = []
        self._altura_inorden(self.raiz, elementos)
        return len(elementos)

    def _altura_inorden(self, nodo, elementos):
        if nodo:
            self._altura_inorden(nodo.izquierda, elementos)
            elementos.append(nodo.empleado)
            self._altura_inorden(nodo.derecha, elementos)
        
    def altura_arbol_preorden(self): #recorrido preorden
        elementos = []
        self._altura_preorden(self.raiz, elementos)
        return len(elementos)

    def _altura_preorden(self, nodo, elementos): #recorrido en preorden
        if nodo:
            elementos.append(nodo.empleado)
            self._altura_preorden(nodo.izquierda, elementos)
            self._altura_preorden(nodo.derecha, elementos)      
#Hasta aqui la clase ArbolEmpleados()          

class Factura: #Creacion de una factura
    def __init__(self, costo_total, servicios_adicionales, metodo_pago, estado_pago):
        self.costo_total = costo_total
        self.servicios_adicionales = servicios_adicionales
        self.metodo_pago = metodo_pago
        self.estado_pago = estado_pago

class NodoAVL: #Creacion de arbol AVL
    def __init__(self, factura):
        self.factura = factura
        self.izquierdo = None
        self.derecho = None
        self.altura = 1

class ArbolAVL:
    def altura(self, nodo):
        return nodo.altura if nodo else 0

    def maximo(self, a, b):
        return a if a > b else b

    def rotacion_derecha(self, y):
        x = y.izquierdo
        T2 = x.derecho

        x.derecho = y
        y.izquierdo = T2

        y.altura = self.maximo(self.altura(y.izquierdo), self.altura(y.derecho)) + 1
        x.altura = self.maximo(self.altura(x.izquierdo), self.altura(x.derecho)) + 1 

        return x

    def rotacion_izquierda(self, x):
        y = x.derecho
        T2 = y.izquierdo

        y.izquierdo = x
        x.derecho = T2

        x.altura = self.maximo(self.altura(x.izquierdo), self.altura(x.derecho)) + 1
        y.altura = self.maximo(self.altura(y.izquierdo), self.altura(y.derecho)) + 1 

        return y

    def factor_equilibrio(self, nodo):
        return self.altura(nodo.izquierdo) - self.altura(nodo.derecho)

    def insertar(self, nodo, factura):
        if not nodo:
            return NodoAVL(factura)

        if factura.costo_total < nodo.factura.costo_total:
            nodo.izquierdo = self.insertar(nodo.izquierdo, factura)
        else:
            nodo.derecho = self.insertar(nodo.derecho, factura)

        nodo.altura = self.maximo(self.altura(nodo.izquierdo), self.altura(nodo.derecho)) + 1

        return self.balancear(nodo)

    def balancear(self, nodo):
        factor_equilibrio = self.factor_equilibrio(nodo)

        if factor_equilibrio > 1:
            if nodo.izquierdo and self.factor_equilibrio(nodo.izquierdo) >= 0:
                return self.rotacion_derecha(nodo)
            elif nodo.izquierdo and self.factor_equilibrio(nodo.izquierdo) < 0:
                nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
                return self.rotacion_derecha(nodo)

        elif factor_equilibrio < -1:
            if nodo.derecho and self.factor_equilibrio(nodo.derecho) <= 0:
                return self.rotacion_izquierda(nodo)
            elif nodo.derecho and self.factor_equilibrio(nodo.derecho) > 0:
                nodo.derecho = self.rotacion_derecha(nodo.derecho)
                return self.rotacion_izquierda(nodo)

        return nodo

    def leer_facturas(self, reservas):
        facturas = []
        with open(reservas, 'r') as archivo:
            archivo.readline()
            for linea in archivo:
                campos = linea.strip().split(';')
                factura = Factura(int(campos[0]), campos[1], campos[2], campos[3])
                facturas.append(factura)

        return facturas

    def serializar(self, archivo):
        with open(f"{archivo}.pickle", 'wb') as f:
            pickle.dump(self, f)

    def deserializar(self, archivo):
        with open(f"{archivo}.pickle", 'rb') as f:
            return pickle.load(f)
        
    def imprimir_facturas(self, nodo):
        if not nodo:
            return  

        print("Costo total:", nodo.factura.costo_total)
        print("Servicios Adicionales:", nodo.factura.servicios_adicionales)
        print("Metodo de pago:", nodo.factura.metodo_pago)
        print("Estado de pago:", nodo.factura.estado_pago)
        print()

        self.imprimir_facturas(nodo.izquierdo)

    def altura_arbol_postorden(self, nodo):
            if nodo is None:
                return 0, 0  # Retornamos tanto la altura como el número de nodos

            # Calcular altura de los subárboles izquierdo y derecho en postorden
            altura_izquierda, nodos_izquierda = self.altura_arbol_postorden(nodo.izquierdo)
            altura_derecha, nodos_derecha = self.altura_arbol_postorden(nodo.derecho)

            # La altura del árbol es la máxima altura de los subárboles más 1 (altura de este nodo)
            altura_actual = max(altura_izquierda, altura_derecha) + 1

            # Contar el número de nodos en este subárbol
            num_nodos_actual = nodos_izquierda + nodos_derecha + 1

            return altura_actual + 4, num_nodos_actual + 4
#Hasta aqui la clase ArbolAVL()      

#MODULO 1
def gestionEmpleados(hotel):

    arbol_empleados = ArbolEmpleados() #se crea el arbol

    arbol_empleados.serializar(hotel) 
    arbol_empleados.deserializar(hotel)

    arbol_empleados.listar()    

    while True:
        print("\n1. Crear Empleado")
        print("2. Buscar Empleado")
        print("3. Modificar Empleado")
        print("4. Eliminar Empleado")
        print("5. Listar Empleados")
        print("6. Regresar y guardar datos")

        opcion = int(input("Seleccione una opcion: "))

        if opcion == 1:

            nombre = input("\nIngrese el nombre del empleado: ")
            posicion = input("Ingrese la posicion del empleado: ")
            salario = float(input("Ingrese el salario del empleado: "))
            fecha_contratacion = input("Ingrese la fecha de contratacion (dd/mm/aaaa)")
            nuevo_empleado = Empleado(nombre, posicion, salario, fecha_contratacion)
            arbol_empleados.agregar(nuevo_empleado)

        elif opcion == 2:

            nombre_buscar = input("Ingrese el nombre del empleado a buscar: ")
            empleado_encontrado = arbol_empleados.leer(nombre_buscar)
            if empleado_encontrado:
                print("Empleado encontrado: ")
                print("Nombre:",empleado_encontrado.nombre)
                print("Posicion:",empleado_encontrado.posicion)
                print("Salario:",empleado_encontrado.salario)
                print("Fecha de contratacion:", empleado_encontrado.fecha_contratacion)
            else:
                print("Empleado no encontrado")

        elif opcion == 3:

            nombre_modificar = input("\nIngrese el nombre del empleado a modificar: ")
            nueva_posicon = input("Ingrese la nueva posicion del empleado: ")
            nuevo_salario = input("Ingrese el nuevo salario del empleado: ")
            nueva_fecha_contratacion = input("Ingrese la nueva fecha de contratacion (dd/mm/aaaa): ")
            empleado_modificado = arbol_empleados.modificar(nombre_modificar, nueva_posicon, nuevo_salario, nueva_fecha_contratacion)
            if empleado_modificado:
                print("Empleado modificado con exito")
            else:
                print("No se pudo modificar el empleado")

        elif opcion == 4: 

            nombre_eliminar = input("\nIngrese el nombre del empleado a eliminar: ")
            arbol_empleados.eliminar(nombre_eliminar)
            empleados = [empleado for empleado in empleados if empleado.nombre != nombre_eliminar]
            print("Empleado eliminado.")

        elif opcion == 5:

            empleados = arbol_empleados.listar()  
            print("\nListado de empleados: ")
            print("{:<15} {:<15} {:<10} {:^25}".format("\nNombre","Posicion","Salario","Fecha de contratacion"))
            for empleado in empleados:
                print("{:<15} {:<15} {:<10} {:^25}".format(empleado.nombre, empleado.posicion, empleado.salario, empleado.fecha_contratacion.strftime('%d/%m/%Y')))

        elif opcion == 6:
            arbol_empleados.actualizar_txt(hotel)
            break
        else:
            print("Opcion no valida")                       

#MODULO 2
def facturacionPagos(reservas):

    arbol_avl = ArbolAVL()

    arbol_avl.serializar(reservas)
    arbol_avl.deserializar(reservas)

    facturas = arbol_avl.leer_facturas(reservas) #lectura de cada factura del archivo .txt

    print("\nFacturas almacendas en el arbol: ")
    for factura in facturas:
        nodo_factura = NodoAVL(factura) #obejto de tipo NodoAVL()
        arbol_avl.insertar(nodo_factura, factura) #se insertan al arbol AVL
        arbol_avl.imprimir_facturas(nodo_factura) #impresion del arbol AVL


#MODULO 3
def estadisticaReportes(arbol_empleados, hotel, arbol_reserva, reserva):

    arbol_empleados.serializar(hotel)
    arbol_empleados.deserializar(hotel)
    facturas = arbol_reserva.leer_facturas(reserva)
    

    while True:

        print("\nModulo de Estadísticas y Reportes")
        print("1. Facturacion por Hotel y Mes (Inorden)")
        print("2. Listar empleados de un hotel por fecha de contratacion (Preorden)")
        print("3. Listar facturas existentes de un hotel y metodos de pago (Postorden)")
        opcion = int(input("Introduce una opcion: "))

        if opcion == 1:

            print("\nLos Cinco Empleados mas antiguos son: ")
            empleados_antiguos = arbol_empleados.cinco_empleados()
            if empleados_antiguos:
                print("\nNombre      Fecha de contratacion")
                for empleado in empleados_antiguos:
                    print("{:<15} {:<15}".format(empleado.nombre, empleado.fecha_contratacion.strftime('%d/%m/%Y')))

            altura_inorden = arbol_empleados.altura_arbol_inorden()
            print("\nAltura del arbol (Inorden): ",altura_inorden)

        if opcion == 2:
            print("\nLista de empleados por fecha de contratacion: ")
            empleados_antiguos = arbol_empleados.listar_fechas()
            if empleados_antiguos:
                print("\nNombre      Fecha de contratacion")
                for empleado in empleados_antiguos:
                    print("{:<15} {:<15}".format(empleado.nombre, empleado.fecha_contratacion.strftime('%d/%m/%Y')))

            altura_preorden = arbol_empleados.altura_arbol_preorden()
            print("\nAltura del arbol (Inorden): ",altura_preorden)

        if opcion == 3:

            print("Hotel: ", reserva)
            for factura in facturas:
                nodo_factura = NodoAVL(factura)
                print("\nMetodo de Pago:", factura.metodo_pago)
    
            altura_postorden = arbol_reserva.altura_arbol_postorden(nodo_factura)
            print("Altura del arbol: ", altura_postorden)

        if opcion == 4:
            break            
 
def configuracion():
    print()    

def main():

    valencia ='valencia.txt'
    margarita = 'margarita.txt'
    caracas = 'caracas.txt'

    reservas_valencia = 'reservas_valencia.txt'
    reservas_margarita = 'reservas_margarita.txt'
    reservas_caracas = 'reservas_caracas.txt'

    while True:

        print("\n***** BIENVENIDO AL SISTEMA DE GESTION DE HOTELERIA ******")
        print("1. Gestion de Empleados")
        print("2. Modulo de Facturación y Pagos")
        print("3. Modulo de Estadística y Reportes")
        print("4. Archivo de Configuracion")
        opcion = int(input("Seleccione una opcion: "))

        if opcion == 1:
            print("\nSeleccione un hotel:")
            print("1. Valencia")
            print("2. Margarita")
            print("3. Caracas")
            eleccion = int(input("Seleccione una opcion: "))
            if eleccion == 1:
                gestionEmpleados(valencia)
            elif eleccion == 2:
                gestionEmpleados(margarita)
            elif eleccion == 3:
                gestionEmpleados(caracas)
                                              
        elif opcion == 2:
            print("\nSeleccione un hotel:")
            print("1. Valencia")
            print("2. Margarita")
            print("3. Caracas")
            eleccion = int(input("Seleccione una opcion: "))
            if eleccion == 1:
                facturacionPagos('reservas_valencia.txt')
            elif eleccion == 2:
                facturacionPagos('reservas_margarita.txt')
            elif eleccion == 3:
                facturacionPagos('reservas_caracas.txt')           

        elif opcion == 3:
            print("\nSeleccione un hotel:")
            print("1. Valencia")
            print("2. Margarita")
            print("3. Caracas")
            eleccion = int(input("Seleccione una opcion: "))
            if eleccion == 1:
                estadisticaReportes(ArbolEmpleados(), valencia, ArbolAVL(), reservas_valencia)
            elif eleccion == 2:
                estadisticaReportes(ArbolEmpleados(), margarita, ArbolAVL(), reservas_margarita)
            elif eleccion == 3:
                estadisticaReportes(ArbolEmpleados(), caracas, ArbolAVL(), reservas_caracas)

        elif opcion == 4:
            configuracion()                                       
main()            