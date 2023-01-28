#!/bin/bash
printhelp()
{
	echo "Usage: $0 [options]
Options:
  -h, --help                    display this help message and exit.
  -n, --hostname HOSTNAME       Hostname of record.
  -z, --zone ZONE               zone of record.
  -t, --type TYPE               type of record.
  -d, --data DATA               data of record." 1>&2
	exit 1
}

dirpath=$(dirname "$0")

hostname=""
zone=""
type=""
data=""

while [ "$1" != "" ]
do
    case "$1" in
        -h|--help)
            printhelp
            ;;
        -n|--hostname)
            shift
            hostname=$1
            ;;
        -z|--zone)
            shift
            zone=$1
            ;;
        -t|--type)
            shift
            type=$1
            ;;
        -d|--data)
            shift
            data=$1
            ;;
    esac
    shift
done

if [ "$hostname" == "" ] || [ "$zone" == "" ] || [ "$type" == "" ] || [ "$data" == "" ]
then
    printhelp
fi

ansible-playbook $dirpath/roles/addrecord/setup.yml -e "{\"host\":\"$hostname\",\"zone\":\"$zone\",\"type\":\"$type\",\"data\":\"$data\"}"


