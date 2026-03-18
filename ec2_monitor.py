import argparse
import time
import boto3


def format_instance(instance):
    """Return a tuple with Instance ID, State, Type, Public IP."""
    instance_id = instance.get('InstanceId', '')
    state = instance.get('State', {}).get('Name', '')
    instance_type = instance.get('InstanceType', '')
    public_ip = instance.get('PublicIpAddress', '')
    return instance_id, state, instance_type, public_ip


def list_instances(region=None):
    """List EC2 instances in the given region."""
    session = boto3.Session(region_name=region) if region else boto3.Session()
    ec2 = session.client('ec2')

    response = ec2.describe_instances()
    instances = []

    for reservation in response.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            instances.append(format_instance(instance))

    return instances


def print_instances(instances):
    """Prints a table of instance details."""
    if not instances:
        print('No se encontraron instancias.')
        return

    # Calculate column widths
    headers = ['InstanceId', 'State', 'Type', 'Public IP']
    widths = [len(h) for h in headers]
    for row in instances:
        widths = [max(w, len(str(val))) for w, val in zip(widths, row)]

    fmt = '  '.join(f'{{:<{w}}}' for w in widths)

    print(fmt.format(*headers))
    print(fmt.format(*['-' * w for w in widths]))
    for row in instances:
        print(fmt.format(*row))


def main():
    parser = argparse.ArgumentParser(description='List and monitor EC2 instances.')
    parser.add_argument('--region', help='AWS region (default: from environment/config)')
    parser.add_argument('--watch', type=int, default=0, help='Refresh interval in seconds (0 means run once)')

    args = parser.parse_args()

    while True:
        instances = list_instances(region=args.region)
        print_instances(instances)

        if args.watch <= 0:
            break

        print(f"\nActualizando en {args.watch} segundos... (Ctrl+C para salir)\n")
        time.sleep(args.watch)


if __name__ == '__main__':
    main()
