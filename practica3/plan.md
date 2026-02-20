## Plan: Práctica 3 — TDD Radar Meteorológico

**Resumen:** Aplicar TDD (Test Driven Development) al módulo `alcance_del_radar` de un Airbus A350. Se parte de un código base simple sin validaciones y un fichero de tests con solo 2 tests implementados. El objetivo es: (1) completar la tabla de 18 tests en 6 categorías, (2) implementar todos los tests en el fichero de tests, y (3) robustecer el código fuente para que pase el 100% de tests con 100% de cobertura.

---

### Contexto técnico

**Fórmula:** $Alcance = \frac{Co \cdot (T - \tau)}{2}$

| Variable | Descripción | Unidad | Rango válido |
|----------|-------------|--------|--------------|
| Alcance | Alcance del radar | km | resultado |
| Co | Velocidad de la luz | km/s | $3 \times 10^5$ (constante) |
| T | Intervalo de repetición de pulsos | segundos | [0, 0.7] |
| tau (τ) | Ancho del pulso | microsegundos | [0, 4] |

**Restricción importante:** T siempre debe ser mayor que tau (tras convertir tau a segundos).

**Estado actual de** `radar_meteorologico.py`: solo calcula la fórmula, sin ninguna validación de tipos ni rangos.

**Estado actual de** `test_radar_meteorologico.py`: 6 métodos de test, solo 2 implementados (test 1 y test 4), los otros 4 lanzan `Exception("no implementado")`.

---

### Tarea 2: Tabla completa de 18 tests

| # | T (s) | tau (µs) | Alcance (km) | Categoría |
|---|-------|----------|-------------|-----------|
| 1 | 0.5 | 2 | 74999.700 | Valores válidos |
| 2 | 0.3 | 1 | 44999.850 | Valores válidos |
| 3 | 0.7 | 4 | 104999.400 | Valores válidos |
| 4 | 0.2 | 5 | ValueError | Valores positivos fuera de rango |
| 5 | 0.8 | 2 | ValueError | Valores positivos fuera de rango |
| 6 | 0.5 | 5 | ValueError | Valores positivos fuera de rango |
| 7 | -0.3 | 2 | ValueError | Valores negativos |
| 8 | 0.5 | -1 | ValueError | Valores negativos |
| 9 | -0.1 | -2 | ValueError | Valores negativos |
| 10 | 0.000001 | 2 | ValueError | T menor que tau |
| 11 | 0.000003 | 4 | ValueError | T menor que tau |
| 12 | "hola" | 2 | TypeError | Entrada de strings |
| 13 | 0.5 | "hola" | TypeError | Entrada de strings |
| 14 | "hola" | "mundo" | TypeError | Entrada de strings |
| 15 | "" | 2 | TypeError | Entrada de strings |
| 16 | True | 2 | TypeError | Entrada de booleanos |
| 17 | 0.5 | False | TypeError | Entrada de booleanos |
| 18 | True | True | TypeError | Entrada de booleanos |

**Cálculos de verificación:**
- Test 1: $\frac{3 \times 10^5 \cdot (0.5 - 2 \times 10^{-6})}{2} = 150000 \times 0.499998 = 74999.700$
- Test 2: $\frac{3 \times 10^5 \cdot (0.3 - 1 \times 10^{-6})}{2} = 150000 \times 0.299999 = 44999.850$
- Test 3: $\frac{3 \times 10^5 \cdot (0.7 - 4 \times 10^{-6})}{2} = 150000 \times 0.699996 = 104999.400$

---

### Tarea 3: Plan de implementación TDD (iteraciones RED → GREEN → REFACTOR)

#### Paso 1 — Ejecutar tests iniciales (RED)

Ejecutar los tests tal cual están para ver qué falla:

```bash
python -m nose -v test_radar_meteorologico.py --with-spec --spec-color --with-coverage
coverage report -m
```

**Resultado esperado:** Test 1 (valores válidos) pasa; test 4 (fuera de rango) falla porque `radar_meteorologico.py` no tiene validación y no lanza `ValueError`. Los otros 4 tests fallan con `Exception("no implementado")`.

#### Paso 2 — Implementar todos los tests en `test_radar_meteorologico.py`

Completar los 4 métodos de test no implementados y añadir más asserts a los 2 existentes:

**`test_valores_validos`** — Añadir tests 2 y 3:
- `assertAlmostEqual(alcance_del_radar(0.3, 1), 44999.850, places=2)`
- `assertAlmostEqual(alcance_del_radar(0.7, 4), 104999.400, places=2)`

**`test_valores_fuera_rango`** — Añadir tests 5 y 6:
- `assertRaises(ValueError, alcance_del_radar, 0.8, 2)` — T fuera de rango
- `assertRaises(ValueError, alcance_del_radar, 0.5, 5)` — tau fuera de rango

**`test_valores_negativos`** — Implementar tests 7, 8, 9:
- `assertRaises(ValueError, alcance_del_radar, -0.3, 2)` — T negativo
- `assertRaises(ValueError, alcance_del_radar, 0.5, -1)` — tau negativo
- `assertRaises(ValueError, alcance_del_radar, -0.1, -2)` — ambos negativos

**`test_T_menor_tau`** — Implementar tests 10, 11:
- `assertRaises(ValueError, alcance_del_radar, 0.000001, 2)` — T < tau tras conversión
- `assertRaises(ValueError, alcance_del_radar, 0.000003, 4)` — T < tau tras conversión

**`test_strings`** — Implementar tests 12, 13, 14, 15:
- `assertRaises(TypeError, alcance_del_radar, "hola", 2)` — T es string
- `assertRaises(TypeError, alcance_del_radar, 0.5, "hola")` — tau es string
- `assertRaises(TypeError, alcance_del_radar, "hola", "mundo")` — ambos string
- `assertRaises(TypeError, alcance_del_radar, "", 2)` — string vacío

**`test_booleanos`** — Implementar tests 16, 17, 18:
- `assertRaises(TypeError, alcance_del_radar, True, 2)` — T es booleano
- `assertRaises(TypeError, alcance_del_radar, 0.5, False)` — tau es booleano
- `assertRaises(TypeError, alcance_del_radar, True, True)` — ambos booleanos

#### Paso 3 — Ejecutar tests (RED)

Volver a ejecutar. **Resultado esperado:** solo test 1 pasa (valores válidos con el assert original). Todo lo demás falla → confirma que estamos en fase RED.

#### Paso 4 — Robustecer `radar_meteorologico.py` (GREEN)

Modificar `alcance_del_radar` añadiendo validaciones **antes** del cálculo, en este orden:

1. **Validación de tipos** (lanza `TypeError`):
	- Comprobar que ni T ni tau son `bool` (importante: `isinstance(True, int)` es `True` en Python, así que hay que comprobar `bool` **antes** que `int`/`float`)
	- Comprobar que T y tau son `int` o `float` (no strings ni otros tipos)

2. **Validación de rangos** (lanza `ValueError`):
	- T debe estar en el rango [0, 0.7]
	- tau debe estar en el rango [0, 4]
	- T debe ser mayor que tau convertido a segundos (T > tau / 10⁶)

3. **Cálculo** (sin cambios respecto al original):
	- Convertir tau a segundos
	- Calcular y retornar `Co * (T - tau) / 2`

#### Paso 5 — Ejecutar tests (GREEN)

Ejecutar de nuevo. **Resultado esperado:** todos los 18 tests (6 métodos) pasan. Cobertura del 100%.

```bash
python -m nose -v test_radar_meteorologico.py --with-spec --spec-color --with-coverage
coverage report -m
```

#### Paso 6 — REFACTOR (opcional)

Revisar el código buscando mejoras sin cambiar el comportamiento:
- Mensajes descriptivos en las excepciones (`raise ValueError("T fuera de rango [0, 0.7]")`)
- Organizar docstrings correctamente
- Si algún test falla, volver al paso 4

---

### Verificación final

| Verificación | Comando / Acción |
|---|---|
| Todos los tests pasan | `python -m nose -v test_radar_meteorologico.py --with-spec --spec-color` |
| Cobertura 100% | `coverage report -m` (sin líneas "Missing") |
| 18 test cases cubiertos | Revisar que los 6 métodos contienen los 18 asserts de la tabla |

### Decisiones

- **`ValueError` vs `TypeError`**: Se usa `TypeError` para entradas con tipo incorrecto (strings, booleanos) y `ValueError` para valores numéricos fuera de rango o relaciones inválidas (T < tau).
- **Booleanos como tipo inválido**: En Python `bool` es subclase de `int`, por lo que hay que comprobar explícitamente `isinstance(x, bool)` antes de `isinstance(x, (int, float))`.
- **Orden de validación**: Tipos primero, luego rangos, luego restricciones entre parámetros (T > tau). Esto garantiza mensajes de error claros y tests predecibles.
