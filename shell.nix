# Development environment
# You can enter it through `nix develop` or (legacy) `nix-shell`
{pkgs ? (import ./nixpkgs.nix) {}}: {
  default = pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
      immudb
      (python3.withPackages(ps: with ps; [
        numpy
        pandas
        bottle
      ]))
    ];
  };
}
