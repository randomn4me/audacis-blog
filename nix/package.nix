{ pkgs, src, tabi }:

pkgs.stdenv.mkDerivation {
  pname = "audacis-blog";
  version = "2024-11-09";
  inherit src;
  nativeBuildInputs = [ pkgs.zola ];
  buildPhase = ''
    runHook preBuild
    
    mkdir -p themes/tabi
    cp -r ${tabi}/* themes/tabi/
    chmod -R u+w themes/
    
    zola build
    
    runHook postBuild
  '';
  installPhase = ''
    mkdir -p $out
    cp -r public/* $out/
  '';
}