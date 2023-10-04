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

    def conversion_fechas(self):
        try:
            return datetime.strptime(self.fecha_contratacion, "%d/%m/%Y")
        except ValueError:
            print("Error al convertir la fecha. Formato incorrecto")

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
        return self._altura_inorden(self.raiz)

    def _altura_inorden(self, nodo):
        if nodo is None:
            return 0
        else:
            altura_izquierda = self._altura_inorden(nodo.izquierda)
            altura_derecha = self._altura_inorden(nodo.derecha)
            return max(altura_izquierda, altura_derecha) + 1
        
    def altura_arbol_preorden(self): #recorrido preorden
        return self._altura_preorden(self.raiz)

    def _altura_preorden(self, nodo):
        if nodo is None:
            return 0
        else:
            altura_izquierda = self._altura_preorden(nodo.izquierda)
            altura_derecha = self._altura_preorden(nodo.derecha)
            return max(altura_izquierda, altura_derecha) + 1        
           
#Hasta aqui la clase ArbolEmpleados()          

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
            print("{:<15} {:<15} {:<10} {:<25}".format("\nNombre","Posicion","Salario","Fecha de contratacion"))
            for empleado in empleados:
                print("{:<15} {:<15} {:<10} {:^25}".format(empleado.nombre, empleado.posicion, empleado.salario, empleado.fecha_contratacion))

        elif opcion == 6:
            arbol_empleados.actualizar_txt(hotel)
            break
        else:
            print("Opcion no valida")                       

#MODULO 2
def facturacionPagos():
    print()

#MODULO 3
def estadisticaReportes(arbol_empleados, hotel):

    arbol_empleados.serializar(hotel)
    arbol_empleados.deserializar(hotel)

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
            print
        if opcion == 4:
            break            
 
def configuracion():
    print()    

def main():

    valencia ='valencia.txt'
    margarita = 'margarita.txt'
    caracas = 'caracas.txt'

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
            facturacionPagos()

        elif opcion == 3:
            print("\nSeleccione un hotel:")
            print("1. Valencia")
            print("2. Margarita")
            print("3. Caracas")
            eleccion = int(input("Seleccione una opcion: "))
            if eleccion == 1:
                estadisticaReportes(ArbolEmpleados(), valencia)
            elif eleccion == 2:
                estadisticaReportes(ArbolEmpleados(), margarita)
            elif eleccion == 3:
                estadisticaReportes(ArbolEmpleados(), caracas)

        elif opcion == 4:
            configuracion()                                       
main()            