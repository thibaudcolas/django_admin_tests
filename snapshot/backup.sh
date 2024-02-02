#!/bin/bash

VERSION=$1
VARIANT=$2
USERNAME=$3
HOST=$4
COOKIES=cookies.txt

if [ -z "$VERSION" ]; then
  VERSION="v5.1"
fi
if [ -z "$VARIANT" ]; then
  VARIANT="english"
fi
if [ -z "$USERNAME" ]; then
  USERNAME="admin"
fi
if [ -z "$HOST" ]; then
  HOST="http://localhost:8000"
fi

touch $COOKIES
echo "localhost:8000	FALSE	/	FALSE	1729046818	auto_login	$USERNAME" > $COOKIES


wget --no-host-directories -P ./django_admin_tests --mirror --reject-regex "(.*)\?(.*)" --load-cookies $COOKIES $HOST/django_admin_tests/$VERSION/$VARIANT/
wget --no-host-directories -P ./django_admin_tests/django_admin_tests $HOST/django_admin_tests/
wget --content-on-error --no-host-directories -P ./django_admin_tests --mirror $HOST/django_admin_tests/$VERSION/$VARIANT/defaults/404/
wget --content-on-error --no-host-directories -P ./django_admin_tests --mirror $HOST/django_admin_tests/$VERSION/$VARIANT/defaults/500/
wget --content-on-error --no-host-directories -P ./django_admin_tests --mirror $HOST/django_admin_tests/$VERSION/$VARIANT/defaults/500-template-missing/
wget --content-on-error --no-host-directories -P ./django_admin_tests --mirror $HOST/django_admin_tests/$VERSION/$VARIANT/defaults/500-template-broken/
wget --content-on-error --no-host-directories -P ./django_admin_tests --mirror $HOST/django_admin_tests/$VERSION/$VARIANT/defaults/500-unicode/
wget --content-on-error --no-host-directories -P ./django_admin_tests --mirror $HOST/django_admin_tests/$VERSION/$VARIANT/defaults/500-plain-text/
wget --content-on-error --no-host-directories -P ./django_admin_tests --mirror $HOST/django_admin_tests/$VERSION/$VARIANT/defaults/403/
wget --content-on-error --no-host-directories -P ./django_admin_tests --mirror $HOST/django_admin_tests/$VERSION/$VARIANT/defaults/400/
wget --content-on-error --no-host-directories -P ./django_admin_tests --mirror $HOST/django_admin_tests/$VERSION/$VARIANT/defaults/csrf_failure/

