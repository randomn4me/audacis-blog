{ pkgs, src, baseUrl }:

pkgs.stdenv.mkDerivation {
  pname = "audacis-blog";
  version = "2024-11-09";
  inherit src;
  nativeBuildInputs = [ pkgs.zola ];

  # zola builds a reqwest client up front in load_data, which panics when no
  # system CA bundle is present. The build itself stays offline.
  SSL_CERT_FILE = "${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt";

  buildPhase = ''
    runHook preBuild

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
