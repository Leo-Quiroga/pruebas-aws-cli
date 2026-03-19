# Comandos AWS CloudFormation CLI

---

## 1. Crear un stack

```bash
aws cloudformation create-stack \
  --stack-name NOMBRE-DEL-STACK \        # nombre único que identifica tu stack
  --template-body file://tu-archivo.yaml \  # ruta al archivo YAML/JSON con la infraestructura
  --parameters \                            # parámetros que acepta el template
    ParameterKey=PARAMETRO1,ParameterValue=VALOR1 \
    ParameterKey=PARAMETRO2,ParameterValue=VALOR2 \
  --region us-west-2                        # región donde se crean los recursos
```

---

## 2. Ver el estado del stack

```bash
aws cloudformation describe-stacks \
  --stack-name NOMBRE-DEL-STACK \
  --region us-west-2 \
  --query 'Stacks[0].StackStatus'  # filtra solo el campo de estado, evita ver todo el JSON
```

**Estados posibles:**
- `CREATE_IN_PROGRESS` — todavía creándose, espera
- `CREATE_COMPLETE` — listo y funcionando
- `ROLLBACK_IN_PROGRESS` — algo falló, deshaciendo cambios
- `ROLLBACK_COMPLETE` — falló y ya deshizo todo
- `DELETE_IN_PROGRESS` — eliminándose
- `DELETE_COMPLETE` — eliminado

---

## 3. Esperar a que termine (bloquea la terminal hasta completarse)

```bash
# Hace polling automático cada ~15s hasta que el stack llega a CREATE_COMPLETE o falla
aws cloudformation wait stack-create-complete \
  --stack-name NOMBRE-DEL-STACK \
  --region us-west-2
```

---

## 4. Ver los outputs (IPs, URLs, IDs)

```bash
# Versión tabla — más legible
aws cloudformation describe-stacks \
  --stack-name NOMBRE-DEL-STACK \
  --region us-west-2 \
  --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \  # [*] itera todos los outputs, toma solo clave y valor
  --output table                                             # formatea como tabla ASCII

# Versión JSON — más detallada (incluye Description, ExportName, etc.)
aws cloudformation describe-stacks \
  --stack-name NOMBRE-DEL-STACK \
  --region us-west-2 \
  --query 'Stacks[0].Outputs'
```

---

## 5. Actualizar un stack existente

```bash
aws cloudformation update-stack \
  --stack-name NOMBRE-DEL-STACK \
  --template-body file://tu-archivo.yaml \  # puede ser el mismo template con cambios o uno nuevo
  --parameters \
    ParameterKey=PARAMETRO1,ParameterValue=VALOR1 \  # solo los parámetros que quieres cambiar
  --region us-west-2
```

Esperar a que termine la actualización:
```bash
aws cloudformation wait stack-update-complete \
  --stack-name NOMBRE-DEL-STACK \
  --region us-west-2
```

---

## 6. Eliminar un stack (borra todos los recursos)

```bash
# ⚠️  Elimina TODOS los recursos creados por el stack (EC2, RDS, VPC, etc.)
aws cloudformation delete-stack \
  --stack-name NOMBRE-DEL-STACK \
  --region us-west-2
```

Esperar a que termine la eliminación:
```bash
aws cloudformation wait stack-delete-complete \
  --stack-name NOMBRE-DEL-STACK \
  --region us-west-2
```

---

## 7. Listar todos tus stacks

```bash
# Ver todos (incluye stacks eliminados)
aws cloudformation list-stacks \
  --region us-west-2

# Ver solo los activos (excluye los eliminados)
aws cloudformation list-stacks \
  --region us-west-2 \
  --query "StackSummaries[?StackStatus!='DELETE_COMPLETE'].[StackName,StackStatus]" \  # filtra con JMESPath: solo los que NO están en DELETE_COMPLETE
  --output table
```

---

## 8. Ver los eventos del stack (útil para entender errores)

```bash
aws cloudformation describe-stack-events \
  --stack-name NOMBRE-DEL-STACK \
  --region us-west-2 \
  --query 'StackEvents[*].[Timestamp,ResourceStatus,ResourceType,ResourceStatusReason]' \  # ResourceStatusReason muestra el mensaje de error exacto
  --output table
```

---

## Flujo completo de un lab

```bash
# 1. Crear — lanza la creación en segundo plano (no bloquea)
aws cloudformation create-stack \
  --stack-name mi-webapp \
  --template-body file://webapp-infrastructure.yaml \
  --parameters \
    ParameterKey=EnvironmentName,ParameterValue=lab \
    ParameterKey=KeyName,ParameterValue=mi-llave-lab \       # nombre del key pair para SSH
    ParameterKey=EnableLoadBalancer,ParameterValue=false \   # false = sin ALB, más barato para labs
  --region us-west-2

# 2. Esperar — bloquea la terminal hasta que el stack esté listo o falle
aws cloudformation wait stack-create-complete \
  --stack-name mi-webapp --region us-west-2

# 3. Ver outputs — muestra IPs, URLs u otros valores exportados por el template
aws cloudformation describe-stacks \
  --stack-name mi-webapp --region us-west-2 \
  --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
  --output table

# 4. Eliminar al terminar — importante para no generar costos innecesarios
aws cloudformation delete-stack \
  --stack-name mi-webapp --region us-west-2
```

---

## Notas útiles

- El `\` al final de cada línea significa que el comando continúa en la siguiente línea. Es solo formato visual.
- Cambia `us-west-2` por tu región si usas otra.
- El comando `wait` bloquea la terminal hasta que termina. Si no lo usas, puedes ir ejecutando `describe-stacks` manualmente para ver el estado.
- Si un stack falla, usa `describe-stack-events` para ver exactamente qué recurso causó el error.
