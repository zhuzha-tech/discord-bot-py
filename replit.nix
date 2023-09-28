{ pkgs }: {
  deps = [
    pkgs.vim
    pkgs.poetry
    pkgs.ruff
    pkgs.python311Full.out
    pkgs.python311Packages.poetry-core
  ];
  env = {
  };
}