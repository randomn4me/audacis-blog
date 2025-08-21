{ self }:
{ config, lib, pkgs, ... }:

let
  cfg = config.services.audacis-blog;
in
{
  options.services.audacis-blog = {
    enable = lib.mkOption {
      type = lib.types.bool;
      default = false;
      description = "Enable the audacis blog service";
    };

    domain = lib.mkOption {
      type = lib.types.nullOr lib.types.str;
      default = null;
      description = "Domain name for the blog. When null, nginx will serve on localhost only without SSL.";
    };
  };

  config = lib.mkIf cfg.enable {
    services.nginx = {
      enable = true;
      recommendedGzipSettings = true;
      recommendedOptimisation = true;
      recommendedProxySettings = true;
      recommendedTlsSettings = lib.mkIf (cfg.domain != null) true;

      virtualHosts = if cfg.domain != null then {
        ${cfg.domain} = {
          enableACME = true;
          forceSSL = true;
          serverAliases = [ "www.${cfg.domain}" ];
          root = "${self.packages.${pkgs.stdenv.hostPlatform.system}.audacis-blog}";
          
          locations."/" = {
            tryFiles = "$uri $uri/ /index.html";
          };
        };
      } else {
        "localhost" = {
          root = "${self.packages.${pkgs.stdenv.hostPlatform.system}.audacis-blog}";
          
          locations."/" = {
            tryFiles = "$uri $uri/ /index.html";
          };
        };
      };
    };

    security.acme = lib.mkIf (cfg.domain != null) {
      acceptTerms = true;
      defaults.email = "admin@${cfg.domain}";
    };

    networking.firewall.allowedTCPPorts = if cfg.domain != null then [ 80 443 ] else [ 80 ];
  };
}