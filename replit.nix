{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.python310Packages.pip
    pkgs.python310Packages.idna
    pkgs.python310Packages.flask
    pkgs.python310Packages.boto3
    pkgs.python310Packages.poetry
    pkgs.python310Packages.discordpy
    pkgs.python310Packages.validators
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
    PYTHONBIN = "${pkgs.python310}/bin/python";
    LANG = "en_US.UTF-8";
  };
}