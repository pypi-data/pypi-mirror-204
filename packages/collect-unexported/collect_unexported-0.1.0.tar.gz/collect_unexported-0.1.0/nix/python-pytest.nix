# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

{ pkgs ? (import
    (fetchTarball {
      url = "https://github.com/ppentchev/nixpkgs/archive/bd1f21853e790e727513a65671661137ab3a9e72.tar.gz";
      sha256 = "0rld4jga4bdim85wc7fcx46pnqdgv52k4kdai46li1acvn0pxk0q";
    })
    { })
, py-ver ? 311
}:
let
  python-name = "python${toString py-ver}";
  python = builtins.getAttr python-name pkgs;
  python-pkgs = python.withPackages (p: with p; [
    cfg_diag
    click
    debian
    pyyaml
    tomli-w

    pip
    pytest
  ]);
in
pkgs.mkShell {
  buildInputs = [ pkgs.git python-pkgs ];
  shellHook = ''
    set -e

    # We need to generate the command-line executable wrapper
    rm -rf nix-target-install
    python3 -m pip install --prefix nix-target-install .

    # However, we don't really need to point PYTHONPATH at that tree
    PATH="$(pwd)/nix-target-install/bin:$PATH" PYTHONPATH="$(pwd)/src" python3 -m pytest -v unit_tests

    rm -rf nix-target-install
    exit
  '';
}
