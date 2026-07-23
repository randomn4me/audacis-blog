{ self }:
{ config, lib, pkgs, ... }:

let
  cfg = config.services.audacis-blog;
  
  # Build the blog with the correct base URL
  buildBlog = baseUrl: import ./package.nix {
    inherit pkgs baseUrl;
    src = self;
  };
  
  # Determine the base URL and build the appropriate package
  blogPackage = buildBlog "https://${cfg.domain}";
in
{
  options.services.audacis-blog = {
    enable = lib.mkOption {
      type = lib.types.bool;
      default = false;
      description = "Enable the audacis blog service";
    };

    domain = lib.mkOption {
      type = lib.types.str;
      description = "Domain name for the blog.";
    };
  };

  config = lib.mkIf cfg.enable {
    services.nginx = {
      enable = true;
      recommendedGzipSettings = true;
      recommendedOptimisation = true;
      recommendedProxySettings = true;
      recommendedTlsSettings = true;

      virtualHosts.${cfg.domain} = {
        enableACME = true;
        forceSSL = true;
        root = "${blogPackage}";
        
        locations."/" = {
          tryFiles = "$uri $uri/ /index.html";
        };
      };
    };

    security.acme = {
      acceptTerms = true;
      defaults.email = lib.mkDefault "admin@${cfg.domain}";
    };

    networking.firewall.allowedTCPPorts = [ 80 443 ];
  };
}
