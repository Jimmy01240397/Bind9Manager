#!/bin/bash
printhelp()
{
	echo "Usage: $0 [options]
Options:
  -h, --help                    display this help message and exit.
  -z, --zone ZONE               zone of record." 1>&2
	exit 1
}

dirpath=$(dirname "$0")

zone=""

while [ "$1" != "" ]
do
    case "$1" in
        -h|--help)
            printhelp
            ;;
        -z|--zone)
            shift
            zone=$1
            ;;
    esac
    shift
done

if [ "$zone" == "" ]
then
    printhelp
fi

ansible-playbook $dirpath/roles/delzone/setup.yml -e "{\"zone\":\"$zone\"}"


