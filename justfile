h    := env_var("MYSQL_HOME")
b    := env_var("MYSQL_BASEDIR")
d    := env_var("MYSQL_DATADIR")
p    := env_var("MYSQL_PID_FILE")
port := env_var("MYSQL_PORT")

mysql *ARGS:
  mysql -h localhost -P {{port}} -u root {{ARGS}}

mysql-init:
  #!/usr/bin/env bash
  set -euxo pipefail
  if [ ! -d "$MYSQL_HOME" ]; then
    # Make sure to use normal authentication method otherwise we can only
    # connect with unix account. But users do not actually exists in nix.
    mysql_install_db --auth-root-authentication-method=normal \
      --datadir=$MYSQL_DATADIR --basedir=$MYSQL_BASEDIR \
      --pid-file=$MYSQL_PID_FILE
  fi

mysql-dump FILE:
  mysqldump -h localhost -P {{port}} -u root > {{FILE}}
