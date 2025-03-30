import os
import json
from abc import ABC, abstractmethod
from datetime import datetime


class IArchivo(ABC):
    """Interfaz para manejar operaciones de archivos."""

    @abstractmethod
    def cargar(self):
        pass
        @abstractmethod
        def eliminar(self):
            pass
    @abstractmethod
    def guardar(self, data):
        pass

class ArchivoJSON(IArchivo):
    """Clase concreta para manejar archivos JSON."""

    def __init__(self, ruta):
        self.ruta = ruta

    def cargar(self):
        if not os.path.exists(self.ruta):
            return []
        try:
            with open(self.ruta, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except json.JSONDecodeError:
            print(f"Error al leer el archivo {self.ruta}.")
            return []

    def guardar(self, data):
        with open(self.ruta, 'w', encoding='utf-8') as archivo:
            json.dump(data, archivo, indent=4)


class Producto:
    """Clase que representa un producto."""

    def __init__(self, id, nombre, precio, categoria, stock):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock


class ProductoEspecial(Producto):
    """Clase que representa un producto especial con descuento."""

    def __init__(self, id, nombre, precio, categoria, stock, descuento):
        super().__init__(id, nombre, precio, categoria, stock)
        self.descuento = descuento

    def calcular_precio_final(self):
        return self.precio * (1 - self.descuento)

    def aplicar_descuento(self, porcentaje):
        self.descuento = porcentaje


class SistemaProductos:
    """Clase principal que maneja las operaciones del sistema."""

    def __init__(self, productos_handler, ventas_handler):
        self.manejador_productos = productos_handler
        self.manejador_ventas = ventas_handler

    def ejecutar(self):
        """Método principal que ejecuta toda la aplicación."""
        while True:
            print("\n===== SISTEMA DE REGISTRO DE PRODUCTOS =====")
            print("1. Registrar producto")
            print("2. Consultar productos")
            print("3. Actualizar producto")
            print("4. Eliminar producto")
            print("5. Registrar venta")
            print("6. Generar reporte de ventas")
            print("7. Salir")

            opcion = input("\nSeleccione una opción: ")

            if opcion == '1':
                self.manejador_productos.registrar_producto()
            elif opcion == '2':
                self.manejador_productos.consultar_productos()
            elif opcion == '3':
                self.manejador_productos.actualizar_producto()
            elif opcion == '4':
                self.manejador_productos.eliminar_producto()
            elif opcion == '5':
                self.manejador_ventas.registrar_venta(self.manejador_productos)
            elif opcion == '6':
                self.manejador_ventas.generar_reporte()
            elif opcion == '7':
                print("¡Gracias por usar el sistema!")
                break
            else:
                print("Opción inválida. Intente nuevamente.")


class ManejadorProductos:
    """Clase que maneja las operaciones relacionadas con productos."""

    def __init__(self, archivo_productos_handler):
        self.archivo_productos = archivo_productos_handler

    def registrar_producto(self):
        print("\n--- REGISTRO DE PRODUCTO ---")
        id = input("ID del producto: ")
        nombre = input("Nombre del producto: ")
        precio = float(input("Precio del producto: "))
        categoria = input("Categoría del producto: ")
        stock = int(input("Stock del producto: "))

        productos = self.archivo_productos.cargar()

        if any(producto['id'] == id for producto in productos):
            print("ERROR: Ya existe un producto con ese ID.")
            return

        nuevo_producto = {
            'id': id,
            'nombre': nombre,
            'precio': precio,
            'categoria': categoria,
            'stock': stock,
        }

        productos.append(nuevo_producto)
        self.archivo_productos.guardar(productos)
        print(f"Producto '{nombre}' registrado exitosamente.")

    def consultar_productos(self):
        print("\n--- LISTADO DE PRODUCTOS ---")
        productos = self.archivo_productos.cargar()

        if not productos:
            print("No hay productos registrados.")
            return

        print(f"{'ID':<10} {'Nombre':<20} {'Precio':<10} {'Categoría':<15} {'Stock':<10}")
        print("-" * 65)

        for producto in productos:
            print(f"{producto['id']:<10} {producto['nombre']:<20} {producto['precio']:<10.2f} {producto['categoria']:<15} {producto['stock']:<10}")

    def actualizar_producto(self):
        print("\n--- ACTUALIZACIÓN DE PRODUCTO ---")
        producto_id = input("ID del producto a actualizar: ")
        productos = self.archivo_productos.cargar()

        for producto in productos:
            if producto['id'] == producto_id:
                print(f"Producto encontrado: {producto['nombre']}")
                nombre = input("Nuevo nombre (Enter para mantener): ")
                precio_str = input("Nuevo precio (Enter para mantener): ")
                categoria = input("Nueva categoría (Enter para mantener): ")
                stock_str = input("Nuevo stock (Enter para mantener): ")

                if nombre:
                    producto['nombre'] = nombre
                if precio_str:
                    producto['precio'] = float(precio_str)
                if categoria:
                    producto['categoria'] = categoria
                if stock_str:
                    producto['stock'] = int(stock_str)

                self.archivo_productos.guardar(productos)
                print("Producto actualizado exitosamente.")
                return

        print("ERROR: No se encontró un producto con ese ID.")

    def eliminar_producto(self):
        """
        Elimina un producto de la lista de productos almacenados.

        Este método solicita al usuario el ID de un producto, busca dicho producto
        en la lista cargada desde el archivo de productos, y lo elimina si se encuentra.
        Si el producto es eliminado exitosamente, se guarda la lista actualizada en el archivo.
        Si no se encuentra un producto con el ID proporcionado, se muestra un mensaje de error.

        Raises:
            KeyError: Si el archivo de productos no contiene un producto con el ID especificado.

        Returns:
            None
        """
        print("\n--- ELIMINACIÓN DE PRODUCTO ---")
        producto_id = input("ID del producto a eliminar: ")
        productos = self.archivo_productos.cargar()

        for i, producto in enumerate(productos):
            if producto['id'] == producto_id:
                productos.pop(i)
                self.archivo_productos.guardar(productos)
                print("Producto eliminado exitosamente.")
                return

        print("ERROR: No se encontró un producto con ese ID.")


class ManejadorVentas:
    """Clase que maneja las operaciones relacionadas con ventas."""

    def __init__(self, archivo_ventas_handler):
        """
        Initializes the instance with the specified sales file handler.

        Args:
            archivo_ventas_handler (ArchivoJSON): The handler for the sales file.
        """
        self.archivo_ventas = archivo_ventas_handler

    def registrar_venta(self, productos_manager):  
        print("\n--- REGISTRO DE VENTA ---")
        producto_id = input("ID del producto vendido: ")
        cantidad = int(input("Cantidad vendida: "))

        productos = productos_manager.archivo_productos.cargar()
        ventas = self.archivo_ventas.cargar()

        for producto in productos:
            if producto['id'] == producto_id:
                if producto['stock'] >= cantidad:
                    producto['stock'] -= cantidad
                    nueva_venta = {
                        'producto_id': producto_id,
                        'cantidad': cantidad,
                        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'total': producto['precio'] * cantidad,
                    }
                    ventas.append(nueva_venta)
                    productos_manager.archivo_productos.guardar(productos)
                    self.archivo_ventas.guardar(ventas)
                    print(f"Venta registrada exitosamente. Total: ${nueva_venta['total']:.2f}")
                    return
                else:
                    print(f"ERROR: Stock insuficiente. Stock actual: {producto['stock']}")
                    return

        print("ERROR: No se encontró un producto con ese ID.")

    def generar_reporte(self):
        print("\n--- REPORTE DE VENTAS ---")
        ventas = self.archivo_ventas.cargar()

        if not ventas:
            print("No hay ventas registradas.")
            return

        print(f"{'Producto ID':<15} {'Cantidad':<10} {'Fecha':<20} {'Total':<10}")
        print("-" * 55)

        total_ventas = 0
        for venta in ventas:
            print(f"{venta['producto_id']:<15} {venta['cantidad']:<10} {venta['fecha']:<20} ${venta['total']:<10.2f}")
            total_ventas += venta['total']

        print("-" * 55)
        print(f"TOTAL VENTAS: ${total_ventas:.2f}")


if __name__ == "__main__":
    archivo_productos = ArchivoJSON("productos.txt")
    archivo_ventas = ArchivoJSON("ventas.json")

    manejador_productos = ManejadorProductos(archivo_productos_handler=archivo_productos)
    manejador_ventas = ManejadorVentas(archivo_ventas)

    sistema = SistemaProductos(productos_handler=manejador_productos, ventas_handler=manejador_ventas)
    sistema.ejecutar()