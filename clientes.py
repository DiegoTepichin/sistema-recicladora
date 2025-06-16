#!/usr/bin/env python3
"""
Sistema de Gestión de Clientes - Recicladora
============================================

Autor: [Tu Nombre]
Fecha: Junio 2025
Descripción: Sistema completo para gestionar clientes y ventas de materiales reciclables

Características:
- Registro y gestión de clientes
- Historial de compras por cliente
- Búsqueda avanzada de clientes
- Reportes detallados
- Ranking de mejores clientes
- Persistencia de datos en JSON
- Análisis básico de ventas

Uso:
    python3 clientes.py

Requisitos:
    - Python 3.6+
    - Módulos: json, datetime (incluidos en Python estándar)
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

class SistemaClientes:
    """
    Clase principal para gestionar el sistema de clientes de la recicladora.
    
    Attributes:
        clientes (dict): Diccionario con todos los datos de clientes
        archivo_datos (str): Ruta del archivo JSON para persistencia
        precios_materiales (dict): Precios por kg de cada material
    """
    
    def __init__(self, archivo_datos: str = "clientes.json"):
        """
        Inicializa el sistema de clientes.
        
        Args:
            archivo_datos (str): Nombre del archivo para guardar datos
        """
        self.archivo_datos = archivo_datos
        self.clientes = {}
        self.precios_materiales = {
            "aluminio": 25.0,
            "papel": 3.0,
            "plastico": 8.0,
            "plástico": 8.0,
            "vidrio": 5.0,
            "carton": 2.5,
            "cartón": 2.5,
            "metal": 15.0,
            "cobre": 80.0
        }
        self.cargar_datos()
    
    def agregar_cliente(self, nombre: str, telefono: str, direccion: str) -> int:
        """
        Agrega un nuevo cliente al sistema.
        
        Args:
            nombre (str): Nombre completo del cliente
            telefono (str): Número de teléfono
            direccion (str): Dirección completa
            
        Returns:
            int: ID del cliente creado
        """
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        
        # Verificar si el cliente ya existe
        for cliente_id, datos in self.clientes.items():
            if datos["telefono"] == telefono:
                print(f"⚠️  Cliente con teléfono {telefono} ya existe (ID: {cliente_id})")
                return cliente_id
        
        cliente_id = max(self.clientes.keys(), default=0) + 1
        self.clientes[cliente_id] = {
            "nombre": nombre.strip().title(),
            "telefono": telefono.strip(),
            "direccion": direccion.strip(),
            "fecha_registro": datetime.now().strftime("%Y-%m-%d"),
            "compras_totales": 0.0,
            "peso_total": 0.0,
            "num_transacciones": 0,
            "historial": [],
            "activo": True
        }
        self.guardar_datos()
        print(f"✅ Cliente {nombre} agregado con ID: {cliente_id}")
        return cliente_id
    
    def registrar_compra(self, cliente_id: int, material: str, peso: float, precio_kg: Optional[float] = None) -> float:
        """
        Registra una compra de un cliente.
        
        Args:
            cliente_id (int): ID del cliente
            material (str): Tipo de material
            peso (float): Peso en kilogramos
            precio_kg (float, optional): Precio por kg (usa precio default si no se especifica)
            
        Returns:
            float: Total de la compra
        """
        if cliente_id not in self.clientes:
            raise ValueError(f"Cliente con ID {cliente_id} no encontrado")
        
        if peso <= 0:
            raise ValueError("El peso debe ser mayor a 0")
        
        material_lower = material.lower()
        if precio_kg is None:
            precio_kg = self.precios_materiales.get(material_lower, 5.0)
        
        total = peso * precio_kg
        fecha_actual = datetime.now()
        
        compra = {
            "fecha": fecha_actual.strftime("%Y-%m-%d %H:%M"),
            "material": material.title(),
            "peso": peso,
            "precio_kg": precio_kg,
            "total": total,
            "mes": fecha_actual.strftime("%Y-%m")
        }
        
        # Actualizar datos del cliente
        cliente = self.clientes[cliente_id]
        cliente["historial"].append(compra)
        cliente["compras_totales"] += total
        cliente["peso_total"] += peso
        cliente["num_transacciones"] += 1
        
        self.guardar_datos()
        print(f"✅ Compra registrada: {peso}kg de {material} = ${total:.2f}")
        return total
    
    def buscar_cliente(self, termino: str) -> List[Tuple[int, Dict]]:
        """
        Busca clientes por nombre o teléfono.
        
        Args:
            termino (str): Término de búsqueda
            
        Returns:
            List[Tuple[int, Dict]]: Lista de tuplas (ID, datos_cliente)
        """
        if not termino.strip():
            return []
        
        termino_lower = termino.lower().strip()
        resultados = []
        
        for id_cliente, datos in self.clientes.items():
            if not datos["activo"]:
                continue
                
            if (termino_lower in datos["nombre"].lower() or 
                termino in datos["telefono"] or
                termino_lower in datos["direccion"].lower()):
                resultados.append((id_cliente, datos))
        
        # Ordenar por nombre
        resultados.sort(key=lambda x: x[1]["nombre"])
        return resultados
    
    def reporte_cliente(self, cliente_id: int) -> None:
        """
        Muestra un reporte detallado de un cliente.
        
        Args:
            cliente_id (int): ID del cliente
        """
        if cliente_id not in self.clientes:
            print(f"❌ Cliente con ID {cliente_id} no encontrado")
            return
        
        cliente = self.clientes[cliente_id]
        
        print(f"\n{'='*50}")
        print(f"📊 REPORTE DETALLADO - CLIENTE {cliente_id}")
        print(f"{'='*50}")
        print(f"👤 Nombre: {cliente['nombre']}")
        print(f"📞 Teléfono: {cliente['telefono']}")
        print(f"📍 Dirección: {cliente['direccion']}")
        print(f"📅 Registro: {cliente['fecha_registro']}")
        print(f"💰 Total comprado: ${cliente['compras_totales']:.2f}")
        print(f"⚖️  Peso total: {cliente['peso_total']:.2f} kg")
        print(f"📋 Transacciones: {cliente['num_transacciones']}")
        
        if cliente['historial']:
            print(f"\n📈 ÚLTIMAS 5 COMPRAS:")
            print("-" * 50)
            for compra in cliente['historial'][-5:]:
                print(f"{compra['fecha']}: {compra['material']} "
                      f"{compra['peso']}kg @ ${compra['precio_kg']:.2f}/kg = ${compra['total']:.2f}")
            
            # Análisis de materiales más comprados
            materiales_count = {}
            for compra in cliente['historial']:
                mat = compra['material']
                if mat not in materiales_count:
                    materiales_count[mat] = {'peso': 0, 'total': 0, 'count': 0}
                materiales_count[mat]['peso'] += compra['peso']
                materiales_count[mat]['total'] += compra['total']
                materiales_count[mat]['count'] += 1
            
            print(f"\n🔍 ANÁLISIS POR MATERIAL:")
            print("-" * 50)
            for material, stats in sorted(materiales_count.items(), 
                                        key=lambda x: x[1]['total'], reverse=True):
                print(f"{material}: {stats['peso']:.1f}kg, "
                      f"${stats['total']:.2f}, {stats['count']} compras")
        else:
            print("\n📝 Sin historial de compras")
    
    def top_clientes(self, limite: int = 10, criterio: str = "total") -> None:
        """
        Muestra el ranking de mejores clientes.
        
        Args:
            limite (int): Número de clientes a mostrar
            criterio (str): Criterio de ordenamiento ('total', 'peso', 'transacciones')
        """
        if not self.clientes:
            print("📝 No hay clientes registrados")
            return
        
        criterios_map = {
            "total": "compras_totales",
            "peso": "peso_total", 
            "transacciones": "num_transacciones"
        }
        
        if criterio not in criterios_map:
            criterio = "total"
        
        campo = criterios_map[criterio]
        clientes_activos = [(id_c, datos) for id_c, datos in self.clientes.items() 
                           if datos["activo"]]
        
        clientes_ordenados = sorted(clientes_activos, 
                                  key=lambda x: x[1][campo], 
                                  reverse=True)
        
        print(f"\n🏆 TOP {limite} CLIENTES - Por {criterio.title()}")
        print("=" * 60)
        
        for i, (id_cliente, datos) in enumerate(clientes_ordenados[:limite], 1):
            if criterio == "total":
                valor = f"${datos['compras_totales']:.2f}"
            elif criterio == "peso":
                valor = f"{datos['peso_total']:.1f}kg"
            else:
                valor = f"{datos['num_transacciones']} compras"
            
            print(f"{i:2d}. {datos['nombre']:<25} - {valor}")
    
    def estadisticas_generales(self) -> None:
        """Muestra estadísticas generales del negocio."""
        if not self.clientes:
            print("📝 No hay datos para mostrar estadísticas")
            return
        
        clientes_activos = [datos for datos in self.clientes.values() if datos["activo"]]
        total_clientes = len(clientes_activos)
        
        if total_clientes == 0:
            print("📝 No hay clientes activos")
            return
        
        ventas_totales = sum(c["compras_totales"] for c in clientes_activos)
        peso_total = sum(c["peso_total"] for c in clientes_activos)
        transacciones_totales = sum(c["num_transacciones"] for c in clientes_activos)
        
        print(f"\n📊 ESTADÍSTICAS GENERALES")
        print("=" * 40)
        print(f"👥 Clientes activos: {total_clientes}")
        print(f"💰 Ventas totales: ${ventas_totales:.2f}")
        print(f"⚖️  Peso total procesado: {peso_total:.2f} kg")
        print(f"📋 Total transacciones: {transacciones_totales}")
        
        if transacciones_totales > 0:
            print(f"💵 Venta promedio: ${ventas_totales/transacciones_totales:.2f}")
            print(f"📈 Peso promedio por transacción: {peso_total/transacciones_totales:.2f} kg")
        
        # Análisis de materiales más vendidos
        materiales_globales = {}
        for cliente in clientes_activos:
            for compra in cliente["historial"]:
                mat = compra["material"]
                if mat not in materiales_globales:
                    materiales_globales[mat] = {"peso": 0, "total": 0}
                materiales_globales[mat]["peso"] += compra["peso"]
                materiales_globales[mat]["total"] += compra["total"]
        
        if materiales_globales:
            print(f"\n🔍 MATERIALES MÁS VENDIDOS:")
            print("-" * 40)
            for material, stats in sorted(materiales_globales.items(), 
                                        key=lambda x: x[1]["total"], reverse=True)[:5]:
                print(f"{material}: {stats['peso']:.1f}kg, ${stats['total']:.2f}")
    
    def exportar_datos(self, formato: str = "json") -> str:
        """
        Exporta los datos a un archivo.
        
        Args:
            formato (str): Formato de exportación ('json', 'csv')
            
        Returns:
            str: Nombre del archivo generado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if formato.lower() == "json":
            archivo = f"backup_clientes_{timestamp}.json"
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(self.clientes, f, indent=2, ensure_ascii=False)
        
        elif formato.lower() == "csv":
            archivo = f"reporte_clientes_{timestamp}.csv"
            with open(archivo, "w", encoding="utf-8") as f:
                f.write("ID,Nombre,Telefono,Direccion,Fecha_Registro,Total_Compras,Peso_Total,Num_Transacciones\n")
                for id_cliente, datos in self.clientes.items():
                    f.write(f"{id_cliente},{datos['nombre']},{datos['telefono']},"
                           f"{datos['direccion']},{datos['fecha_registro']},"
                           f"{datos['compras_totales']:.2f},{datos['peso_total']:.2f},"
                           f"{datos['num_transacciones']}\n")
        
        print(f"✅ Datos exportados a: {archivo}")
        return archivo
    
    def guardar_datos(self) -> None:
        """Guarda los datos en el archivo JSON."""
        try:
            with open(self.archivo_datos, "w", encoding="utf-8") as f:
                json.dump(self.clientes, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error al guardar datos: {e}")
    
    def cargar_datos(self) -> None:
        """Carga los datos desde el archivo JSON."""
        try:
            if os.path.exists(self.archivo_datos):
                with open(self.archivo_datos, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.clientes = {int(k): v for k, v in data.items()}
                print(f"✅ Datos cargados: {len(self.clientes)} clientes")
            else:
                print("📝 Archivo de datos no encontrado, iniciando nuevo sistema")
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
            print("📝 Iniciando con base de datos vacía")
            self.clientes = {}

def mostrar_menu() -> None:
    """Muestra el menú principal."""
    print("\n" + "="*50)
    print("🏪 SISTEMA CLIENTES RECICLADORA")
    print("="*50)
    print("1. 👤 Agregar cliente")
    print("2. 💰 Registrar compra")
    print("3. 🔍 Buscar cliente")
    print("4. 📊 Reporte de cliente")
    print("5. 🏆 Top clientes")
    print("6. 📈 Estadísticas generales")
    print("7. 💾 Exportar datos")
    print("8. ⚙️  Configurar precios")
    print("9. 🚪 Salir")
    print("-"*50)

def configurar_precios(sistema: SistemaClientes) -> None:
    """Permite configurar los precios de los materiales."""
    print("\n💰 PRECIOS ACTUALES:")
    print("-" * 30)
    for material, precio in sistema.precios_materiales.items():
        print(f"{material.title()}: ${precio:.2f}/kg")
    
    print("\n¿Qué material quieres actualizar?")
    material = input("Material: ").lower().strip()
    
    if material in sistema.precios_materiales:
        try:
            nuevo_precio = float(input(f"Nuevo precio para {material} (actual: ${sistema.precios_materiales[material]:.2f}): $"))
            if nuevo_precio > 0:
                sistema.precios_materiales[material] = nuevo_precio
                print(f"✅ Precio actualizado: {material} = ${nuevo_precio:.2f}/kg")
            else:
                print("❌ El precio debe ser mayor a 0")
        except ValueError:
            print("❌ Precio inválido")
    else:
        print(f"❌ Material '{material}' no encontrado")

def menu_principal():
    """Función principal del programa."""
    sistema = SistemaClientes()
    
    # Mensaje de bienvenida
    print("🎉 ¡Bienvenido al Sistema de Clientes de la Recicladora!")
    
    while True:
        try:
            mostrar_menu()
            opcion = input("Elige una opción (1-9): ").strip()
            
            if opcion == "1":
                print("\n👤 AGREGAR NUEVO CLIENTE")
                print("-" * 25)
                nombre = input("Nombre completo: ").strip()
                if not nombre:
                    print("❌ El nombre es obligatorio")
                    continue
                
                telefono = input("Teléfono: ").strip()
                direccion = input("Dirección: ").strip()
                
                try:
                    sistema.agregar_cliente(nombre, telefono, direccion)
                except ValueError as e:
                    print(f"❌ Error: {e}")
            
            elif opcion == "2":
                print("\n💰 REGISTRAR COMPRA")
                print("-" * 20)
                try:
                    cliente_id = int(input("ID del cliente: "))
                    
                    # Mostrar cliente
                    if cliente_id in sistema.clientes:
                        cliente = sistema.clientes[cliente_id]
                        print(f"Cliente: {cliente['nombre']} - {cliente['telefono']}")
                    else:
                        print("❌ Cliente no encontrado")
                        continue
                    
                    print("\nMateriales disponibles:")
                    for mat, precio in sistema.precios_materiales.items():
                        print(f"  • {mat.title()}: ${precio:.2f}/kg")
                    
                    material = input("\nMaterial: ").strip()
                    peso = float(input("Peso en kg: "))
                    
                    # Opción de precio personalizado
                    precio_custom = input("¿Precio personalizado? (Enter para usar precio estándar): ").strip()
                    precio_kg = float(precio_custom) if precio_custom else None
                    
                    sistema.registrar_compra(cliente_id, material, peso, precio_kg)
                    
                except ValueError as e:
                    print(f"❌ Error: {e}")
                except Exception as e:
                    print(f"❌ Error inesperado: {e}")
            
            elif opcion == "3":
                print("\n🔍 BUSCAR CLIENTE")
                print("-" * 16)
                termino = input("Buscar por nombre, teléfono o dirección: ").strip()
                resultados = sistema.buscar_cliente(termino)
                
                if resultados:
                    print(f"\n✅ Encontrados {len(resultados)} resultados:")
                    print("-" * 60)
                    for id_cliente, datos in resultados:
                        print(f"ID: {id_cliente} | {datos['nombre']} | {datos['telefono']} | ${datos['compras_totales']:.2f}")
                else:
                    print("❌ No se encontraron clientes")
            
            elif opcion == "4":
                print("\n📊 REPORTE DE CLIENTE")
                print("-" * 22)
                try:
                    cliente_id = int(input("ID del cliente: "))
                    sistema.reporte_cliente(cliente_id)
                except ValueError:
                    print("❌ ID inválido")
            
            elif opcion == "5":
                print("\n🏆 TOP CLIENTES")
                print("-" * 14)
                try:
                    limite = int(input("¿Cuántos clientes mostrar? (default 10): ") or "10")
                    print("\nCriterios: total, peso, transacciones")
                    criterio = input("Criterio (default: total): ").strip() or "total"
                    sistema.top_clientes(limite, criterio)
                except ValueError:
                    sistema.top_clientes()
            
            elif opcion == "6":
                sistema.estadisticas_generales()
            
            elif opcion == "7":
                print("\n💾 EXPORTAR DATOS")
                print("-" * 16)
                formato = input("Formato (json/csv): ").strip().lower() or "json"
                sistema.exportar_datos(formato)
            
            elif opcion == "8":
                configurar_precios(sistema)
            
            elif opcion == "9":
                print("\n👋 ¡Gracias por usar el Sistema de Clientes!")
                print("💾 Datos guardados automáticamente")
                break
            
            else:
                print("❌ Opción no válida. Elige un número del 1 al 9")
        
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            print("Por favor, reporta este error al desarrollador")

if __name__ == "__main__":
    # Verificar que estamos en la carpeta correcta
    if not os.path.exists("clientes.json"):
        print("📁 Creando archivo de datos...")
    
    # Ejecutar programa principal
    menu_principal()