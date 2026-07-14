# Matriz de Roles y Permisos

El sistema implementa cuatro grupos de usuarios predeterminados:

| Permiso / Módulo | Administrador | Asesor Interno | Asesor Externo | Consulta |
|---|:---:|:---:|:---:|:---:|
| Gestión de Usuarios | Sí | No | No | No |
| Gestión de Configuración | Sí | No | No | No |
| Propietarios (Ver) | Sí | Sí | No | Sí |
| Propietarios (Editar) | Sí | Sí | No | No |
| Inmuebles (Ver) | Sí | Sí | Sí (Ventas) | Sí |
| Inmuebles (Editar) | Sí | Sí | No | No |
| Contratos y Alquileres | Sí | Sí | No | Sí (Solo Ver) |
| Pagos y Recaudos | Sí | Sí | No | No |
| Órdenes de Reparación | Sí | Sí | No | Sí (Solo Ver) |
| Fichas de Venta | Sí | No | Sí | No |
| Auditoría del Sistema | Sí (Solo Ver) | No | No | No |

## Comando de Inicialización
```bash
python manage.py seed_roles
```
