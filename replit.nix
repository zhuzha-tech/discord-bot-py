{ pkgs }: {
  deps = [
    pkgs.vim
    pkgs.htop
    pkgs.ruff
    pkgs.poetry
    pkgs.python311Full.out
    pkgs.python311Packages.poetry-core
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      # Needed for pandas / numpy
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
      # Needed for pygame
      pkgs.glib
      # Needed for matplotlib
      pkgs.xorg.libX11
    ];
    PYTHONBIN = "${pkgs.python311}/bin/python";
    LANG = "en_US.UTF-8";
  };
}