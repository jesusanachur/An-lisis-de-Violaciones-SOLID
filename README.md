# An-lisis-de-Violaciones-SOLID

ProductoReader: Solo operaciones de lectura

ProductoWriter: Operaciones de escritura

VentaProcessor: Operaciones de ventas

Las clases concretas pueden implementar una o más interfaces según sea necesario.

5. Violación del Principio de Inversión de Dependencias (DIP)

Principio violado: Dependency Inversion Principle (DIP)

Justificación:
La clase SistemaProductos depende directamente de implementaciones concretas (archivos JSON) en lugar de abstracciones.

Solución propuesta:

Crear interfaces ProductoStorage y VentaStorage.

Implementar versiones concretas como JsonProductoStorage.

Inyectar estas dependencias en el constructor.

┌───────────────────┐       ┌───────────────────┐
│    MenuPrincipal  │       │    Producto       │
└─────────┬─────────┘       └─────────┬─────────┘
          │                           △
          │                           │
          │                   ┌───────┴───────┐
          │                   │               │
          │         ┌─────────▼───────┐ ┌─────▼─────────┐
          │         │ ProductoNormal  │ │ ProductoEspecial │
          │         └─────────────────┘ └─────────────────┘
          │
┌─────────▼─────────┐       ┌───────────────────┐
│    ProductoService├───────► ProductoRepository │
└─────────┬─────────┘       └───────────────────┘
          │
┌─────────▼─────────┐       ┌───────────────────┐
│    VentaService   ├───────►   VentaRepository  │
└───────────────────┘       └───────────────────┘
