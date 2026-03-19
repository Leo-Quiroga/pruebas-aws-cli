# import boto3
# import json
# from botocore.exceptions import ClientError

# # clientes 
# ec2 = boto3.client('ec2')
# s3 = boto3.client('s3')
# iam = boto3.client('iam')
# cloudwatch = boto3.client('cloudwatch')

# # inventario general
# inventario = {
#     "ec2": [],
#     "s3": [],
#     "iam": []
# }

# # =========================
# # EC2
# # =========================
# try: 

#     # listar instancias
#     response = ec2.describe_instances()

#     # procesar instancias
#     instancias = [
#         i for r in response['Reservations'] # para cada reserva, obtener las instancias y agregarlas a la lista
#         for i in r['Instances']
#     ] # obtener las instancias de cada reserva y agregarlas a la lista
    
#     print(f"Instancias encontradas: {len(instancias)}") # imprimir el número de instancias encontradas

#     for instance in instancias: # imprimir el ID de cada instancia
#         datos_instancia = {
#             "InstanceId": instance['InstanceId'],
#             "State": instance['State']['Name'],
#             "Type": instance['InstanceType']
#         }

#         inventario["ec2"].append(datos_instancia)
#         print(datos_instancia)

# except ClientError as e:
#     print(f"Error EC2: {e}")

# # =========================
# # S3
# # =========================

# try:
#     # listar buckets de s3
#     response = s3.list_buckets()
    
#     # obtener los buckets
#     print(f"Buckets encontrados: {len(response['Buckets'])}")
    
#     # procesar buckets
#     for bucket in response['Buckets']:
#         datos_bucket = {
#             "Name": bucket['Name'],
#             "CreationDate": str(bucket['CreationDate'])
#         }

#         inventario["s3"].append(datos_bucket)
#         print(datos_bucket)

# except ClientError as e:
#     print(f"Error S3: {e}")

# # =========================
# # IAM
# # =========================
# try:
#     # listar usuarios de IAM
#     response = iam.list_users()

#     print(f"Usuarios encontrados: {len(response['Users'])}")

#     # procesar usuarios
#     for user in response['Users']:
#         datos_user = {
#             "UserName": user['UserName'],
#             "CreateDate": str(user['CreateDate'])
#         }

#         inventario["iam"].append(datos_user)
#         print(datos_user)

# except ClientError as e:
#     print(f"Error IAM: {e}")

# # =========================
# # Guardar inventario JSON
# # =========================
# with open('inventario_aws.json', 'w') as archivo:
#     json.dump(inventario, archivo, indent=4)

# print("Inventario guardado en inventario_aws.json")

# # =========================
# # Métricas CloudWatch
# # =========================
# cloudwatch.put_metric_data(
#     Namespace='InventarioAWS',
#     MetricData=[
#         {
#             'MetricName': 'NumeroInstanciasEC2',
#             'Value': len(inventario["ec2"]),
#             'Unit': 'Count'
#         },
#         {
#             'MetricName': 'NumeroBucketsS3',
#             'Value': len(inventario["s3"]),
#             'Unit': 'Count'
#         },
#         {
#             'MetricName': 'NumeroUsuariosIAM',
#             'Value': len(inventario["iam"]),
#             'Unit': 'Count'
#         }
#     ]
# )

# print("Métricas enviadas a CloudWatch")
import boto3
import json
from botocore.exceptions import ClientError
from datetime import datetime

# ==========================================
# CLIENTES AWS
# ==========================================
ec2 = boto3.client('ec2')
s3 = boto3.client('s3')
iam = boto3.client('iam')
cloudwatch = boto3.client('cloudwatch')

# ==========================================
# INVENTARIO GENERAL
# ==========================================
inventario = {
    "fecha": str(datetime.now()),
    "ec2": [],
    "s3": [],
    "iam": []
}

# ==========================================
# FUNCION EC2
# ==========================================
def obtener_ec2():
    try:
        response = ec2.describe_instances()

        instancias = [
            i for r in response['Reservations']
            for i in r['Instances']
        ]

        for instance in instancias:
            inventario["ec2"].append({
                "InstanceId": instance['InstanceId'],
                "Estado": instance['State']['Name'],
                "Tipo": instance['InstanceType']
            })

    except ClientError as e:
        print(f"Error EC2: {e}")

# ==========================================
# FUNCION S3
# ==========================================
def obtener_s3():
    try:
        response = s3.list_buckets()

        for bucket in response['Buckets']:
            inventario["s3"].append({
                "Nombre": bucket['Name'],
                "Creado": str(bucket['CreationDate'])
            })

    except ClientError as e:
        print(f"Error S3: {e}")

# ==========================================
# FUNCION IAM
# ==========================================
def obtener_iam():
    try:
        response = iam.list_users()

        for user in response['Users']:
            inventario["iam"].append({
                "Usuario": user['UserName'],
                "Creado": str(user['CreateDate'])
            })

    except ClientError as e:
        print(f"Error IAM: {e}")

# ==========================================
# INFORME LEGIBLE
# ==========================================
def mostrar_informe():
    print("\n========== INFORME INVENTARIO AWS ==========")
    print(f"Fecha: {inventario['fecha']}")

    print("\nEC2:")
    if inventario["ec2"]:
        for item in inventario["ec2"]:
            print(
                f"- ID: {item['InstanceId']} | Estado: {item['Estado']} | Tipo: {item['Tipo']}"
            )
    else:
        print("- No hay instancias")

    print("\nS3:")
    if inventario["s3"]:
        for item in inventario["s3"]:
            print(
                f"- Bucket: {item['Nombre']} | Creado: {item['Creado']}"
            )
    else:
        print("- No hay buckets")

    print("\nIAM:")
    if inventario["iam"]:
        for item in inventario["iam"]:
            print(
                f"- Usuario: {item['Usuario']} | Creado: {item['Creado']}"
            )
    else:
        print("- No hay usuarios")

# ==========================================
# GUARDAR JSON
# ==========================================
def guardar_json():
    with open('inventario_aws.json', 'w') as archivo:
        json.dump(inventario, archivo, indent=4)

# ==========================================
# GUARDAR TXT
# ==========================================
def guardar_txt():
    with open('informe_aws.txt', 'w', encoding='utf-8') as archivo:

        archivo.write("========== INFORME INVENTARIO AWS ==========\n")
        archivo.write(f"Fecha de ejecución: {inventario['fecha']}\n")
        archivo.write("\n")

        archivo.write("========== RECURSOS EC2 ==========\n")
        if inventario["ec2"]:
            for i, item in enumerate(inventario["ec2"], start=1):
                archivo.write(f"Instancia {i}\n")
                archivo.write(f"  ID: {item['InstanceId']}\n")
                archivo.write(f"  Estado: {item['Estado']}\n")
                archivo.write(f"  Tipo: {item['Tipo']}\n")
                archivo.write("\n")
        else:
            archivo.write("No hay instancias EC2 registradas.\n\n")

        archivo.write("========== RECURSOS S3 ==========\n")
        if inventario["s3"]:
            for i, item in enumerate(inventario["s3"], start=1):
                archivo.write(f"Bucket {i}\n")
                archivo.write(f"  Nombre: {item['Nombre']}\n")
                archivo.write(f"  Fecha creación: {item['Creado']}\n")
                archivo.write("\n")
        else:
            archivo.write("No hay buckets S3 registrados.\n\n")

        archivo.write("========== RECURSOS IAM ==========\n")
        if inventario["iam"]:
            for i, item in enumerate(inventario["iam"], start=1):
                archivo.write(f"Usuario {i}\n")
                archivo.write(f"  Nombre: {item['Usuario']}\n")
                archivo.write(f"  Fecha creación: {item['Creado']}\n")
                archivo.write("\n")
        else:
            archivo.write("No hay usuarios IAM registrados.\n\n")

        archivo.write("========== RESUMEN GENERAL ==========\n")
        archivo.write(f"Total EC2: {len(inventario['ec2'])}\n")
        archivo.write(f"Total S3: {len(inventario['s3'])}\n")
        archivo.write(f"Total IAM: {len(inventario['iam'])}\n")
    
        archivo.write("\n========== ALERTAS ==========\n")
        archivo.write(f"Alerta EC2 alta: {'SI' if len(inventario['ec2']) > 2 else 'NO'}\n")
        archivo.write(f"Alerta S3 alta: {'SI' if len(inventario['s3']) > 0 else 'NO'}\n")

# ==========================================
# ALERTAS + METRICAS CLOUDWATCH
# ==========================================
def enviar_metricas():
    alerta_ec2 = 1 if len(inventario["ec2"]) > 2 else 0
    alerta_s3 = 1 if len(inventario["s3"]) > 0 else 0

    metricas = [
        {
            'MetricName': 'NumeroInstanciasEC2',
            'Value': len(inventario["ec2"]),
            'Unit': 'Count'
        },
        {
            'MetricName': 'NumeroBucketsS3',
            'Value': len(inventario["s3"]),
            'Unit': 'Count'
        },
        {
            'MetricName': 'NumeroUsuariosIAM',
            'Value': len(inventario["iam"]),
            'Unit': 'Count'
        },
        {
            'MetricName': 'AlertaEC2Alta',
            'Value': alerta_ec2,
            'Unit': 'Count'
        },
        {
            'MetricName': 'AlertaS3Alta',
            'Value': alerta_s3,
            'Unit': 'Count'
        }
    ]

    cloudwatch.put_metric_data(
        Namespace='InventarioAWS',
        MetricData=metricas
    )
    
    cloudwatch.put_metric_alarm(
    AlarmName='AlertaS3Alta',
    ComparisonOperator='GreaterThanOrEqualToThreshold',
    EvaluationPeriods=1,
    MetricName='AlertaS3Alta',
    Namespace='InventarioAWS',
    Period=60,
    Statistic='Maximum',
    Threshold=1,
    ActionsEnabled=True,
    AlarmActions=[
        'arn:aws:sns:us-west-2:697009138708:alertas-aws'
    ],
    Unit='Count'
    )

    print("\nMétricas enviadas a CloudWatch")

# ==========================================
# EJECUCION PRINCIPAL
# ==========================================
obtener_ec2()
obtener_s3()
obtener_iam()

mostrar_informe()
guardar_json()
guardar_txt()
enviar_metricas()

print("\nProceso completado correctamente")