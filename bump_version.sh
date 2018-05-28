#! /bin/bash

SED_FLAGS=-i.bak

if [[ $# -lt 2 ]]
then
  echo -e "Usage: $0 version git_tag"

  exit 1
fi

VERSION=$1

TAG=$2

sed $SED_FLAGS "s|\(.*version: \"\).*|\1$VERSION\"|" ./conda/meta.yaml

sed $SED_FLAGS "s|\(.*git_rev: \).*|\1$TAG|" ./conda/meta.yaml

sed $SED_FLAGS "s|\(__version__ = '\).*\('\)|\1$VERSION\2|" ./cwt/__init__.py