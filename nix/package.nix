{ pkgs, src, tabi, baseUrl }:

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
    
    # Override base_url in config.toml for the build
    sed -i 's|base_url = .*|base_url = "${baseUrl}"|' config.toml
    
    zola build
    
    runHook postBuild
  '';
  installPhase = ''
    mkdir -p $out
    cp -r public/* $out/
  '';
}