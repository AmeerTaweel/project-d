# Development environment
# You can enter it through `nix develop` or (legacy) `nix-shell`
{pkgs ? (import ./nixpkgs.nix) {}}: {
  default = pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
      just
      hivemind
      mariadb
      (python3.withPackages(ps: with ps; [
        numpy
        pandas
        mysql-connector
        bottle
      ]))
    ];
    shellHook = ''
      export MYSQL_BASEDIR=${pkgs.mariadb}
      export MYSQL_HOME="$PWD/mysql"
      export MYSQL_DATADIR="$MYSQL_HOME/data"
      export MYSQL_UNIX_PORT="$MYSQL_HOME/mysql.sock"
      export MYSQL_PID_FILE="$MYSQL_HOME/mysql.pid"
      export MYSQL_LOG_FILE="$MYSQL_HOME/mysql.log"
      export MYSQL_PORT=3306
    '';
  };
}
