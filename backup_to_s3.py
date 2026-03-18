import boto3
import os
from datetime import datetime
from botocore.exceptions import ClientError


def backup_folder_to_s3(local_folder, bucket_name):
    """Escanea una carpeta local y sube todos los archivos a un bucket S3."""

    s3_client = boto3.client('s3')

    # Detectar región (usando la configuración actual de AWS CLI/entorno)
    region = boto3.Session().region_name

    # Verificar si el bucket existe (y crearlo si no existe)
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"El bucket '{bucket_name}' ya existe")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"El bucket no existe. Creando bucket '{bucket_name}' en región {region}...")
            if region == 'us-east-1':
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            print(f"Bucket '{bucket_name}' creado correctamente")
        else:
            print(f"Error al verificar el bucket: {e}")
            return

    # Carpeta de fecha (YYYY-MM-DD)
    date_folder = datetime.now().strftime('%Y-%m-%d')

    files_uploaded = 0
    files_failed = 0

    # Recorrer archivos de la carpeta
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, local_folder)
            s3_key = f"{date_folder}/{relative_path.replace(os.sep, '/')}"

            try:
                s3_client.upload_file(local_file_path, bucket_name, s3_key)
                print(f"Archivo subido: {local_file_path} -> s3://{bucket_name}/{s3_key}")
                files_uploaded += 1
            except Exception as e:
                print(f"Error al subir {local_file_path}: {e}")
                files_failed += 1

    print(f"\nResumen: {files_uploaded} archivos subidos, {files_failed} errores")


if __name__ == "__main__":
    local_folder = "/workspaces/pruebas-aws-cli/ejercicios"
    bucket_name = "bucket-pruebas-awscli-restar"
    backup_folder_to_s3(local_folder, bucket_name)
