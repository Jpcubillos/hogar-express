# Decisiones de Negocio Pendientes

Los siguientes requerimientos contienen contradicciones o están a la espera de aprobación por parte del cliente. Se han dejado marcados con comentarios `TODO` en el código para evitar lógica de negocio falsa.

1. **IPC de Actualización Anual:**
   - *Pendiente:* Día exacto del año y porcentaje final aplicable por IPC.
   - *Ubicación:* `apps.rentals`

2. **Cálculo de Recargo diario por mora (RN-07 / RN-08):**
   - *Pendiente:* Aprobación del porcentaje diario exacto del 1.76% y si aplica festivos.
   - *Ubicación:* `apps.payments`

3. **Traslado a Afianzadora (RN-09):**
   - *Pendiente:* Definición del día límite de mora exacto (Día 10 o 11) para pasar a cobro jurídico.
   - *Ubicación:* `apps.guarantors`

4. **Regla de Prorrateo e Inicio del Contrato (RN-02 / RN-04):**
   - *Pendiente:* Cobro de doble mes si inicia después del día 15.
   - *Ubicación:* `apps.rentals`
