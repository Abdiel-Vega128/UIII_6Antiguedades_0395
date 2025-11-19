# TODO: Add New Models and Corrections to Django Project

## Steps to Complete
- [x] Add Empleado model to app_Antiguedades/models.py with fields: nombre, apellido, puesto, salario, telefono
- [x] Add DetalleVenta model to app_Antiguedades/models.py with fields: FK to Venta, FK to PiezaAntiguedad, cantidad, precio_unitario, subtotal, total
- [x] Add Venta model to app_Antiguedades/models.py with fields: fecha_venta, total, metodo_pago, FK to Empleado, FK to Cliente
- [x] Run Django migrations: python manage.py makemigrations, then python manage.py migrate
- [ ] Test the new models (optional: create admin entries or views)
- [x] Consult user on corrections: Remove comprador, fecha_venta, precio_venta from PiezaAntiguedad; add status field; clarify precio field
- [ ] Apply corrections if approved by user
